# Requirements

This is a public product brief, not a user's private equipment or questionnaire record.

## Confirmed product direction

The user describes music in ordinary language, without needing DAW or music-theory expertise.
Support original songs, backing music and personal listening projects without a genre allowlist.
A request may delegate everything or only lyrics, melody, accompaniment, a section, or one part.
Inputs may be a short brief, a reference track/artist, hummed audio, MIDI or an existing project.
Lyrics, language, vocal production and intermediate approvals are selected per task, not permanent defaults.
Preserve editable MIDI, separated source audio and the Live Set when a DAW deliverable is requested.
A stem or complete WAV is not a substitute for the editable project.
Use available instruments and samples first; obtain explicit permission before spending or uploading private audio.
Target local Windows, Codex and Ableton Live first. Version and MCP capabilities require runtime discovery.
Music theory should remain broad. A simple interface must not impose simple music.

## Decisions for this first increment

- One entry skill handles request scope and chooses small topic references as needed.
- References are new scoped summaries with upstream provenance, not a full copied textbook collection.
- Bundle complete pinned source snapshots, including references and notices, inside the plugin and Git repository. No upstream runtime fetch, submodule or install-time download is allowed.
- Preservation and adaptation are independent: all original files remain accessible locally even when editorial adaptation is pending.
- One Mido-based helper creates/inspects MIDI and replaces notes in one track/interval with integrity checks.
- No bundled MCP server, DAW controller, synthesizer, audio model, account integration or automatic spending.
- The first verified path is JSON notes -> editable MIDI -> bounded note edit -> file readback.
- Real Live creation, device loading, save/reopen and audio review are a separate, required next acceptance test.

## Completion has three independent meanings

Package: metadata, paths, dependencies, helper tests and distribution archive are valid.
Behavior: real Codex traces satisfy the task-scope scenarios in evals/scenarios.json.
Music/DAW: Live opens the result, sources remain editable, and the user has heard the audio.
Do not report one of these as proof of the other two.
