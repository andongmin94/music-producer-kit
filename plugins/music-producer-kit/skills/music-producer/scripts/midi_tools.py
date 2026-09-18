"""Create, inspect and safely patch note-only regions of Standard MIDI files.

No DAW connection, audio rendering, melody transcription or musical grading.
Times are zero-based quarter-note beats, irrespective of the time signature.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
from pathlib import Path
from typing import Any

import mido

PPQ = 480


def _number(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{label}: expected a finite number")
    if not math.isfinite(value):
        raise ValueError(f"{label}: expected a finite number")
    return float(value)


def _integer(value: Any, low: int, high: int, label: str) -> int:
    if type(value) is not int or not low <= value <= high:
        raise ValueError(f"{label}: expected an integer in {low}..{high}")
    return value


def _tick(value: Any, ppq: int, label: str) -> int:
    scaled = _number(value, label) * ppq
    if scaled < 0 or not math.isfinite(scaled):
        raise ValueError(f"{label}: must be non-negative and finite")
    result = round(scaled)
    if abs(scaled - result) > 1e-6:
        raise ValueError(f"{label}: not representable at {ppq} ticks per quarter note")
    return result


def _object(value: Any, required: set[str], optional: set[str], label: str) -> dict:
    if not isinstance(value, dict):
        raise ValueError(f"{label}: expected an object")
    missing = required - value.keys()
    extra = value.keys() - required - optional
    if missing or extra:
        raise ValueError(f"{label}: missing={sorted(missing)}, unknown={sorted(extra)}")
    return value


def load_json(path: Path) -> Any:
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result
    return json.loads(path.read_text(encoding="utf-8-sig"), object_pairs_hook=unique)


def _events(track: mido.MidiTrack) -> list[tuple[int, int, Any]]:
    tick = 0
    events = []
    for index, message in enumerate(track):
        if type(message.time) is not int or message.time < 0:
            raise ValueError("MIDI delta times must be non-negative integers")
        tick += message.time
        events.append((tick, index, message))
    return events


def _pairs(track: mido.MidiTrack) -> list[tuple[int, int, int, int, int, int, int]]:
    active = {}
    pairs = []
    for tick, index, msg in _events(track):
        if msg.type not in {"note_on", "note_off"}:
            continue
        key = (msg.channel, msg.note)
        if msg.type == "note_on" and msg.velocity > 0:
            if key in active:
                raise ValueError("Overlapping notes of the same pitch/channel are ambiguous")
            active[key] = (tick, index, msg.velocity)
        else:
            if key not in active:
                raise ValueError("Unmatched note-off; repair the source MIDI first")
            start, on_index, velocity = active.pop(key)
            if tick <= start:
                raise ValueError("Zero-length or negative-length note")
            pairs.append((on_index, index, start, tick, msg.note, msg.channel, velocity))
    if active:
        raise ValueError("Unclosed note-on; repair the source MIDI first")
    return pairs


def _rebuild(events: list[tuple[int, int, Any]]) -> mido.MidiTrack:
    track = mido.MidiTrack()
    previous = 0
    for tick, _, message in sorted(events, key=lambda e: (e[0], e[1])):
        track.append(message.copy(time=tick - previous))
        previous = tick
    return track


def _note_events(notes: Any, channel: int, ppq: int, start: int, end: int):
    if not isinstance(notes, list):
        raise ValueError("notes: expected an array")
    events = []
    intervals: dict[int, list[tuple[int, int]]] = {}
    for index, raw in enumerate(notes):
        note = _object(raw, {"pitch", "start", "duration", "velocity"}, set(), f"note {index}")
        pitch = _integer(note["pitch"], 0, 127, "pitch")
        velocity = _integer(note["velocity"], 1, 127, "velocity")
        on = _tick(note["start"], ppq, "start")
        off = on + _tick(note["duration"], ppq, "duration")
        if not start <= on < off <= end:
            raise ValueError("Note lies outside the allowed region or has no positive duration")
        intervals.setdefault(pitch, []).append((on, off))
        # New note-offs precede coincident original events; original events keep their order.
        events.extend([(on, 10**12 + index, mido.Message("note_on", channel=channel, note=pitch, velocity=velocity)),
                       (off, -1, mido.Message("note_off", channel=channel, note=pitch, velocity=0))])
    for spans in intervals.values():
        spans.sort()
        if any(left[1] > right[0] for left, right in zip(spans, spans[1:])):
            raise ValueError("Replacement notes overlap at the same pitch")
    return events


def _load_bytes(data: bytes) -> mido.MidiFile:
    mid = mido.MidiFile(file=io.BytesIO(data))
    if mid.type != 1 or mid.ticks_per_beat <= 0:
        raise ValueError("This tool supports synchronous type-1, PPQ-based MIDI only")
    if not mid.tracks:
        raise ValueError("MIDI has no tracks")
    for track in mid.tracks:
        if not track or track[-1].type != "end_of_track":
            raise ValueError("Each track must end with end_of_track")
        if sum(msg.type == "end_of_track" for msg in track) != 1:
            raise ValueError("A track must have exactly one end_of_track")
        _events(track)
    return mid


def _signature(track: mido.MidiTrack, skip: set[int] | None = None) -> str:
    events = [[tick, msg.copy(time=0).dict()] for tick, index, msg in _events(track)
              if skip is None or index not in skip]
    return hashlib.sha256(json.dumps(events, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _serialize(mid: mido.MidiFile) -> bytes:
    buffer = io.BytesIO()
    mid.save(file=buffer)
    return buffer.getvalue()


def _write_new(path: Path, data: bytes) -> None:
    # Never overwrite user work, even through a symlink or stale output path.
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as target:
        target.write(data)


def create(score: Any, output: Path) -> dict:
    score = _object(score, {"bpm", "meter", "length_beats", "tracks"}, set(), "score")
    bpm = _number(score["bpm"], "bpm")
    if bpm <= 0:
        raise ValueError("bpm must be positive")
    tempo = round(60_000_000 / bpm)
    if not 1 <= tempo <= 0xFFFFFF:
        raise ValueError("Tempo cannot be represented in a MIDI tempo event")
    meter = score["meter"]
    if not isinstance(meter, list) or len(meter) != 2:
        raise ValueError("meter must be [numerator, denominator]")
    numerator = _integer(meter[0], 1, 32, "meter numerator")
    denominator = _integer(meter[1], 1, 32, "meter denominator")
    if denominator & (denominator - 1):
        raise ValueError("meter denominator must be a power of two")
    end = _tick(score["length_beats"], PPQ, "length_beats")
    if end <= 0:
        raise ValueError("length_beats must be positive")
    if not isinstance(score["tracks"], list) or not score["tracks"]:
        raise ValueError("tracks must be a non-empty array")
    mid = mido.MidiFile(type=1, ticks_per_beat=PPQ)
    mid.tracks.append(mido.MidiTrack([
        mido.MetaMessage("track_name", name="Conductor"),
        mido.MetaMessage("set_tempo", tempo=tempo),
        mido.MetaMessage("time_signature", numerator=numerator, denominator=denominator),
        mido.MetaMessage("end_of_track", time=end),
    ]))
    names = {"Conductor"}
    for raw in score["tracks"]:
        spec = _object(raw, {"name", "channel", "notes"}, {"program"}, "track")
        name = spec["name"]
        if not isinstance(name, str) or not name.strip() or name in names:
            raise ValueError("Track names must be non-empty and unique; Conductor is reserved")
        names.add(name)
        channel = _integer(spec["channel"], 0, 15, "channel")
        events = [(0, 0, mido.MetaMessage("track_name", name=name)),
                  (end, 10**15, mido.MetaMessage("end_of_track"))]
        if "program" in spec:
            program = _integer(spec["program"], 0, 127, "program")
            events.append((0, 1, mido.Message("program_change", channel=channel, program=program)))
        events.extend(_note_events(spec["notes"], channel, PPQ, 0, end))
        mid.tracks.append(_rebuild(events))
    # SMF has no universal text charset marker; use ASCII track names for portability.
    for name in names:
        try:
            name.encode("ascii")
        except UnicodeEncodeError as exc:
            raise ValueError("Use ASCII MIDI track names for portable text encoding") from exc
    data = _serialize(mid)
    reopened = _load_bytes(data)
    for track in reopened.tracks:
        _pairs(track)
    _write_new(output, data)
    return {"status": "created", "sha256": hashlib.sha256(data).hexdigest(),
            "tracks": len(mid.tracks), "length_beats": end / PPQ, "audio_reviewed": False}


def inspect(path: Path) -> dict:
    data = path.read_bytes()
    mid = _load_bytes(data)
    tracks = []
    for index, track in enumerate(mid.tracks):
        pairs = _pairs(track)
        tracks.append({"index": index, "name": track.name, "events_sha256": _signature(track),
                       "length_beats": _events(track)[-1][0] / mid.ticks_per_beat,
                       "notes": [{"pitch": p, "channel": c, "start": s / mid.ticks_per_beat,
                                  "duration": (e - s) / mid.ticks_per_beat, "velocity": v}
                                 for _, _, s, e, p, c, v in pairs]})
    return {"sha256": hashlib.sha256(data).hexdigest(), "type": mid.type,
            "ticks_per_beat": mid.ticks_per_beat, "tracks": tracks, "audio_reviewed": False}


def _selection(track: mido.MidiTrack, start: int, end: int) -> set[int]:
    selected = set()
    for on, off, s, e, *_ in _pairs(track):
        if s < end and e > start:
            if s < start or e > end:
                raise ValueError("A source note crosses the edit boundary; do not trim it silently")
            selected.update((on, off))
    return selected


def patch(source: Path, output: Path, track_name: str, start_beats: float,
          end_beats: float, notes: Any, expected_sha256: str) -> dict:
    data = source.read_bytes()
    actual_sha = hashlib.sha256(data).hexdigest()
    if actual_sha != expected_sha256:
        raise ValueError("Source changed or wrong SHA256; inspect again before editing")
    if source.resolve() == output.resolve():
        raise ValueError("Source and output must be different files")
    mid = _load_bytes(data)
    targets = [i for i, t in enumerate(mid.tracks) if t.name == track_name]
    if len(targets) != 1:
        raise ValueError("Target track name must identify exactly one existing track")
    index = targets[0]
    track = mid.tracks[index]
    channels = {m.channel for m in track if hasattr(m, "channel")}
    if len(channels) != 1:
        raise ValueError("Target must contain exactly one MIDI channel")
    if any(m.type == "control_change" and m.control in {64, 66, 120, 123} for m in track):
        raise ValueError("Pedal/channel-mode controllers require a performance-aware editor")
    start = _tick(start_beats, mid.ticks_per_beat, "start")
    end = _tick(end_beats, mid.ticks_per_beat, "end")
    if not 0 <= start < end <= _events(track)[-1][0]:
        raise ValueError("Edit region must be within the existing target track")
    removed = _selection(track, start, end)
    protected = _signature(track, removed)
    unchanged = {i: _signature(t) for i, t in enumerate(mid.tracks) if i != index}
    kept = [e for e in _events(track) if e[1] not in removed]
    kept.extend(_note_events(notes, channels.pop(), mid.ticks_per_beat, start, end))
    mid.tracks[index] = _rebuild(kept)
    result = _serialize(mid)
    reopened = _load_bytes(result)
    after = reopened.tracks[index]
    if _signature(after, _selection(after, start, end)) != protected:
        raise ValueError("Protected target events changed; refusing output")
    if any(_signature(reopened.tracks[i]) != sig for i, sig in unchanged.items()):
        raise ValueError("An unrelated track changed; refusing output")
    _write_new(output, result)
    return {"status": "patched", "input_sha256": actual_sha,
            "output_sha256": hashlib.sha256(result).hexdigest(), "track": track_name,
            "region_quarter_beats": [start / mid.ticks_per_beat, end / mid.ticks_per_beat],
            "unchanged_track_indices": sorted(unchanged), "protected_events_preserved": True,
            "audio_reviewed": False}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    new = sub.add_parser("create", help="Create a new editable type-1 MIDI file")
    new.add_argument("score", type=Path)
    new.add_argument("output", type=Path)
    read = sub.add_parser("inspect", help="Read note events and source SHA256")
    read.add_argument("source", type=Path)
    edit = sub.add_parser("patch", help="Replace notes inside one track and interval")
    edit.add_argument("source", type=Path)
    edit.add_argument("--output", type=Path, required=True)
    edit.add_argument("--track", required=True)
    edit.add_argument("--start", type=float, required=True)
    edit.add_argument("--end", type=float, required=True)
    edit.add_argument("--notes", type=Path, required=True)
    edit.add_argument("--expected-sha256", required=True)
    args = parser.parse_args()
    try:
        if args.command == "create":
            result = create(load_json(args.score), args.output)
        elif args.command == "inspect":
            result = inspect(args.source)
        else:
            result = patch(args.source, args.output, args.track, args.start, args.end,
                           load_json(args.notes), args.expected_sha256)
    except (ValueError, OSError, EOFError, KeyError, TypeError, OverflowError) as exc:
        parser.exit(2, f"error: {exc}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
