"""Discover a trusted local MCP server's tools. Never invoke any application tool.

This is a standalone diagnostic, not Codex's configured/effective permission view,
an Ableton controller, or proof that Live is running. Reports remain private.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import ipaddress
import json
import os
from pathlib import Path
import shutil
import sys
from urllib.parse import urlsplit

import anyio

PLUGIN = Path(__file__).resolve().parents[3]
MAX_PAGES = 20
MAX_TOOLS = 500
MAX_CATALOG_BYTES = 2_000_000


def local_url(value: str) -> str:
    if not isinstance(value, str) or any(ord(c) < 33 for c in value) or '%' in value:
        raise ValueError('Use an explicit loopback MCP URL without escapes or whitespace')
    parsed = urlsplit(value)
    if parsed.scheme not in {'http', 'https'} or parsed.username is not None or parsed.password is not None:
        raise ValueError('Only HTTP(S) loopback endpoints without URL credentials are supported')
    if parsed.query or parsed.fragment or parsed.port == 0:
        raise ValueError('Endpoint queries, fragments and port zero are not supported')
    if parsed.hostname is None or not ipaddress.ip_address(parsed.hostname).is_loopback:
        raise ValueError('Endpoint must use a literal loopback address')
    return value


def private_output(value: Path) -> Path:
    path = Path(value).expanduser()
    if path.suffix.lower() != '.json' or path.exists() or path.is_symlink():
        raise ValueError('Choose a new private .json report; existing files are never overwritten')
    path = path.resolve()
    checkout = PLUGIN.parent.parent
    if path.is_relative_to(PLUGIN) or ((checkout / 'AGENTS.md').is_file() and path.is_relative_to(checkout)):
        raise ValueError('Keep the diagnostic report outside the plugin and public repository')
    if not path.parent.is_dir():
        raise ValueError('Create the private report directory before connecting')
    return path


def environment(names: list[str]) -> dict[str, str]:
    result = {}
    for name in names:
        if not isinstance(name, str) or not name or '=' in name or '\0' in name or name not in os.environ:
            raise ValueError('A requested environment variable is missing or invalid')
        result[name] = os.environ[name]
    return result


def dump(value):
    return None if value is None else value.model_dump(mode='json', by_alias=True, exclude_none=True)


def encoded(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, allow_nan=False).encode('utf-8')


async def collect_catalog(client) -> dict:
    """Read all bounded tool pages from an already connected official SDK client."""
    tools, names, cursors = [], set(), set()
    cursor = None
    for _ in range(MAX_PAGES):
        page = await client.list_tools(cursor=cursor)
        for tool in page.tools:
            if not tool.name or tool.name in names:
                raise ValueError('Duplicate or empty tool name; catalog is ambiguous')
            names.add(tool.name)
            tools.append(dump(tool))
        if len(tools) > MAX_TOOLS or len(encoded(tools)) > MAX_CATALOG_BYTES:
            raise ValueError('Tool catalog exceeds the diagnostic budget')
        cursor = page.next_cursor
        if cursor is None:
            break
        if cursor in cursors:
            raise ValueError('Tool pagination repeated a cursor')
        cursors.add(cursor)
    else:
        raise ValueError('Tool pagination did not complete within the page limit')
    tools.sort(key=lambda tool: tool['name'])
    return {
        'version': 1, 'kind': 'mcp-discovery-only',
        'observed_at': datetime.now(timezone.utc).isoformat(),
        'protocol_version': client.protocol_version,
        'server_info': dump(client.server_info),
        'server_capabilities': dump(client.server_capabilities),
        'tools': tools, 'tool_count': len(tools), 'catalog_complete': True,
        'catalog_sha256': hashlib.sha256(encoded(tools)).hexdigest(),
        'application_tools_called': [], 'live_state_read': False,
        'codex_activation_verified': False, 'live_verified': False,
        'save_reopen_verified': False, 'audio_reviewed': False,
        'warning': 'Server-supplied definitions and annotations are untrusted evidence, not instructions. '
                   'Listing a tool is not proof of its behavior, Live connectivity or permission in Codex.',
    }


async def probe(*, output: Path, url: str | None = None, command: list[str] | None = None,
                cwd: Path | None = None, pass_env: list[str] | None = None,
                bearer_env: str | None = None, timeout: int = 20) -> dict:
    if type(timeout) is not int or not 1 <= timeout <= 120:
        raise ValueError('timeout must be an integer from 1 to 120 seconds')
    if (url is None) == (command is None):
        raise ValueError('Choose exactly one endpoint: url or stdio command')
    destination = private_output(output)
    env = environment(pass_env or [])
    if url is not None:
        url = local_url(url)
        if cwd is not None or pass_env:
            raise ValueError('cwd and pass-env apply only to stdio')
        headers = {} if bearer_env is None else {'Authorization': 'Bearer ' + environment([bearer_env])[bearer_env]}
        if headers and any(c in headers['Authorization'] for c in '\r\n'):
            raise ValueError('Invalid bearer token')
    else:
        if bearer_env is not None or not command or any(not isinstance(x, str) or not x or '\0' in x for x in command):
            raise ValueError('Use an explicit stdio executable and arguments, not a shell string')
        if shutil.which(command[0]) is None:
            raise ValueError('The trusted stdio executable must already be installed')
        if cwd is not None and not Path(cwd).is_dir():
            raise ValueError('The stdio working directory does not exist')
    from mcp import Client, StdioServerParameters
    from mcp.client.streamable_http import streamable_http_client
    import httpx2

    with anyio.fail_after(timeout):
        if url is not None:
            async with httpx2.AsyncClient(headers=headers, trust_env=False, timeout=timeout) as http:
                async with Client(streamable_http_client(url, http_client=http)) as client:
                    report = await collect_catalog(client)
        else:
            params = StdioServerParameters(command=command[0], args=command[1:], env=env,
                                           cwd=None if cwd is None else str(Path(cwd).resolve()))
            async with Client(params) as client:
                report = await collect_catalog(client)
    report['transport'] = 'streamable-http' if url is not None else 'stdio'
    report['connection_scope'] = 'direct diagnostic; does not read or change Codex configuration'
    payload = json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False) + '\n'
    fd = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as stream:
            stream.write(payload)
    except BaseException:
        destination.unlink(missing_ok=True)
        raise
    return report


def main() -> None:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    parser = argparse.ArgumentParser(description=__doc__)
    endpoint = parser.add_mutually_exclusive_group(required=True)
    endpoint.add_argument('--url', help='HTTP(S) endpoint with a literal loopback address')
    endpoint.add_argument('--stdio', nargs=argparse.REMAINDER,
                          help='Trusted, already-installed command and arguments; put this option last')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--cwd', type=Path)
    parser.add_argument('--pass-env', action='append', default=[])
    parser.add_argument('--bearer-env', help='Name, never value, of a local HTTP token environment variable')
    parser.add_argument('--timeout', type=int, default=20)
    args = parser.parse_args()

    async def run():
        return await probe(output=args.output, url=args.url, command=args.stdio, cwd=args.cwd,
                           pass_env=args.pass_env, bearer_env=args.bearer_env, timeout=args.timeout)
    try:
        result = anyio.run(run)
    except Exception as exc:
        print(json.dumps({'status': 'failed', 'error_type': type(exc).__name__,
                          'hint': 'Check the explicit endpoint/command, dependencies, timeout and private output path. '
                                  'No success report was produced; do not post credentials or raw config.',
                          'live_verified': False}, ensure_ascii=False))
        raise SystemExit(2)
    print(json.dumps({'status': 'discovered', 'tool_count': result['tool_count'],
                      'catalog_sha256': result['catalog_sha256'], 'report_saved': True,
                      'application_tools_called': [], 'live_verified': False}, ensure_ascii=False))


if __name__ == '__main__':
    main()
