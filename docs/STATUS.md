# Current status

Updated: 2026-09-18. Milestone: 0.6.0 local MCP discovery and Windows acceptance handoff.

## Implemented in this increment

- mcp_probe.py connects to an explicitly authorized local HTTP or installed stdio MCP server through the official Python SDK 2.2.0. No custom JSON-RPC codec, application tool calls, model calls or new Ableton server.
- Reads the actual paginated tool catalog, schemas, server-reported identity/capabilities and negotiated protocol; records a private timestamped catalog hash.
- Rejects non-loopback HTTP URLs, URL credentials/query data, duplicate tools, repeated cursors, oversized/incomplete catalogs, invalid destinations and timeouts. HTTP proxy environment is disabled; credentials are explicitly selected by environment-variable name.
- Does not read or modify Codex config/auth files. Direct probe success is distinct from Codex activation, Live state, edits, save/reopen and listening. Those flags remain false.
- Added executable unit and SDK protocol-fixture tests plus Windows first-run instructions. No application tool is called by the diagnostic; process startup itself still requires trust.
- Connected the diagnostic through the existing Ableton reference so the single producer skill can find it without another always-active skill.

## Observed so far

Actual main was inspected at 687cf87; no open PRs existed before this work. Older work branches were observed and not mistaken for unfinished requirements.
Standalone local Linux/Python 3.13.5: the nine new probe unit tests passed. The complete repository could not be cloned here because GitHub DNS was unavailable; the SDK dependency was not installed locally. No local full-suite or SDK protocol pass is claimed.
New implementation and full Windows/Linux CI: pending at this checkpoint. The earlier 0.5.0 96-test pass is baseline evidence only.
Official MCP SDK release v2.2.0 and its Client/transport API were inspected. Codex MCP documentation was checked for configuration and permission distinctions.
ulm0/ableton-live-mcp README was inspected: it explicitly lacks transport control, third-party plugin insertion and parameter automation curves. It was not adopted as a complete backend or installed.

## Preserved product

The 41-module/89-file selected source library, removed-specialist boundary, Mido helper, SoundFile helper and ko/en/ja guides are unchanged.
No original source pack, audit path, speculative DAW adapter, extra discovery skill or extra CI workflow has been restored or added.
Dependencies now include the official MCP SDK in addition to Mido and SoundFile; normal installation may need network, but retained knowledge does not fetch upstream sources.

## Unverified and deliberately separate

Actual user PC access is not available in this chat. Searching available app integrations did not expose an Ableton connection.
Codex activation, real Live state, creating/editing a Live Set, save/reopen, rendering, listening and native-language review: NOT RUN.
Existing 21 model behavior scenarios: DEFINED, NOT RUN. SDK fixtures are protocol tests, not a model or Ableton simulator.
MCP server selection is not finalized without checking the installed Live version and required operations. No automatic install, account connection, purchase, upload or sandbox-permission change is authorized by this code.
A discovery report is untrusted server evidence and can contain private schema text. Keep it outside this public repo/plugin; it is not a certificate of supported musical behavior.

## Next concrete step

Complete current PR tests, then run docs/windows-first-run.md in the actual local Windows Codex environment.
Inspect existing connections/version; use mcp_probe.py on the authorized endpoint; separately verify Codex tool availability and a reviewed read-only Live state call.
Only in an authorized disposable Set, create the four-bar harmony/bass study, revise bass bar 2, compare protected content, save/reopen and record actual evidence in a private workspace.
Stop at the particular missing capability rather than invent tools or substitute more broad knowledge editing for a real local test.

## Session continuity

Read AGENTS.md, requirements, actual refs, open PRs and their checks before making another branch. Preserve completed interrupted work rather than rebuilding it.
Keep requirements, source selection and the three-language boundary; do not repeat the user's questionnaire.
Record actual run IDs, failures, fixes, limitations and next actions at session end. A queued run or published plan is not an executed result.
