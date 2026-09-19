# Ableton execution: discover capabilities, then act

No Ableton MCP server is bundled. This is an execution procedure supported by a real diagnostic client, not an imaginary API adapter.
For ordinary production use [the installed workflow](live-workflow.md), which reuses the owner-tested ableton_live backend.
Only for a genuinely missing connection, server changes or a missing tool, use [MCP discovery and first acceptance](mcp-connection.md).
The diagnostic connects through the official SDK and reads tool definitions only; it does not invoke application tools or prove Live is running.

## Before writing

Read the available MCP tools, exact schemas, server/version and current Live state.
Keep standalone discovery, Codex tool availability and actual Live state as separate observations.
Record a private capability note for the operations needed now: track/clip/note read/write, Arrangement placement, device/sample loading, save, export and reopen.
Use IDs and paths obtained from actual reads; do not guess tool names, index bases or device parameters.
Mark untested and unsupported operations separately. Do not infer support from an advertised tool count or a readOnlyHint annotation.
Session View clips and Arrangement clips are not interchangeable evidence.

## Scope and timing

Read the target and relevant context. Save an identifiable recoverable take before writes when supported.
Identify tempo/meter changes and each tool's units; MIDI-helper beats are quarter notes while API/display positions may differ.
Preserve protected parts, clip boundaries, automation and routing. A whole-track overwrite is not a chorus-only edit.
When notes overlap a boundary or a held pedal sustains into another section, do not silently trim performance data.
Batch calls only when the tool supports it and ordering is safe. Read back actual state after mutation.

## Sources and devices

Prefer owned installed devices and local licensed audio. Do not make purchases or consume credits without explicit permission.
Keep private workspace paths and account credentials out of version control; paid samples are not redistributed with this plugin.
Inspect actual Drum Rack assignments; sample key and tempo labels may need verification.
Existing VST loading does not imply access to Melodyne's note editor or a singing engine's lyrics editor.
Retain source recordings and editable MIDI; freeze/render to a new version rather than destroying the editable source by default.

## Completion

For a requested Live deliverable, verify actual .als/project save, source references, devices and editability after reopening.
Check file collection separately from external plugin installation/library dependencies.
A MIDI export alone or a successful save command is not this full acceptance test.
Record a manual intervention as manual, not an automated capability. Do not close an unsaved song or erase scratch work without authorization.
If a required capability is unavailable, report it and the completed portion honestly; do not relabel a substitute as the requested finished Set.

Official behavior references to verify against the installed Live version:
https://www.ableton.com/en/manual/live-concepts/
https://www.ableton.com/en/manual/managing-files-and-sets/
https://www.ableton.com/en/manual/converting-audio-to-midi/
https://docs.cycling74.com/apiref/lom/
