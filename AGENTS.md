# Development contract

Read README.md, docs/STATUS.md and docs/requirements.md before work.
Read docs/source-selection.md and the installed library guide before adapting knowledge.

## Product invariants

- Natural-language music production, Ableton-first; a simple interface need not mean simple music.
- Lyric/vocal languages are Korean, English and Japanese, singly or mixed. Instrumentals are valid.
- Chinese-specialist production material is removed from both the working library and shipped source data. Do not keep an alternate archive, audit mode, hidden copy or restoration fallback.
- General theory written in Chinese is not Chinese-specialist production. Preserve useful craft and Japanese kanji; do not classify the task language by Unicode ranges.
- Whole-song and narrow edits are equally valid. Preserve approved material outside the request.
- The selected source catalog is the one inventory. Source URLs are provenance, not dependencies. Retain relevant detail, examples, exceptions and origin hashes; describe edited source files as selected, not complete unmodified upstream snapshots.
- No submodules, source downloads, automatic updates, compatibility layers or remote recovery.
- No compulsory asymmetry, chromatic harmony, detuning or changed choruses.
- A MIDI file is not a Live Set; passing tests is not hearing, native review or musical quality.
- Verify actual tool schemas; never invent MCP operations, device mappings or save/reopen success.
- Reuse Mido for MIDI and SoundFile for audio headers. Do not reimplement audio codecs or build a sample database server.
- Local sample inspection is read-only and private. File presence and filenames do not verify a license, BPM, key or quality.
- No purchases, credit use, account changes or external audio upload without explicit permission.
- No private audio, paid samples, credentials, real user paths or unpublished songs in this public repository.
- Preserve third-party LICENSE/NOTICE. No project-wide license grant without the owner.

## Session continuity

Inspect actual repository state, not old plans. Keep main usable through coherent tested changes.
Run python tools/check.py and python -m unittest discover -s tests -v; distinguish local and remote results.
Update docs/STATUS.md with outcomes, blockers and the next step before ending each session.
Never call a queued run passing or a defined model scenario executed. Song state belongs in the private song workspace.
Do not re-ask permanent genre/voice questions or reopen the language scope without a new owner decision.

## Current priority

Complete an actual Windows/Codex/Ableton smoke test: inspect capabilities, create editable material, save/reopen and perform a scoped edit.
Use the local sample inventory to identify real available files rather than inventing presets or sample names.
Continue in-scope specialist craft curation only where it helps these workflows.
