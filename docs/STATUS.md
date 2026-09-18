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
- The one-time network snapshot workflow has been removed after its successful capture. Normal installation/read/verification never fetches upstream sources.

## Verification recorded so far

Source capture run 35299006712: SUCCESS. Both pinned Git commits fetched, all tracked blob hashes checked, ZIP readback checked, and source data committed as 9da6420.
Existing package/MIDI tests passed in that source-capture run.
Local Linux: 19 new reader unit tests PASS, including network-disabled reading, missing/corrupt archive errors, line ranges, paths and notice integrity.
Six distribution integration tests added, including install-ZIP extraction separated from the checkout with network calls blocked.
Final Windows/Linux suite and package build for 0.2.0: pending observation at this checkpoint.
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
