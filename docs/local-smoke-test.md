# Windows and Ableton acceptance test

The 2026-09-19 owner handoff records completed PC-level connection/edit/save/reopen tests. Installed-plugin end-to-end acceptance remains separate; follow [the current installed-flow test](installed-flow-acceptance.md).

## 1. Install the skill package

In PowerShell, with a local Codex installation:

```powershell
codex plugin marketplace add andongmin94/music-producer-kit
codex plugin marketplace list
```

Open the supported desktop Plugins interface, select Music Producer Kit, install it, then start a new conversation.
Marketplace registration alone is not installation or proof of skill activation.
Ask Codex to use `music-producer` and verify the loaded SKILL.md path in the session.
Client availability varies; check `codex plugin --help` and the current official docs rather than inventing flags.

For local plugin development, register the checked-out repository with `codex plugin marketplace add .` instead of registering both copies.
Do not also install the same skill separately or activate both upstream packs alongside this version.

Official packaging and install reference: https://developers.openai.com/plugins/build/plugins

## 2. Test the offline MIDI helper

With Python 3.12+ and a checkout of the repository:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r plugins/music-producer-kit/requirements.txt
.\.venv\Scripts\python.exe tools/check.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
$skill = 'plugins/music-producer-kit/skills/music-producer'
$out = Join-Path $env:TEMP ('mpk-smoke-' + [guid]::NewGuid().ToString('N'))
.\.venv\Scripts\python.exe "$skill/scripts/midi_tools.py" create "$skill/examples/song.json" "$out/take-1.mid"
$before = .\.venv\Scripts\python.exe "$skill/scripts/midi_tools.py" inspect "$out/take-1.mid" | ConvertFrom-Json
.\.venv\Scripts\python.exe "$skill/scripts/midi_tools.py" patch "$out/take-1.mid" --output "$out/take-2.mid" --track Drums --start 4 --end 8 --notes "$skill/examples/drums-replacement.json" --expected-sha256 $before.sha256
```

These are original two-bar test notes, not a demonstration of final musical quality.
The helper does not play MIDI, install instruments or create an .als file.

## 3. Installed workflow acceptance

Use the existing owner-tested ableton_live connection in a fresh supported Codex desktop session. Do not reselect/reinstall a server or use a separate SDK writer to conceal missing native exposure.
Run [installed-flow acceptance](installed-flow-acceptance.md), using only the shipped skill and helpers. New/open/save are the host's real UI automation, not missing MCP methods or user-manual work by default.

## Report

Mark each stage PASS / FAIL / NOT RUN, including exact command or observed tool evidence.
Do not mark an unrun stage as PASS. Keep private diagnostic paths and audio out of any public report.

## Local sample inventory before sound selection

Use the sample guide on an explicitly chosen owned sample directory. Save the JSON outside this repository and the installed plugin.
Inspect a selected file again before an actual Live import. The inventory does not establish a Splice license or that audio was heard.
See [sample workflow](../plugins/music-producer-kit/skills/music-producer/references/samples.md).
