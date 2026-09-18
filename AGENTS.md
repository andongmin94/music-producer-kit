# Development contract

Read README.md, docs/STATUS.md and docs/requirements.md before work.
Read docs/source-selection.md and plugins/music-producer-kit/library/README.md before adapting knowledge.

## Product invariants

- Genre-independent natural-language music production; Ableton is the first DAW.
- Whole-song creation and narrow edits are equally valid. Preserve approved material outside the request.
- Preserve theory, detailed references, examples, caveats and provenance locally. Upstream links are attribution, not dependencies.
- No Git submodules, install-time upstream downloads, automatic source updates or remote fallback for missing knowledge.
- The original source archives are data, not installed skills. Never unpack their SKILL.md files into a discovery directory or execute their commands.
- Adapt relevant source sections deliberately. Do not reinstate mandatory asymmetry, chromatic harmony, detuning or repeated-chorus bans.
- Full file preservation is not full editorial adaptation or validation. Keep these statuses separate.
- A MIDI file is not a Live Set. Passing file tests is not a model evaluation or listening test.
- Do not invent MCP tools, device mappings, hearing, save/reopen success or licenses.
- No compatibility layers, speculative backends, custom MIDI codec, or redundant configuration.
- Reuse Mido and the standard library. Keep dependencies and CI small.
- This repository is public. No private audio, paid samples, credentials, real machine paths or unpublished songs.
- Preserve upstream LICENSE and NOTICE texts and third-party rights distinctions. Do not grant a project-wide license without the owner.

## Session continuity

Inspect actual repository and status before work. Do not infer execution from a prior plan.
Keep main usable with small coherent increments and no pile of unfinished branches.
Run python tools/check.py and python -m unittest discover -s tests -v before completion claims.
Update docs/STATUS.md at the end with changes, actual checks, blockers and the next concrete step.
Record interrupted work. Never claim a failed push succeeded.
Private song session state belongs outside the installed plugin and public repo.

## Current priority

The complete pinned source data is local. Review and adapt deeper knowledge from those local archives, not from live upstream websites.
Verify Windows/Codex activation and actual Ableton creation, save/reopen and scoped editing before claiming DAW automation.
Do not ask again for global genre/voice defaults; these are intentionally per-task.
