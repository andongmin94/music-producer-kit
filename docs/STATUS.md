# Current status

Updated: 2026-09-18. Milestone: 0.4.0 Korean/English/Japanese scope and language-specific curation.

## Implemented in this increment

- Owner-confirmed lyric/vocal scope: ko, en, ja, including mixtures. Instrumental work remains independent of lyric language and non-excluded genres remain broad.
- Chinese/Mandarin/Cantonese production, Chinese-style songwriting and Chinese traditional orchestration removed from active routing and future editorial priorities.
- Default source list/read/outline/find excludes five Chinese-specialist modules and mc-orchestration/reference-minyue.md. Default module count: 42.
- An explicit maintenance-only archive-audit view preserves access to all 47 modules; it is not a production fallback.
- Chinese-written general theory stays available. No character-range language detector is used; Japanese kanji must not be rejected as Mandarin.
- Common prosody is separated from three focused Korean/English/Japanese guides with local source locators and original working examples.
- Eight additional behavioral scenario definitions cover long Korean syllables, Japanese kanji, English melisma, mixtures, excluded requests, general-theory language and instrumental genres.
- Fifteen additional static/tool/distribution tests. Existing preservation test explicitly uses archive-audit mode for full coverage.

## Preservation and implementation limits

All 121 original files / 47 modules / 2,512,420 bytes remain unchanged, including source archives and original notices.
Module/file scope filtering does not scrub every Chinese-specific sentence from shared source documents. Curated routing and source warnings distinguish transferable theory from excluded examples.
No new dependency, remote source lookup, automatic updater, synthesizer, MCP implementation, DAW controller or permanent CI workflow was added.
The existing Mido helper and editable harmony study are unchanged.

## Verification checkpoint

Baseline 0.3.0: PR #1 runs 35306688700 and 35306874476 passed before merge; 78 tests and packaging on Windows/Linux were observed.
The 0.4.0 changes and 15 new tests are written. Their CI result is pending at this checkpoint; the old baseline pass is not a new-version pass.
This chat container could not resolve github.com for a local clone. No full local checkout/test pass is claimed; integrated validation will be observed through GitHub Actions.

Actual Codex behavior scenarios: 20 DEFINED, NOT RUN. Static tests of definitions do not execute prompts.
Codex activation, actual Ableton/MCP operations, Live save/reopen, rendering, listening and native-language performance review: NOT RUN.
Full archival preservation: COMPLETE. Editorial adaptation or independent verification of every in-scope source paragraph/table: NOT COMPLETE.
No project-wide license grant, Splice/Melodyne/singing connector or purchase authorization was added.

## Next concrete step

Observe Windows/Linux CI for this change before merging. Record the run and fix failures without weakening the scope contract.
Then verify actual Windows/Codex activation and real MCP capabilities, and prove editable Live creation, save/reopen and a scoped edit.
Continue useful general theory and ko/en/ja specialist curation; Chinese-specific modules are excluded, not deferred.

## Session handoff

Read actual state, AGENTS.md and requirements before continuing. Do not re-ask for permanent genre/voice defaults or reopen the language scope without a new owner decision.
Keep private recordings, paths, samples and unpublished songs outside this public repository.
Update status with actual run IDs, results, limitations and next steps at the end of each session.
