# Windows and Ableton acceptance test

Status: procedure only; not yet executed on the target Windows machine.

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

## 3. Discover the actual Ableton connection

In a scratch Live Set, let the agent list the actual MCP tools and inspect their schemas.
Record server/version and evidence for: state read, MIDI track/clip creation, note read/write, instrument/sample loading, Arrangement access, save, export and reopen.
Record unsupported features explicitly. Session clips do not automatically prove Arrangement support.
Do not install every available MCP server; select one after reviewing its maintained implementation and applicable interfaces.
Never put machine-specific configuration or credentials in this public repo.

## 4. Live acceptance

Use only existing devices. Load the generated tracks or create their notes through verified tools.
Keep MIDI clips editable. Check drum note-to-pad assignments and instrument availability.
Play the set. Save a new project and collect referenced audio where supported; external plugin libraries remain separate dependencies.
Reopen the set and verify the actual tracks, MIDI, devices, audio references and automation.
Request: '두 번째 마디의 드럼만 바꿔. 멜로디와 베이스는 그대로.'
Compare before/after Live data, not just the tool's success response. Listen separately when audio access exists.
MIDI helper hashes do not verify Live devices, automation, routing or source-file collection.

## Report

Mark each stage PASS / FAIL / NOT RUN, including exact command or observed tool evidence.
Do not mark an unrun stage as PASS. Keep private diagnostic paths and audio out of any public report.

## Local sample inventory before sound selection

Use the sample guide on an explicitly chosen owned sample directory. Save the JSON outside this repository and the installed plugin.
Inspect a selected file again before an actual Live import. The inventory does not establish a Splice license or that audio was heard.
See [sample workflow](../plugins/music-producer-kit/skills/music-producer/references/samples.md).
