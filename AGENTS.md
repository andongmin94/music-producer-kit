# Development contract

Read README.md, docs/STATUS.md and docs/requirements.md before changing code.
Read docs/source-selection.md before importing upstream knowledge.

## Product invariants

- Build a genre-independent, natural-language music production plugin; Ableton is the first DAW.
- Whole-song creation and narrow edits are equally valid. Preserve approved material outside the request.
- Keep theory, examples, caveats and source links. Do not turn stylistic preferences into mandatory rules.
- A readable MIDI file is not an Ableton Set. Static checks are not model evaluations or listening tests.
- Do not invent MCP tools, parameter mappings, hearing, save/reopen success or purchased licenses.
- Do not add compatibility layers, speculative backends, a custom MIDI codec, or redundant configuration.
- Reuse Mido for Standard MIDI I/O. Keep dependencies and CI small.
- This repository is public. No private questionnaire, local paths, audio, paid samples, credentials or unpublished songs.
- Do not grant a project-wide redistribution license without the owner's decision. Preserve third-party notices.

## Session continuity

At the start, inspect the actual repository and current status; don't infer success from an old chat.
Implement the smallest tested end-to-end increment. Keep main usable; no pile of unfinished feature branches.
Run `python tools/check.py` and `python -m unittest discover -s tests -v` before a completion claim.
Before finishing every work session, update docs/STATUS.md with what changed, actual checks, limitations and the next concrete step.
Record interrupted or blocked work as such. Commit small coherent checkpoints; never claim a failed push succeeded.
Keep raw audio and machine-specific diagnostics in an external private workspace.

## Current priority

Finish the Windows/Codex installation and real Ableton capability smoke test before expanding integrations.
Expand advanced reference knowledge incrementally from the inventory, with scope and source decisions recorded.
Do not ask again for fixed global genre/voice preferences; they are intentionally per-task.
