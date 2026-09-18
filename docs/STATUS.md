# Current status

Updated: 2026-09-18. Milestone: 0.2.0 self-contained upstream source preservation.

## Implemented

- Complete tracked-file snapshots of both pinned sources are committed locally: 29 composition modules / 74 files and 18 lyric modules / 47 files. Total 121 files, 2,512,420 original bytes.
- Original file bytes, LICENSE/NOTICE, source commits/tree IDs, per-file Git blob SHA and SHA256, and archive SHA256 are preserved. See SOURCE_SNAPSHOT_REPORT.json.
- Source archives are included inside the plugin, not Git submodules or references to a remote installation.
- A standard-library-only reader lists modules/files and reads bounded line ranges from local archives without extraction, execution or downloads.
- One curated entry skill remains discoverable; raw source workflows are data, not operating policies.
- Package checks verify both archives, source-file hashes, notices and 47-module coverage. Only the two named source ZIPs are allowlisted.
- Existing scoped MIDI helper remains unchanged.
- The one-time network snapshot workflow was removed after its successful capture. Normal installation/read/verification never fetches upstream sources.

## Observed verification

Source capture run 35299006712: SUCCESS. Both pinned Git commits fetched, all tracked blob hashes checked, ZIP readback checked, and source data committed as 9da6420.
Local Linux: 19 new reader unit tests PASS.
CI run 35299974015 on code commit 342d6f60522f8883a3f59fc26005a9ea969937d2: SUCCESS on both windows-latest and ubuntu-latest, Python 3.12.
Each platform passed package validation, the 64-test suite (39 existing + 19 reader + 6 distribution), and install-ZIP generation.
The distribution test extracts the built ZIP into an independent directory, removes its source checkout copy, blocks network calls, and verifies/reads the bundled library.
Every module and associated local reference is readable; the complete 121-file inventory and original byte count match.
Missing/corrupt archives, unsafe paths, notice changes and unlisted files are rejected. No remote recovery is attempted.
The reproducible-package test passes independently on both platforms; cross-platform ZIP byte identity was not asserted.
The initial integration run 35299878510 caught an over-specific expected error string in the missing-archive test. Commit 342d6f6 tests rejection/network isolation without depending on which validator runs first.

Static/offline tests are not Codex behavioral or music-quality evaluations.
Codex plugin activation, actual Ableton MCP operations, Live save/reopen and listening: NOT RUN.

## Preservation versus adaptation

Full original file preservation: COMPLETE.
Editorial conversion of every source paragraph/table into curated production guidance: NOT COMPLETE.
Detailed knowledge can now be consulted locally; do not silently turn an archived source's imperatives or inferred rules into new instructions.
Source books, recordings, private tools and corpora that upstream never shipped were not acquired.
No bundled MCP server, Splice/Melodyne/singing connector, or project-wide license grant.

## Next concrete step

Verify real Windows/Codex activation and actual MCP schemas, then create a scratch Live Set and prove save/reopen plus a drum-only edit.
Continue section-level adaptation from the LOCAL library, retaining conditions, counterexamples and provenance.
Do not repeat resolved genre/voice preference questions or restore a dependency on upstream websites.

## Session handoff

Read actual repository state, this file and AGENTS.md first.
Keep private equipment paths, recordings and samples outside this public repository.
Append actual outcomes and blockers before each session ends; do not call a queued run a passing run.
