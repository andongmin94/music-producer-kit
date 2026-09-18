# Deterministic MIDI helper

The bundled [script](../scripts/midi_tools.py) uses Mido, not a custom MIDI encoder.
Install the plugin's requirements into the selected Python environment. Do not silently modify system Python.
Run it with that interpreter. Write all outputs to a user workspace, never inside an installed plugin.

## Create

`python midi_tools.py create score.json take-1.mid`

See [the original two-bar fixture](../examples/song.json).
Required score fields: bpm, meter [numerator, denominator], length_beats, tracks.
Each track: unique ASCII name, channel (0-15), optional program (0-127), notes.
Each note: pitch (0-127), start, duration, velocity (1-127).
Time is in zero-based quarter-note beats, not bar numbers; output resolution is 480 ticks per quarter note.
The fixture's Drums channel is 9 (MIDI channel 10), but Live still needs verified pad/sound assignments.
All notes must lie within the requested duration. Same-pitch overlaps in one channel are rejected rather than interpreted ambiguously.
Unsupported fields are rejected, not silently ignored. JSON does not generate audio or install instruments.

## Inspect

`python midi_tools.py inspect take-1.mid`

Returns source SHA256, track event fingerprints, lengths and note data.
The tool supports synchronous type-1 PPQ MIDI only. SMPTE timing and type-0/type-2 files require an explicit separate conversion before this tool can be used.
No automatic conversion is hidden inside an edit. Tempo maps in existing supported files remain untouched.

## Replace notes in one interval

`python midi_tools.py patch take-1.mid --output take-2.mid --track Drums --start 4 --end 8 --notes notes.json --expected-sha256 SHA_FROM_INSPECT`

The interval is [start,end); note-offs may be at end. Replacement note starts use absolute quarter-beat positions, not offsets from the edit start.
See [replacement notes](../examples/drums-replacement.json).
Only the matching single-channel target's note events in the interval change.
Other tracks and the target's non-note events/out-of-region notes are fingerprinted and verified after serialization and re-reading.
Original notes crossing the boundary, sustain/sostenuto/channel-mode control usage, ambiguous note pairing, a changed input hash and existing output files cause an error.
This conservative helper is not a general performance editor; route those unsupported cases to a verified editor, never disable safeguards to claim success.

The report's protected_events_preserved covers this MIDI edit only, not Live device parameters, mixer automation, audible equivalence or source licensing.
All commands create new outputs; no force-overwrite option exists.

Mido project and API reference: https://github.com/mido/mido
