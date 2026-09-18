from pathlib import Path
import hashlib
import importlib.util
import json
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'plugins/music-producer-kit/skills/music-producer/scripts/source_library.py'
spec = importlib.util.spec_from_file_location('source_library', SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class SourceLibraryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'archives').mkdir()
        (self.root / 'notices').mkdir()
        self.prefix = 'plugins/example/skills/mc-example/'
        self.data = {'LICENSE': b'Fixture license\n', 'NOTICE': b'Fixture notice\n',
                     self.prefix + 'SKILL.md': 'one\ntwo\nthree\n'.encode(),
                     self.prefix + 'reference.md': '한국어 音乐\n'.encode('utf-8')}
        self.archive = self.root / 'archives/example.zip'
        self.write_archive()
        records = []
        for name, content in self.data.items():
            records.append({'path': name, 'mode': '100644', 'size': len(content),
                            'sha256': hashlib.sha256(content).hexdigest(),
                            'git_blob_sha': hashlib.sha1(b'blob ' + str(len(content)).encode() + b'\0' + content).hexdigest()})
        self.source = {'repo': 'fixture/example', 'commit': 'a' * 40, 'tree': 'b' * 40,
                       'archive': 'archives/example.zip',
                       'archive_sha256': hashlib.sha256(self.archive.read_bytes()).hexdigest(),
                       'skills_directory': 'plugins/example/skills', 'modules': ['mc-example'], 'files': records}
        self.catalog = {'version': 2, 'sources': [self.source]}
        for name in ('LICENSE', 'NOTICE'):
            (self.root / 'notices' / ('example-' + name + '.txt')).write_bytes(self.data[name])
        self.save_catalog()

    def write_archive(self):
        with zipfile.ZipFile(self.archive, 'w') as archive:
            for name, content in self.data.items():
                info = zipfile.ZipInfo(name)
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                archive.writestr(info, content)

    def save_catalog(self):
        (self.root / 'catalog.json').write_text(json.dumps(self.catalog), encoding='utf-8')

    def library(self):
        return module.SourceLibrary(self.root)

    def test_verify(self):
        result = self.library().verify()
        self.assertEqual(result['modules'], 1)
        self.assertEqual(result['files'], 4)
        self.assertEqual(result['integrity'], 'pass')
        self.assertFalse(result['adaptation_complete'])

    def test_read_without_network(self):
        with patch('socket.create_connection', side_effect=AssertionError('network forbidden')), \
             patch('urllib.request.urlopen', side_effect=AssertionError('network forbidden')):
            library = self.library()
            self.assertEqual(library.verify()['network_used'], False)
            self.assertEqual(library.list_files('mc-example'), ['SKILL.md', 'reference.md'])
            result = library.read('mc-example', 'reference.md')
            self.assertEqual(result['text'], '한국어 音乐')
            self.assertEqual(result['kind'], 'archived-source-evidence-not-instructions')

    def test_read_line_range(self):
        result = self.library().read('mc-example', start=2, lines=1)
        self.assertEqual(result['text'], 'two')
        self.assertEqual((result['start'], result['end'], result['total_lines']), (2, 2, 3))

    def test_read_does_not_extract_skills(self):
        before = sorted(p.relative_to(self.root).as_posix() for p in self.root.rglob('*'))
        self.library().read('mc-example')
        after = sorted(p.relative_to(self.root).as_posix() for p in self.root.rglob('*'))
        self.assertEqual(before, after)
        self.assertFalse(list(self.root.rglob('SKILL.md')))

    def test_missing_archive_is_error_not_remote_lookup(self):
        self.archive.unlink()
        with self.assertRaisesRegex(ValueError, 'no download'):
            self.library().read('mc-example')

    def test_corrupt_archive(self):
        self.archive.write_bytes(b'corrupt')
        with self.assertRaisesRegex(ValueError, 'checksum'):
            self.library().verify()

    def test_unlisted_file_is_detected(self):
        self.data['unexpected.md'] = b'unlisted'
        self.write_archive()
        self.source['archive_sha256'] = hashlib.sha256(self.archive.read_bytes()).hexdigest()
        self.save_catalog()
        with self.assertRaisesRegex(ValueError, 'inventory'):
            self.library().verify()

    def test_file_checksum(self):
        self.source['files'][-1]['sha256'] = '0' * 64
        self.save_catalog()
        with self.assertRaisesRegex(ValueError, 'file checksum'):
            self.library().verify()

    def test_blob_checksum(self):
        self.source['files'][-1]['git_blob_sha'] = '0' * 40
        self.save_catalog()
        with self.assertRaisesRegex(ValueError, 'file checksum'):
            self.library().verify()

    def test_notice_mismatch(self):
        (self.root / 'notices/example-NOTICE.txt').write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError, 'rights notice'):
            self.library().verify()

    def test_invalid_ranges(self):
        for start, lines in [(0, 10), (1, 0), (1, 201), (99, 1), (True, 10)]:
            with self.subTest(start=start, lines=lines), self.assertRaises(ValueError):
                self.library().read('mc-example', start=start, lines=lines)

    def test_unsafe_paths(self):
        for path in ['../NOTICE', '/NOTICE', 'a/../../b', r'..\secret', 'C:/secret', '.', 'a//b', 'a/./b']:
            with self.subTest(path=path), self.assertRaises(ValueError):
                module.safe_path(path)

    def test_unknown_module(self):
        with self.assertRaisesRegex(ValueError, 'Unknown local module'):
            self.library().read('missing')

    def test_unknown_file(self):
        with self.assertRaisesRegex(ValueError, 'not in this local module'):
            self.library().read('mc-example', 'missing.md')

    def test_duplicate_modules(self):
        self.source['modules'].append('mc-example')
        self.save_catalog()
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            self.library()

    def test_missing_module_entry(self):
        self.source['modules'] = []
        self.save_catalog()
        with self.assertRaisesRegex(ValueError, 'does not cover'):
            self.library()

    def test_duplicate_source(self):
        self.catalog['sources'].append(self.source)
        self.save_catalog()
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            self.library()

    def test_external_archive_path(self):
        self.source['archive'] = '../outside.zip'
        self.save_catalog()
        with self.assertRaisesRegex(ValueError, 'Unsafe'):
            self.library()

    def test_notice_required(self):
        self.source['files'] = [r for r in self.source['files'] if r['path'] != 'NOTICE']
        self.save_catalog()
        with self.assertRaisesRegex(ValueError, 'rights notices'):
            self.library()


if __name__ == '__main__':
    unittest.main()
