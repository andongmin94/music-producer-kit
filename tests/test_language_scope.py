"""Physical source removal; no hidden/audit copy or language detection by script."""
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
from source_library import SourceLibrary, PRODUCTION_LANGUAGES

REMOVED = {'mc-style-chinese-pop', 'lw-mandarin', 'lw-cantonese',
           'lw-chinese-style', 'lw-tone-check', 'lw-case-studies'}
TOPICS = re.compile(r'普通话|粤语|国语|华语|中国风|民族管弦|民乐|十三辙|平仄|倒字|宫商角徵羽|reference-minyue|reference-corpus')
GUIDES = ('lyrics-korean.md', 'lyrics-english.md', 'lyrics-japanese.md')


class LanguageScopeTests(unittest.TestCase):
    def test_languages_and_single_selected_view(self):
        library = SourceLibrary()
        self.assertEqual(PRODUCTION_LANGUAGES, ('ko', 'en', 'ja'))
        self.assertEqual(len(library.modules), 41)
        self.assertEqual(library.list_modules(), sorted(library.modules))
        self.assertFalse(set(library.modules) & REMOVED)
        self.assertFalse(library.verify()['complete_upstream_snapshot'])

    def test_removed_modules_fail_before_opening_any_archive(self):
        library = SourceLibrary()
        with patch.object(library, '_archive', side_effect=AssertionError('must not open')):
            for module in REMOVED:
                for op in [lambda: library.list_files(module), lambda: library.read(module),
                           lambda: library.find(module, 'text'), lambda: library.outline(module)]:
                    with self.subTest(module=module), self.assertRaises(ValueError): op()

    def test_no_audit_api_or_cli(self):
        with self.assertRaises(TypeError): SourceLibrary(archive_audit=True)
        script = SKILL / 'scripts/source_library.py'
        result = subprocess.run([sys.executable, str(script), '--archive-audit', 'list'], capture_output=True, encoding='utf-8', timeout=30)
        self.assertEqual(result.returncode, 2)
        self.assertIn('unrecognized arguments', result.stderr)
        self.assertNotIn('ARCHIVE_ONLY_', script.read_text(encoding='utf-8'))

    def test_removed_content_is_absent_from_archive_bytes_and_catalog(self):
        library = SourceLibrary()
        for source in library.sources:
            with zipfile.ZipFile(library.root / source['archive']) as archive:
                for name in archive.namelist():
                    self.assertFalse(REMOVED & set(name.split('/')), name)
                    self.assertNotIn('reference-minyue', name)
                    self.assertNotIn('reference-corpus', name)
                    if name in {'LICENSE', 'NOTICE'}: continue  # Rights notices are not production material.
                    text = archive.read(name).decode('utf-8')
                    self.assertIsNone(TOPICS.search(text), name)
                    for module in REMOVED: self.assertNotIn(module, text, name)
        self.assertEqual(library.verify()['files'], 89)

    def test_legacy_archives_and_duplicate_inventory_are_gone(self):
        for filename in ['music-composition-skills.zip', 'lyric-writing-skills.zip']:
            self.assertFalse((PLUGIN / 'library/archives' / filename).exists())
        self.assertFalse((ROOT / 'docs/upstream-inventory.json').exists())
        self.assertFalse((ROOT / 'docs/SOURCE_SNAPSHOT_REPORT.json').exists())
        self.assertEqual(SourceLibrary().catalog['version'], 2)

    def test_general_theory_and_all_three_language_sources_survive(self):
        library = SourceLibrary()
        for module in ['mc-harmony','mc-melody','mc-style-latin','mc-style-jazz','lw-korean','lw-english','lw-japanese']:
            self.assertTrue(library.read(module, lines=20)['text'])
        self.assertTrue(library.find('mc-harmony', '和弦')['matches'])
        self.assertTrue(library.find('lw-japanese', 'モーラ')['matches'])

    def test_selection_hashes_and_locators(self):
        library = SourceLibrary()
        self.assertEqual(library.verify()['integrity'], 'pass')
        for source in library.sources:
            edited = [f for f in source['files'] if f.get('editorial_selection')]
            self.assertTrue(edited)
            for record in edited:
                self.assertRegex(record['upstream_git_blob_sha'], '^[a-f0-9]{40}$')
                self.assertRegex(record['upstream_sha256'], '^[a-f0-9]{64}$')
                self.assertTrue(record['retained_original_lines'])
        for guide in GUIDES:
            text = (SKILL / 'references' / guide).read_text(encoding='utf-8')
            matches = re.findall(r'`source:([a-z0-9-]+)/([A-Za-z0-9_.-]+):(\d+)-(\d+)`',text)
            self.assertTrue(matches)
            for module, file, start, end in matches:
                result = library.read(module,file,int(start),int(end)-int(start)+1)
                self.assertEqual(result['end'],int(end))

    def test_independent_distribution_contains_no_old_snapshot(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'kit.zip'
            package.build_package(ROOT, output)
            install = Path(directory) / 'install'
            with zipfile.ZipFile(output) as z:
                self.assertFalse(any(n.endswith('/music-composition-skills.zip') or n.endswith('/lyric-writing-skills.zip') for n in z.namelist()))
                z.extractall(install)
            plugin = install / package.PLUGIN
            spec = importlib.util.spec_from_file_location('selected_installed', plugin / 'skills/music-producer/scripts/source_library.py')
            module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
            with patch('socket.create_connection', side_effect=AssertionError('network')), \
                 patch('urllib.request.urlopen', side_effect=AssertionError('network')):
                library = module.SourceLibrary()
                self.assertEqual(library.verify()['modules'],41)
                self.assertTrue(library.read('lw-korean')['text'])
            self.assertEqual(len(list(plugin.rglob('SKILL.md'))),1)

    def test_model_scenarios_still_not_executed(self):
        scenarios = json.loads((ROOT / 'evals/scenarios.json').read_text(encoding='utf-8'))
        self.assertEqual(scenarios['execution_status'],'not-run')


if __name__ == '__main__': unittest.main()
