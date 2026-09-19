# Requirements

The user describes music in ordinary language without theory or DAW expertise.
Inputs may be a short brief, reference, hummed audio, MIDI, lyrics or existing project. Entire songs and a single requested edit are equally valid.
Keep MIDI, separate original audio and an editable Live Set when requested; WAV/stems are not substitutes.

## Confirmed scope

Korean (ko), English (en) and Japanese (ja) lyric/vocal work, including mixtures. Instrumentals need no language.
Chinese-specialist lyrics, pronunciation, genres, orchestration and case material are removed, including original copies in the current source library and distribution.
No archive-audit exception, hidden backup, automatic translation or later specialist workstream.
General theory written in Chinese and Japanese kanji remain valid; source script alone does not determine a song language.
Non-excluded genres remain broad. Language, voice and approval choices vary per song.

## Working implementation

One producer entry selects task guides. A local selected-source catalog supplies retained details without an upstream service.
Mido creates, inspects and safely edits bounded MIDI regions. SoundFile reads headers of locally selected samples; a private JSON inventory supports filename search and selected-file hash inspection.
Read only an explicit sample directory. Do not follow links/junctions, buy credits, upload audio or infer licenses from a filename.
Use owned tools first. Additional spending and private upload need explicit permission.
Windows/Codex/Ableton are the first target. The 2026-09-19 owner handoff records successful connection and a disposable four-bar edit/save/reopen; preserve those facts separately from installed-plugin acceptance.
Use the existing native ableton_live tools for production. Save/new/open are host Windows UI actions, not fabricated MCP methods. No new backend or private direct-SDK production script is required.
The plugin prepares note payloads, validates owned-clip edits and compares native readbacks/saved XML. The local host provides real application calls and observed UI actions. Rendering/listening still require their own evidence.

## Separate completion criteria

Package: file paths, source selection, MIDI/audio helpers, tests and distribution are valid.
Behavior: real Codex traces satisfy the scenarios in evals/scenarios.json.
Music/DAW: Live opens editable material and save/reopen, scoped changes and listening are actually verified.
A pass in one does not establish the others.
