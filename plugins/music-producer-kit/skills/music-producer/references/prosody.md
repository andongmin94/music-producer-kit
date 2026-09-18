# Prosody: Korean, English and Japanese

Production language set: `ko`, `en`, `ja`. Select only languages present in this task; instrumentals have no lyric language.
A Korean conversation does not force Korean lyrics. A Japanese artist reference does not authorize switching an English lyric into Japanese.
Unsupported languages are outside this kit's product scope: identify the limitation, preserve supplied material, and do not silently translate it or load excluded modules.

| Sung language | Read when that language is actually present |
|---|---|
| Korean | [Korean lyric setting](lyrics-korean.md) |
| English | [English lyric setting](lyrics-english.md) |
| Japanese | [Japanese lyric setting](lyrics-japanese.md) |

## 1. Distinguish text, pronunciation and music

Written characters, pronounced syllables or morae, note events and musical beats are different quantities.
A syllable may span several notes; multiple syllables may use separate attacks at the same pitch.
A tied continuation, a repeated-pitch attack and a breath do not have identical articulation.
Keep the original text, intended reading and note assignment together in the private song workspace.
Do not infer pronunciation language from script alone: Japanese kanji are not a request for Mandarin; romanization does not automatically mean English.

## 2. Inspect the fixed side before filling the other

Music-first: obtain actual notes, rests, pickups, duration and phrase boundaries. Fit words within protected notes.
Lyrics-first: establish the reading and intended emphasis, then compose the setting; recheck after music changes.
Jointly delegated: choose the smallest useful change and record it. Do not keep contradictory section maps.
If both words and notes are fixed and the intended setting does not fit, identify the conflict instead of changing either silently.
A theory or text-only task does not require DAW setup.

## 3. Use an event assignment, not equality of counts

Original illustrative map for a five-event melody: `go` uses events 1-3; `home` uses events 4-5.
This is two syllables over five events, not five invented syllables. The syllable's vowel carries the moving pitch.
For each phrase, record only useful information: section/time range, original line, intended sung units, unit-to-note assignment, breath and uncertain pronunciation.
Count after selecting the actual reading. A consonant closure or a sustained vowel need not receive a new pitched attack.
An event map describes intent; it does not prove correct audible pronunciation or a successful synthesis.

## 4. Mixed-language phrases

Mark the language of each sung span, not a new language for the whole song.
For `오늘은 stay here`, handle `오늘은` with Korean rules and `stay here` with the intended English pronunciation. Do not respell the English as Korean unless that is the chosen performance.
For `きみと stay here`, keep Japanese timing and the English syllable plan distinct. A katakana loanword and an English-sung word are different readings.
Two or three supported languages can coexist. Do not add Mandarin/Cantonese material as a fusion default.
Borrowed words, names and kanji need their actual reading confirmed where ambiguous; do not classify them by Unicode ranges and remove them automatically.

## 5. Review the affected phrase

Check preserved words, preserved note data, pronunciation, intended emphasis, breath and the incoming/outgoing seam.
A changed key may affect the performer without changing syllable count; a rhythm edit may require remapping despite unchanged pitches.
Read back actual file/tool state for structural checks. Label listening, native-language review and vocalist approval as unverified unless they happened.
Do not enforce equal line lengths, deliberate asymmetry, mandatory rhyme breaks or changed lyrics on every chorus.
Mandarin tone matching, Cantonese pitch categories and Chinese rhyme classes are not pending production features.

## Local evidence and editorial boundary

[Local reader](../../../library/README.md):

- `source:lw-korean/SKILL.md:60-202` — written syllables, liaison and explicitly inferred singing advice.
- `source:lw-japanese/SKILL.md:50-122` — mora, reading and note-mapping distinctions.
- `source:lw-english/SKILL.md:47-97` — lexical stress and phrase emphasis.
- `source:lw-workflow/LYR-SPEC.schema.md:1-77` — historical text/music interface; shared Chinese-specific fields are not retained.

The examples and workflow are project-authored adaptations. The archived sources are not pronunciation engines or universal artistic laws. Detailed language references are local; external citations in the language guides are verification provenance, not runtime dependencies.
