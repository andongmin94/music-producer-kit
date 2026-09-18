# Current status

Updated: 2026-09-18. Milestone: 0.5.0 physically selected sources and read-only local sample discovery.

## Implemented

- Removed the full source snapshot ZIPs and the archive-audit API/CLI, rather than hiding excluded data.
- Replaced them with 41 retained modules / 89 files / 1,805,308 bytes. Removed six specialist/corpus modules, topical examples and folk-orchestra content; cleaned topical sections/cross-links in shared files. Unneeded upstream installer/presentation files were also removed: 32 source files deleted, 43 retained files edited.
- General craft prose written in Chinese and ko/en/ja sources remain. Legal notices are retained unmodified.
- One version-2 selected catalog contains current hashes and original hashes/ranges for edited files. Removed duplicate upstream inventory and the obsolete full-snapshot report. Current counts/decisions are in SOURCE_SELECTION_REPORT.json.
- Updated guide locators to actual selected-source positions. No empty-line preservation, alternate view, network recovery or upstream download.
- Added sample_library.py and a producer reference: explicitly scoped local directory -> read-only audio-header inventory -> literal filename search -> selected-file reinspection and SHA256.
- SoundFile 0.13.1 handles audio headers, including float WAV/FLAC/AIFF. No custom codec, account integration, listening claim, key/BPM detector or automatic license approval.
- Original sample files are not modified. Reports are private, exclusively created, and forbidden inside the sample root/installed plugin/project checkout.
- Existing Mido helper is unchanged. One permanent Windows/Linux CI workflow remains the target final structure.

## Observed verification in this work session

A complete checkout was transferred through an authenticated GitHub Actions artifact after this container could not resolve github.com for cloning. Development/tests were then run on that local tree.
Local Linux / Python 3.13.5 / Mido 1.3.3 / SoundFile 0.13.1: python tools/check.py PASS; unittest discovery 96 tests PASS; install ZIP build PASS.
Generated audio fixtures exercise PCM and float WAV, stereo, FLAC, AIFF, malformed files, Unicode filenames, scoped/limited scans, protected outputs, stale inspection, hashes, CLI and network-blocked operation. No user recordings or sample library were accessed.
Removal tests inspect actual inner archive bytes, absence of the old ZIPs and audit mode, original provenance, offline retrieval, guide locators and independent distribution.
During local editing an old archive_audit assertion and a text-edit anchor were corrected; the final local suite passed.
Remote checks on the final branch/main have not yet been recorded at this checkpoint. Do not treat the prior 0.4.0 CI as validation of 0.5.0.

## Limits

Current-tree/new-distribution deletion is complete for the selected Chinese-specialist modules, dedicated corpora/examples and reviewed mixed-document sections. This is not Git history rewriting; old commits and existing external clones are not retroactively erased.
The retained library is selected source evidence, not a complete untouched upstream snapshot or a certification of every assertion.
Sample metadata is header-only. It does not prove complete decode, license rights, musical suitability or sound similarity. Filename search does not recheck current files; inspect again before actual use.
Actual Codex behavior: 21 scenarios DEFINED, NOT RUN. Codex activation, Ableton MCP, Live creation/save/reopen, rendering/listening and native-language review: NOT RUN.
No project-wide license, Splice/Melodyne/singing-engine connector, purchase or upload authorization was added.

## Next concrete step

On the target Windows environment, activate the kit, scan an explicitly supplied owned sample directory, inspect actual Ableton MCP schemas, and prove a small editable Live Set plus save/reopen and a scoped edit.
Do not expand unsupported languages, restore excluded sources, infer tool availability from a README, or substitute another round of broad knowledge expansion for a real DAW smoke test.

## Session handoff

Read AGENTS.md, requirements and actual repository state. Preserve private paths, audio and unreleased songs outside this public repo.
Record real test runs/failures/blockers at session end. A plan, defined scenario or successful MIDI file is not an executed Ableton workflow.
