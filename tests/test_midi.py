"""Deterministic file behavior tests, not evaluations of the LLM or audio quality."""
import copy
import hashlib
import json
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import unittest

import mido

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "plugins/music-producer-kit/skills/music-producer"
sys.path.insert(0, str(SKILL / "scripts"))
import midi_tools as midi


def note(pitch=36, start=4, duration=0.25, velocity=96):
    return dict(pitch=pitch, start=start, duration=duration, velocity=velocity)


class MidiTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source = self.root / "source.mid"
        self.output = self.root / "output.mid"
        self.score = midi.load_json(SKILL / "examples/song.json")
        midi.create(self.score, self.source)
        self.original = self.source.read_bytes()
        self.sha = hashlib.sha256(self.original).hexdigest()

    def patch(self, **overrides):
        kwargs = dict(source=self.source, output=self.output, track_name="Drums",
                      start_beats=4, end_beats=8, notes=[note()], expected_sha256=self.sha)
        kwargs.update(overrides)
        return midi.patch(**kwargs)

    def edit_source(self, fn):
        mid = mido.MidiFile(self.source)
        fn(mid)
        mid.save(self.source)
        self.sha = hashlib.sha256(self.source.read_bytes()).hexdigest()

    def test_create_readback(self):
        result = midi.inspect(self.source)
        self.assertEqual(len(result["tracks"]), 4)
        self.assertTrue(all(t["length_beats"] == 8 for t in result["tracks"]))
        self.assertFalse(result["audio_reviewed"])

    def test_conductor(self):
        track = mido.MidiFile(self.source).tracks[0]
        self.assertEqual(next(m.tempo for m in track if m.type == "set_tempo"), 500000)
        self.assertEqual(next(m.denominator for m in track if m.type == "time_signature"), 4)

    def test_patch_only_requested_notes(self):
        report = self.patch()
        self.assertTrue(report["protected_events_preserved"])
        before, after = midi.inspect(self.source), midi.inspect(self.output)
        for i in [0, 1, 2]:
            self.assertEqual(before["tracks"][i], after["tracks"][i])
        self.assertEqual([n for n in before["tracks"][3]["notes"] if n["start"] < 4],
                         [n for n in after["tracks"][3]["notes"] if n["start"] < 4])
        self.assertEqual(self.source.read_bytes(), self.original)

    def test_wrong_hash(self):
        with self.assertRaisesRegex(ValueError, "Source changed"):
            self.patch(expected_sha256="0" * 64)
        self.assertFalse(self.output.exists())

    def test_same_output(self):
        with self.assertRaises(ValueError):
            self.patch(output=self.source)
        self.assertEqual(self.source.read_bytes(), self.original)

    def test_existing_output(self):
        self.output.write_bytes(b"keep me")
        with self.assertRaises(FileExistsError):
            self.patch()
        self.assertEqual(self.output.read_bytes(), b"keep me")

    def test_existing_create_output(self):
        with self.assertRaises(FileExistsError):
            midi.create(self.score, self.source)
        self.assertEqual(self.source.read_bytes(), self.original)

    def test_crossing_original_note(self):
        self.score["tracks"][2]["notes"] = [note(start=3, duration=2)]
        other = self.root / "crossing.mid"
        midi.create(self.score, other)
        with self.assertRaisesRegex(ValueError, "crosses"):
            self.patch(source=other, expected_sha256=midi.inspect(other)["sha256"])

    def test_boundary_note_off_before_new_on(self):
        self.score["tracks"][2]["notes"] = [note(start=0, duration=4), note(start=4, duration=4)]
        other = self.root / "boundary.mid"
        midi.create(self.score, other)
        self.patch(source=other, start_beats=0, end_beats=4,
                   notes=[note(start=0, duration=4)], expected_sha256=midi.inspect(other)["sha256"])
        self.assertEqual(len(midi.inspect(self.output)["tracks"][3]["notes"]), 2)

    def test_replacement_outside_region(self):
        for bad in [note(start=3), note(start=8), note(start=7, duration=2)]:
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                self.patch(notes=[bad])

    def test_replacement_overlapping_pitch(self):
        with self.assertRaises(ValueError):
            self.patch(notes=[note(duration=2), note(start=5, duration=2)])

    def test_nonpositive_duration(self):
        for duration in [0, -1]:
            with self.subTest(duration=duration), self.assertRaises(ValueError):
                self.patch(notes=[note(duration=duration)])

    def test_invalid_numbers(self):
        for value in [float("nan"), float("inf"), True, "4"]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.patch(start_beats=value)

    def test_invalid_note_values(self):
        for field, value in [("pitch", 128), ("pitch", -1), ("velocity", 0),
                             ("velocity", 128), ("pitch", True), ("pitch", 60.0)]:
            bad = note()
            bad[field] = value
            with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                self.patch(notes=[bad])

    def test_off_grid(self):
        with self.assertRaisesRegex(ValueError, "not representable"):
            self.patch(notes=[note(start=4.0001)])

    def test_unknown_json_fields(self):
        bad = note()
        bad["duraton"] = 1
        with self.assertRaisesRegex(ValueError, "unknown"):
            self.patch(notes=[bad])

    def test_empty_replacement(self):
        self.patch(notes=[])
        self.assertTrue(all(n["start"] < 4 for n in midi.inspect(self.output)["tracks"][3]["notes"]))

    def test_wrong_or_duplicate_track(self):
        with self.assertRaises(ValueError):
            self.patch(track_name="Not a track")
        self.edit_source(lambda m: setattr(m.tracks[2], "name", "Drums"))
        with self.assertRaises(ValueError):
            self.patch()

    def test_sustain_rejected(self):
        self.edit_source(lambda m: m.tracks[3].insert(0, mido.Message("control_change", channel=9, control=64, value=127)))
        with self.assertRaisesRegex(ValueError, "performance-aware"):
            self.patch()

    def test_volume_control_preserved(self):
        self.edit_source(lambda m: m.tracks[3].insert(0, mido.Message("control_change", channel=9, control=7, value=99)))
        self.assertTrue(self.patch()["protected_events_preserved"])
        self.assertEqual(mido.MidiFile(self.output).tracks[3][0].value, 99)

    def test_multiple_channels_rejected(self):
        self.edit_source(lambda m: m.tracks[3].insert(0, mido.Message("program_change", channel=1, program=0)))
        with self.assertRaisesRegex(ValueError, "one MIDI channel"):
            self.patch()

    def test_unclosed_note_rejected(self):
        self.edit_source(lambda m: m.tracks[3].insert(0, mido.Message("note_on", channel=9, note=99, velocity=96)))
        with self.assertRaisesRegex(ValueError, "Unclosed"):
            self.patch()

    def test_type_zero_rejected(self):
        mid = mido.MidiFile(type=0)
        mid.tracks.append(mido.MidiTrack([mido.MetaMessage("end_of_track")]))
        mid.save(self.source)
        with self.assertRaisesRegex(ValueError, "type-1"):
            midi.inspect(self.source)

    def test_meter_validation(self):
        for value in [[4, 3], [True, 4], [4], "4/4"]:
            score = copy.deepcopy(self.score)
            score["meter"] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                midi.create(score, self.output)

    def test_eighth_meter_uses_quarter_beats(self):
        score = copy.deepcopy(self.score)
        score["meter"] = [7, 8]
        midi.create(score, self.output)
        self.assertEqual(midi.inspect(self.output)["tracks"][0]["length_beats"], 8)

    def test_duplicate_json_key_rejected(self):
        path = self.root / "bad.json"
        path.write_text('{"bpm":120,"bpm":90}')
        with self.assertRaises(ValueError):
            midi.load_json(path)

    def test_bom_json(self):
        path = self.root / "bom.json"
        path.write_text('{"ok": true}', encoding="utf-8-sig")
        self.assertEqual(midi.load_json(path), {"ok": True})

    def test_cli_end_to_end(self):
        script = str(SKILL / "scripts/midi_tools.py")
        result = subprocess.run([sys.executable, script, "patch", str(self.source),
                                 "--output", str(self.output), "--track", "Drums", "--start", "4", "--end", "8",
                                 "--notes", str(SKILL / "examples/drums-replacement.json"),
                                 "--expected-sha256", self.sha], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(json.loads(result.stdout)["protected_events_preserved"])

    def test_randomized_patches_keep_other_tracks(self):
        rng = random.Random(20260918)
        for i in range(20):
            notes = [note(pitch=rng.choice([36, 38, 42]), start=4 + beat * 0.5,
                          velocity=rng.randint(40, 120)) for beat in range(8)]
            self.patch(output=self.root / f"take-{i}.mid", notes=notes)
            result = midi.inspect(self.root / f"take-{i}.mid")
            original = midi.inspect(self.source)
            self.assertEqual(result["tracks"][:3], original["tracks"][:3])


if __name__ == "__main__":
    unittest.main()
