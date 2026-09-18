# Current status

Updated: 2026-09-18. Milestone: 0.5.0 physically selected sources and read-only local sample discovery.

## Implemented

- Removed the full source snapshot ZIPs and the archive-audit API/CLI, rather than hiding excluded data.
- Retained 41 modules / 89 files / 1,805,308 bytes. Removed six specialist/corpus modules, topical examples and folk-orchestra content; cleaned reviewed topical sections/cross-links in shared files. Unneeded upstream installer/presentation files were also removed: 32 source files deleted, 43 retained files edited.
- General craft prose written in Chinese and Korean/English/Japanese sources remain. Legal notices are retained unmodified.
- One version-2 selected catalog records current and original hashes/ranges for edited files. Removed the duplicate upstream inventory and obsolete full-snapshot report. SOURCE_SELECTION_REPORT.json records deletion/selection locations, not removed content.
- Updated guide locators to actual selected-source positions. No empty-line preservation, alternate view, upstream download or remote recovery.
- Added sample_library.py and producer guidance: explicitly scoped local directory -> read-only audio-header inventory -> literal filename search -> selected-file reinspection and SHA256.
- SoundFile 0.13.1 reads headers, including float WAV/FLAC/AIFF. No custom codec, account integration, key/BPM detector, listening claim or automatic license approval.
- Original sample files are not modified. Private reports are exclusively created outside the sample root, installed plugin and project checkout.
- Existing Mido helper is unchanged. Temporary editing/transfer workflows are absent from the final tree; one ordinary Windows/Linux CI workflow remains.

## Observed verification

PR #3 head a680f9b9b03751110f352b519bf43946224dea38 was preserved from the interrupted session.
Its ordinary CI run 35311126409 completed successfully on windows-latest and ubuntu-latest, Python 3.12. Both jobs passed package validation, unittest discovery and distribution ZIP generation; the Ubuntu log explicitly records 96 passing tests.
These results were read and verified during recovery. The current documentation-only update records the observed implementation run; no later unobserved check is claimed to have passed.

The preceding implementation session recorded a full local Linux checkout with Python 3.13.5, Mido 1.3.3 and SoundFile 0.13.1: package validation, 96 tests and ZIP generation passed. The source apply workflow 35311073133 also passed before committing a680f9b. These are earlier-session records, not a claim of a new full local run during recovery.

Audio fixtures test PCM/float WAV, stereo, FLAC, AIFF, malformed files, Unicode names, bounded scans, protected outputs, stale inspection, hashes, CLI and network-blocked operation. No personal recordings or sample directory were accessed.
Removal tests inspect actual inner ZIP content, absence of full original archives and the audit API/flag, selected provenance, offline retrieval, updated guide locators and independent distribution.
The earlier 42-module/103-test alternative created during recovery is duplicate PR #4, not the chosen implementation. Keep PR #3's more complete corpus removal, single catalog and audio-header tool; do not merge both alternatives.

## Limits

Current-tree/new-distribution deletion covers the selected Chinese-specialist modules, dedicated corpora/examples and reviewed mixed-document sections. It is not a rewrite of Git history; old commits and external clones are not retroactively erased.
The retained library is selected source evidence, not an untouched upstream snapshot or certification of every assertion.
Sample metadata is header-only. It does not prove full-file decode, license rights, musical suitability or sound similarity. Filename search does not recheck current files; inspect again before actual use.
Actual Codex behavior: 21 scenarios DEFINED, NOT RUN. Codex activation, Ableton MCP, Live creation/save/reopen, rendering/listening and native-language review: NOT RUN.
No project-wide license, Splice/Melodyne/singing-engine connector, purchase or upload authorization was added.

## Next concrete step

On the target Windows machine, activate the kit, scan an explicitly supplied owned sample directory, inspect actual Ableton MCP schemas, and prove a small editable Live Set plus save/reopen and a scoped edit.
Do not expand unsupported languages, restore excluded sources, infer capabilities from marketing text, or substitute another broad documentation expansion for real DAW validation.

## Recovery and session handoff

Before creating a new branch, inspect main, existing work branches, open pull requests and their checks. An interrupted chat may already have saved the requested implementation outside main.
Resume and validate that work before rebuilding it. Explicitly close a superseded duplicate rather than merging two incompatible implementations.
Read AGENTS.md and requirements; keep private paths, audio and unreleased songs outside this public repo.
Record actual run IDs, failures, blockers and next actions before ending each session. A plan, defined scenario or successful MIDI file is not an executed Ableton workflow.
