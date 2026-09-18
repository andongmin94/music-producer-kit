# Melody and form: develop an idea without losing it

Read for melodic creation, humming-to-song work, phrase revision or formal development. A mix-only change does not authorize rewriting the melody.

## 1. Identify the seed and the protected version

For humming, retain the original recording. Separate uncertain transcription from a proposed artistic change.
Pitch errors, octave errors, missed pickups and quantization errors are different diagnoses. Do not correct expressive timing by default.
For an existing MIDI line, inspect actual pitches, durations, onsets and rests rather than inferring it from a track name.
A useful seed can be a rhythm, interval contour, riff, lyric accent or timbral gesture. It need not always be a new sung tune.
Record the characteristic that should survive: a syncopated pickup, a repeated pitch, a leap-and-return, or a particular phrase ending.
The statement is a short production note, not a demand for a large specification document.

## 2. Shape a phrase with independent controls

Contour, interval size, duration and metrical placement can change independently.
Stepwise motion, repeated tones, prepared leaps and unprepared leaps are expressive options. An ascending line is not intrinsically happy, nor a descending one intrinsically sad.
A resting point comes from harmony, rhythm, register, articulation and context together; the lowest or longest note need not be the ending.
A hook need not be the highest, busiest or loudest part.

For a singer, consider tessitura (where the voice spends time), repeated high notes, approach to difficult intervals, breath opportunities and the words at the peak.
Do not infer comfortable range or passaggio from gender, a reference artist or one successful extreme note.
A provisional guide can be written without an interview; identify it as provisional until a singer or actual recording validates it.
Do not impose the archived sixth-leap limit, fixed octave range or fixed climax fraction as laws. A large leap may be the user's central idea.

## 3. An original motif example

The following is one 4/4 bar measured in quarter-note beats, not seconds. Pitch numbers are authoritative; C4 = 60 in this document.

```text
pitches:   60   62   64   67
onsets:   0.0  0.5  1.0  2.0
durations: 0.5  0.5  1.0  2.0
```

The last note ends at beat 4.0. Keep a rest explicitly when a rest is intended rather than extending the last note to fill the bar.
A repeat can use exactly these notes. An ending variant could replace the final 67 with 65 while keeping timing, but must be checked against the actual chord.
Transposing the pitches by two semitones gives 62, 64, 66, 69. That preserves semitone intervals but is not necessarily a diatonic sequence within the original C-major context.
A tonal sequence preserves a scale-degree pattern and may change interval sizes. Do not silently substitute one operation for the other.
These examples illustrate operations, not default material to reuse in every generated song.

## 4. Development menu

| Operation | What is retained | What changes | Common failure |
|---|---|---|---|
| Repeat | The recognizable material | Nothing, or only production context | Rewriting a requested exact repeat |
| Sequence | A contour or interval/rhythm relationship | Starting pitch or scale-degree position | Accidental harmonic collision |
| Vary | Selected identity features | A rhythm, ending, ornament or articulation | Changing all identity cues together |
| Fragment | A meaningful part of the idea | Length and subsequent context | Fragments with no phrase direction |
| Extend | Earlier statement | Continuation or delayed closure | Padding without a destination |
| Contract | Main information | Removed repetitions or shorter values | Deleting the identifying pickup |
| Augment/diminish | Pitch sequence or rhythmic proportions | Durations by a factor | Broken section length or unintended tempo change |
| Add a counterline | Primary line | A complementary voice | Competing peaks and dense simultaneous attacks |
| Return | Earlier identity | Context after intervening material | Treating every return as a new theme |
| Contrast | Some continuity cue if desired | A genuinely different idea | An accidental unrelated song inside the song |

These are alternatives, not a ten-item checklist. Exact repetition may provide the intended identity or function.
No fixed maximum fraction of new material applies to every piece.

## 5. From phrase to requested deliverable

For a whole song, choose section functions and duration from the brief and the actual material; do not mistake copying one loop for completing an undelegated form.
For a loop request, a coherent loop can be the complete deliverable. No verse, pre-chorus, lyrics, modulation or climax is required.
For a section rewrite, inspect the incoming and outgoing seams but preserve protected neighboring content.
An arrangement can communicate a new section without changing the melody: register of support, sustained versus short accompaniment, percussion subdivision, space or silence can do it.
For a bridge, a change in harmony or perspective may be sufficient; a wholly unrelated tune is optional.
For a final chorus, first decide whether recognition or transformation is wanted. An exact chorus can be correct.

## 6. Duration and loop seams

A constant 4/4, 120-quarter-note-BPM section of 8 bars lasts 16 seconds. This says nothing about its musical energy.
General constant-meter quarter beats per bar = numerator * 4 / denominator. Sum segment durations separately for meter or tempo changes.
A loop has both a musical seam and an audio seam. Check note-offs, pickups, automation resets, sustain and effect tails when the available tools can expose them.
Do not promise a click-free loop from MIDI alone or infer rendered tail behavior without audio.
A turnaround implying return may suit a loop; a final cadence may suit a finite song. Neither is obligatory.

## 7. Scoped review

Name the changed identity dimension and compare the protected dimensions against the source.
When instructed to preserve a melody exactly, even an octave shift, note shortening or pickup adjustment needs authorization.
A strong artistic reason can be proposed outside scope without applying it silently.
Do not claim improved singability or memorability from file validity. Mark the remaining listening or performer check.

## Local evidence and editorial boundary

[Local source reader](../../../library/README.md):

- `source:mc-melody/SKILL.md:47-135` — contour, timing and preparation of leaps; absolute leap and climax rules are not retained.
- `source:mc-development/SKILL.md:1-115` — identity, development versus accumulation, repetition and thematic continuity.
- `source:mc-workflow/SKILL.md:185-220` — numerical duration and section consistency; aesthetic gates removed.

The motif and time calculations are original examples. The protected-material, loop-delivery and transcription protocols are project decisions, not quotations or demonstrated musical-quality improvements.
