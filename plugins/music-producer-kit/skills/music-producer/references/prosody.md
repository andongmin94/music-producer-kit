# Prosody: map the intended words to the actual music

Read only for the languages present in the current vocal or lyric task. A language absent from this guide is not prohibited; identify the expertise or evidence still needed.
This guide makes practical review distinctions. It does not implement a pronunciation engine, automatic tone detector or native-speaker certification.

## 1. Keep four things separate

Written characters, pronounced syllables or morae, musical note events and elapsed musical beats are different quantities.
A syllable can span several notes (melisma). Several syllables can use different short attacks on the same pitch.
Sustaining one syllable on a moving melody is not adding new syllables. A MIDI note array alone contains no reliable word segmentation.
Keep written text, intended reading, note alignment and any breath/sustain decisions together in the private song workspace.
Use one section map shared with the composition rather than duplicated tempo/key/bar metadata.

## 2. Map events, not only counts

Inspect pickups, rests, long notes, repeated-pitch attacks, ties and phrase peaks in the actual melody.
For an original five-note example, 'go' may span events 1-3 and 'home' events 4-5. Two syllables then map to five note events.
Equal syllable and note counts are not a correctness requirement; an explicit valid mapping is more useful.
Where a lyric has more attacks than the fixed melody, try a different wording or an authorized regrouping. Do not rewrite locked MIDI silently.
A breath inside a word or across a close grammatical bond is a review point, not a universal ban on expressive phrasing.
Count only after selecting the pronunciation actually intended for this take.

## 3. Korean

Start from the intended sung syllables, not the number of individual jamo. A written Hangul block is a useful initial syllable unit for ordinary full spelling, not a guarantee about every contraction or performance.
받침 is not an extra syllable. In '집에 가', a pronunciation guide can be '지 / 베 / 가': three syllables, with liaison rather than a new note for the final consonant.
Contractions, elision and chosen colloquial wording can change the number of sung units. Preserve a written lyric and its intended reading separately when they differ.
Examine long notes at the vowel and consonant transition. A closed syllable can sustain its vowel and place the final consonant near the release.
Do not automatically replace every ㄱ/ㄷ/ㅂ-final syllable, shorten a peak note or add nasal pitch solely to satisfy the archived recommendation.
The archived Korean source explicitly marks its singing rules as inference from pronunciation textbooks. Keep that weaker evidence status visible.
For intelligibility, review rapid consonant transitions and breath placement with the actual performer or audio; a spelling count cannot settle them.

## 4. Japanese

Use the intended reading rather than kanji count. Distinguish morae from syllables, kana characters and musical beats.
A contracted kana combination such as 'きょ' is one mora; the following long-vowel unit in 'きょう' adds another. This gives two morae, not a command for two separate MIDI notes.
In 'がっこう', the small っ and long-vowel unit contribute to four morae: が / っ / こ / う.
A moraic nasal, geminate closure or long vowel needs appropriate timing/articulation; it need not receive a separate pitched attack.
A spelling such as 'フリー' and an English-sung 'free' have different pronunciation planning. 'Free' can still be one syllable sung over several pitches.
Pitch accent, dialect, context and the actual sung phrase influence intelligibility. Do not assert that every word has an accented high-low pattern, or that every mismatch necessarily changes the word heard.
A peak, a long vowel, an intentionally emphasized particle or a compressed phrase can be expressive. The source's numerical limit on accent deviations is not a pass/fail rule here.
When a reading is uncertain, preserve the uncertainty and request or consult an appropriate pronunciation source rather than fabricate an accent contour.

## 5. English

Mark pronounced syllables and lexical stress, then decide phrase emphasis from intended meaning.
Lexical stress depends on the actual word and usage; do not change it casually to fit a rhyme. Phrase emphasis can legitimately change the point of the line.
Counting only stresses is insufficient for note assignment: an unstressed syllable still needs sung time unless an actual elision is intended.
Musical prominence can come from duration, pitch, attack, dynamics or syncopation, not just a notated downbeat.
Function words can be intentionally emphasized. They are not banned from strong positions.
Dialect and contractions affect the reading; do not invent extra vowel syllables in consonant clusters just to fill notes.
For mixed-language text, keep the English pronunciation decision distinct from surrounding Japanese or Korean timing conventions.

## 6. Mandarin, Cantonese and other languages

Do not reuse Japanese pitch-accent rules, English lexical stress or Korean syllable conventions as a substitute for lexical-tone analysis.
Mandarin and Cantonese require their own pronunciation and tone-melody treatment. Read the relevant bundled language module only when it is in scope.
A simplified contour mismatch can flag a risk, not prove what every listener will hear. Context, polyphony, multiple notes per syllable and articulation complicate classification.
Do not report a numerical tone-error rate without a defined reading, examined positions and a real method. Do not claim the bundled pack contains an executed automatic detector.
Detailed Chinese rhyme classes and Cantonese pitch-category tables are preserved but are not certified or fully rewritten in this increment.
For another language, use the common alignment method while explicitly identifying language-specific gaps. Do not silently translate the user's lyric into a supported language.

## 7. Recheck after a change

After editing melody, rhythm, key or text, revisit the affected alignment and any adjacent pickup or breath.
If the user asked only for alignment, preserve word meaning and note data; propose incompatible changes separately.
A valid map proves intended assignment, not successful intelligibility, pronunciation or vocal synthesis. Those need appropriate listening or performer checks.
Return a lyric sheet and alignment notes when requested; do not invent a vocal.wav or Live lyric-metadata feature.

## Local evidence and editorial boundary

[Local source reader](../../../library/README.md):

- `source:lw-korean/SKILL.md:65-220` — syllables, liaison and explicitly inferred singing advice; automatic coda replacement removed.
- `source:lw-japanese/SKILL.md:53-145` — mora/note distinction and phrasing risks; forced one-mora/one-note and accent quotas removed.
- `source:lw-english/SKILL.md:50-100` — stress and emphasis; a universal unstressed-syllable/downbeat ban is not retained.
- `source:lw-workflow/LYR-SPEC.schema.md:1-95` — bidirectional handoff; common Chinese character-count and rhyme requirements removed.

Examples and corrective distinctions are this project's exposition, not reproduced lyrics. Detailed native diction and the full five-language reference tables still require further editorial review; file tests do not validate natural sung language.
