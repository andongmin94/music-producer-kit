# Current status

Updated: 2026-09-18. Milestone: 0.3.0 scoped craft guides and local source navigation.

## Implemented

- Seven working guides: harmony, melody/form, rhythm, texture/instruments, lyric craft, prosody and vocal production. The single entry skill selects only the applicable guide; former broad summaries are routing indexes.
- Each guide records bounded local source ranges, editorial corrections and remaining specialist coverage. See knowledge-curation.md.
- Explicit distinctions between protected melody/chords/bass, tonal conventions and requirements, pronunciation and written counts, note events and syllables, recorded vocals and synthesis.
- The existing standard-library source reader supports module-scoped literal search and fenced-code-aware ATX outlines, with bounded output, source positions and evidence warnings.
- An original four-bar editable harmony/bass study using the existing Mido helper, with document-to-note and protected-edit checks.
- Fourteen additional tests. No new dependencies, MCP implementation or extra permanent CI workflow.

## Observed verification

CI run 35306688700 for PR #1, head 9108ef409df015331f62817b2ac9ba202af78d46, passed on ubuntu-latest and windows-latest with Python 3.12.
Both jobs passed package validation, unittest discovery and install-ZIP generation. Ubuntu log explicitly records 78 tests, all passing (64 existing + 14 added).
Validated behavior of the tools: literal Unicode/case-insensitive module search; bounded results and truncation; heading pagination; exclusion of fenced-code headings; invalid arguments; network-disabled reads; no source extraction; real source-range markers; independent distribution; original MIDI voicing/length correspondence; scoped bass replacement with unchanged harmony and source.
The current documentation-only follow-up records that observed run; it does not claim an unobserved later run passed.

The review-only source inspection run 35305684141 read selected evidence directly from the local archives and passed the baseline 64-test suite on both platforms.
Its temporary source-inspection CI step and review-branch trigger have been removed. One ordinary Windows/Linux CI workflow remains.
No complete new-version local checkout/test run in this chat container is claimed; the integrated results above were observed in GitHub Actions.

Static/offline tests are not model behavioral or musical-quality evaluations. The 12 model behavior scenarios remain defined, NOT RUN.
Codex plugin activation, actual Ableton MCP operations, Live save/reopen, audio rendering and listening: NOT RUN.
No Splice/Melodyne/singing connector or project-wide license grant has been added.

## Preservation versus editorial adaptation

Both complete pinned source snapshots remain unchanged: 47 modules, 121 tracked files, 2,512,420 original bytes, with file/archive hashes and LICENSE/NOTICE.
The original SKILL.md files remain archived data, not discoverable skills. No upstream download, submodule, silent remote recovery or automatic update is introduced.
The scoped MIDI helper remains unchanged. Source books, audio, private tools and corpora never shipped by upstream are not included.

Full original file preservation: COMPLETE.
Selected seven-guide adaptation with local examples and caveats: IMPLEMENTED; offline tool/package/example tests PASS in the run above.
Editorial conversion or independent verification of every source paragraph/table: NOT COMPLETE.
Genre, specialist orchestration, extended harmony/form/counterpoint, language and sound-design details remain in the local library for targeted review.
See knowledge-curation.md for what moved and what still needs work; do not claim all 47 modules were fully rewritten.

## Next concrete step

Verify real Windows/Codex activation and actual MCP schemas; prove an editable scratch Live Set, save/reopen and a scoped edit before claiming DAW automation.
Continue specialist knowledge adaptation from local evidence without a genre whitelist or mandatory aesthetic gates.
Use the installed local outline/find/read commands rather than reading whole archives or fetching upstream websites.

## Session handoff

Read actual repository state, AGENTS.md and this file before work.
Do not repeat resolved global genre/voice questions. Keep private paths, recordings, samples and unpublished songs outside this repository.
Record actual test run IDs, failures, fixes and remaining blockers when ending a session. A queued run is not a passing run.
