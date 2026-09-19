"""Synthetic backend-shaped data; not a model run or real Live verification."""
import copy
import gzip
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'plugins/music-producer-kit/skills/music-producer'
sys.path.insert(0, str(SKILL / 'scripts'))
import live_workflow as w
import live_set_diff as sets


def fixture():
    score = w.load(SKILL / 'examples/harmony-study.json')
    bindings = {t['name']: {'index': i, 'name': t['name'], 'is_midi_track': True,
                           'clip_slots': [], 'devices': [{'index': 0, 'name': 'Fixture instrument'}],
                           'volume': 0.7, 'panning': 0.0, 'output_meter_level': 0.0}
                for i, t in enumerate(score['tracks'])}
    plan = w.compile_score(score, bindings, {'Bass': 4})
    def read(tool, arguments, result): return {'tool': tool, 'arguments': arguments, 'result': result}
    reads = [read('get_session_info', {}, {'tempo': 96, 'signature_numerator': 4, 'signature_denominator': 4,
                  'track_count': 2, 'return_track_count': 0, 'master_track': {'name': 'Master', 'volume': 0.8, 'panning': 0.0}}),
             read('get_arrangement_info', {}, {'tempo': 96, 'is_playing': False, 'record_mode': False, 'current_song_time': 0, 'loop': False})]
    full = {'tempo': 96, 'time_signature': '4/4', 'song_length': 16, 'tracks_with_clips': [], 'scenes': []}
    for name, info in bindings.items():
        ti = info['index']
        reads.extend([read('get_track_info', {'track_index': ti}, info),
                      read('get_track_routing', {'track_index': ti}, {'input_routing_type': 'No Input', 'output_routing_type': 'Master'}),
                      read('get_device_parameters', {'track_index': ti, 'device_index': 0}, {'parameters': [{'index': 0, 'value': 0.5}]})])
        clips = []
        for ci, c in enumerate(c for c in plan['clips'] if c['arguments']['track_index'] == ti):
            a = c['arguments']
            clip_name = f'{name} {ci+1}'
            clips.append({'name': clip_name, 'start_time': a['time'], 'end_time': a['time']+a['length'],
                          'length': a['length'], 'is_midi_clip': True, 'is_audio_clip': False})
            reads.append(read('get_arrangement_clip_notes', {'track_index': ti, 'arrangement_clip_index': ci},
                              {'track_index': ti, 'arrangement_clip_index': ci, 'clip_name': clip_name,
                               'start_time': a['time'], 'length': a['length'], 'note_count': len(a['notes']), 'notes': a['notes']}))
        full['tracks_with_clips'].append({'track_index': ti, 'track_name': name, 'clips': clips})
    reads.append(read('get_full_arrangement', {}, full))
    return score, bindings, plan, {'set_key': 'synthetic-test-project', 'reads': reads}


def changed_capture(capture, edit):
    c = copy.deepcopy(capture)
    for r in c['reads']:
        if r['tool'] == 'get_arrangement_clip_notes' and r['arguments']['track_index'] == 1 and r['result']['start_time'] == 4:
            r['result']['notes'] = edit['create']['arguments']['notes']
            r['result']['note_count'] = len(r['result']['notes'])
    return c


class LiveWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.score, self.bindings, self.plan, self.capture = fixture()
        self.before = w.checkpoint(self.capture)
        self.receipt = w.verify_creation(self.plan, self.before)
        self.notes = [{'pitch': 45, 'start': 4, 'duration': 2, 'velocity': 72},
                      {'pitch': 52, 'start': 6, 'duration': 2, 'velocity': 72}]
        self.edit = w.plan_edit(self.before, self.receipt, 'Bass', 4, 8, self.notes)

    def test_creation_requires_empty_discovered_destinations(self):
        with self.assertRaises(ValueError): w.verify_empty(self.plan, self.before)
        c = copy.deepcopy(self.capture)
        c['reads'] = [r for r in c['reads'] if r['tool'] != 'get_arrangement_clip_notes']
        next(r['result'] for r in c['reads'] if r['tool'] == 'get_full_arrangement')['tracks_with_clips'] = []
        self.assertTrue(w.verify_empty(self.plan, w.checkpoint(c))['destinations_empty_in_readback'])
        info = next(r['result'] for r in c['reads'] if r['tool'] == 'get_track_info')
        info['clip_slots'] = [{'index':0,'has_clip':True,'clip':{'name':'Protected'}}]
        with self.assertRaises(ValueError): w.verify_empty(self.plan, w.checkpoint(c))

    def test_first_route_compile_checkpoint_edit_compare_reopen(self):
        self.assertEqual(len(self.plan['clips']), 5)
        self.assertEqual(self.edit['delete']['arguments'], {'track_index': 1, 'arrangement_clip_index': 1})
        self.assertEqual([n['start_time'] for n in self.edit['create']['arguments']['notes']], [0, 2])
        after = w.checkpoint(changed_capture(self.capture, self.edit))
        self.assertTrue(w.verify_edit(self.before, after, self.edit)['observed_fields_preserved'])
        self.assertTrue(w.verify_reopen(after, copy.deepcopy(after))['observed_readbacks_match'])
        self.assertFalse(w.verify_reopen(after, after)['ui_open_action_proven'])

    def test_deletion_checkpoint_blocks_stale_or_collateral_changes(self):
        absent = copy.deepcopy(self.capture)
        absent['reads'] = [r for r in absent['reads'] if not
                           (r['tool'] == 'get_arrangement_clip_notes' and r['arguments']['track_index'] == 1
                            and r['result']['start_time'] == 4)]
        full = next(r['result'] for r in absent['reads'] if r['tool'] == 'get_full_arrangement')
        full['tracks_with_clips'][1]['clips'].pop(1)
        self.assertTrue(w.verify_removed(self.before, w.checkpoint(absent), self.edit)['target_absent_in_readback'])
        with self.assertRaises(ValueError): w.verify_removed(self.before, self.before, self.edit)
        absent['reads'][0]['result']['master_track']['volume'] = 0.1
        with self.assertRaises(ValueError): w.verify_removed(self.before, w.checkpoint(absent), self.edit)

    def test_updated_receipt_supports_the_next_edit(self):
        after = w.checkpoint(changed_capture(self.capture, self.edit))
        result = w.verify_edit(self.before, after, self.edit)
        next_notes = [{'pitch': 47, 'start': 4, 'duration': 4, 'velocity': 72}]
        next_edit = w.plan_edit(after, result['receipt'], 'Bass', 4, 8, next_notes)
        self.assertEqual(next_edit['create']['arguments']['notes'][0]['pitch'], 47)
        with self.assertRaises(ValueError): w.plan_edit(after, self.receipt, 'Bass', 4, 8, next_notes)

    def test_tampered_edit_actions_fail(self):
        edited = w.checkpoint(changed_capture(self.capture, self.edit))
        plan = copy.deepcopy(self.edit); plan['delete']['arguments']['track_index'] = 0
        with self.assertRaises(ValueError): w.verify_edit(self.before, edited, plan)

    def test_native_track_names_can_use_korean_and_japanese(self):
        score = copy.deepcopy(self.score); bindings = copy.deepcopy(self.bindings)
        for old, new in [('Harmony', '피아노'), ('Bass', 'ベース')]:
            next(t for t in score['tracks'] if t['name'] == old)['name'] = new
            bindings[new] = bindings.pop(old); bindings[new]['name'] = new
        plan = w.compile_score(score, bindings, {'ベース': 4})
        self.assertEqual({c['track_name'] for c in plan['clips']}, {'피아노', 'ベース'})

    def test_installed_distribution_can_compile_without_checkout(self):
        sys.path.insert(0, str(ROOT / 'tools'))
        import check as package
        import zipfile
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); archive = root / 'kit.zip'; package.build_package(ROOT, archive)
            with zipfile.ZipFile(archive) as z: z.extractall(root / 'installed')
            installed = root / 'installed/plugins/music-producer-kit/skills/music-producer'
            bindings = root / 'bindings.json'; bindings.write_text(json.dumps(self.bindings),encoding='utf-8')
            output = root / 'plan.json'
            result = subprocess.run([sys.executable, str(installed / 'scripts/live_workflow.py'),
                                     'compile', str(installed / 'examples/harmony-study.json'),
                                     '--bindings', str(bindings), '--output', str(output)],
                                    cwd=root, capture_output=True, text=True, timeout=20)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(len(json.loads(output.read_text())['clips']), 2)
            self.assertTrue((installed / 'scripts/live_set_diff.py').is_file())
            self.assertTrue((installed / 'references/live-workflow.md').is_file())

    def test_longer_piece_and_non_four_four_use_quarter_beats(self):
        score = copy.deepcopy(self.score)
        score['meter'] = [6, 8]; score['length_beats'] = 48
        for track in score['tracks']:
            track['notes'] = [{'pitch': 60, 'start': 30, 'duration': 3, 'velocity': 80}]
        plan = w.compile_score(score, self.bindings, {'Bass': 3})
        self.assertEqual(len(plan['clips']), 17)
        self.assertEqual(plan['meter'], [6, 8])

    def test_crossing_split_is_not_cut(self):
        with self.assertRaises(ValueError): w.compile_score(self.score, self.bindings, {'Harmony': 2})

    def test_duplicate_wrong_missing_bindings(self):
        for change in ['duplicate', 'wrong_name', 'not_midi', 'missing']:
            b = copy.deepcopy(self.bindings)
            if change == 'duplicate': b['Bass']['index'] = 0
            elif change == 'wrong_name': b['Bass']['name'] = 'Other'
            elif change == 'not_midi': b['Bass']['is_midi_track'] = False
            else: del b['Bass']
            with self.subTest(change=change), self.assertRaises(ValueError): w.compile_score(self.score, b)

    def test_rejects_backend_string_errors_instead_of_success(self):
        c = copy.deepcopy(self.capture); c['reads'][0]['result'] = 'Error getting session info: timeout'
        with self.assertRaises(ValueError): w.checkpoint(c)
        c['reads'][0]['result'] = {'status': 'error', 'message': 'failed'}
        with self.assertRaises(ValueError): w.checkpoint(c)

    def test_json_string_read_result_accepted(self):
        c = copy.deepcopy(self.capture)
        for r in c['reads']: r['result'] = json.dumps(r['result'])
        self.assertEqual(w.checkpoint(c)['state_sha256'], self.before['state_sha256'])

    def test_missing_read_fails_closed(self):
        for i in range(len(self.capture['reads'])):
            c = copy.deepcopy(self.capture); c['reads'].pop(i)
            with self.subTest(i=i), self.assertRaises(ValueError): w.checkpoint(c)

    def test_duplicate_read_or_notes_fails(self):
        c = copy.deepcopy(self.capture); c['reads'].append(copy.deepcopy(c['reads'][0]))
        with self.assertRaises(ValueError): w.checkpoint(c)
        c = copy.deepcopy(self.capture)
        r = next(r for r in c['reads'] if r['tool'] == 'get_arrangement_clip_notes')
        r['result']['note_count'] += 1
        with self.assertRaises(ValueError): w.checkpoint(c)

    def test_running_or_incoherent_state_rejected(self):
        c = copy.deepcopy(self.capture); c['reads'][1]['result']['is_playing'] = True
        with self.assertRaises(ValueError): w.checkpoint(c)
        c['reads'][1]['result']['is_playing'] = False; c['reads'][1]['result']['tempo'] = 123
        with self.assertRaises(ValueError): w.checkpoint(c)

    def test_indices_can_reorder_but_protected_data_cannot(self):
        c = changed_capture(self.capture, self.edit)
        for r in c['reads']:
            if r['tool'] == 'get_arrangement_clip_notes' and r['arguments']['track_index'] == 1:
                ci = (r['arguments']['arrangement_clip_index'] + 2) % 4
                r['arguments']['arrangement_clip_index'] = ci; r['result']['arrangement_clip_index'] = ci
            if r['tool'] == 'get_full_arrangement': r['result']['tracks_with_clips'][1]['clips'].reverse()
            if r['tool'] == 'get_arrangement_info': r['result']['current_song_time'] = 8
            if r['tool'] == 'get_track_info': r['result']['output_meter_level'] = 0.3
        self.assertTrue(w.verify_edit(self.before, w.checkpoint(c), self.edit)['observed_fields_preserved'])

    def test_protected_melody_mixer_routing_device_master_changes_fail(self):
        for which in ['melody', 'mixer', 'routing', 'device', 'master']:
            c = changed_capture(self.capture, self.edit)
            for r in c['reads']:
                if which == 'melody' and r['tool'] == 'get_arrangement_clip_notes' and r['arguments']['track_index'] == 0:
                    r['result']['notes'][0]['pitch'] = 61
                if which == 'mixer' and r['tool'] == 'get_track_info': r['result']['volume'] = 0.1
                if which == 'routing' and r['tool'] == 'get_track_routing': r['result']['output_routing_type'] = 'Other'
                if which == 'device' and r['tool'] == 'get_device_parameters': r['result']['parameters'][0]['value'] = 0.1
                if which == 'master' and r['tool'] == 'get_session_info': r['result']['master_track']['volume'] = 0.2
            with self.subTest(which=which), self.assertRaises(ValueError): w.verify_edit(self.before, w.checkpoint(c), self.edit)

    def test_wrong_target_stale_receipt_and_boundary_are_rejected(self):
        for name, start, end in [('Unknown', 4, 8), ('Bass', 3, 8), ('Bass', 4, 9), ('Bass', 4, 12)]:
            with self.subTest(name=name, start=start, end=end), self.assertRaises(ValueError):
                w.plan_edit(self.before, self.receipt, name, start, end, self.notes)
        receipt = copy.deepcopy(self.receipt); receipt['state_sha256'] = 'stale'
        with self.assertRaises(ValueError): w.plan_edit(self.before, receipt, 'Bass', 4, 8, self.notes)

    def test_changed_set_and_tampered_checkpoint_fail(self):
        c = copy.deepcopy(self.capture); c['set_key'] = 'different project'
        with self.assertRaises(ValueError): w.verify_reopen(self.before, w.checkpoint(c))
        check = copy.deepcopy(self.before); check['state']['set_key'] = 'tampered'
        with self.assertRaises(ValueError): w.checked(check)

    def test_foreign_note_features_are_not_silently_lost(self):
        c = copy.deepcopy(self.capture)
        r = next(r for r in c['reads'] if r['tool'] == 'get_arrangement_clip_notes')
        r['result']['notes'][0]['probability'] = 0.5
        with self.assertRaises(ValueError): w.checkpoint(c)

    def test_non_destructive_cli_and_private_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            capture = root / 'capture.json'; capture.write_text(json.dumps(self.capture), encoding='utf-8')
            out = root / 'checkpoint.json'
            cmd = [sys.executable, str(SKILL / 'scripts/live_workflow.py'), 'checkpoint', str(capture), '--output', str(out)]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
            self.assertEqual(result.returncode, 0, result.stderr)
            original = out.read_bytes()
            self.assertNotEqual(subprocess.run(cmd, capture_output=True, timeout=20).returncode, 0)
            self.assertEqual(out.read_bytes(), original)
            with self.assertRaises(ValueError): w.save_new({}, SKILL / 'private.json')
            with patch('socket.create_connection', side_effect=AssertionError('network not allowed')):
                self.assertTrue(w.checked(w.load(out)))


class SetDiffTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.xml = '<Ableton><LiveSet><Tracks><MidiTrack Id="1"><Notes><MidiNoteEvent Key="45" Duration="4"/></Notes><Automation Value="0.3"/></MidiTrack></Tracks><Transport Value="0"/></LiveSet></Ableton>'
        self.a = self.write('a.als', self.xml)

    def write(self, name, xml):
        path = self.root / name
        path.write_bytes(gzip.compress(xml.encode('utf-8')))
        return path

    def test_identical_and_all_fields_including_automation_are_observed(self):
        b = self.write('b.als', self.xml)
        self.assertTrue(sets.compare(self.a, b)['xml_equivalent'])
        b = self.write('b.als', self.xml.replace('Key="45"', 'Key="52"').replace('Value="0.3"', 'Value="0.5"'))
        result = sets.compare(self.a, b)
        self.assertEqual(result['difference_count'], 2)
        self.assertFalse(result['ui_reopen_proven'])
        self.assertTrue(any('/Automation' in d['path'] for d in result['differences']))

    def test_ids_and_cursor_not_silently_ignored(self):
        b = self.write('b.als', self.xml.replace('Id="1"','Id="2"').replace('Transport Value="0"','Transport Value="4"'))
        self.assertEqual(sets.compare(self.a, b)['difference_count'], 2)

    def test_truncation_and_added_subtree_explicit(self):
        b = self.write('b.als', self.xml.replace('</Notes>', '<MidiNoteEvent Key="52"/></Notes>').replace('Transport Value="0"','Transport Value="4"'))
        r = sets.compare(self.a, b, 1)
        self.assertTrue(r['truncated']); self.assertGreater(r['difference_count'], 1)

    def test_malformed_other_format_dtd_and_budget_rejected(self):
        for xml in ['<not-live/>', '<Ableton>', '<!DOCTYPE Ableton [<!ENTITY x "bad">]><Ableton><LiveSet/></Ableton>']:
            with self.subTest(xml=xml), self.assertRaises((ValueError, sets.ET.ParseError)):
                sets.read_set(self.write('bad.als', xml))
        with patch.object(sets, 'MAX_BYTES', 10), self.assertRaises(ValueError): sets.read_set(self.a)
        with patch.object(sets, 'MAX_NODES', 2), self.assertRaises(ValueError): sets.read_set(self.a)

    def test_does_not_modify_sources(self):
        b = self.write('b.als', self.xml.replace('Key="45"','Key="52"'))
        old = (self.a.read_bytes(), b.read_bytes()); sets.compare(self.a,b)
        self.assertEqual(old, (self.a.read_bytes(), b.read_bytes()))


if __name__ == '__main__': unittest.main()
