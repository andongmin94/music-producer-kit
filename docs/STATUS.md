# Current status

Updated: 2026-09-19. Milestone: 0.7.0 installed-producer workflow integration.

## Product state: do not collapse these observations

- Real PC connection, editable four-bar Arrangement, one scoped edit, UI save/reopen: VERIFIED IN THE OWNER'S LOCAL HANDOFF below, not rerun in this hosted environment.
- Reusable installed-skill workflow and deterministic note/readback/Set-diff helpers: IMPLEMENTED in this increment.
- Installed plugin activation plus natural-language create/edit/save/reopen in the same user flow: NOT YET RUN. This is the next local acceptance, not another initial setup exercise.

## Implemented in 0.7.0

The existing single producer skill now routes ordinary Live tasks to references/live-workflow.md. It uses the already installed ableton_live native MCP; no new server, direct SDK writer or parallel connection is added. The handoff's separate backend/kit environments and desktop-core versus old PATH-CLI distinction are preserved.

live_workflow.py compiles the existing score format into clip-local notes for the inspected backend, checks empty destinations, records complete required ordinary-track readbacks, verifies creation and provides owned-basic-clip receipts. Narrow edits require a current matching receipt and exactly one clip range. Deletion is followed by an absence/protected-field check before creation. Successful readback updates the receipt for the next edit. Plans are not executed by this helper; Codex's native tools retain their actual permission boundaries.

live_set_diff.py reads saved gzip/XML Sets without writing them. It reports all changed paths, including IDs, cursor, automation and device data, with file hashes and bounded output. No XML region is automatically exempted. This complements incomplete MCP readbacks; it is not a proof of UI action, external assets, or all supported Live format variants.

The working score is not restricted to the four-bar test: duration, meter, part names and clip segmentation are data. Korean/Japanese part names remain intact. The conservative replacement helper does not silently destroy advanced or manually altered performances to satisfy a partial edit.

Added 26 tests for native-shaped fixtures, creation and empty-target checks, scoped changes, intermediate deletion readback, stale/tampered plans, consecutive edits, protected mixer/routing/devices/master, Unicode names, other durations/meters, independent installed ZIP operation, private outputs and saved XML changes. Synthetic fixtures are explicitly not real Live/model traces.

Four installed-user scenarios were added to the existing 21: 25 DEFINED, NOT RUN. docs/installed-flow-acceptance.md specifies fresh installed-path activation, native calls, automated UI actions, repeated scoped changes and saved/reopened evidence. The authoring helpers are internal to the skill; the user does not supply their JSON or shell commands.

## Observed hosted validation

The attachment was extracted and used as the working baseline; remote main was still 983946c and open PRs were empty. The supplied local README/STATUS/handoff observations were preserved rather than replaced with older remote claims.

Local Python has Mido 1.3.3 and SoundFile 0.13.1, but no mcp/httpx2 installation and no reachable package service. Initial full baseline discovery exposed those missing SDK dependencies; that failed attempt is not a full passing run.
The five existing ProbeSDKTests are not runnable here. They remain enabled and unchanged in the repository/CI; local regression reporting explicitly separates them rather than removing or weakening them.
New helpers require no new dependencies. Local package validation passed. All 26 added tests passed, including the independently extracted install ZIP. The explicit local regression ran 131 of 136 discovered tests successfully; only the five pre-existing SDK transport tests were not run here because mcp/httpx2 are absent. Those tests remain required in ordinary Windows/Linux CI. Remote results are pending at this checkpoint.

There is no Codex executable, configured model API, private Windows workspace or Live process in this environment. Actual model/installed-user scenarios cannot be executed here; do not relabel deterministic fixture tests as model evaluations.

## Local Windows first connection — 2026-09-19

Initial inspection found no Ableton MCP. Following the owner's trial approval, the pinned nicholasbien/ableton-mcp-pro implementation was installed privately, with one Live User Library Remote Script and one Codex stdio entry. Actual Live 12 Suite 12.4.6 exposed 78 tools through the server. Its Live-side TCP listener was verified on literal IPv4 loopback; no firewall exception or public endpoint was added.

The existing desktop-bundled Codex core completed exactly one read-only get_session_info MCP call in a fresh ephemeral run. The older PATH CLI could not use the configured default model; the already-installed desktop core worked without an upgrade or model change. The current already-open task did not hot-load the new tools; the editing sequence used the official MCP Python SDK against the same installed server. Native Codex exposure and SDK application calls are distinct evidence.

In an authorized new disposable Set, the four-bar harmony-study fixture was created as editable Arrangement MIDI: one Harmony clip and four one-bar Bass clips, using actually discovered Electric and Operator devices. Only Bass bar 2 was replaced with the planned two-note revision. Before/after native readbacks preserved all other notes, clip bounds, devices, routing and mixer values. Saved Set XML independently preserved all content outside the target clip except the transport cursor; the replacement clip's internal identities changed as expected.

Both baseline and revised .als files were saved through the native Live UI and actually reopened in sequence. The revised Set's 15 native readbacks matched the pre-save state exactly, and the changed notes were visible in Live's editable piano roll. The owner manually removed the pre-existing administrator launch setting; subsequent native UI work was automated. No existing saved song was changed. Detailed paths, versions, tool calls, comparisons and rollback scope remain only in the private first-run workspace.

Local package validation and full unittest discovery passed using the separate diagnostic Python 3.12 environment: 110 tests run, 109 passed and one symlink-capability skip. Earlier missing-dependency and sandbox temporary-directory failures remain recorded privately. These are local results, not new CI results. No purchases, credit use, external audio uploads or account changes occurred. Listening, rendering, musical quality and arbitrary existing-song/MPE preservation were not tested.

## Preserved implementation and limits

The 41-module/89-file/1,805,308-byte selected library, legal notices, Mido helper, SoundFile helper, read-only mcp_probe, existing requirements and one permanent CI workflow are unchanged. No Chinese-specialist originals, hidden backup, compatibility view, automatic download or extra entry skill was restored.

MCP readbacks omit advanced note properties, some automation and return-device details. The initial owned-clip route is intentionally limited; it is not a verified arbitrary existing-song editor. Requests beyond it require an actually supported preservation path, not destructive fallback.
Checkpoint hashes prove consistency of supplied observations, not that those observations came from Live. Reopen comparisons require an independent actual host open event and saved-file identity. Saved XML review is explicit and includes every reported difference; private real Sets were not included in the attachment.

Save/new/open have no MCP tools in the approved backend. The host's already demonstrated Windows UI automation supplies them. This kit does not claim to ship or test a new UI driver here.
No listening, rendering, full-song quality or native-language review is newly claimed. No purchases, credit use, private uploads, account/config changes or broader permissions were performed.

## Next local action: installed user flow, not setup

Use docs/installed-flow-acceptance.md with the updated installation in a fresh local desktop Codex session. Record the actual installed SKILL.md path/hash and plugin version, then issue ordinary create / bass-bar-only-edit / saved-version-reopen requests without injecting checkout instructions or using the private SDK writer.
Retain the working ableton_live entry, backend commit and separate environments. Use already verified UI automation for new/save/open. Validate helpers against the actual readback shape and actual .als files, then record results and blockers privately. Send back only a redacted summary; do not upload raw calls, samples or projects by default.
Stop at the specific missing capability or mismatch and report it rather than reinstalling the environment or repeating the user's musical interview.

## Session continuity

Read the handoff, actual refs, open PRs, AGENTS and this status before further work. Preserve the latest local evidence even when remote docs lag.
Record the scope of every test result and the next concrete action. A usable MIDI file, passing package, or matching fixture is not a completed installed-plugin music workflow.
