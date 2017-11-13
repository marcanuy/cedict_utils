#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CedictParser and CedictEntry unit tests
"""

import unittest
from cedict_utils.cedict import CedictParser, CedictEntry


class TestCedictParser(unittest.TestCase):
    """Main parser test case
    """
    def test_remove_lines_with_comments(self):
        an_entry = 'K書 K书 [K shu1] /to cram (Taiwan,khè su 齧書, lit./ 啃書|啃书[ken3 shu1]/\n'
        lines = ['# CC-CEDICT\n', '# Community Chinese-English dictionary.\n',
                 '# \n',
                 '# Creative Commons Attribution-Share Alike 3.0\n',
                 '#! publisher=MDBG\n',
                 an_entry]
        parser = CedictParser(lines=lines)
        
        parser._filter_comments()

        self.assertEqual(len(parser.lines), 1)
        self.assertEqual(an_entry, parser.lines[0])

    def test_remove_new_lines(self):
        original_lines = ['# CC-CEDICT\n', '# Community Chinese-English dictionary.\n',
                 '# \n',
                 '#! publisher=MDBG\n',
                 'K書 K书 [K shu1] /to cram (Taiwan,khè su 齧書, lit./ 啃書|啃书[ken3 shu1]/\n']
        expected_lines = ['# CC-CEDICT', '# Community Chinese-English dictionary.',
                          '# ',
                          '#! publisher=MDBG',
                          'K書 K书 [K shu1] /to cram (Taiwan,khè su 齧書, lit./ 啃書|啃书[ken3 shu1]/']
        parser = CedictParser(lines=original_lines)
        
        parser._filter_new_lines()

        self.assertCountEqual(parser.lines, expected_lines)

    def test_remove_empty_lines(self):
        original_lines = [' ',
                          '',
                          '# \n',
                          '#! publisher=MDBG\n',
                          '\n',
                          'K書 K书 [K shu1] /to cram (Taiwan,khè su 齧書, lit./ 啃書|啃书[ken3 shu1]/\n']
        expected_lines = ['# \n',
                          '#! publisher=MDBG\n',
                          'K書 K书 [K shu1] /to cram (Taiwan,khè su 齧書, lit./ 啃書|啃书[ken3 shu1]/\n']
        parser = CedictParser(lines=original_lines)

        parser._filter_empty_entries()

        self.assertCountEqual(parser.lines, expected_lines)

    def test_sanitize_lines(self):
        """ Test if all filters are being applied """
        original_lines = [' ',
                          '',
                          '# \n',
                          '#! publisher=MDBG\n',
                          '\n',
                          'K書 K书 [K shu1] /to cram (Taiwan,khè su 齧書, lit./ 啃書|啃书[ken3 shu1]/\n']
        expected_lines = ['K書 K书 [K shu1] /to cram (Taiwan,khè su 齧書, lit./ 啃書|啃书[ken3 shu1]/']
        parser = CedictParser(lines=original_lines)

        parser._sanitize()

        self.assertCountEqual(parser.lines, expected_lines)
        

    def test_parse_entry(self):
        lines = ['K書 K书 [K shu1] /to cram (Taiwan,khè su 齧書, lit./ 啃書|啃书[ken3 shu1]/\n']
        parser = CedictParser(lines=lines)
        
        entries = parser.parse()

        self.assertTrue(type(entries[0]), CedictEntry)

class TestCedictEntry(unittest.TestCase):
    """CedictEntry test case
    """

    def test_make_entry_from_cedict_line(self):
        line = 'K書 K书 [K shu1] /to cram (Taiwan,khè su 齧書, lit./ 啃書|啃书[ken3 shu1]/'
        traditional = 'K書'
        simplified = 'K书'
        pinyin = 'K shu1'
        meanings = ['to cram (Taiwan,khè su 齧書, lit.',
                    ' 啃書|啃书[ken3 shu1]']

        entry = CedictEntry.make(line)

        self.assertTrue(type(entry), CedictEntry)
        self.assertEqual(traditional, entry.traditional)
        self.assertEqual(simplified, entry.simplified)
        self.assertEqual(pinyin, entry.pinyin)
        self.assertEqual(meanings, entry.meanings)

    def test_make_entry_from_cedict_line_one_meaning(self):
        line = 'K書 K书 [K shu1] /啃書|啃书[ken3 shu1]/'
        meanings = ['啃書|啃书[ken3 shu1]']

        entry = CedictEntry.make(line)

        self.assertEqual(meanings, entry.meanings)

    def test_make_entry_from_cedict_line_replaces_double_in_quotes_in_meaning(self):
        line = 'K書 K书 [K shu1] /啃"h "u1/'
        meanings = ["啃'h 'u1"]

        entry = CedictEntry.make(line)

        self.assertEqual(meanings, entry.meanings)


    # def test_expand_abbreviations(self):
    #     meaning = "this abbr. and fig. humble expr. Tw."
    #     expected = "this abbreviation and metaphorically " \
    #                "humble expression used in Taiwan"

    #     result = expand_abbreviations(meaning)

    #     self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
