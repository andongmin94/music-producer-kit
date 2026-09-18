# Current status

Updated: 2026-09-18. Milestone: 0.5.0 physical source removal and local sample discovery.

## Implemented on the current work branch

- Replaced the two complete original ZIPs with selected data. Removed five Chinese-specialist modules, the dedicated folk-instrument reference, the fusion example and redundant upstream installer/root presentation files.
- Removed designated subject sections/paragraphs/rows from shared documents. Retained general theory and ko/en/ja material; blank lines preserve citation positions, not removed content.
- Removed archive-audit API/CLI, hidden source views and recovery routes. Actual retained content, catalog and inventory agree; current and origin file hashes are distinct.
- Replaced the obsolete snapshot report with SOURCE_SELECTION_REPORT.json, which stores only deletion locations and retained-data facts, not deleted passages.
- Added read-only local sample filename/path discovery with bounded traversal, relative paths, hashes, symlink/junction avoidance and explicit non-analysis/non-license status.
- Preserved the existing Mido editing path, craft guides, three language guides and single producer entry skill.

## Verification observed so far

Source-edit workflow 35311908808 completed successfully on the isolated work branch. Retained archive/file hashes and the simplified reader were verified there.
The new sample helper was tested separately in this chat container: 12 tests passed on Linux/Python 3.13.5. Minor structural/output changes after that standalone run require integrated validation below.
Full new-version Windows/Linux package tests and ZIP generation: pending at this checkpoint. Baseline 0.4.0 results are not proof of this version.
Local full checkout is unavailable because this container could not resolve github.com. Integrated repository verification uses GitHub Actions; no local full-suite result is claimed.

## Product boundaries

Korean, English, Japanese and instrumental work are in scope. Chinese-specialist originals are not retained for maintenance or future expansion.
Topic-removal checks cover designated subjects and explicit locations, not all conceivable cultural associations or scholarly accuracy.
Git history has not been force-rewritten. Current-tree/new-package removal does not retroactively replace existing copies or historical commits.
No new library dependency, automatic purchase, audio upload, Splice/Melodyne integration, singing engine or audio decoder was added.
Codex behavior scenarios remain DEFINED, NOT RUN. Real activation, Ableton/MCP operations, Live save/reopen, rendering and listening remain NOT RUN.
A filename match does not establish sound content, key, tempo, quality or rights.

## Next concrete step

Finish branch-wide regression/distribution checks and remove temporary edit scripts/workflow before merge.
Then validate on the actual Windows machine: skill activation, real MCP schemas, selected local sample loading, editable Live Set creation, save/reopen and a protected one-part edit.
Continue in-scope knowledge work without restoring deleted originals or broadening the settled languages.

## Handoff

Read actual repository state, AGENTS.md and requirements first. Do not repeat the user's settled questionnaire.
Record actual test results and blockers before every session ends. Keep private audio, sample names/paths and unpublished work outside this repo.
