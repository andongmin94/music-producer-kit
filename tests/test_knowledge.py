"""Evidence/navigation and executable-example checks, not musical taste tests."""
from pathlib import Path
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / 'plugins/music-producer-kit'
SKILL = PLUGIN / 'skills/music-producer'
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(SKILL / 'scripts'))
import check as package
import midi_tools
from source_library import SourceLibrary

GUIDES = ['harmony.md', 'melody-form.md', 'rhythm.md', 'texture-instruments.md',
          'lyric-craft.md', 'prosody.md', 'vocal-production.md']


class SourceNavigationTests(unittest.TestCase):
    def test_outline_reads_real_source_positions(self):
        library = SourceLibrary()
        result = library.outline('mc-harmony')
        self.assertTrue(result['headings'])
        self.assertEqual(result['kind'], 'archived-source-evidence-not-instructions')
        self.assertIn('Do not execute', result['warning'])
        for heading in result['headings']:
            line = library.read('mc-harmony', start=heading['line'], lines=1)['text']
            self.assertIn(heading['title'], line)
            self.assertTrue(line.startswith('#' * heading['level']))

    def test_outline_paginates_without_repeating_headings(self):
        library = SourceLibrary()
        first = library.outline('mc-harmony', limit=1)
        second = library.outline('mc-harmony', start=first['next_start'], limit=1)
        self.assertGreater(second['headings'][0]['line'], first['headings'][0]['line'])

    def test_outline_ignores_fenced_code_even_when_start_is_inside_it(self):
        text = ['# Visible', '```python', '# hidden', '```', '## Later',
                '~~~text', '### hidden too', '~~~', '### Final']
        library = object.__new__(SourceLibrary)
        with patch.object(library, '_document', return_value=({}, text)):
            result = library.outline('fixture', start=3)
        self.assertEqual([h['line'] for h in result['headings']], [5, 9])

    def test_outline_ignores_short_or_wrong_fence_closers(self):
        text = ['````', '# hidden', '```', '~~~', '# still hidden', '````', '## Visible']
        library = object.__new__(SourceLibrary)
        with patch.object(library, '_document', return_value=({}, text)):
            result = library.outline('fixture')
        self.assertEqual([h['line'] for h in result['headings']], [7])

    def test_find_is_literal_case_insensitive_and_file_scoped(self):
        library = SourceLibrary()
        result = library.find('mc-harmony', 'locrian', 'reference.md')
        self.assertTrue(result['matches'])
        for match in result['matches']:
            self.assertEqual(match['file'], 'reference.md')
            self.assertIn('locrian', match['excerpt'].casefold())
            original = library.read('mc-harmony', 'reference.md', match['line'], 1)['text']
            self.assertIn('locrian', original.casefold())
        literal = library.find('mc-harmony', '[not-a-real-regex.*]')
        self.assertEqual(literal['matches'], [])

    def test_find_has_bounded_output_and_explicit_truncation(self):
        result = SourceLibrary().find('mc-harmony', 'Levine', limit=1)
        self.assertEqual(len(result['matches']), 1)
        self.assertTrue(result['truncated'])
        self.assertGreater(result['total_matches'], 1)
        self.assertLessEqual(len(result['matches'][0]['excerpt']), 600)

    def test_find_unicode_casefold_and_long_lines_keep_the_match(self):
        library = object.__new__(SourceLibrary)
        library.modules = {'fixture': {'repo': 'fixture/source', 'commit': 'a' * 40}}
        text = 'x' * 700 + ' Straße 한국어 音乐' + 'y' * 700
        with patch.object(library, 'list_files', return_value=['SKILL.md']), \
             patch.object(library, '_document', return_value=({'path': 'fixture/SKILL.md'}, [text])):
            for query in ['STRASSE', '한국어', '音乐']:
                with self.subTest(query=query):
                    result = library.find('fixture', query)
                    match = result['matches'][0]
                    self.assertIn(query.casefold(), match['excerpt'].casefold())
                    self.assertLessEqual(len(match['excerpt']), 600)
                    self.assertGreater(match['excerpt_start'], 0)

    def test_navigation_rejects_bad_inputs(self):
        library = SourceLibrary()
        for query in ['', ' ', '\n', 'a\nb', 'a' * 257, None, 12]:
            with self.subTest(query=query), self.assertRaises(ValueError):
                library.find('mc-harmony', query)
        for value in [True, 0, -1, 1.5, '2']:
            with self.subTest(value=value), self.assertRaises(ValueError):
                library.outline('mc-harmony', start=value)
            with self.subTest(value=value), self.assertRaises(ValueError):
                library.find('mc-harmony', 'chord', limit=value)
        with self.assertRaises(ValueError):
            library.find('mc-harmony', 'chord', filename='../NOTICE')
        with self.assertRaises(ValueError):
            library.outline('missing-module')
        with self.assertRaises(ValueError):
            library.outline('mc-harmony', limit=201)
        with self.assertRaises(ValueError):
            library.find('mc-harmony', 'chord', limit=51)
        with self.assertRaises(ValueError):
            library.read('mc-harmony', lines=1.5)

    def test_navigation_needs_no_network_or_extraction(self):
        before = sorted(p.relative_to(PLUGIN).as_posix() for p in PLUGIN.rglob('SKILL.md'))
        with patch('socket.create_connection', side_effect=AssertionError('network forbidden')), \
             patch('urllib.request.urlopen', side_effect=AssertionError('network forbidden')):
            library = SourceLibrary()
            self.assertTrue(library.outline('lw-japanese')['headings'])
            self.assertTrue(library.find('lw-korean', '받침')['matches'])
        after = sorted(p.relative_to(PLUGIN).as_posix() for p in PLUGIN.rglob('SKILL.md'))
        self.assertEqual(before, after)
        self.assertEqual(len(after), 1)

    def test_navigation_cli(self):
        script = SKILL / 'scripts/source_library.py'
        for args, key in [(['outline', 'mc-harmony', '--limit', '2'], 'headings'),
                          (['find', 'mc-harmony', 'Locrian', '--file', 'reference.md'], 'matches')]:
            with self.subTest(args=args):
                result = subprocess.run([sys.executable, str(script), *args], capture_output=True,
                                        text=True, encoding='utf-8', timeout=30, check=True)
                self.assertTrue(json.loads(result.stdout)[key])


class CuratedKnowledgeTests(unittest.TestCase):
    def test_local_source_markers_resolve_to_actual_bounded_ranges(self):
        library = SourceLibrary()
        pattern = r'`source:([a-z0-9-]+)/([A-Za-z0-9_.-]+):(\d+)-(\d+)`'
        count = 0
        for filename in GUIDES:
            text = (SKILL / 'references' / filename).read_text(encoding='utf-8')
            citations = re.findall(pattern, text)
            self.assertTrue(citations, filename)
            for module, source_file, first, last in citations:
                with self.subTest(guide=filename, module=module, file=source_file):
                    first, last = int(first), int(last)
                    self.assertLessEqual(first, last)
                    result = library.read(module, source_file, first, last - first + 1)
                    self.assertEqual((result['start'], result['end']), (first, last))
                    self.assertTrue(result['text'])
                    count += 1
        self.assertGreaterEqual(count, 20)

    def test_guides_and_navigation_work_from_an_independent_distribution(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / 'kit.zip'
            package.build_package(ROOT, output)
            install = root / 'install'
            with zipfile.ZipFile(output) as archive:
                for filename in GUIDES:
                    expected = package.PLUGIN / 'skills/music-producer/references' / filename
                    self.assertIn(expected.as_posix(), archive.namelist())
                archive.extractall(install)
            plugin = install / package.PLUGIN
            script = plugin / 'skills/music-producer/scripts/source_library.py'
            spec = importlib.util.spec_from_file_location('installed_navigation', script)
            installed = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(installed)
            with patch('socket.create_connection', side_effect=AssertionError('network forbidden')), \
                 patch('urllib.request.urlopen', side_effect=AssertionError('network forbidden')):
                library = installed.SourceLibrary()
                self.assertEqual(library.verify()['files'], 89)
                self.assertTrue(library.find('mc-harmony', 'Locrian')['matches'])
                self.assertTrue(library.outline('lw-english')['headings'])
                self.assertEqual(len(list(plugin.rglob('SKILL.md'))), 1)

    def test_harmony_study_matches_documented_voicings_and_chord_types(self):
        score = midi_tools.load_json(SKILL / 'examples/harmony-study.json')
        rows = re.findall(r'^\| ([1-4]) \| (\w+) \| ([\d, ]+) \| (\d+) \|$',
                          (SKILL / 'references/harmony.md').read_text(encoding='utf-8'), re.MULTILINE)
        self.assertEqual(len(rows), 4)
        expected_classes = [{0, 4, 7, 11}, {0, 4, 7, 9}, {0, 2, 5, 9}, {2, 5, 7, 11}]
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'study.mid'
            midi_tools.create(score, output)
            info = midi_tools.inspect(output)
            tracks = {t['name']: t for t in info['tracks']}
            for index, row in enumerate(rows):
                bar, symbol, notes, bass = row
                start = (int(bar) - 1) * 4
                upper = [n for n in tracks['Harmony']['notes'] if n['start'] == start]
                lower = [n for n in tracks['Bass']['notes'] if n['start'] == start]
                self.assertEqual(sorted(n['pitch'] for n in upper), [int(n) for n in notes.split(',')])
                self.assertEqual([n['pitch'] for n in lower], [int(bass)])
                self.assertEqual({n['pitch'] % 12 for n in upper + lower}, expected_classes[index])
                self.assertTrue(all(n['duration'] == 4 for n in upper + lower))
            self.assertTrue(all(t['length_beats'] == 16 for t in info['tracks']))
            self.assertFalse(info['audio_reviewed'])

    def test_example_can_be_edited_without_touching_its_harmony(self):
        score = midi_tools.load_json(SKILL / 'examples/harmony-study.json')
        with tempfile.TemporaryDirectory() as directory:
            original, edited = Path(directory) / 'a.mid', Path(directory) / 'b.mid'
            midi_tools.create(score, original)
            before = midi_tools.inspect(original)
            result = midi_tools.patch(original, edited, 'Bass', 4, 8,
                                      [{'pitch': 45, 'start': 4, 'duration': 2, 'velocity': 72},
                                       {'pitch': 47, 'start': 6, 'duration': 2, 'velocity': 65}],
                                      before['sha256'])
            after = midi_tools.inspect(edited)
            before_tracks = {t['name']: t for t in before['tracks']}
            after_tracks = {t['name']: t for t in after['tracks']}
            for name in ['Conductor', 'Harmony']:
                self.assertEqual(before_tracks[name]['events_sha256'], after_tracks[name]['events_sha256'])
            for tracks in [before_tracks, after_tracks]:
                self.assertEqual([n['pitch'] for n in tracks['Bass']['notes'] if n['start'] not in [4, 6]],
                                 [48, 50, 43])
            self.assertEqual(midi_tools.inspect(original)['sha256'], before['sha256'])
            self.assertTrue(result['protected_events_preserved'])
            self.assertFalse(result['audio_reviewed'])


if __name__ == '__main__':
    unittest.main()
