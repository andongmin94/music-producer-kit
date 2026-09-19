"""Retirement and private saved-file checks; no official SDK or Live emulation."""
from pathlib import Path
import gzip
import json
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / 'plugins/music-producer-kit'
SCRIPT = PLUGIN / 'skills/music-producer/scripts'
sys.path.insert(0, str(SCRIPT))
sys.path.insert(0, str(ROOT / 'tools'))
import live_set_diff as sets
import check as package


class OfficialFirstTests(unittest.TestCase):
    def test_retired_writer_and_instructions_absent(self):
        self.assertFalse((SCRIPT / 'live_workflow.py').exists())
        self.assertFalse((SCRIPT.parent / 'references/live-workflow.md').exists())
        # The shipped operating text must not depend on the old backend or port.
        for p in [SCRIPT.parent / 'SKILL.md', *sorted((SCRIPT.parent / 'references').glob('*.md'))]:
            text = p.read_text(encoding='utf-8')
            with self.subTest(path=p.name):
                for old in ('nicholasbien', 'ableton_live', 'live_workflow.py', '127.0.0.1:9877'):
                    self.assertNotIn(old, text)

    def test_saved_comparison_has_no_backend_or_protocol_dependency(self):
        import ast
        tree = ast.parse((SCRIPT / 'live_set_diff.py').read_text(encoding='utf-8'))
        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.update(alias.name.split('.')[0] for alias in node.names)
            if isinstance(node, ast.ImportFrom) and node.module:
                imports.add(node.module.split('.')[0])
        self.assertFalse(imports & {'live_workflow', 'mcp', 'mcp_probe'})

    def test_package_rejects_reintroduced_writer(self):
        import shutil
        with tempfile.TemporaryDirectory() as directory:
            copy = Path(directory) / 'copy'
            shutil.copytree(ROOT, copy, ignore=shutil.ignore_patterns('.git', '__pycache__', 'dist'))
            writer = copy / 'plugins/music-producer-kit/skills/music-producer/scripts/live_workflow.py'
            writer.write_text('# retired route', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'Retired trial-backend'):
                package.check(copy)

    def test_private_report_is_exclusive_and_unicode_safe(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            target = root / '검사.json'
            sets.save_report({'result': '확인 / 確認'}, target)
            expected = target.read_bytes()
            self.assertEqual(json.loads(target.read_text(encoding='utf-8'))['result'], '확인 / 確認')
            with self.assertRaises(FileExistsError):
                sets.save_report({'wrong': True}, target)
            self.assertEqual(target.read_bytes(), expected)
            with self.assertRaises(ValueError):
                sets.save_report({'nonfinite': float('nan')}, root / 'bad.json')
            self.assertFalse((root / 'bad.json').exists())

    def test_private_report_rejects_plugin_repository_and_bad_destination(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            plugin = root / 'checkout/plugins/kit'
            plugin.mkdir(parents=True)
            (root / 'checkout/AGENTS.md').write_text('test', encoding='utf-8')
            with patch.object(sets, 'PLUGIN', plugin):
                for target in (plugin / 'out.json', root / 'checkout/out.json', root / 'missing/out.json', root / 'out.als'):
                    with self.subTest(target=target), self.assertRaises(ValueError):
                        sets.save_report({}, target)
            self.assertFalse(list(root.rglob('*.json')))

    def test_private_report_rejects_symlink(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            original = root / 'original.json'
            original.write_text('keep', encoding='utf-8')
            alias = root / 'alias.json'
            try:
                alias.symlink_to(original)
            except OSError:
                self.skipTest('Host does not grant symlink creation')
            with self.assertRaises(ValueError):
                sets.save_report({}, alias)
            self.assertEqual(original.read_text(), 'keep')

    def test_independent_distribution_saved_file_cli(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / 'kit.zip'
            package.build_package(ROOT, output)
            installed = root / 'installed'
            with zipfile.ZipFile(output) as z:
                names = z.namelist()
                self.assertFalse(any(n.endswith(('live_workflow.py', 'live-workflow.md')) for n in names))
                self.assertIn('docs/official-path-review.md', names)
                z.extractall(installed)
            xml = '<Ableton><LiveSet><Transport Value="0"/></LiveSet></Ableton>'
            a, b, report = root / 'a.als', root / 'b.als', root / 'diff.json'
            a.write_bytes(gzip.compress(xml.encode()))
            b.write_bytes(gzip.compress(xml.replace('"0"', '"4"').encode()))
            before = (a.read_bytes(), b.read_bytes())
            helper = installed / 'plugins/music-producer-kit/skills/music-producer/scripts/live_set_diff.py'
            cmd = [sys.executable, str(helper), str(a), str(b), '--output', str(report)]
            result = subprocess.run(cmd, cwd=root, capture_output=True, encoding='utf-8', timeout=20)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            data = json.loads(report.read_text(encoding='utf-8'))
            self.assertEqual(data['difference_count'], 1)
            self.assertFalse(data['ui_reopen_proven'])
            self.assertEqual(data['scope_approval'], 'not-automated')
            self.assertEqual(before, (a.read_bytes(), b.read_bytes()))
            second = subprocess.run(cmd, cwd=root, capture_output=True, encoding='utf-8', timeout=20)
            self.assertNotEqual(second.returncode, 0)

    def test_official_route_not_claimed_complete(self):
        manifest = json.loads((PLUGIN / 'plugin.json').read_text(encoding='utf-8'))
        self.assertIn('no current Live production backend', manifest['description'])
        result = package.check()
        self.assertFalse(result['live_verified'])
        self.assertFalse(result['behavior_scenarios_executed'])
        self.assertFalse(result['host_installation_verified'])
        scenarios = json.loads((ROOT / 'evals/scenarios.json').read_text(encoding='utf-8'))
        self.assertEqual(scenarios['execution_status'], 'not-run')
        ids = {s['id'] for s in scenarios['scenarios']}
        self.assertTrue({'official-sdk-not-mcp', 'official-beta-approval'} <= ids)
        for scenario in scenarios['scenarios']:
            self.assertNotIn('existing native ableton_live', ' '.join(scenario['must']))


if __name__ == '__main__':
    unittest.main()
