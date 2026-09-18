# Current status

Updated: 2026-09-18. Milestone: 0.5.0 physical source removal and local sample discovery.

## Implemented

- Replaced both complete original ZIPs with composition-selected.zip and lyrics-selected.zip. The retained library has 42 modules, 93 files and 1,842,265 bytes, down from 47 modules/121 files/2,512,420 bytes.
- Removed five Chinese-specialist modules, the dedicated folk-instrument reference, the fusion example and redundant upstream installer/root presentation files. Removed designated subject sections/paragraphs/rows inside shared documents; retained general theory and ko/en/ja material.
- Blank lines preserve citation positions but contain no deleted content. Current file hashes and origin hashes are recorded separately.
- Removed archive-audit API/CLI, hidden views and source recovery routes. The inventory lists only physically retained modules. SOURCE_SELECTION_REPORT.json records removal locations, not removed text.
- Added standard-library read-only local sample filename/path discovery with bounded traversal, relative paths, sizes, hashes, link/junction avoidance and explicit non-analysis/non-license status.
- Existing Mido editing, craft references, three language guides and one producer entry skill remain. No new dependency.
- Temporary source-edit scripts and workflow were removed from the final tree. One ordinary Windows/Linux CI workflow remains.

## Observed verification

Source-edit workflow 35311908808 succeeded on the isolated branch, including retained archive/file integrity and reader checks.
The new sample helper was exercised separately in this container: 12 tests passed on Linux/Python 3.13.5 before final integration.
Transition workflow 35312565338 passed package validation, unittest discovery and ZIP generation on Ubuntu/Python 3.12 and committed the verified adjustments as 2106ef4.
The preceding transition run 35312473145 exposed one obsolete assertion in the all-file read test: its 42 subtests expected the removed archive_audit key. The test now asserts that key is absent; no compatibility field was restored.
The suite contains 103 tests (old audit-view tests replaced, 12 sample tests added). Final ordinary PR Windows/Linux validation after temporary workflow removal is not yet observed at this checkpoint.
A full local checkout is unavailable because this container could not resolve github.com. Repository-wide tests are run in GitHub Actions, not claimed as local results.

## Product boundaries

Korean, English, Japanese and instrumental work are in scope. Chinese-specialist originals are not retained for maintenance or future expansion.
Removal verification covers designated subjects, files and locations; it is not semantic proof about every conceivable cultural association or scholarly accuracy.
Git history has not been force-rewritten. Current-tree/new-package deletion does not retroactively replace old commits or existing user copies.
No new library dependency, automatic spending/upload, Splice/Melodyne connector, singing engine or audio decoder was added.
Codex behavior scenarios: 20 DEFINED, NOT RUN. Real activation, Ableton/MCP operations, Live save/reopen, rendering and listening: NOT RUN.
A sample filename match is not evidence about sound content, key, tempo, quality or rights.

## Next concrete step

Observe final PR checks and merge only after the retained-source, MIDI, sample and distribution regressions pass.
Then validate on the actual Windows machine: activation, real MCP schemas, selected local sample loading, editable Live Set creation, save/reopen and a protected one-part edit.
Continue in-scope music knowledge without restoring deleted originals or broadening the settled languages.

## Handoff

Read actual state, AGENTS.md and requirements first; do not repeat the settled questionnaire.
Record actual tests, limitations and blockers before ending each session. Keep private audio, sample paths and unpublished work outside this repo.
