# Installed workflow: use the existing Live connection

Read for actual Ableton creation or a partial edit. This is the production path, not another setup interview.
Resolve every relative helper/example path from THIS installed skill directory. Do not run a development checkout's duplicate skill or a private historical helper instead.
The user should describe the music and the change, not specify scripts or schemas. Prepare the small JSON inputs and run the bundled helpers yourself in the private song workspace.

## Existing host, not another backend

The owner already trial-installed `nicholasbien/ableton-mcp-pro` at commit `6ae148de18c8042df041b95c6e830bcdf22be526` as `ableton_live`.
Prefer its native tools in the current Codex session, after inspecting their actual schemas. Do not start a second server, replace configuration, install another pack, or use mcp_probe.py to bypass missing native tools.
A fresh desktop session may be needed to expose a new connection. The owner's older PATH CLI failed with the configured model; the existing desktop-bundled core worked. Inspect the actual executable/version; do not change the model or upgrade the CLI to make a test pass.
The verified server environment uses MCP 1.30.0 while the kit diagnostic environment uses 2.2.0. Keep them separate. Do not pip-install kit requirements into the server's environment.
`127.0.0.1:9877` is this backend's Live-side TCP bridge, NOT a Streamable HTTP MCP URL.
For a genuine missing connection, use [connection diagnostics](mcp-connection.md); preserve the owner's prior approval and rollback boundary.

New Set, Save As and Open are not tools in this pinned backend. Use the local host's actual Windows computer/UI automation when available and authorized. That is automated UI work, not a manual user action and not an MCP save call.
No UI driver is bundled here: confirm the host can observe the window and dialogs before a write-dependent task. Do not send blind coordinates or fixed-delay key sequences into an unobserved window.
If required UI capability is unavailable, report that precise block; do not rebuild the backend or silently substitute MIDI for the requested Set.

## 1. Establish an authorized workspace and current Set

Keep a short session.md with the approved goal, protected material, a stable private `set_key`, current saved version and installed skill location/version.
An identifier in a JSON file is not authorization. Check actual current Live state and the host window; resolve any unsaved-work ambiguity before new/open/close.
For a new piece create an approved blank Set using the host UI. A template can create default tracks: do not remove even these without scope approval.
For an edit, preserve the current baseline as a separate .als before modifying it. Never overwrite an existing saved song as an incidental setup step.
Keep snapshots/plans/receipts outside the installed plugin and public checkout. Reuse the already working diagnostic Python environment, not system Python.

## 2. Create the delegated music through native tools

Compose using the current brief and existing craft guides. The existing JSON score format in [MIDI](midi.md) works for any supported length and meter; the four-bar example is an acceptance fixture, not a universal song template.
Use actual native `get_session_info`, `get_arrangement_info`, `get_full_arrangement` and track reads. Create new MIDI tracks only when required, then re-read indices with `get_track_info` and give new tracks their intended names.
For an approved new Set, use actual `set_tempo` / `set_time_signature` schemas and verify them after writes. Do not alter tempo/meter during a bass-only edit.
Choose an actually discovered stock device/preset using this server's browser/loading tools. `program: 0` in MIDI is not a Live instrument ID.

Put the raw `get_track_info` result for each new destination in `bindings.json`, keyed by its matching score track name. Verify these tracks have no Arrangement material before applying the plan.
Optional `segments.json` maps a score track name to a clip length in quarter-note beats. For the fixture, `{"Bass":4}` keeps Harmony as one phrase and Bass in separately editable bars. For another song, choose musically appropriate section boundaries. A note crossing a requested split is rejected rather than shortened.

From the installed skill directory (use its resolved absolute script path when cwd is the private workspace):

```text
python scripts/live_workflow.py compile score.json --bindings bindings.json --segments segments.json --output create-plan.json
```

Before applying, capture the current empty destinations as in section 3 and run `python scripts/live_workflow.py verify-empty create-plan.json empty-checkpoint.json --output empty-check.json`. This checks occupancy and identities, not user permission or an atomic lock.
For each returned clip, call the existing native `create_arrangement_midi_clip` using its exact arguments. Do not execute the plan as an unchecked batch.
The pinned schema takes `track_index`, Arrangement `time`, `length`, and clip-local `notes` with pitch/start_time/duration/velocity/mute. The helper converts global score times to clip-local note times.
After each write, read actual state. Text beginning with Error, stale setter results or a timeout are NOT success. A timed-out write may still be queued: inspect Live before doing anything again, never blindly retry a mutation.

## 3. Capture the native evidence once per stable stage

With transport stopped, store a JSON bundle `{"set_key":"...","reads":[...]}`.
Each read item is `{"tool":"get_session_info","arguments":{},"result":...}`. Store the actual decoded backend JSON return object or its JSON string, not a fabricated summary and not the outer MCP content wrapper.
Use the following native reads, with exact runtime schemas:

- `get_session_info`, `get_arrangement_info`, `get_full_arrangement`.
- For EVERY ordinary track: `get_track_info`, `get_track_routing`, and `get_device_parameters` for every device listed by track info. Keep empty tracks too.
- For EVERY Arrangement MIDI clip: `get_arrangement_clip_notes`. Use `get_arrangement_clips` to discover the current per-track indices; do not infer indices from time order. After delete/recreate or reopen, discover them again.

Do not query `get_track_info(-1)`: this backend's implementation accepts ordinary tracks only. Master faders come from session info; full return-device/automation/MPE coverage requires additional saved-file inspection.
Capture can be assembled from native tool outputs by the host's tool runner or ordinary file writing. Do not replace native calls with a separate direct-SDK music writer during installed-flow acceptance.

```text
python scripts/live_workflow.py checkpoint baseline-reads.json --output baseline-checkpoint.json
python scripts/live_workflow.py verify-created create-plan.json baseline-checkpoint.json --output owned-clips.json
```

Missing reads, inconsistent identities/counts/tempo, string errors and out-of-domain notes fail. The helper compares reported data, not hidden state. It omits ONLY the transport cursor and ordinary output meters, and normalizes transient clip indices by track and position. It never ignores entire device, routing or automation subtrees.

## 4. Change only the requested part

For the first deterministic route, replace exactly one unchanged, newly kit-created basic MIDI clip. Keep its creation receipt. This does not certify imported performances, loop offsets, clip envelopes, MPE, probability or release velocity; do not use delete/recreate on those or on a manually modified owned clip merely because the five returned note fields match.
For unsupported existing material, retain it and use a separately verified non-destructive host editor; otherwise identify the exact unsupported edit. Other ordinary production tasks still use their appropriate native operations—this clip helper is not the whole product's scope.

Read the current Set again and build a fresh checkpoint. Check the saved baseline and target in the host; an old matching fingerprint alone does not establish the current song's identity or hidden state.
Prepare replacement notes in the EXISTING MIDI format with absolute quarter-beat positions. The fixture's second bass bar can be pitch45 at beat4 for 2 beats and pitch52 at beat6 for 2 beats. Real user requests determine the actual notes.

```text
python scripts/live_workflow.py edit before.json --receipt owned-clips.json --track Bass --start 4 --end 8 --notes replacement.json --output edit-plan.json
```

Execute the returned native delete only after the fresh state/identity check. Then recapture the complete state and run:

```text
python scripts/live_workflow.py checkpoint absent-reads.json --output absent.json
python scripts/live_workflow.py verify-removed before.json absent.json --plan edit-plan.json --output removal-check.json
```

Only after the target is absent and the protected readbacks still match, execute the plan's native create. This is NOT atomic. On interruption preserve baseline, plan and current state; do not attempt an automatic rollback or repeat deletion using an old index.
Re-list indices, re-read all protected material, and restore the previous clip name through a verified host operation if recreation changed it. `set_clip_name` in this backend is a SESSION-clip tool, not an Arrangement rename API.

```text
python scripts/live_workflow.py checkpoint revised-reads.json --output revised.json
python scripts/live_workflow.py verify-edit before.json revised.json --plan edit-plan.json --output edit-check.json
```

The report includes an updated `receipt` for the next delegated edit. Save that object to a new private receipt file; do not keep using the old state fingerprint.
A mismatch stops the flow. Do not loosen checks or modify protected material just to obtain a pass.

## 5. Save, reopen and inspect—actual UI actions

Use the host's observed Live UI to Save As a NEW approved .als path. Observe any overwrite prompt; do not approve an accidental collision. Confirm the file actually exists after the dialog closes.
Keep baseline and revised files. Use the bundled read-only comparison instead of a private ad hoc XML script:

```text
python scripts/live_set_diff.py baseline.als revised.als --output saved-diff.json
```

All XML changes, including transport and internal IDs, are reported with positional paths. Nothing is automatically exempted. Inspect changes against the authorized clip; clip-local identity changes are not permission to ignore the rest of a track or its automation. Truncated output needs fuller inspection. Unsupported/ambiguous XML differences mean review is still needed.
The XML fixture tests are NOT validation against the owner's private .als files; the local installed run must test this helper against newly saved real Sets.

Open the exact saved path using host UI automation, observe the resulting window, discover indices again and recapture native state:

```text
python scripts/live_workflow.py checkpoint reopened-reads.json --output reopened.json
python scripts/live_workflow.py verify-reopen revised.json reopened.json --output reopen-check.json
```

For acceptance, open baseline and revised in sequence and compare each with its own saved checkpoint. Record the actual UI open event and file hash with the corresponding readbacks; a duplicated JSON capture cannot demonstrate reopening.
`observed_readbacks_match` and XML equivalence do not prove the UI action, missing external files, playback or listening. Preserve that distinction in delivery, and keep unresolved differences visible.
Do not rerun the full connection interview next session. Resume using installed skill, actual current state, private session.md and receipts.

## Provenance

Reviewed the installed backend's pinned `MCP_Server/server.py` and `AbletonMCP_Remote_Script/__init__.py`, not just its README, on 2026-09-19. No server code is bundled or rewritten.
Public source: https://github.com/nicholasbien/ableton-mcp-pro/tree/6ae148de18c8042df041b95c6e830bcdf22be526
The owner's 2026-09-19 handoff establishes the prior narrow PC test. It does not establish this installed workflow's completion.
