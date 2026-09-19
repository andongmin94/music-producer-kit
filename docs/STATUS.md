# Current status

Updated: 2026-09-19. Version: 0.7.1 official-first correction, NOT a completed production plugin.

## Current state

The owner's latest official-first handoff supersedes the 0.7.0 recommendation to reuse the trial MCP.
The handoff reports removal of the Codex entry, Live control-surface selection, listener/process, and trial-only server/Remote Script folders. Private evidence/test Sets were retained and the user's current Set was not touched.
No replacement MCP, official Extensions SDK or Live Beta has been installed according to that handoff. Do not restore the removed trial or interpret a previous successful run as a current connection.

## Changes

Applied the new decision to the verified 0.7.0 source tree (926d67a5cb0dc37fc8637a1a423e16fbd17c6c4b), not the older 0.6.0 code in the handoff ZIP.
Removed the backend-specific live_workflow.py, its operation guide and the 21 tests for that retired route. There is no compatibility switch or hidden fallback.
Preserved the five generic saved-Set tests in test_live_set_diff.py and moved its small report writer into live_set_diff.py, removing its dependency on the retired module.
Music/lyric guides, source data and notices, Mido, SoundFile, read-only MCP probe and pinned requirements are unchanged. One entry skill and one CI workflow remain.
Updated the skill, manifest, README, requirements and acceptance docs to say the replacement is unimplemented. The installed-flow criteria remain, but execution is explicitly blocked pending that integration.
Added official-path-review.md with checked public facts and the specific local SDK/API review needed next. No guessed official API, SDK download, new bridge, account access or PC change was made here.
Updated five existing behavioral definitions and added two official-path/approval cases. All 27 model scenarios remain DEFINED, NOT RUN.

## Evidence and remaining work

Official public SDK/FAQ pages were read on 2026-09-19. They specify the Suite Beta channel; the detailed SDK/download link required an authenticated Centercode session in this environment.
The exact SDK invocation, note editing, persistence and distribution contract is not available here yet. Existing PC tests and third-party API shapes do not answer those questions.
Read docs/official-path-review.md next: safely inspect available host/SDK facts; obtain missing official material through the owner; request separate approval for any installation. Then implement ONE documented route and execute docs/installed-flow-acceptance.md.
Actual official-first Live creation/edit/save/reopen, installed model flow and audio quality: NOT RUN. Packet/file checks are not substitutes.

## Validation for this correction

Local Python 3.13.5 ran 118 of 123 discovered tests successfully, including all eight new official-first retirement/report checks and the five retained saved-Set comparison tests.
The five existing ProbeSDKTests could not run locally because mcp/httpx2 are not installed. They remain enabled and unchanged for the full Windows/Linux CI; no full local pass is claimed.
Package validation and selected-library integrity passed locally.
Code head 63576fa4cf82ebe6d20b6627af0a966bd69ce5e8 passed ordinary CI run 35438537092 on ubuntu-latest and windows-latest, Python 3.12. Both jobs completed package validation, all test discovery and ZIP generation successfully. The Ubuntu log explicitly records 123 tests, all passing, including the five SDK tests unavailable locally.
The tested local and remote code trees matched at 4afdff5c8a6db15302b92b65d7d52a18383b2bbd. This documentation-only follow-up records that observed run, not an unobserved later result.
The removed 21 tests belonged to the deleted backend-specific code, not failing retained functionality. Test totals must not be compared as quality scores.

## Historical PC experiment — successful, subsequently removed

Initial inspection found no Ableton MCP. Following the owner's trial approval, the pinned nicholasbien/ableton-mcp-pro implementation was installed privately, with one Live User Library Remote Script and one Codex stdio entry. Actual Live 12 Suite 12.4.6 exposed 78 tools through the server. Its Live-side TCP listener was verified on literal IPv4 loopback; no firewall exception or public endpoint was added.

The existing desktop-bundled Codex core completed exactly one read-only get_session_info MCP call in a fresh ephemeral run. The older PATH CLI could not use the configured default model; the already-installed desktop core worked without an upgrade or model change. The current already-open task did not hot-load the new tools; the editing sequence used the official MCP Python SDK against the same installed server. Native Codex exposure and SDK application calls are distinct evidence.

In an authorized new disposable Set, the four-bar harmony-study fixture was created as editable Arrangement MIDI: one Harmony clip and four one-bar Bass clips, using actually discovered Electric and Operator devices. Only Bass bar 2 was replaced with the planned two-note revision. Before/after native readbacks preserved all other notes, clip bounds, devices, routing and mixer values. Saved Set XML independently preserved all content outside the target clip except the transport cursor; the replacement clip's internal identities changed as expected.

Both baseline and revised .als files were saved through the native Live UI and actually reopened in sequence. The revised Set's 15 native readbacks matched the pre-save state exactly, and the changed notes were visible in Live's editable piano roll. The owner manually removed the pre-existing administrator launch setting; subsequent native UI work was automated. No existing saved song was changed. Detailed paths, versions, tool calls, comparisons and rollback scope remain only in the private first-run workspace.

Local package validation and full unittest discovery passed using the separate diagnostic Python 3.12 environment: 110 tests run, 109 passed and one symlink-capability skip. Earlier missing-dependency and sandbox temporary-directory failures remain recorded privately. These are local results, not new CI results. No purchases, credit use, external audio uploads or account changes occurred. Listening, rendering, musical quality and arbitrary existing-song/MPE preservation were not tested.

## Evidence boundary

The preceding experiment is kept as historical evidence from the owner's local handoff; it is not new hosted execution and does not endorse or retain its backend.
The 0.7.0 installed-flow implementation passed 136 Windows/Linux tests before the supplier decision changed, but its full natural-language PC acceptance was never run.
No new SDK or driver is bundled. SDK-based kit code would still be kit-authored, not Ableton-provided or manufacturer-certified.
Private logs, sample files, credentials and .als projects were not added. Chinese-specialist material stays removed. No purchases, external uploads, configuration changes or history rewriting.
