# Rhythm and rhythm-section programming

Read for groove, drums, bass attacks, rhythmic density or time calculations. A rhythm edit is not implicit permission to change tempo or melody.

## 1. Separate the controls

Tempo is speed in a declared beat unit. Meter groups time. Subdivision divides beats. Accent gives events prominence. Microtiming displaces events relative to their intended grid.
Half-time feel can change the backbeat without halving the transport BPM. Twice as many hats can increase density without doubling BPM.
Syncopation can involve displaced accents, anticipation, ties or rests; it is not restricted to a single tied-note formula.
A notated offbeat is not the same thing as an arbitrary millisecond delay.
Decide which of these the request concerns before moving notes.

## 2. Concrete helper time units

The MIDI helper uses quarter-note beats and zero-based onsets. An edit region is [start, end): its start is included and its end is the boundary.
In 4/4, bar 1 starts at 0, bar 2 at 4 and bar 5 at 16 quarter beats.
In 7/8, each bar is 3.5 quarter beats. In 6/8, each bar is 3 quarter beats although a performer may feel two dotted-quarter pulses.
For 6/8 at dotted-quarter = 80, the equivalent quarter-note BPM is 120. Do not insert 80 as a quarter-note tempo without interpreting the intended unit.
At quarter BPM b, a displacement of d milliseconds is d*b/60000 quarter beats. At 120 BPM, 10 ms = 0.02 quarter beats.
The existing helper requires representable PPQ positions; use its validation rather than silently rounding expressive input.
Live API time units and displayed bar labels must be discovered separately; do not assume they share every helper convention.

## 3. A straight 4/4 example, not a universal drum recipe

```text
quarter-beat grid: 0   0.5   1   1.5   2   2.5   3   3.5
kick attacks:     0                   2
snare attacks:             1                   3
closed-hat:       0   0.5   1   1.5   2   2.5   3   3.5
```

A half-time variant may place the main snare at 2 while leaving BPM unchanged. The two examples are not necessarily interchangeable within a genre.
Hat articulation and velocity can change without shifting attacks. Open-hat release and choking depend on the actual device and samples.
MIDI pitch 36 or channel 10 does not prove a kick is loaded: inspect the Drum Rack mapping or instrument actually used.

## 4. Kick and bass relationships

Aligned attacks emphasize a shared pulse. Answering gestures separate their events. Interlocking gestures distribute a combined pattern.
These are compositional options, not genre-based bans. Check bass sustain as well as onsets: long low notes can overlap kicks even when attacks alternate.
A root at a harmonic arrival can clarify harmony, but inversions, anticipations, pedal notes and intentional rests are valid.
Do not impose the archived 'bass must play the root on every chord-change downbeat' rule.
When only drums are authorized, retain the bass and search for a compatible drum pattern. Propose a bass change separately when necessary.

## 5. Groove without compulsory randomness

First preserve the identity of the pattern. Choose whether exact quantization, swing, a deliberate part offset or a performance-derived pattern serves the request.
Swing is a relationship between subdivision positions, not a command to delay every other event by a fixed amount at every tempo.
A two-to-one eighth-note ratio puts the second attack at 2/3 of a quarter-note pair; it is one example, not the definition of all swing.
Avoid independently randomizing every attack, note length and velocity: that can erase relationships that make the groove coherent.
If using repeatable randomized proposals, retain the seed and the original for comparison; do not equate reproducibility with quality.
Exact electronic timing can be the finished choice. Preserve an approved groove rather than 'humanizing' it automatically.

## 6. Articulation, fills and realism

Velocity may change loudness, timbre or sample layer depending on the instrument. It is not interchangeable with a track-volume fader.
A ghost note is a low-prominence rhythmic gesture; its placement and timbre matter, not just a small velocity number.
Fills can introduce a seam, answer a phrase, or deliberately withhold a familiar event. A fixed four-bar fill can be correct.
When acoustic realism is requested, check plausible simultaneous hits, sticking, pedal behavior and transitions. Synthetic music may intentionally ignore physical limbs.
After shortening a note, inspect the release and sample behavior where possible. A one-shot may keep sounding after MIDI note-off.
Do not fix an arrangement conflict with unverified choke or CC settings.

## 7. What to verify

Read back timestamps and note lengths; check protected event signatures for a scoped edit.
Listen to the interaction of kick, bass and melody when audio exists, not just each part soloed.
Check that the fill returns to the intended pattern and the last note does not cross an unauthorized boundary.
Without audio, report the pattern and timing changes and leave the audible groove judgement open.

## Local evidence and editorial boundary

[Local source reader](../../../library/README.md):

- `source:mc-rhythm-groove/SKILL.md:41-98` — tempo versus density, metric position and anticipation; rigid definitions and root mandates relaxed.
- `source:mc-rhythm-section/SKILL.md:1-100` — feel, pattern selection, kick-bass relationship and performance context.

The grid and unit calculations are project examples. Device-specific mappings are deliberately not inferred from these sources. Specialist genre patterns remain available in the full local archive.
