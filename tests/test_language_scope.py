"""Physical retained-source checks, not a hidden production/audit view."""
from pathlib import Path
import inspect
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
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(PLUGIN / 'skills/music-producer/scripts'))
import check as package
import source_library
from source_library import SourceLibrary

EXCLUDED = {'mc-style-chinese-pop', 'lw-mandarin', 'lw-cantonese', 'lw-chinese-style', 'lw-tone-check'}
TOPICS = re.compile(r'mc-style-chinese-pop|lw-(?:mandarin|cantonese|chinese-style|tone-check)|reference-minyue'
                    r'|\b(?:Mandarin|Cantonese|Mandopop|Cantopop|guofeng|minyue|erhu|guzheng|suona)\b'
                    r'|Chinese[- ](?:pop|folk|traditional|style|lyrics?|prosody|language|orchestr|tonal)'
                    r'|中国|中國|中文|普通话|普通話|粤语|粵語|国语|國語|华语|華語|十三辙|倒字|协音|平仄'
                    r'|民乐|民樂|民族管弦|二胡|琵琶|古筝|唢呐|宫商|宫调式|宫系统|五声调式|同一首歌', re.I)


class LanguageScopeTests(unittest.TestCase):
    def test_supported_languages_and_catalog(self):
        library = SourceLibrary()
        self.assertEqual(source_library.PRODUCTION_LANGUAGES, ('ko', 'en', 'ja'))
        self.assertEqual(len(library.list_modules()), 42)
        self.assertEqual(set(library.list_modules()), set(library.modules))
        self.assertTrue(EXCLUDED.isdisjoint(library.modules))

    def test_original_archives_are_physically_absent(self):
        names = {p.name for p in (PLUGIN / 'library/archives').iterdir()}
        self.assertEqual(names, {'composition-selected.zip', 'lyrics-selected.zip'})
        self.assertFalse((ROOT / 'docs/SOURCE_SNAPSHOT_REPORT.json').exists())

    def test_removed_subject_files_not_inside_selected_archives(self):
        library = SourceLibrary()
        for source in library.sources:
            with zipfile.ZipFile(PLUGIN / 'library' / source['archive']) as archive:
                for name in archive.namelist():
                    self.assertFalse(EXCLUDED.intersection(Path(name).parts), name)
                    self.assertNotIn('reference-minyue', name)
                    self.assertNotIn('example-02-fusion', name)
                    self.assertTrue(name in {'LICENSE', 'NOTICE'} or name.startswith(source['skills_directory'] + '/'))

    def test_shared_documents_do_not_retain_designated_subject_content(self):
        library = SourceLibrary()
        for source in library.sources:
            with zipfile.ZipFile(PLUGIN / 'library' / source['archive']) as archive:
                for name in archive.namelist():
                    if name in {'LICENSE', 'NOTICE'}:
                        continue  # Legal credit text is not a production guide.
                    with self.subTest(file=name):
                        self.assertIsNone(TOPICS.search(archive.read(name).decode('utf-8')))

    def test_no_access_bypass_in_reader_api(self):
        self.assertEqual(list(inspect.signature(SourceLibrary).parameters), ['root'])
        self.assertFalse(hasattr(source_library, 'ARCHIVE_ONLY_MODULES'))
        self.assertFalse(hasattr(source_library, 'ARCHIVE_ONLY_FILES'))
        with self.assertRaises(TypeError):
            SourceLibrary(archive_audit=True)

    def test_obsolete_cli_flag_is_removed(self):
        result = subprocess.run([sys.executable, str(Path(source_library.__file__)), '--archive-audit', 'list'],
                                capture_output=True, text=True, encoding='utf-8', timeout=20)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('unrecognized arguments', result.stderr)

    def test_removed_modules_are_unknown_at_every_entrypoint(self):
        library = SourceLibrary()
        for module in EXCLUDED:
            for action in [lambda: library.list_files(module), lambda: library.read(module),
                           lambda: library.outline(module), lambda: library.find(module, 'test')]:
                with self.subTest(module=module), self.assertRaisesRegex(ValueError, 'Unknown local module'):
                    action()

    def test_removed_reference_cannot_be_read_or_searched(self):
        library = SourceLibrary()
        self.assertNotIn('reference-minyue.md', library.list_files('mc-orchestration'))
        with self.assertRaises(ValueError):
            library.read('mc-orchestration', 'reference-minyue.md')
        self.assertEqual(library.find('mc-orchestration', '二胡')['matches'], [])

    def test_general_theory_and_japanese_are_retained(self):
        library = SourceLibrary()
        self.assertTrue(library.find('mc-harmony', 'Locrian', 'reference.md')['matches'])
        self.assertTrue(library.find('mc-harmony', '和弦')['matches'])
        self.assertTrue(library.find('lw-japanese', 'モーラ')['matches'])
        self.assertTrue(library.find('lw-korean', '받침')['matches'])

    def test_report_matches_retained_bytes_and_records_edits(self):
        report = json.loads((ROOT / 'docs/SOURCE_SELECTION_REPORT.json').read_text(encoding='utf-8'))
        verification = SourceLibrary().verify()
        for key in ['modules', 'files', 'bytes']:
            self.assertEqual(verification[key], report[key])
        self.assertFalse(report['original_backups_retained'])
        self.assertFalse(report['history_rewritten'])
        self.assertTrue(all(s['removed_files'] for s in report['sources']))
        self.assertTrue(all(s['edited_files'] for s in report['sources']))
        for source in SourceLibrary().sources:
            self.assertTrue(all('origin_git_blob_sha' in r for r in source['files']))

    def test_distribution_has_only_selected_sources_and_no_network_recovery(self):
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / 'kit.zip'
            with patch('socket.create_connection', side_effect=AssertionError('network forbidden')), \
                 patch('urllib.request.urlopen', side_effect=AssertionError('network forbidden')):
                package.build_package(ROOT, target)
            with zipfile.ZipFile(target) as archive:
                names = archive.namelist()
                inner = {Path(n).name for n in names if n.endswith('.zip')}
                self.assertEqual(inner, {'composition-selected.zip', 'lyrics-selected.zip'})
                self.assertFalse(any('.maintenance/' in n for n in names))
                for language in ['korean', 'english', 'japanese']:
                    self.assertIn(f'plugins/music-producer-kit/skills/music-producer/references/lyrics-{language}.md', names)

    def test_new_language_guides_keep_local_source_locators(self):
        library = SourceLibrary()
        for language in ['korean', 'english', 'japanese']:
            path = PLUGIN / f'skills/music-producer/references/lyrics-{language}.md'
            markers = re.findall(r'`source:([a-z0-9-]+)/([A-Za-z0-9_.-]+):(\d+)-(\d+)`', path.read_text(encoding='utf-8'))
            self.assertTrue(markers)
            for module, filename, start, end in markers:
                result = library.read(module, filename, int(start), int(end) - int(start) + 1)
                self.assertTrue(result['text'].strip())

    def test_language_behavior_scenarios_are_not_claimed_executed(self):
        data = json.loads((ROOT / 'evals/scenarios.json').read_text(encoding='utf-8'))
        self.assertEqual(data['execution_status'], 'not-run')
        self.assertGreaterEqual(len(data['scenarios']), 20)


if __name__ == '__main__':
    unittest.main()
