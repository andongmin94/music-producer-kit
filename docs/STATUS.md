# Current status

Updated: 2026-09-18. Milestone: 0.6.0 local MCP discovery and Windows acceptance handoff.

## Implemented

- mcp_probe.py uses the official MCP Python SDK 2.2.0 to inspect an explicitly authorized literal-loopback HTTP endpoint or trusted installed stdio server. No custom JSON-RPC transport or Ableton MCP server is added.
- Reads the actual paginated tool catalog, input/output schemas, server-reported identity/capabilities and negotiated protocol. Keeps a private timestamped report and catalog hash; it never calls application tools, resources or prompts.
- Checks endpoint/report scope, exclusive output creation, duplicate names, repeated cursors, page/tool/size budgets and timeouts. HTTP proxy inheritance is disabled. Credentials are explicitly selected by environment-variable name rather than printed or copied into the report.
- Does not read or change Codex configuration/credentials. Discovery, Codex availability, Live state, edits, save/reopen and listening remain separate claims; the diagnostic never sets the latter verification flags true.
- Added a concrete Windows first-run request and acceptance sequence: inspect versions/existing connection, discover tools, read the actual Set, use an authorized disposable four-bar harmony/bass test, revise bass bar 2, compare protected content and verify save/reopen.
- Fourteen additional tests: nine units and five official-SDK transport/connection tests. The fixture exposes a write tool whose invocation is forbidden; it is not an Ableton simulator.

## Observed verification

PR #5 code head 69b742bfd12c3dda20c16386eda275a26de58daa: CI run 35317232583 completed successfully on windows-latest and ubuntu-latest, Python 3.12.
Both jobs passed package validation, full unittest discovery and distribution ZIP generation. The Windows log explicitly records 110 passing tests (96 existing + 14 added).
Actual protocol checks cover in-memory SDK discovery, a stdio child process, a loopback HTTP ASGI server, ignored proxy environment, server shutdown, refused HTTP connections and a hanging stdio timeout with no success report. No application tool was executed by discovery.

The first run 35316828602 passed 109 tests and packaging on Ubuntu but failed one Windows unit assertion comparing a normalized path with its 8.3 temporary-directory alias.
The fixture now resolves its root before comparison and still checks existing-file protection and rejection of plugin/repository output paths. Runtime path validation was not weakened and no compatibility branch was added.
An additional positive HTTP transport test was added before the successful run above; the new test is not merely an HTTP failure simulation.

Nine standalone unit tests had passed earlier in this chat container on Linux/Python 3.13.5. GitHub cloning was unavailable here and the new SDK was not locally installed, so the complete SDK/repository results are GitHub Actions observations, not a local full-suite claim.
This documentation follow-up records the observed code run. It does not assert that an unobserved later run has passed.

## Preserved product and boundaries

The 41-module/89-file/1,805,308-byte selected library, removed-specialist boundary, Mido and SoundFile helpers, ko/en/ja guides and single producer skill are unchanged.
No complete upstream source, audit bypass, automatic knowledge download, second entry skill or extra CI workflow was restored or added.
Dependencies now include the official MCP SDK; package installation can require network, but retained music knowledge does not fetch upstream sources.
The diagnostic starts a trusted specified stdio process; it is not a sandbox that prevents that process's startup side effects. HTTP reports can contain private server-supplied schema text. Keep reports and stderr outside this public repo and review before sharing.

Actual user-PC access was not available in this chat; available app discovery did not expose an Ableton connection.
Codex activation, real Live state, creating/editing a Live Set, save/reopen, rendering/listening and native-language review: NOT RUN.
The existing 21 behavior scenarios remain DEFINED, NOT RUN. Protocol fixture tests do not execute model prompts or grade music.
MCP server selection is not finalized without inspecting the installed Live version and required functions. No automatic install, purchase, upload, account change or sandbox-permission change was performed.
ulm0/ableton-live-mcp was inspected as one candidate and explicitly lacks transport control, third-party insertion and automation curves. It was not adopted as a complete production backend.

## Next concrete step: actual local Windows acceptance

Run docs/windows-first-run.md in Codex on the Windows machine that has Ableton installed, not in a hosted web workspace.
Inspect the existing connection/version, run mcp_probe.py on the authorized endpoint, then separately check actual Codex tool availability and a reviewed read-only Live state call.
Use only an authorized disposable Set for the four-bar study and bass-only revision. Save/reopen and record actual evidence in the private song workspace; manual interventions must remain labeled manual.
If a required capability is absent, stop at that specific boundary instead of inventing tools or substituting another round of broad documentation expansion for a real local test.

## Session continuity

Read AGENTS.md, requirements, actual refs, open PRs and their checks before making another branch. Recover saved interrupted work before rebuilding it.
Do not repeat the user's questionnaire or restore excluded language specialties. Keep private audio, paths, diagnostics and unpublished work outside the repo.
Record actual run IDs, failures, fixes, limitations and next actions at the end of a session. A plan, queued run or successful MIDI file is not an executed Live workflow.
