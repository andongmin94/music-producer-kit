# Local evidence library: preservation is not production scope

Both pinned originals remain intact: **47 modules, 121 tracked files, 2,512,420 original bytes**.
[catalog.json](catalog.json) records exact commits, paths and hashes. No upstream connection or installation is needed.
The active producer supports **Korean (ko), English (en), Japanese (ja)** and instrumental work.
Raw archives are source evidence, not discoverable skills or operating instructions.

## Default production view

Use the [curated producer guides](../skills/music-producer/SKILL.md) first. For relevant detail, run the reader from the installed plugin directory:

```text
python skills/music-producer/scripts/source_library.py list
python skills/music-producer/scripts/source_library.py list mc-harmony
python skills/music-producer/scripts/source_library.py outline mc-harmony --file reference.md --limit 20
python skills/music-producer/scripts/source_library.py find mc-harmony "Locrian" --file reference.md --limit 8
python skills/music-producer/scripts/source_library.py read mc-harmony --file reference.md --start 57 --lines 55
python skills/music-producer/scripts/source_library.py verify
```

The default module list contains **42** modules. Five Chinese-specialist modules are absent and explicit access through list/read/outline/find is rejected.
The dedicated Chinese-folk-instrument file is likewise absent from its module's file list, search and normal reads.
This is a module/file boundary, not an automatic language classifier or a sentence-by-sentence scrubber.
Mixed-purpose general documents may still contain Chinese-specific examples. Use relevant general sections only; do not convert those examples into production instructions.
Chinese-written harmony, rhythm, general orchestration and other transferable theory remain accessible. Japanese kanji are not classified as Mandarin.

| Topic | Production evidence |
|---|---|
| General theory and form | mc-melody, mc-harmony, mc-progressions, mc-modulation, mc-rhythm-groove, mc-form, mc-counterpoint, mc-development |
| Arrangement and sound | mc-arrangement-arch, mc-orchestration, mc-texture-layering, mc-rhythm-section, mc-sound-design, mc-vocal-direction, mc-mix-intent |
| Genres | The eight explicit choices in the [music index](../skills/music-producer/references/music.md), as relevant |
| General lyric craft | lw-song-intent, lw-structure, lw-imagery, lw-rhyme, lw-narrative |
| Lyric language | lw-korean, lw-english, lw-japanese |
| Transferable traditions | lw-rap, lw-musical-theatre |
| Evidence/notation review | case-study and symbolic-score material only for relevant, in-scope questions; no workflow adoption |

No command establishes native diction or musical quality. Sources contain inferences and known contradictions.
Read only the needed module and section. Preserve the technique's conditions and caveats.

## Navigation semantics

list MODULE includes specialist references that are within the selected view.
outline returns actual ATX heading positions outside fenced code, bounded output and next_start; it is not a full Markdown parser.
find is literal case-insensitive search within one module, optionally one file. It returns line numbers, clipped excerpts and truncation state; it does not translate or classify language.
read accepts up to 200 lines. outline accepts up to 200 headings and find up to 50 matches. Smaller requests normally suffice.
The marker `source:mc-harmony/reference.md:57-111` names the local module, file and inclusive lines; it is not a remote fetch instruction.
Archive/file integrity is checked before reading. verify checks all original bytes and notices, even when production access excludes a module.
Missing or corrupt material is an error, never a reason to download a replacement. Nothing is extracted, installed or executed.

## Archive-only maintenance

Excluded from production: mc-style-chinese-pop, lw-mandarin, lw-cantonese, lw-chinese-style, lw-tone-check and mc-orchestration/reference-minyue.md.
They are retained in the original backups for provenance and loss prevention, not as product capabilities or pending curation tasks.
An explicit --archive-audit reader flag lets repository maintainers inspect preserved evidence. It is not a fallback when a production request is rejected and must not be used by the producer to expand language scope.
Full archival verification is always possible without that flag. The scope constants live in source_library.py; no remote catalog or runtime policy service is involved.

## Rights and intact backups

[Composition snapshot](archives/music-composition-skills.zip) · [Lyric snapshot](archives/lyric-writing-skills.zip)

[Composition LICENSE](notices/music-composition-skills-LICENSE.txt) · [Composition NOTICE](notices/music-composition-skills-NOTICE.txt)

[Lyric LICENSE](notices/lyric-writing-skills-LICENSE.txt) · [Lyric NOTICE](notices/lyric-writing-skills-NOTICE.txt)

Original file bytes, excerpts and LICENSE/NOTICE are not altered by scope filtering.
These archives do not include additional books, purchased samples, private recordings or tools never shipped upstream.
Third-party quotations retain their rights; see [NOTICE](../NOTICE.md). Preservation and public availability do not imply every passage is licensed by this project.
