"""Saved-file checks; not a Live connection or a model evaluation."""
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
SKILL = ROOT / 'plugins/music-producer-kit/skills/music-producer'
sys.path.insert(0, str(SKILL / 'scripts'))
sys.path.insert(0, str(ROOT / 'tools'))
import live_set_diff as sets
import check as package

class SetDiffTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.xml = '<Ableton><LiveSet><Tracks><MidiTrack Id="1"><Notes><MidiNoteEvent Key="45" Duration="4"/></Notes><Automation Value="0.3"/></MidiTrack></Tracks><Transport Value="0"/></LiveSet></Ableton>'
        self.a = self.write('a.als', self.xml)

    def write(self, name, xml):
        path = self.root / name
        path.write_bytes(gzip.compress(xml.encode('utf-8')))
        return path

    def test_identical_and_all_fields_including_automation_are_observed(self):
        b = self.write('b.als', self.xml)
        self.assertTrue(sets.compare(self.a, b)['xml_equivalent'])
        b = self.write('b.als', self.xml.replace('Key="45"', 'Key="52"').replace('Value="0.3"', 'Value="0.5"'))
        result = sets.compare(self.a, b)
        self.assertEqual(result['difference_count'], 2)
        self.assertFalse(result['ui_reopen_proven'])
        self.assertTrue(any('/Automation' in d['path'] for d in result['differences']))

    def test_ids_and_cursor_not_silently_ignored(self):
        b = self.write('b.als', self.xml.replace('Id="1"','Id="2"').replace('Transport Value="0"','Transport Value="4"'))
        self.assertEqual(sets.compare(self.a, b)['difference_count'], 2)

    def test_truncation_and_added_subtree_explicit(self):
        b = self.write('b.als', self.xml.replace('</Notes>', '<MidiNoteEvent Key="52"/></Notes>').replace('Transport Value="0"','Transport Value="4"'))
        r = sets.compare(self.a, b, 1)
        self.assertTrue(r['truncated']); self.assertGreater(r['difference_count'], 1)

    def test_malformed_other_format_dtd_and_budget_rejected(self):
        for xml in ['<not-live/>', '<Ableton>', '<!DOCTYPE Ableton [<!ENTITY x "bad">]><Ableton><LiveSet/></Ableton>']:
            with self.subTest(xml=xml), self.assertRaises((ValueError, sets.ET.ParseError)):
                sets.read_set(self.write('bad.als', xml))
        with patch.object(sets, 'MAX_BYTES', 10), self.assertRaises(ValueError): sets.read_set(self.a)
        with patch.object(sets, 'MAX_NODES', 2), self.assertRaises(ValueError): sets.read_set(self.a)

    def test_does_not_modify_sources(self):
        b = self.write('b.als', self.xml.replace('Key="45"','Key="52"'))
        old = (self.a.read_bytes(), b.read_bytes()); sets.compare(self.a,b)
        self.assertEqual(old, (self.a.read_bytes(), b.read_bytes()))


if __name__ == '__main__': unittest.main()
