from pathlib import Path
import json
import shutil
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import check as package


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'repo'
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns('.git', '.venv', '__pycache__', 'dist'))

    def test_valid_package(self):
        result = package.check(self.root)
        self.assertEqual(result['skills'], 1)
        self.assertEqual(result['source_modules'], 41)
        self.assertFalse(result['behavior_scenarios_executed'])

    def test_package_excludes_private_workspace(self):
        private = self.root / 'work'
        private.mkdir()
        (private / 'private.json').write_text('{"secret":"not for release"}')
        (self.root / '.env').write_text('TOKEN=private')
        output = Path(self.tmp.name) / 'package.zip'
        package.build_package(self.root, output)
        with zipfile.ZipFile(output) as z:
            names = z.namelist()
            self.assertIn('.agents/plugins/marketplace.json', names)
            self.assertIn('plugins/music-producer-kit/plugin.json', names)
            self.assertFalse(any('private' in n or n.endswith('.env') for n in names))

    def test_package_is_reproducible(self):
        a, b = Path(self.tmp.name) / 'a.zip', Path(self.tmp.name) / 'b.zip'
        package.build_package(self.root, a)
        package.build_package(self.root, b)
        self.assertEqual(a.read_bytes(), b.read_bytes())

    def test_archive_no_overwrite(self):
        output = Path(self.tmp.name) / 'exists.zip'
        output.write_bytes(b'keep')
        with self.assertRaises(FileExistsError):
            package.build_package(self.root, output)
        self.assertEqual(output.read_bytes(), b'keep')

    def test_broken_reference(self):
        p = self.root / 'plugins/music-producer-kit/skills/music-producer/SKILL.md'
        p.write_text(p.read_text() + '\n[missing](references/missing.md)\n')
        with self.assertRaisesRegex(ValueError, 'Broken link'):
            package.check(self.root)

    def test_escaping_marketplace(self):
        p = self.root / '.agents/plugins/marketplace.json'
        data = json.loads(p.read_text())
        data['plugins'][0]['source']['path'] = '../other-plugin'
        p.write_text(json.dumps(data))
        with self.assertRaises(ValueError):
            package.check(self.root)

    def test_duplicate_discovery(self):
        (self.root / '.agents/skills').mkdir()
        with self.assertRaisesRegex(ValueError, 'obsolete'):
            package.check(self.root)

    def test_path_escape(self):
        with self.assertRaises(ValueError):
            package.within(self.root, self.root.parent / 'outside.txt')

    def test_incomplete_inventory(self):
        p = self.root / 'plugins/music-producer-kit/library/catalog.json'
        data = json.loads(p.read_text(encoding='utf-8'))
        data['sources'][0]['modules'].pop()
        p.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, 'cover'):
            package.check(self.root)

    def test_skill_name_mismatch(self):
        p = self.root / 'plugins/music-producer-kit/skills/music-producer/SKILL.md'
        p.write_text(p.read_text().replace('name: music-producer', 'name: wrong-name', 1))
        with self.assertRaises(ValueError):
            package.check(self.root)


if __name__ == '__main__':
    unittest.main()
