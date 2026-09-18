from pathlib import Path
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'plugins/music-producer-kit/skills/music-producer/scripts'))
import sample_library as samples


class SampleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'samples'
        self.root.mkdir()
        self.write('Drums/Kick Bright.wav', b'fixture only, not an audio recording')
        self.write('Drums/kick tight.FLAC', b'different fixture')
        self.write('Drums/snare.aiff', b'snare fixture')
        self.write('ピアノ/夜のコード.wav', b'keys fixture')
        self.write('타악기/부드러운 킥.wav', b'kick fixture')
        self.write('not-a-sample.txt', b'private')

    def write(self, name, data):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def test_filename_search_and_hash(self):
        result = samples.find_samples(self.root, 'DRUMS kick')
        self.assertEqual(len(result['matches']), 2)
        for item in result['matches']:
            self.assertEqual(item['sha256'], hashlib.sha256((self.root / item['path']).read_bytes()).hexdigest())
            self.assertEqual(item['bytes'], (self.root / item['path']).stat().st_size)
        self.assertFalse(result['audio_analyzed'])
        self.assertFalse(result['license_verified'])
        self.assertTrue(result['scan_complete'])

    def test_unicode_and_literal_query(self):
        self.assertEqual(len(samples.find_samples(self.root, '夜')['matches']), 1)
        self.assertEqual(len(samples.find_samples(self.root, '킥')['matches']), 1)
        self.assertEqual(samples.find_samples(self.root, '*')['matches'], [])

    def test_limit_is_explicit_and_deterministic(self):
        first = samples.find_samples(self.root, '', 2)
        self.assertEqual(first, samples.find_samples(self.root, '', 2))
        self.assertEqual(len(first['matches']), 2)
        self.assertEqual(first['matched_in_visited_files'], 5)
        self.assertTrue(first['truncated'])

    def test_no_network_or_writes(self):
        before = sorted(p.relative_to(self.root).as_posix() for p in self.root.rglob('*'))
        with patch('socket.create_connection', side_effect=AssertionError('network forbidden')), \
             patch('urllib.request.urlopen', side_effect=AssertionError('network forbidden')):
            result = samples.find_samples(self.root, 'kick')
        self.assertFalse(result['network_used'])
        self.assertEqual(before, sorted(p.relative_to(self.root).as_posix() for p in self.root.rglob('*')))
        self.assertNotIn(str(self.root), json.dumps(result))

    def test_no_matches_is_not_error(self):
        result = samples.find_samples(self.root, 'not present')
        self.assertEqual(result['matches'], [])
        self.assertTrue(result['scan_complete'])

    def test_argument_validation(self):
        for limit in [0, -1, True, 1.5, 101, '3']:
            with self.subTest(limit=limit), self.assertRaises(ValueError):
                samples.find_samples(self.root, limit=limit)
        for query in [None, 'x' * 257, '\n', '\0']:
            with self.subTest(query=query), self.assertRaises(ValueError):
                samples.find_samples(self.root, query)
        with self.assertRaises(ValueError):
            samples.find_samples(self.root / 'missing')
        with self.assertRaises(ValueError):
            samples.find_samples(self.root / 'Drums/Kick Bright.wav')

    def test_scan_budget_is_reported(self):
        with patch.object(samples, 'MAX_FILES', 2):
            result = samples.find_samples(self.root)
        self.assertEqual(result['files_visited'], 2)
        self.assertFalse(result['scan_complete'])
        self.assertTrue(result['truncated'])

    def test_large_file_does_not_trigger_unbounded_hashing(self):
        with patch.object(samples, 'MAX_HASH_BYTES', 1):
            result = samples.find_samples(self.root, 'snare')
        item = result['matches'][0]
        self.assertIsNone(item['sha256'])
        self.assertEqual(item['hash_status'], 'skipped-size-limit')

    def test_read_error_is_reported_not_claimed_missing(self):
        original = Path.open
        def failure(path, *args, **kwargs):
            if path.suffix == '.aiff':
                raise PermissionError('fixture')
            return original(path, *args, **kwargs)
        with patch.object(Path, 'open', failure):
            result = samples.find_samples(self.root, 'snare')
        self.assertFalse(result['scan_complete'])
        self.assertEqual(result['matches'], [])
        self.assertEqual(result['warnings'][0]['error'], 'PermissionError')

    def test_changed_file_is_not_given_a_stable_hash(self):
        original = hashlib.file_digest
        target = self.root / 'Drums/snare.aiff'
        def changed(stream, *args, **kwargs):
            result = original(stream, *args, **kwargs)
            target.write_bytes(b'changed while reading')
            return result
        with patch.object(hashlib, 'file_digest', changed):
            result = samples.find_samples(self.root, 'snare')
        self.assertEqual(result['matches'], [])
        self.assertFalse(result['scan_complete'])

    def test_symlinks_are_not_followed(self):
        outside = Path(self.temp.name) / 'outside'
        outside.mkdir()
        (outside / 'secret.wav').write_bytes(b'never read')
        try:
            (self.root / 'link').symlink_to(outside, target_is_directory=True)
            (self.root / 'alias.wav').symlink_to(outside / 'secret.wav')
        except OSError:
            self.skipTest('Creating symlinks is not permitted on this host')
        result = samples.find_samples(self.root)
        self.assertFalse(any('secret' in m['path'] or 'alias' in m['path'] for m in result['matches']))
        with self.assertRaises(ValueError):
            samples.find_samples(self.root / 'link')

    def test_cli(self):
        result = subprocess.run([sys.executable, str(Path(samples.__file__)), str(self.root), '--query', 'kick'],
                                capture_output=True, text=True, encoding='utf-8', timeout=20, check=True)
        self.assertEqual(len(json.loads(result.stdout)['matches']), 2)


if __name__ == '__main__':
    unittest.main()
