# Vocal production: guide, recording or synthesis

Read when the task actually includes vocal performance or audio production. Lyrics alone, a vocal-melody MIDI guide and a sung recording are different deliverables.

## 1. Pick only the requested route

A melody guide provides notes and rhythm, optionally a guide instrument. It is not a singer.
A recorded-vocal edit starts from a real recording and preserves the original take.
A singing-synthesis request needs a verified engine and input/control path; a lyric document or MIDI file does not supply that capability.
A text-only lyric request needs none of the above setup.
Do not infer voice-cloning permission from an artist reference, a sample filename or an instruction to use a similar musical style.

## 2. Make a performance direction actionable

Describe what the phrase needs: clearer consonant attacks, a longer vowel, gentler onset, a denser or lighter tone, a contrasting phrase ending, or a more restrained delivery.
Distinguish level from timbre and expression. A fader change does not produce a different vocal articulation.
Consider where a consonant starts and where the vowel carries the pitch and duration. Avoid treating every syllable as an indivisible rectangular MIDI event.
These are communication choices, not demonstrated engine parameters. A tool must actually support a requested control before it is promised.
Avoid universal instructions to sing breathily, detune, vary each chorus or leave errors for 'humanity'. A tight, consistent performance can be intended.

## 3. Harmony and doubles

Choose the function first: emphasize a word, widen a phrase, support a chord, answer the lead or provide another character.
A harmony voice needs its own note/word alignment and a check against the actual chords; a parallel third is not correct for every event.
A recorded double is a separate performance. Copying one waveform is not automatically the same result, and a delay-based double can alter phase behavior.
Retain separately editable voices and source takes. Do not flatten a lead and its backing vocals into one file unless that deliverable is requested.
Panning, timing alignment and effects depend on the arrangement and actual recordings; no fixed double/triple recipe is required.

## 4. Pitch and timing edits

Identify whether the user wants correction, a deliberate effect or preservation of a characteristic gesture.
Distinguish note center, drift, vibrato, transition and timing rather than forcing every frame onto an ideal grid.
Changes to formants, vowel duration or consonant placement may alter identity and intelligibility. Inspect actual controls and compare when audio is available.
A pitch editor being installed does not prove that its internal editor is exposed through the available MCP or host API.
Do not fabricate Melodyne scripting, synthesis, license access or successful rendering.
Save an editable take/version and record what was changed before producing an optional flattened export.

## 5. Verify the right thing

Check the resulting file, timeline, protected regions and source availability. Successful playback is not evidence that the agent listened.
Where listening is possible, compare expression, wording, pitch behavior and the fit in the full mix, not only the isolated vocal.
Without listening, report structural/parameter checks and the remaining performer or user review.
Do not diagnose a buried vocal as primarily bad intonation without evidence; arrangement density, level, tone, space and masking are also candidates.

## Local evidence and editorial boundary

[Local source reader](../../../library/README.md):

- `source:mc-vocal-direction/SKILL.md:1-105` — performance vocabulary and consonant/vowel distinction; perfection-as-AI claims and fixed delivery quotas removed.
- `source:mc-workflow/SKILL.md:220-300` — scope of source diagnostics and handoff; diagnostic hypotheses are not measured facts.

Specific harmony stacks, recorded examples and detailed mix practice are still in the local archives pending fuller adaptation. Actual Melodyne, Splice and singing-engine connectors are not supplied by this guide.
