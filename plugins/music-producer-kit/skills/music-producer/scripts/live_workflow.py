"""Compile note payloads and compare native Ableton MCP readbacks, without connecting.

Target: nicholasbien/ableton-mcp-pro at 6ae148de18c8042df041b95c6e830bcdf22be526.
Codex owns native MCP calls and Windows UI actions. This helper never executes a
plan, opens a server, saves a Live Set, or certifies unobserved performance data.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
import tempfile
from typing import Any

import midi_tools

BACKEND = 'nicholasbien/ableton-mcp-pro'
PLUGIN = Path(__file__).resolve().parents[3]
MAX_JSON_BYTES = 16_000_000
READS = frozenset({'get_session_info', 'get_arrangement_info', 'get_full_arrangement',
                  'get_track_info', 'get_track_routing', 'get_device_parameters',
                  'get_arrangement_clip_notes'})
LIMITS = ('Readbacks cover reported ordinary-track notes, devices, routing and mixer values, '
          'plus session/master fields. They do not cover all automation, return-device state, '
          'MPE, probability or release velocity. File/XML review and actual UI reopen evidence '
          'are separate. A matching snapshot is not proof that a tool or UI action ran.')


def digest(value: Any) -> str:
    data = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)
    return hashlib.sha256(data.encode('utf-8')).hexdigest()


def load(path: Path) -> Any:
    if path.stat().st_size > MAX_JSON_BYTES:
        raise ValueError('JSON exceeds the workflow budget')
    result = midi_tools.load_json(path)
    digest(result)  # Also reject NaN/Infinity accepted by Python's JSON decoder.
    return result


def save_new(value: Any, path: Path) -> None:
    path = Path(path).expanduser()
    resolved = path.resolve()
    checkout = PLUGIN.parent.parent
    if resolved.is_relative_to(PLUGIN) or ((checkout / 'AGENTS.md').is_file() and resolved.is_relative_to(checkout)):
        raise ValueError('Keep song plans and readbacks outside the plugin and public checkout')
    if path.suffix.lower() != '.json' or not path.parent.is_dir() or path.is_symlink():
        raise ValueError('Use a new .json file in an existing private directory')
    payload = json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n'
    with path.open('x', encoding='utf-8') as stream:
        stream.write(payload)


def index(value: Any) -> int:
    return midi_tools._integer(value, 0, 100_000, 'index')


def beat(value: Any) -> float:
    return midi_tools._tick(value, midi_tools.PPQ, 'beat') / midi_tools.PPQ


def native_notes(notes: Any, start: float, end: float) -> list[dict]:
    # The existing Mido validator defines the note domain; no new note codec.
    midi_tools._note_events(notes, 0, midi_tools.PPQ, round(start * midi_tools.PPQ), round(end * midi_tools.PPQ))
    return sorted(({'pitch': n['pitch'], 'start_time': beat(n['start']) - start,
                    'duration': beat(n['duration']), 'velocity': n['velocity'], 'mute': False}
                   for n in notes), key=lambda n: (n['start_time'], n['pitch'], n['duration']))


def checked_notes(notes: Any, length: float) -> list[dict]:
    if not isinstance(notes, list):
        raise ValueError('Native notes must be an array')
    plain = []
    result = []
    for n in notes:
        midi_tools._object(n, {'pitch', 'start_time', 'duration', 'velocity', 'mute'}, set(), 'native note')
        if type(n['mute']) is not bool:
            raise ValueError('Native mute must be boolean')
        # This integration handles basic integral-velocity note data only.
        velocity = midi_tools._number(n['velocity'], 'velocity')
        if not velocity.is_integer():
            raise ValueError('Fractional velocities require a different verified editing path')
        plain.append({'pitch': n['pitch'], 'start': n['start_time'], 'duration': n['duration'], 'velocity': int(velocity)})
        result.append({**n, 'start_time': beat(n['start_time']), 'duration': beat(n['duration']), 'velocity': int(velocity)})
    midi_tools._note_events(plain, 0, midi_tools.PPQ, 0, round(length * midi_tools.PPQ))
    return sorted(result, key=lambda n: (n['start_time'], n['pitch'], n['duration'], n['velocity'], n['mute']))


def compile_score(score: dict, bindings: dict, segments: dict | None = None) -> dict:
    """Compile a validated score for already discovered NEW empty MIDI tracks.

    Bindings are raw get_track_info objects keyed by score track name. The host
    must confirm current empty destinations and authorization before applying.
    """
    midi_tools._object(score, {'bpm','meter','length_beats','tracks'}, set(), 'score')
    if not isinstance(bindings, dict) or (segments is not None and not isinstance(segments, dict)):
        raise ValueError('Bindings and segments must be objects')
    segments = segments or {}
    # Native Live names are Unicode. The temporary MIDI is only a note-domain
    # validator, so use neutral ASCII labels there rather than a MIDI charset
    # limitation silently restricting the visible Live track names.
    if not isinstance(score.get('tracks'), list) or not score['tracks']:
        raise ValueError('Score tracks must be a nonempty list')
    raw_names = [t.get('name') for t in score['tracks']]
    if any(not isinstance(n, str) or not n.strip() for n in raw_names) or len(set(raw_names)) != len(raw_names):
        raise ValueError('Live part names must be nonempty and unique')
    validation_score = copy.deepcopy(score)
    for i, track in enumerate(validation_score['tracks']):
        track['name'] = f'Part-{i}'
    with tempfile.TemporaryDirectory() as tmp:
        midi_tools.create(validation_score, Path(tmp) / 'validation.mid')
    names = set(raw_names)
    if set(bindings) != names or set(segments) - names:
        raise ValueError('Bind every score track exactly once; segment names must exist')
    duration = beat(score['length_beats'])
    clips, seen = [], set()
    for track in score['tracks']:
        info = bindings[track['name']]
        if info.get('name') != track['name'] or info.get('is_midi_track') is not True:
            raise ValueError('Binding must be an actual matching MIDI-track readback')
        ti = index(info['index'])
        if ti in seen:
            raise ValueError('Two score parts cannot silently share one destination track')
        seen.add(ti)
        width = beat(segments.get(track['name'], duration))
        if width <= 0:
            raise ValueError('Clip segment length must be positive')
        starts = range(0, round(duration * midi_tools.PPQ), round(width * midi_tools.PPQ))
        for tick in starts:
            start, end = tick / midi_tools.PPQ, min(tick / midi_tools.PPQ + width, duration)
            notes = [n for n in track['notes'] if start <= n['start'] < end]
            # Crossing a split is rejected, not trimmed or duplicated.
            converted = native_notes(notes, start, end)
            clips.append({'track_name': track['name'], 'tool': 'create_arrangement_midi_clip',
                          'arguments': {'track_index': ti, 'time': start, 'length': end - start, 'notes': converted}})
    return {'version': 1, 'kind': 'arrangement-note-plan', 'backend': BACKEND,
            'tempo': score['bpm'], 'meter': score['meter'], 'length_beats': duration,
            'clips': clips, 'source_score_sha256': digest(score), 'executed': False,
            'precondition': 'Fresh native state; authorized destinations are empty. Discover instruments separately. '
                            'No MIDI program number implies a Live device. Execute via existing native MCP, then read back.'}


def _key(tool: str, arguments: dict) -> str:
    return tool + ':' + json.dumps(arguments, sort_keys=True, separators=(',', ':'), allow_nan=False)


def _object_result(value: Any) -> dict:
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except json.JSONDecodeError as exc:
            raise ValueError('Backend returned non-JSON/error text; do not treat it as a successful read') from exc
    if not isinstance(value, dict) or 'error' in value or value.get('status') == 'error':
        raise ValueError('Expected successful decoded backend read data, not a tool wrapper or error')
    return copy.deepcopy(value)


def checkpoint(capture: dict) -> dict:
    """Normalize a host-collected bundle of native reads; never manufacture reads.

    Capture = {set_key: private stable project label, reads: [{tool, arguments,
    result: decoded return JSON or its JSON string}]}. All ordinary-track reads
    and all Arrangement MIDI note reads are required. Additional fields stay in
    comparisons; only named live meter/cursor fields are excluded.
    """
    midi_tools._object(capture, {'set_key', 'reads'}, set(), 'capture')
    if not isinstance(capture['set_key'], str) or not capture['set_key'].strip():
        raise ValueError('An identified current Set is required')
    if not isinstance(capture['reads'], list) or len(capture['reads']) > 1000:
        raise ValueError('Invalid read bundle')
    reads, clips = {}, []
    for raw in capture['reads']:
        midi_tools._object(raw, {'tool', 'arguments', 'result'}, set(), 'read')
        tool, arguments = raw['tool'], raw['arguments']
        if tool not in READS or not isinstance(arguments, dict):
            raise ValueError('Only documented read tools belong in the checkpoint')
        key = _key(tool, arguments)
        if key in reads:
            raise ValueError('Duplicate read; collect one fresh coherent snapshot')
        result = _object_result(raw['result'])
        reads[key] = result
        if tool == 'get_arrangement_clip_notes':
            midi_tools._object(result, {'track_index', 'arrangement_clip_index', 'clip_name', 'start_time', 'length', 'note_count', 'notes'}, set(), 'native clip read')
            ti, ci = index(arguments['track_index']), index(arguments['arrangement_clip_index'])
            if result.get('track_index') != ti or result.get('arrangement_clip_index') != ci:
                raise ValueError('Note read returned the wrong clip/track')
            start, length = beat(result['start_time']), beat(result['length'])
            notes = checked_notes(result['notes'], length)
            if result.get('note_count') != len(notes) or length <= 0:
                raise ValueError('Incomplete note readback')
            clips.append({'track_index': ti, 'index': ci, 'name': result['clip_name'],
                          'start': start, 'length': length, 'notes': notes})

    def required(tool: str, **args) -> dict:
        key = _key(tool, args)
        if key not in reads:
            raise ValueError('Missing required read: ' + key)
        return reads[key]

    session = required('get_session_info')
    arrangement = required('get_arrangement_info')
    full = required('get_full_arrangement')
    if arrangement.get('is_playing') is not False or arrangement.get('record_mode') not in (False, 0):
        raise ValueError('Stop playback/recording before capturing protected state')
    count = index(session['track_count'])
    if count > 128:
        raise ValueError('This checkpoint is bounded to 128 ordinary tracks')
    tracks = {}
    for ti in range(count):
        info = required('get_track_info', track_index=ti)
        if info.get('index') != ti or not isinstance(info.get('name'), str):
            raise ValueError('Track identity mismatch')
        tracks[ti] = info['name']
        required('get_track_routing', track_index=ti)
        for device in info['devices']:
            required('get_device_parameters', track_index=ti, device_index=index(device['index']))
    expected = []
    for track in full['tracks_with_clips']:
        ti = index(track['track_index'])
        if tracks.get(ti) != track['track_name']:
            raise ValueError('Arrangement and track identity disagree')
        track['clips'].sort(key=lambda c: (c['start_time'], c['end_time'], c['name']))
        for c in track['clips']:
            if c['is_midi_clip']:
                expected.append((ti, beat(c['start_time']), beat(c['length']), c['name']))
    actual = [(c['track_index'], c['start'], c['length'], c['name']) for c in clips]
    if len(actual) != len(set(actual)) or sorted(actual) != sorted(expected):
        raise ValueError('Missing, duplicated or inconsistent Arrangement MIDI readbacks')
    if session['tempo'] != full['tempo'] or session['tempo'] != arrangement['tempo']:
        raise ValueError('State changed during capture: inconsistent tempo')
    if full['time_signature'] != f"{session['signature_numerator']}/{session['signature_denominator']}":
        raise ValueError('Inconsistent time signature')
    # Track order is meaningful; clip indices may change on delete/recreate.
    full['tracks_with_clips'].sort(key=lambda t: t['track_index'])
    normalized = {}
    for key, result in reads.items():
        tool = key.split(':', 1)[0]
        if tool == 'get_arrangement_clip_notes':
            continue
        if tool == 'get_arrangement_info':
            result.pop('current_song_time', None)
        if tool == 'get_track_info':
            result.pop('output_meter_level', None)
        normalized[key] = result
    stable_clips = [{k: v for k, v in c.items() if k != 'index'} for c in clips]
    stable_clips.sort(key=lambda c: (c['track_index'], c['start'], c['length'], c['name']))
    state = {'set_key': capture['set_key'], 'reads': normalized, 'clips': stable_clips}
    return {'version': 1, 'kind': 'native-readback-checkpoint', 'capture': capture,
            'state_sha256': digest(state), 'state': state,
            'coverage': LIMITS, 'application_calls_executed_by_helper': False}


def checked(check: dict) -> dict:
    if check.get('kind') != 'native-readback-checkpoint':
        raise ValueError('Expected a checkpoint, not a plan')
    current = checkpoint(check['capture'])
    if current != check:
        raise ValueError('Checkpoint has been altered or is internally inconsistent')
    return current


def verify_empty(plan: dict, before: dict) -> dict:
    before = checked(before)
    if plan.get('kind') != 'arrangement-note-plan' or plan.get('backend') != BACKEND:
        raise ValueError('Expected an Arrangement note plan for the selected backend')
    indices = {c['arguments']['track_index'] for c in plan['clips']}
    full = before['state']['reads'][_key('get_full_arrangement', {})]
    if any(t['track_index'] in indices and t['clips'] for t in full['tracks_with_clips']):
        raise ValueError('A destination already contains Arrangement clips; do not overwrite it')
    for c in plan['clips']:
        ti = c['arguments']['track_index']
        info = before['state']['reads'][_key('get_track_info', {'track_index': ti})]
        if info['name'] != c['track_name'] or info.get('is_midi_track') is not True:
            raise ValueError('Destination identity changed')
        if any(slot['has_clip'] for slot in info['clip_slots']):
            raise ValueError('Destination has Session material; use authorized empty tracks')
    return {'status': 'pass', 'destinations_empty_in_readback': True,
            'state_sha256': before['state_sha256'], 'authorization_proven': False,
            'note': 'This does not authorize writes or create an atomic lock; re-read after each native action.'}


def verify_creation(plan: dict, after: dict) -> dict:
    after = checked(after)
    state = after['state']
    session = state['reads'][_key('get_session_info', {})]
    if session['tempo'] != plan['tempo'] or [session['signature_numerator'], session['signature_denominator']] != plan['meter']:
        raise ValueError('Actual tempo/meter differs from the plan')
    matched = []
    for c in plan['clips']:
        args = c['arguments']
        info = state['reads'][_key('get_track_info', {'track_index': args['track_index']})]
        if info['name'] != c['track_name']:
            raise ValueError('Destination identity changed')
        found = [r for r in state['clips'] if r['track_index'] == args['track_index'] and r['start'] == args['time']]
        if len(found) != 1 or found[0]['length'] != args['length'] or found[0]['notes'] != args['notes']:
            raise ValueError('Created notes or bounds do not match the plan')
        matched.append(found[0])
    indices = {c['arguments']['track_index'] for c in plan['clips']}
    if len([c for c in state['clips'] if c['track_index'] in indices]) != len(matched):
        raise ValueError('Unexpected clips on the new destination tracks')
    return {'kind': 'owned-basic-clip-receipt', 'version': 1, 'set_key': state['set_key'],
            'state_sha256': after['state_sha256'], 'clips': matched,
            'coverage': LIMITS, 'note': 'Use only while these freshly created simple clips remain unmodified. '
            'This receipt cannot prove hidden properties in an imported or manually modified performance.'}


def plan_edit(before: dict, receipt: dict, track_name: str, start: float, end: float, notes: list) -> dict:
    before = checked(before)
    start, end = beat(start), beat(end)
    if end <= start or receipt.get('kind') != 'owned-basic-clip-receipt':
        raise ValueError('A positive range and a verified kit-created clip receipt are required')
    if receipt.get('set_key') != before['state']['set_key'] or receipt.get('state_sha256') != before['state_sha256']:
        raise ValueError('Receipt is stale or belongs to another Set; inspect before touching it')
    infos = [r for k, r in before['state']['reads'].items() if k.startswith('get_track_info:') and r['name'] == track_name]
    if len(infos) != 1:
        raise ValueError('Track name is missing or ambiguous')
    ti = infos[0]['index']
    candidates = [c for c in before['state']['clips'] if c['track_index'] == ti and c['start'] < end and c['start'] + c['length'] > start]
    if len(candidates) != 1 or candidates[0]['start'] != start or candidates[0]['length'] != end - start:
        raise ValueError('This safe path replaces exactly one owned clip; do not trim a larger or overlapping clip')
    target = candidates[0]
    if target not in receipt['clips']:
        raise ValueError('Target is not an owned basic clip')
    current_note_read = [r for r in before['capture']['reads'] if r['tool'] == 'get_arrangement_clip_notes'
                         and r['arguments']['track_index'] == ti
                         and _object_result(r['result'])['start_time'] == start]
    ci = _object_result(current_note_read[0]['result'])['arrangement_clip_index']
    converted = native_notes(notes, start, end)
    return {'kind': 'scoped-arrangement-edit', 'version': 1, 'backend': BACKEND,
            'set_key': before['state']['set_key'], 'expected_state_sha256': before['state_sha256'],
            'receipt': copy.deepcopy(receipt),
            'target': target, 'track_name': track_name,
            'delete': {'tool': 'delete_arrangement_clip', 'arguments': {'track_index': ti, 'arrangement_clip_index': ci}},
            'create': {'tool': 'create_arrangement_midi_clip', 'arguments': {'track_index': ti, 'time': start, 'length': end-start, 'notes': converted}},
            'executed': False, 'atomic': False,
            'instructions': 'Freshly recheck BEFORE delete. Then verify absence before create. '
                            'After any timeout or text error do NOT blindly retry; read Live first. '
                            'Re-list clip indices. Restore the clip name only with a real supported host action. '
                            'Never use this path on imported, MPE, automated, loop-offset or manually modified clips.'}


def validate_edit(before: dict, plan: dict) -> None:
    if plan.get('kind') != 'scoped-arrangement-edit':
        raise ValueError('Expected a scoped edit plan')
    args = plan['create']['arguments']
    start = plan['target']['start']
    notes = [{'pitch': n['pitch'], 'start': n['start_time'] + start,
              'duration': n['duration'], 'velocity': n['velocity']} for n in args['notes']]
    regenerated = plan_edit(before, plan['receipt'], plan['track_name'], start,
                            start + plan['target']['length'], notes)
    if regenerated != plan:
        raise ValueError('Edit plan or clip indices changed; regenerate from fresh readbacks')


def verify_removed(before: dict, absent: dict, plan: dict) -> dict:
    before, absent = checked(before), checked(absent)
    validate_edit(before, plan)
    expected = copy.deepcopy(before['state'])
    target = plan['target']
    expected['clips'].remove(target)
    full = expected['reads'][_key('get_full_arrangement', {})]
    track = next(t for t in full['tracks_with_clips'] if t['track_index'] == target['track_index'])
    track['clips'] = [c for c in track['clips'] if not
                      (c['start_time'] == target['start'] and c['length'] == target['length']
                       and c['name'] == target['name'])]
    if not track['clips']:
        full['tracks_with_clips'].remove(track)
    if expected != absent['state']:
        raise ValueError('Deletion has not settled or changed protected fields; do not create/retry yet')
    return {'status': 'pass', 'target_absent_in_readback': True, 'coverage': LIMITS,
            'next_action': plan['create'], 'atomic': False}


def verify_edit(before: dict, after: dict, plan: dict) -> dict:
    before, after = checked(before), checked(after)
    validate_edit(before, plan)
    expected = copy.deepcopy(before['state'])
    matches = [c for c in expected['clips'] if c == plan['target']]
    if len(matches) != 1:
        raise ValueError('Target did not match the baseline')
    matches[0]['notes'] = plan['create']['arguments']['notes']
    if expected != after['state']:
        raise ValueError('Requested result or protected readback fields differ; stop and inspect')
    receipt = copy.deepcopy(plan['receipt'])
    receipt['clips'][receipt['clips'].index(plan['target'])] = copy.deepcopy(matches[0])
    receipt['state_sha256'] = after['state_sha256']
    return {'status': 'pass', 'observed_fields_preserved': True, 'receipt': receipt,
            'before_sha256': before['state_sha256'], 'after_sha256': after['state_sha256'],
            'coverage': LIMITS, 'saved_set_or_reopen_proven': False, 'audio_reviewed': False}


def verify_reopen(before: dict, reopened: dict) -> dict:
    before, reopened = checked(before), checked(reopened)
    if before['state'] != reopened['state']:
        raise ValueError('Post-reopen readbacks differ from the saved-state checkpoint')
    return {'status': 'pass', 'observed_readbacks_match': True, 'state_sha256': reopened['state_sha256'],
            'coverage': LIMITS, 'ui_open_action_proven': False,
            'note': 'Pair this with the actual host UI open event and .als file identity, not a duplicate capture.'}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    compile_cmd = commands.add_parser('compile')
    compile_cmd.add_argument('score', type=Path)
    compile_cmd.add_argument('--bindings', type=Path, required=True)
    compile_cmd.add_argument('--segments', type=Path)
    cp = commands.add_parser('checkpoint'); cp.add_argument('capture', type=Path)
    empty = commands.add_parser('verify-empty'); empty.add_argument('plan', type=Path); empty.add_argument('before', type=Path)
    created = commands.add_parser('verify-created'); created.add_argument('plan', type=Path); created.add_argument('after', type=Path)
    edit = commands.add_parser('edit'); edit.add_argument('before', type=Path); edit.add_argument('--receipt', type=Path, required=True)
    edit.add_argument('--track', required=True); edit.add_argument('--start', type=float, required=True); edit.add_argument('--end', type=float, required=True); edit.add_argument('--notes', type=Path, required=True)
    removed = commands.add_parser('verify-removed'); removed.add_argument('before', type=Path); removed.add_argument('absent', type=Path); removed.add_argument('--plan', type=Path, required=True)
    verify = commands.add_parser('verify-edit'); verify.add_argument('before', type=Path); verify.add_argument('after', type=Path); verify.add_argument('--plan', type=Path, required=True)
    reopen = commands.add_parser('verify-reopen'); reopen.add_argument('saved', type=Path); reopen.add_argument('reopened', type=Path)
    for sub in [compile_cmd, cp, empty, created, edit, removed, verify, reopen]:
        sub.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == 'compile': result = compile_score(load(args.score), load(args.bindings), load(args.segments) if args.segments else None)
        elif args.command == 'checkpoint': result = checkpoint(load(args.capture))
        elif args.command == 'verify-empty': result = verify_empty(load(args.plan), load(args.before))
        elif args.command == 'verify-created': result = verify_creation(load(args.plan), load(args.after))
        elif args.command == 'edit': result = plan_edit(load(args.before), load(args.receipt), args.track, args.start, args.end, load(args.notes))
        elif args.command == 'verify-removed': result = verify_removed(load(args.before), load(args.absent), load(args.plan))
        elif args.command == 'verify-edit': result = verify_edit(load(args.before), load(args.after), load(args.plan))
        else: result = verify_reopen(load(args.saved), load(args.reopened))
        save_new(result, args.output)
    except (ValueError, OSError, KeyError, TypeError) as exc:
        parser.exit(2, f'error: {exc}\n')
    print(json.dumps({'status': 'written', 'command': args.command, 'application_tools_called': [], 'audio_reviewed': False}))


if __name__ == '__main__':
    main()
