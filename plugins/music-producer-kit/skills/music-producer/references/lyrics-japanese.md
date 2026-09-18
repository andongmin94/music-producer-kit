# Japanese lyric setting

Use for Japanese-sung spans. Start from [the common mapping method](prosody.md). Japanese kanji do not imply that Chinese pronunciation material is needed.

## 1. Establish the reading

Keep the written lyric and intended kana reading separate, especially for kanji, names, numbers and ambiguous readings.
Do not infer a Chinese reading from shared characters. Do not remove kanji as part of the Chinese-scope exclusion.
Count morae from the chosen Japanese reading, not the number of kanji or Unicode code points.
Do not fabricate a pitch-accent dictionary lookup or native-language approval.

## 2. Morae are not MIDI beats

A contracted combination such as `きょ` is one mora. A long-vowel unit adds time in the reading; the small っ and moraic ん also contribute to the mora count.
The Tokyo University of Foreign Studies teaching module explains these counting distinctions and the role of special morae in Japanese timing.
They describe pronunciation, not a requirement that every mora become one quarter note or one pitched attack.

| Reading | Mora grouping | Count | Setting question |
|---|---|---:|---|
| きょう | きょ / う | 2 | Can the long vowel continue without a new attack? |
| がっこう | が / っ / こ / う | 4 | Where does closure fall, and how does the long vowel continue? |
| フリー | フ / リ / ー | 3 | Is this the chosen Japanese loanword reading? |

The examples illustrate pronunciation units. They do not dictate tempo, pitch, breath or the final performance duration.
An English-sung `free` is a different reading from Japanese `フリー`; one English syllable may still span several notes.

## 3. Preserve special timing without inventing sounds

A geminate closure need not be assigned a sustained pitched vowel. Preserve its timing against the following consonant.
A moraic nasal and a long vowel need an appropriate continuation; they are not necessarily fresh vowel attacks.
If a phrase is too dense, consider authorized changes to wording, placement, sustain or grouping, not simply dropping every special mora.
Do not strip long vowels, nasal timing or closures merely to make a count equal the melody's note count.
The Japan Foundation's teaching discussion reports comprehension problems from missing or inserted special morae; it does not establish a universal automatic song-error threshold.

## 4. Accent and musical emphasis

Pitch accent, intonation, dialect and context are not interchangeable concepts.
A melody need not duplicate a spoken pitch contour at every event. Check whether the intended words remain understandable in the actual phrase.
An emphasized particle or an unexpected high note may be deliberate. There is no fixed maximum number of allowed accent deviations.
Treat a suspected ambiguity as something to examine, not proof of the exact alternate sentence every listener will hear.
Do not map Mandarin/Cantonese lexical-tone categories onto Japanese words.

## 5. Music-first and lyrics-first work

Music-first: inspect the protected note events, proposed kana reading, rests and pickups; map the units without changing locked melody data.
Lyrics-first: keep the meaning and chosen reading, build a musical phrase, and revisit fit once notes exist.
Shared kanji, kana count or an artist name cannot determine the exact melody to use.
When both sides are fixed, report a local conflict rather than changing protected notes or words silently.
Rhyme and traditional phrase lengths are optional musical choices, not mandatory checks for every Japanese lyric.

## 6. Handoff

Provide the requested written lyric, kana reading when useful, and affected unit-to-note assignments.
Mark unresolved pronunciation, performance and listening checks separately. No successful vocal render is implied by a readable MIDI file.
For English or Korean spans inside the song, load only their corresponding language guide and keep one shared section map.

## Evidence and editorial boundary

[Local reader](../../../library/README.md): `source:lw-japanese/SKILL.md:53-145`.
The archive's one-mora/one-note shortcuts and numerical accent-deviation gates are not adopted.
Primary pronunciation teaching references checked on 2026-09-18:
- [Tokyo University of Foreign Studies: 拍感覚基礎](https://www.coelang.tufs.ac.jp/mt/ja/pmod/practical/01-10-01.php).
- [Japan Foundation: 日本語特殊拍の習得](https://www.jpf.go.jp/j/project/japanese/teach/tsushin/research/031.html).
Relevant distinctions are summarized in this local guide; the links are provenance and are not needed at runtime. Musical setting examples and protection rules are project-authored adaptations, not reproduced lyrics or claims of native singing validation.
