from pathlib import Path
import importlib.util
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import check as package
from source_library import SourceLibrary


class OfflineDistributionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'repo'
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns('.git', '.venv', '__pycache__', 'dist'))
        self.plugin = self.root / package.PLUGIN

    def test_distribution_is_independent_of_checkout_and_network(self):
        output = Path(self.temp.name) / 'package.zip'
        package.build_package(self.root, output)
        install = Path(self.temp.name) / 'installed'
        with zipfile.ZipFile(output) as archive:
            for name in package.ARCHIVES:
                self.assertIn((package.PLUGIN / 'library/archives' / name).as_posix(), archive.namelist())
            archive.extractall(install)
        shutil.rmtree(self.root)
        plugin = install / package.PLUGIN
        script = plugin / 'skills/music-producer/scripts/source_library.py'
        spec = importlib.util.spec_from_file_location('installed_source_library', script)
        installed = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(installed)
        with patch('socket.create_connection', side_effect=AssertionError('network forbidden')), \
             patch('urllib.request.urlopen', side_effect=AssertionError('network forbidden')):
            library = installed.SourceLibrary()
            self.assertEqual(library.verify()['modules'], 47)
            self.assertTrue(library.read('mc-harmony', 'reference.md', lines=5)['text'])
            self.assertTrue(library.read('lw-korean', lines=5)['text'])

    def test_missing_archive_fails_package(self):
        self.assertEqual(package.check(self.root)['status'], 'pass')
        (self.plugin / 'library/archives/music-composition-skills.zip').unlink()
        with patch('socket.create_connection', side_effect=AssertionError('network forbidden')), \
             patch('urllib.request.urlopen', side_effect=AssertionError('network forbidden')):
            with self.assertRaises(ValueError):
                package.check(self.root)

    def test_unknown_zip_not_packaged(self):
        extra = self.plugin / 'library/archives/private-samples.zip'
        extra.write_bytes(b'private')
        self.assertNotIn(extra, package.package_files(self.root))

    def test_every_module_and_reference_has_a_local_file(self):
        library = SourceLibrary(self.plugin / 'library')
        library.verify()
        for module in sorted(library.modules):
            with self.subTest(module=module):
                self.assertIn('SKILL.md', library.list_files(module))
                for filename in library.list_files(module):
                    result = library.read(module, filename, lines=1)
                    self.assertEqual(result['source'], library.modules[module]['repo'])

    def test_complete_snapshot_counts(self):
        result = package.check(self.root)['local_source_library']
        self.assertEqual((result['sources'], result['modules'], result['files']), (2, 47, 121))
        self.assertEqual(result['bytes'], 2512420)

    def test_archived_skill_files_are_not_discoverable(self):
        self.assertEqual(len(list(self.plugin.rglob('SKILL.md'))), 1)


if __name__ == '__main__':
    unittest.main()
