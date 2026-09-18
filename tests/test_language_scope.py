"""Test production retrieval boundaries, not native diction or LLM compliance."""
from pathlib import Path
import hashlib
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
from source_library import (SourceLibrary, PRODUCTION_LANGUAGES,
                            ARCHIVE_ONLY_MODULES, ARCHIVE_ONLY_FILES)

GUIDES = ('lyrics-korean.md', 'lyrics-english.md', 'lyrics-japanese.md')


class LanguageScopeTests(unittest.TestCase):
    def test_production_languages_are_exact(self):
        self.assertEqual(PRODUCTION_LANGUAGES, ('ko', 'en', 'ja'))
        self.assertEqual(SourceLibrary().verify()['production_languages'], ['ko', 'en', 'ja'])

    def test_default_listing_excludes_only_designated_modules(self):
        library = SourceLibrary()
        self.assertEqual(len(library.modules), 47)
        self.assertEqual(len(library.list_modules()), 42)
        self.assertEqual(set(library.list_modules()), set(library.modules) - ARCHIVE_ONLY_MODULES)
        self.assertTrue({'lw-korean', 'lw-english', 'lw-japanese', 'mc-style-latin', 'mc-style-jazz'} <= set(library.list_modules()))

    def test_excluded_modules_rejected_by_every_production_entrypoint(self):
        library = SourceLibrary()
        with patch.object(library, '_archive', side_effect=AssertionError('excluded archive must not be opened')):
            for module in sorted(ARCHIVE_ONLY_MODULES):
                operations = [lambda m=module: library.list_files(m),
                              lambda m=module: library.read(m),
                              lambda m=module: library.outline(m),
                              lambda m=module: library.find(m, 'a')]
                for index, operation in enumerate(operations):
                    with self.subTest(module=module, operation=index), self.assertRaisesRegex(ValueError, 'excluded'):
                        operation()

    def test_specialist_file_is_hidden_and_direct_reads_are_rejected(self):
        library = SourceLibrary()
        for module, filename in ARCHIVE_ONLY_FILES:
            self.assertNotIn(filename, library.list_files(module))
            for operation in [lambda: library.read(module, filename),
                              lambda: library.outline(module, filename),
                              lambda: library.find(module, 'a', filename)]:
                with self.assertRaisesRegex(ValueError, 'excluded'):
                    operation()

    def test_module_search_does_not_read_hidden_files(self):
        library = SourceLibrary()
        with patch.object(library, '_document', wraps=library._document) as document:
            library.find('mc-orchestration', '民', limit=2)
            consulted = {call.args[1] for call in document.call_args_list}
        self.assertTrue(consulted)
        self.assertNotIn('reference-minyue.md', consulted)

    def test_archive_audit_preserves_complete_read_access(self):
        library = SourceLibrary(archive_audit=True)
        self.assertEqual(len(library.list_modules()), 47)
        for module in sorted(ARCHIVE_ONLY_MODULES):
            with self.subTest(module=module):
                self.assertTrue(library.read(module, lines=1)['archive_audit'])
        for module, filename in ARCHIVE_ONLY_FILES:
            self.assertIn(filename, library.list_files(module))
            self.assertTrue(library.read(module, filename, lines=1)['text'])

    def test_audit_is_explicit_and_does_not_leak_to_a_new_instance(self):
        SourceLibrary(archive_audit=True).read('lw-mandarin', lines=1)
        with self.assertRaisesRegex(ValueError, 'excluded'):
            SourceLibrary().read('lw-mandarin', lines=1)
        for invalid in [1, 'true', None, []]:
            with self.subTest(value=invalid), self.assertRaises(ValueError):
                SourceLibrary(archive_audit=invalid)

    def test_general_chinese_written_theory_is_not_removed(self):
        result = SourceLibrary().read('mc-harmony', lines=80)
        self.assertTrue(any('\u4e00' <= character <= '\u9fff' for character in result['text']))
        self.assertFalse(result['archive_audit'])
        self.assertTrue(SourceLibrary().read('lw-japanese', lines=80)['text'])

    def test_both_views_work_without_network_or_extraction(self):
        before = sorted(p.relative_to(PLUGIN).as_posix() for p in PLUGIN.rglob('*'))
        with patch('socket.create_connection', side_effect=AssertionError('network forbidden')), \
             patch('urllib.request.urlopen', side_effect=AssertionError('network forbidden')):
            self.assertTrue(SourceLibrary().find('lw-english', 'stress')['matches'])
            self.assertTrue(SourceLibrary(archive_audit=True).read('lw-cantonese', lines=1)['text'])
            self.assertEqual(SourceLibrary().verify()['files'], 121)
        after = sorted(p.relative_to(PLUGIN).as_posix() for p in PLUGIN.rglob('*'))
        self.assertEqual(before, after)

    def test_cli_defaults_and_explicit_audit(self):
        script = SKILL / 'scripts/source_library.py'
        for args, size in [(['list'], 42), (['--archive-audit', 'list'], 47)]:
            result = subprocess.run([sys.executable, str(script), *args], capture_output=True,
                                    text=True, encoding='utf-8', timeout=30, check=True)
            self.assertEqual(len(json.loads(result.stdout)), size)
        result = subprocess.run([sys.executable, str(script), 'read', 'lw-mandarin'],
                                capture_output=True, text=True, encoding='utf-8', timeout=30)
        self.assertEqual(result.returncode, 2)
        self.assertIn('excluded', result.stderr)
        self.assertFalse(result.stdout)

    def test_scope_and_language_guides_survive_independent_distribution(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'kit.zip'
            package.build_package(ROOT, output)
            install = Path(directory) / 'installed'
            with zipfile.ZipFile(output) as archive:
                archive.extractall(install)
            plugin = install / package.PLUGIN
            for guide in GUIDES:
                self.assertTrue((plugin / 'skills/music-producer/references' / guide).is_file())
            script = plugin / 'skills/music-producer/scripts/source_library.py'
            spec = importlib.util.spec_from_file_location('installed_scope', script)
            installed = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(installed)
            with patch('socket.create_connection', side_effect=AssertionError('network forbidden')), \
                 patch('urllib.request.urlopen', side_effect=AssertionError('network forbidden')):
                library = installed.SourceLibrary()
                self.assertEqual(len(library.list_modules()), 42)
                self.assertEqual(library.verify()['files'], 121)
                for module in ('lw-korean', 'lw-english', 'lw-japanese'):
                    self.assertTrue(library.read(module, lines=1)['text'])
                with self.assertRaisesRegex(ValueError, 'excluded'):
                    library.read('lw-cantonese')
            self.assertEqual(len(list(plugin.rglob('SKILL.md'))), 1)

    def test_new_guide_evidence_locations_exist(self):
        pattern = r'`source:([a-z0-9-]+)/([A-Za-z0-9_.-]+):(\d+)-(\d+)`'
        for guide in GUIDES:
            text = (SKILL / 'references' / guide).read_text(encoding='utf-8')
            markers = re.findall(pattern, text)
            self.assertTrue(markers, guide)
            for module, filename, first, last in markers:
                first, last = int(first), int(last)
                result = SourceLibrary().read(module, filename, first, last - first + 1)
                self.assertEqual(result['end'], last)

    def test_supported_guides_are_routed_without_old_expansion_promises(self):
        entry = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
        prosody = (SKILL / 'references/prosody.md').read_text(encoding='utf-8')
        for guide in GUIDES:
            self.assertIn(guide, entry)
            self.assertIn(guide, prosody)
        for path in [SKILL / 'references/prosody.md', SKILL / 'references/lyrics.md']:
            text = path.read_text(encoding='utf-8')
            self.assertNotIn('No language is prohibited', text)
            self.assertNotIn('A language absent from this guide is not prohibited', text)
        music = (SKILL / 'references/music.md').read_text(encoding='utf-8')
        self.assertNotIn('mc-style-chinese-pop', music)
        self.assertIn('mc-style-latin', music)

    def test_source_archives_are_byte_unchanged(self):
        expected = {
            'music-composition-skills.zip': '591a1dbea44018f388c62cbcf9eb3df234c26b9a9ffa114f51d22e661fc6d60f',
            'lyric-writing-skills.zip': 'd9464be2e885dafb676723d3d7cc192fb3bba174274bbfb0e372c1dc1a93968f',
        }
        for filename, digest in expected.items():
            data = (PLUGIN / 'library/archives' / filename).read_bytes()
            self.assertEqual(hashlib.sha256(data).hexdigest(), digest)
        self.assertEqual(SourceLibrary().verify()['bytes'], 2512420)

    def test_language_scenarios_are_defined_not_claimed_executed(self):
        data = json.loads((ROOT / 'evals/scenarios.json').read_text(encoding='utf-8'))
        self.assertEqual(data['execution_status'], 'not-run')
        names = {s['id'] for s in data['scenarios']}
        self.assertTrue({'ko-sustain', 'ja-kanji', 'en-melisma', 'mixed-ko-en-ja',
                         'excluded-mandarin', 'excluded-cantonese', 'general-theory-language',
                         'latin-instrumental'} <= names)


if __name__ == '__main__':
    unittest.main()
