"""Protocol-fixture and diagnostic tests. None of these start Ableton or Codex."""
import asyncio
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'plugins/music-producer-kit/skills/music-producer/scripts/mcp_probe.py'
sys.path.insert(0, str(SCRIPT.parent))
import mcp_probe as probe


class Model:
    def __init__(self, **data):
        self.data = data
        self.__dict__.update(data)

    def model_dump(self, **kwargs):
        return self.data


def tool(name):
    return Model(name=name, inputSchema={'type': 'object', 'properties': {}},
                 annotations={'readOnlyHint': False})


class Pages:
    protocol_version = 'fixture-only'
    server_info = Model(name='Fixture, not Live', version='1')
    server_capabilities = Model(tools={})

    def __init__(self, pages):
        self.pages = iter(pages)
        self.seen = []

    async def list_tools(self, cursor=None):
        self.seen.append(cursor)
        return next(self.pages)


def page(tools, cursor=None):
    return SimpleNamespace(tools=tools, next_cursor=cursor)


class ProbeUnitTests(unittest.TestCase):
    def test_loopback_urls(self):
        for url in ['http://127.0.0.1:8722/mcp', 'http://[::1]:8000/mcp', 'https://127.0.0.1/mcp']:
            self.assertEqual(probe.local_url(url), url)
        for url in ['https://example.com/mcp', 'http://localhost/mcp', 'http://192.168.1.2/mcp',
                    'file:///etc/passwd', 'http://u:p@127.0.0.1/mcp', 'http://127.0.0.1/?token=secret',
                    'http://127.0.0.1/#fragment', 'http://127.0.0.1:0/mcp',
                    'http://127.0.0.1/mcp\n', 'http://127.0.0.1/%2e%2e', '']:
            with self.subTest(url=url), self.assertRaises(ValueError):
                probe.local_url(url)

    def test_pages_and_honest_verification_flags(self):
        client = Pages([page([tool('z')], 'second'), page([tool('a')])])
        result = asyncio.run(probe.collect_catalog(client))
        self.assertEqual(client.seen, [None, 'second'])
        self.assertEqual([t['name'] for t in result['tools']], ['a', 'z'])
        self.assertEqual(result['catalog_sha256'], hashlib.sha256(probe.encoded(result['tools'])).hexdigest())
        self.assertEqual(result['application_tools_called'], [])
        for key in ['live_state_read', 'codex_activation_verified', 'live_verified', 'save_reopen_verified', 'audio_reviewed']:
            self.assertFalse(result[key])
        self.assertNotIn('instructions', result)

    def test_empty_catalog_and_absent_identity(self):
        client = Pages([page([])])
        client.server_info = None
        result = asyncio.run(probe.collect_catalog(client))
        self.assertEqual(result['tool_count'], 0)
        self.assertIsNone(result['server_info'])
        self.assertFalse(result['live_verified'])

    def test_repeated_cursor_and_duplicate_tools_fail(self):
        for pages in [[page([], 'x'), page([], 'x')],
                      [page([tool('a')], 'x'), page([tool('a')])]]:
            with self.subTest(pages=pages), self.assertRaises(ValueError):
                asyncio.run(probe.collect_catalog(Pages(pages)))

    def test_budgets(self):
        for name, value, pages in [('MAX_TOOLS', 1, [page([tool('a'), tool('b')])]),
                                   ('MAX_PAGES', 1, [page([], 'more')]),
                                   ('MAX_CATALOG_BYTES', 5, [page([tool('a')])])]:
            with self.subTest(name=name), patch.object(probe, name, value), self.assertRaises(ValueError):
                asyncio.run(probe.collect_catalog(Pages(pages)))

    def test_private_exclusive_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            # Windows may supply an 8.3 alias for the same real temporary directory.
            root = Path(tmp).resolve()
            path = root / 'report.json'
            self.assertEqual(probe.private_output(path), path)
            path.write_text('protected', encoding='utf-8')
            with self.assertRaises(ValueError):
                probe.private_output(path)
            self.assertEqual(path.read_text(), 'protected')
            with self.assertRaises(ValueError):
                probe.private_output(root / 'missing/report.json')
            with self.assertRaises(ValueError):
                probe.private_output(root / 'report.txt')
            plugin = root / 'repo/plugins/kit'
            plugin.mkdir(parents=True)
            (root / 'repo/AGENTS.md').write_text('fixture')
            with patch.object(probe, 'PLUGIN', plugin):
                for path in [plugin / 'private.json', root / 'repo/private.json']:
                    with self.assertRaises(ValueError):
                        probe.private_output(path)

    def test_explicit_environment(self):
        with patch.dict(os.environ, {'MPK_PROBE_SECRET': 'private'}, clear=True):
            self.assertEqual(probe.environment(['MPK_PROBE_SECRET']), {'MPK_PROBE_SECRET': 'private'})
            self.assertEqual(probe.environment([]), {})
            with self.assertRaises(ValueError):
                probe.environment(['MISSING'])
            with self.assertRaises(ValueError):
                probe.environment(['BAD=NAME'])

    def test_invalid_inputs_fail_before_sdk_or_server_start(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / 'report.json'
            cases = [{'timeout': 0}, {'timeout': True}, {'command': []},
                     {'url': 'http://192.168.0.1/mcp'}, {'command': ['certainly-not-an-installed-mcp-8123']},
                     {'url': 'http://127.0.0.1/mcp', 'cwd': Path(tmp)},
                     {'url': 'http://127.0.0.1/mcp', 'command': [sys.executable]}]
            for case in cases:
                with self.subTest(case=case), self.assertRaises(ValueError):
                    asyncio.run(probe.probe(output=output, **case))
                self.assertFalse(output.exists())

    def test_discovery_code_does_not_call_application_tools(self):
        import ast
        tree = ast.parse(SCRIPT.read_text(encoding='utf-8'))
        called = {n.func.attr for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)}
        self.assertNotIn('call_tool', called)
        self.assertNotIn('read_resource', called)
        self.assertNotIn('get_prompt', called)


class ProbeSDKTests(unittest.TestCase):
    def test_real_in_memory_sdk_only_discovers(self):
        from mcp import Client
        from mcp.server import MCPServer
        server = MCPServer('Probe fixture, not Ableton')
        invoked = []

        @server.tool()
        def forbidden_write(value: int) -> int:
            invoked.append(value)
            return value

        async def run():
            async with Client(server) as client:
                return await probe.collect_catalog(client)

        result = asyncio.run(run())
        self.assertEqual([t['name'] for t in result['tools']], ['forbidden_write'])
        self.assertEqual(result['tools'][0]['inputSchema']['properties']['value']['type'], 'integer')
        self.assertEqual(invoked, [])
        self.assertFalse(result['live_verified'])

    def test_real_stdio_cli_report_and_no_tool_execution(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            output = root / 'report.json'
            sentinel = root / 'called'
            fixture = ROOT / 'tests/fixtures/probe_server.py'
            result = subprocess.run([sys.executable, str(SCRIPT), '--output', str(output), '--timeout', '15',
                                     '--stdio', sys.executable, str(fixture), str(sentinel)],
                                    capture_output=True, encoding='utf-8', timeout=25)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            summary = json.loads(result.stdout)
            self.assertEqual(summary['status'], 'discovered')
            report = json.loads(output.read_text(encoding='utf-8'))
            self.assertEqual(report['transport'], 'stdio')
            self.assertEqual(report['tool_count'], 1)
            self.assertFalse(sentinel.exists())
            self.assertNotIn(str(sentinel), output.read_text(encoding='utf-8'))
            self.assertFalse(report['save_reopen_verified'])

    def test_timeout_creates_no_success_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / 'report.json'
            result = subprocess.run([sys.executable, str(SCRIPT), '--output', str(output), '--timeout', '1',
                                     '--stdio', sys.executable, '-c', 'import time; time.sleep(30)'],
                                    capture_output=True, encoding='utf-8', timeout=15)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(json.loads(result.stdout)['status'], 'failed')
            self.assertFalse(output.exists())

    def test_loopback_http_failure_is_not_live_success(self):
        import socket
        with tempfile.TemporaryDirectory() as tmp, socket.socket() as sock:
            sock.bind(('127.0.0.1', 0))
            output = Path(tmp) / 'report.json'
            result = subprocess.run([sys.executable, str(SCRIPT), '--output', str(output), '--timeout', '2',
                                     '--url', f'http://127.0.0.1:{sock.getsockname()[1]}/mcp'],
                                    capture_output=True, encoding='utf-8', timeout=15)
            self.assertEqual(result.returncode, 2)
            self.assertFalse(output.exists())
            self.assertFalse(json.loads(result.stdout)['live_verified'])

    def test_real_loopback_http_catalog_without_proxy_or_tool_calls(self):
        import socket
        import threading
        import time
        import uvicorn
        from mcp.server import MCPServer

        mcp = MCPServer('HTTP fixture, not Ableton')
        invoked = []

        @mcp.tool()
        def forbidden_write(value: int) -> int:
            invoked.append(value)
            return value

        with tempfile.TemporaryDirectory() as tmp, socket.socket() as sock:
            sock.bind(('127.0.0.1', 0))
            sock.listen(128)
            endpoint = f'http://127.0.0.1:{sock.getsockname()[1]}/mcp'
            server = uvicorn.Server(uvicorn.Config(mcp.streamable_http_app(),
                                                   log_level='error', access_log=False,
                                                   timeout_graceful_shutdown=2))
            failures = []

            def serve():
                try:
                    server.run(sockets=[sock])
                except BaseException as error:
                    failures.append(error)

            thread = threading.Thread(target=serve, daemon=True)
            thread.start()
            try:
                deadline = time.monotonic() + 10
                while not server.started and thread.is_alive() and time.monotonic() < deadline:
                    time.sleep(0.02)
                self.assertTrue(server.started, str(failures))
                output = Path(tmp) / 'report.json'
                with patch.dict(os.environ, {'HTTP_PROXY': 'http://127.0.0.1:1',
                                              'HTTPS_PROXY': 'http://127.0.0.1:1',
                                              'ALL_PROXY': 'http://127.0.0.1:1', 'NO_PROXY': ''}):
                    result = asyncio.run(probe.probe(output=output, url=endpoint, timeout=10))
                self.assertEqual(result['transport'], 'streamable-http')
                self.assertEqual([t['name'] for t in result['tools']], ['forbidden_write'])
                self.assertEqual(invoked, [])
                self.assertEqual(json.loads(output.read_text(encoding='utf-8'))['catalog_sha256'],
                                 result['catalog_sha256'])
                self.assertFalse(result['live_state_read'])
                self.assertFalse(result['live_verified'])
            finally:
                server.should_exit = True
                thread.join(timeout=5)
                if thread.is_alive():
                    server.force_exit = True
                    thread.join(timeout=3)
            self.assertFalse(thread.is_alive(), 'HTTP fixture did not stop')
            self.assertFalse(failures)


if __name__ == '__main__':
    unittest.main()
