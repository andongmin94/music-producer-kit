# Current status

Updated: 2026-09-18. Milestone: 0.3.0 scoped craft guides and local source navigation.

## Implemented in this increment

- Seven working guides: harmony, melody/form, rhythm, texture/instruments, lyric craft, prosody and vocal production. The single entry skill selects only the applicable guide; the former broad summaries are routing indexes.
- Each guide records bounded local source ranges, its editorial corrections and the remaining specialist coverage. See knowledge-curation.md.
- Explicit distinctions between protected melody/chords/bass, tonal conventions and requirements, real pronunciation and written counts, note events and syllables, recorded vocals and synthesis.
- The existing standard-library source reader now supports module-scoped literal search and fenced-code-aware ATX outlines, with bounded output, source positions and preserved evidence warnings.
- An original four-bar editable harmony/bass study using the existing Mido helper, with document-to-note and protected-edit tests.
- Fourteen new tests for navigation, source markers, independent distribution and executable examples. No new dependencies, MCP implementation or extra permanent CI workflow.

## Preserved working product

Both complete pinned source snapshots remain unchanged: 47 modules, 121 tracked files, 2,512,420 original bytes, with file/archive hashes and original LICENSE/NOTICE.
The original SKILL.md files remain archived data, not discoverable skills. No upstream download, submodule, silent remote recovery or automatic update is introduced.
The scoped MIDI helper remains unchanged. Source books, audio, internal tools and corpora never shipped by upstream are not included.

## Observed verification before final validation

Baseline 0.2.0: CI run 35299974015 passed the 64-test suite and package build on Windows/Linux, Python 3.12.
Review-branch run 35305684141 also passed the baseline suite on both platforms and read selected evidence directly from the local archives. Its temporary source-inspection CI step has been removed from the final change.
The new 0.3.0 guide/navigation/example tests are written; their final CI result is not yet recorded at this checkpoint.
Do not interpret prior baseline passes as validation of the new code.

Static/offline tests are not model behavioral or musical-quality evaluations.
Codex plugin activation, actual Ableton MCP operations, Live save/reopen, audio rendering and listening: NOT RUN.
No Splice/Melodyne/singing connector or project-wide license grant has been added.

## Preservation versus editorial adaptation

Complete original file preservation: COMPLETE.
Selected seven-guide adaptation with local examples and caveats: IMPLEMENTED, validation pending at this checkpoint.
Editorial conversion or independent verification of every source paragraph/table: NOT COMPLETE.
Genre, specialist orchestration, extended harmony/form/counterpoint, language and sound-design details remain in the local library for targeted review.
See knowledge-curation.md for what moved and what still needs work; do not claim all 47 modules were fully rewritten.

## Next concrete step

Observe the current code's Windows/Linux tests and package build before merging.
Then verify real Windows/Codex activation and actual MCP schemas; prove an editable scratch Live Set, save/reopen and a scoped edit before claiming DAW automation.
Continue specialist knowledge adaptation from local evidence without a genre whitelist or mandatory aesthetic gates.

## Session handoff

Read actual repository state, AGENTS.md and this file before work.
Do not repeat resolved global genre/voice questions. Keep private paths, recordings, samples and unpublished songs outside this repository.
Record actual test run IDs, failures, fixes and remaining blockers when ending a session. A queued run is not a passing run.
