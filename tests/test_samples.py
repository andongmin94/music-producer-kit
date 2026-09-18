"""Local sample inspection with generated audio fixtures, not listening or rights checks."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import soundfile as sf

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / 'plugins/music-producer-kit/skills/music-producer/scripts'
sys.path.insert(0, str(SCRIPTS))
import sample_library as samples


class SampleTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / 'samples'
        self.root.mkdir()
        sf.write(self.root / 'Kick_한글_120_C.wav', [[0.0, 0.25]] * 800, 8000, subtype='PCM_16')
        sf.write(self.root / '声_float.wav', [0.125] * 1600, 8000, subtype='FLOAT')
        sf.write(self.root / 'bass.flac', [0.0] * 400, 8000)
        sf.write(self.root / 'hat.aiff', [0.0] * 100, 8000)
        (self.root / 'bad.wav').write_bytes(b'not a wave')
        (self.root / 'not-a-sample.txt').write_text('ignored')

    def test_real_headers_in_multiple_formats(self):
        result = samples.scan(self.root)
        rows = {e['path']: e for e in result['entries']}
        self.assertEqual(len(rows), 4)
        kick = rows['Kick_한글_120_C.wav']
        self.assertEqual((kick['channels'], kick['frames'], kick['sample_rate']), (2, 800, 8000))
        self.assertAlmostEqual(kick['duration_seconds'], 0.1)
        self.assertEqual(rows['声_float.wav']['subtype'], 'FLOAT')
        self.assertEqual(rows['bass.flac']['format'], 'FLAC')
        self.assertIsNone(kick['bpm'])
        self.assertIsNone(kick['key'])
        self.assertEqual(kick['license'], 'not-verified')
        self.assertFalse(result['audio_reviewed'])
        self.assertEqual(result['issues'], [{'path': 'bad.wav', 'reason': 'unreadable-or-unsupported-audio'}])

    def test_read_only_and_no_network(self):
        before = {p.name: p.read_bytes() for p in self.root.iterdir()}
        with patch('socket.create_connection', side_effect=AssertionError('network')), \
             patch('urllib.request.urlopen', side_effect=AssertionError('network')), \
             patch.object(sf, 'read', side_effect=AssertionError('no waveform decoding')):
            samples.scan(self.root)
            result = samples.inspect(self.root, 'bass.flac')
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.root.iterdir()})
        self.assertEqual(result['entry']['sha256'], hashlib.sha256(before['bass.flac']).hexdigest())

    def test_filename_search_is_literal_and_not_audition(self):
        catalog = samples.scan(self.root)
        result = samples.find(catalog, 'KICK 한글')
        self.assertEqual(len(result['matches']), 1)
        self.assertFalse(result['current_files_rechecked'])
        self.assertFalse(result['audio_reviewed'])
        self.assertEqual(samples.find(catalog, '.*')['matches'], [])

    def test_bound_and_report_creation(self):
        result = samples.scan(self.root, limit=1)
        self.assertEqual(result['examined_files'], 1)
        self.assertTrue(result['truncated'])
        output = Path(self.tmp.name) / 'inventory.json'
        samples.save(result, output)
        self.assertEqual(json.loads(output.read_text(encoding='utf-8')), result)
        with self.assertRaises(FileExistsError): samples.save(result, output)
        with self.assertRaises(ValueError): samples.save(result, self.root / 'index.json')

    def test_outside_paths_and_missing_files_rejected(self):
        for name in ['../secret.wav', '/secret.wav', 'C:/secret.wav', 'a/./b.wav', r'a\b.wav']:
            with self.subTest(name=name), self.assertRaises(ValueError): samples.inspect(self.root, name)
        with self.assertRaises(OSError): samples.inspect(self.root, 'missing.wav')

    def test_links_are_not_followed(self):
        link = self.root / 'alias.wav'
        try: link.symlink_to(self.root / 'bass.flac')
        except OSError: self.skipTest('This runner does not allow symbolic-link creation')
        result = samples.scan(self.root)
        self.assertNotIn('alias.wav', [e['path'] for e in result['entries']])
        with self.assertRaises(ValueError): samples.inspect(self.root, 'alias.wav')

    def test_no_language_classification_from_file_script(self):
        result = samples.scan(self.root)
        self.assertIn('声_float.wav', [e['path'] for e in result['entries']])
        self.assertIn('Kick_한글_120_C.wav', [e['path'] for e in result['entries']])

    def test_arguments_and_changed_file(self):
        for value in [True, 0, -1, 10001, '2']:
            with self.subTest(value=value), self.assertRaises(ValueError): samples.scan(self.root, value)
        for value in ['', ' ', None, 'x' * 257]:
            with self.subTest(query=value), self.assertRaises(ValueError): samples.find({'version':1,'entries':[]}, value)
        real_info = sf.info
        def change(path):
            info = real_info(path)
            with open(path, 'ab') as f: f.write(b'changed')
            return info
        with patch.object(sf, 'info', side_effect=change), self.assertRaisesRegex(ValueError, 'changed'):
            samples.inspect(self.root, 'bass.flac')

    def test_cli_scan_find_inspect(self):
        script = SCRIPTS / 'sample_library.py'
        output = Path(self.tmp.name) / 'samples.json'
        def run(*args):
            p = subprocess.run([sys.executable, str(script), *map(str,args)],capture_output=True,encoding='utf-8',timeout=30,check=True)
            return json.loads(p.stdout)
        self.assertEqual(run('scan',self.root,'--output',output)['files'], 4)
        self.assertEqual(len(run('find',output,'kick')['matches']), 1)
        self.assertIn('sha256',run('inspect',self.root,'bass.flac')['entry'])


if __name__ == '__main__': unittest.main()
