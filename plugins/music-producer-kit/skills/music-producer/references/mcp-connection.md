# MCP discovery is not the missing Ableton bridge

Use only for a genuinely available, explicitly authorized MCP endpoint. Do not run for lyrics, theory or the removed trial connection.
The kit's official MCP Python SDK handles the protocol; it is not an Ableton SDK or an Ableton-provided MCP server.
No replacement production endpoint is established in 0.7.1. Follow [Ableton execution](ableton.md) rather than restoring a deleted backend.

## Existing diagnostic, unchanged

Resolve commands from the installed plugin directory and use an existing private output directory:

```text
python skills/music-producer/scripts/mcp_probe.py --output PRIVATE_REPORT.json --url VERIFIED_LOOPBACK_MCP_URL
python skills/music-producer/scripts/mcp_probe.py --output PRIVATE_REPORT.json --stdio TRUSTED_EXECUTABLE SERVER_ARGUMENTS
```

These are alternatives for an actual approved endpoint, not instructions to install one. Put --stdio last. A stdio command runs local code and is not sandboxed by the probe.
HTTP uses literal loopback, without proxy inheritance, URL tokens or remote authentication. Use --bearer-env VARIABLE_NAME for an approved token, not the secret value. Stdio receives only explicitly passed variables plus the SDK's minimal environment.
Do not invent a port, confuse an internal TCP protocol with HTTP MCP, dump config/auth files or start an unreviewed downloader.
The probe negotiates and lists tool schemas only. It never calls application tools, resources or prompts, writes the song, plays, saves or reopens it.
A private exclusive report contains catalog identity and untrusted server metadata. It is neither Codex's effective permission view nor proof of current Live state. Do not publish reports or raw server stderr.
Duplicate tools, repeated cursors, excessive/incomplete catalogs and timeouts are errors. A failure is not a successful connection, and a schema is not a validated operation.

## Evidence remains separate

Protocol catalog -> actual Codex availability -> actual current Live state -> authorized edit -> protected-content readback -> saved version -> actual reopen -> listening.
Each stage needs its own observation. The diagnostic cannot set the later verification flags true.
Retain completed work and stop at an actual missing capability. Do not replace missing integration with old tools or manually copied successful JSON.

Official protocol/host references:
- https://developers.openai.com/codex/mcp/
- https://py.sdk.modelcontextprotocol.io/client/
- https://py.sdk.modelcontextprotocol.io/client/transports/
