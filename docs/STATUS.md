# Current status

Updated: 2026-09-18. Milestone: 0.4.0 Korean/English/Japanese scope and language-specific curation.

## Implemented

- Owner-confirmed lyric/vocal scope: ko, en, ja, including mixtures. Instrumentals need no lyric language; non-excluded genres remain broad.
- Chinese/Mandarin/Cantonese production, Chinese-style songwriting and Chinese traditional orchestration removed from active routing and future editorial priorities.
- Default source list/read/outline/find excludes five specialist modules and mc-orchestration/reference-minyue.md. Production module count: 42.
- Explicit archive-audit mode is maintenance-only evidence access to all 47 modules, not a production fallback.
- Chinese-written general theory remains accessible; no character-range language detector is used. Japanese kanji must not be rejected as Mandarin.
- Common prosody is separated from three focused Korean/English/Japanese guides with local source locators and original examples. English/Japanese pronunciation distinctions were additionally checked against primary teaching materials cited in those guides.
- Eight new behavior scenario definitions and fifteen new static/tool/distribution tests. Full-preservation read tests explicitly use the audit view.

## Observed verification

PR #2 run 35308062775 on head 05321c8da8dcd903ca907793799360b258b954e5: SUCCESS on windows-latest and ubuntu-latest, Python 3.12.
Both jobs passed python tools/check.py, unittest discovery and install-ZIP generation. The Ubuntu log explicitly records 93 passing tests (78 existing + 15 added).
Verified: default 42-module list, rejection of all five excluded modules through every reader entrypoint, hidden specialist file, module search excluding that file, explicit and non-sticky audit access, original archive hashes, full 121-file verification, network-free access, no extraction, packaged language guides, source-line locators and CLI scope behavior.
The independent distribution test uses the installed package copy and preserves the same access boundary without upstream access.
The original source snapshot count remains 47 modules / 121 files / 2,512,420 bytes. Both archive SHA256 values match the original captures.
This documentation-only follow-up records the observed code run; it does not claim that a later unobserved run passed.
A full local checkout/test pass in this chat container is not claimed: github.com name resolution prevented cloning. Integrated results above were observed in GitHub Actions.

## Remaining limits

Scope filtering is module/file-level, not sentence-level removal of every Chinese-specific example from shared source documents. Use only relevant general sections; archived wording is not operating policy.
No new dependency, remote source lookup, automatic update, synth, MCP implementation, DAW controller or permanent CI workflow was added. Mido and the editable harmony study are unchanged.
Actual Codex behavior scenarios: 20 DEFINED, NOT RUN. Definition tests do not execute prompts.
Codex activation, actual Ableton/MCP operations, Live save/reopen, rendering, listening and native-language performance review: NOT RUN.
Full archival preservation: COMPLETE. Independent verification/editorial adaptation of every in-scope paragraph/table: NOT COMPLETE.
No project-wide license grant, Splice/Melodyne/singing connector or purchase authorization was added.

## Next concrete step

Verify actual Windows/Codex activation and real MCP capabilities, then prove editable Live creation, save/reopen and a scoped edit.
Continue useful general theory and ko/en/ja specialist curation. Chinese specialties are archive-only, not a deferred workstream.
Keep the three-language boundary and preserve words/notes on narrow edits. Do not infer pronunciation language from script alone.

## Session handoff

Read actual state, AGENTS.md and requirements before continuing. Do not re-ask for permanent genre/voice defaults or reopen the language scope without a new owner decision.
Keep private recordings, paths, samples and unpublished songs outside this public repository.
Update status with actual run IDs, results, limitations and next steps before ending every session.
