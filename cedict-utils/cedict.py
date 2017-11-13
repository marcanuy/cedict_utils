#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Parser class for cedict Chinese-English dictionary files
"""

import os
import io
import logging


class CedictParser:
    """Parser class. Reads a cedict file and return a list of 
    CedictEntry instances with each line processed.
    """


    filters = ['_filter_comments',
               '_filter_new_lines',
               '_filter_empty_entries']

    def __init__(self, **kwargs):

        self.lines = kwargs.get('lines', [])
        self.file_path = kwargs.get('file_path')
        self.lines_count = kwargs.get('lines_count', None)
        if kwargs.get('file_path'):
            self.read_file()
        else:
            self.file_path = "data/cedict_ts.u8"

    def read_file(self):
        """Import the cedict file sanitizing each entry
        """
        __location__ = os.path.realpath(
            os.path.join(os.getcwd(), os.path.dirname(__file__)))
        with io.open(os.path.join(__location__, self.file_path), "r",
                     encoding='utf-8') as file_handler:
            if self.lines_count:
                logging.info("Loaded %s lines of the dictionary", self.lines_count)
            self.lines = file_handler.readlines()
            self._sanitize()

    def _sanitize(self):
        from operator import methodcaller
        #f = methodcaller('_filter_comments')
        # f(b) returns b._filter_comments().
        for fun in self.filters:
            caller = methodcaller(fun)
            caller(self)

    def _filter_comments(self):
        """ remove lines starting with # or #! """
        self.lines = [line for line in self.lines
                      if not line.startswith(("#", "#!"))]

    def _filter_new_lines(self):
        self.lines = [line.strip('\n') for line in self.lines]

    def _filter_empty_entries(self):
        self.lines = [line for line in self.lines if line.strip()]

    def parse(self):
        """ Parse Cedict lines and return a list of CedictEntry items """
        result = []
        for line in self.lines[:self.lines_count]:
            entry = CedictEntry.make(line)
            result.append(entry)
        return result


class CedictEntry: # pylint: disable=too-few-public-methods
    """A representation of a cedict entry

    Keyword arguments:
    traditional -- entry in traditional hanzi
    simplified -- entry in simplified hanzi
    pinyin -- entry pronunciation with tone numbers
    meanings -- list of different meanings for an entry
    raw_line -- the original full line
    """

    def __init__(self, **kwargs):
        self.traditional = kwargs.get('traditional', '')
        self.simplified = kwargs.get('simplified', '')
        self.pinyin = kwargs.get('pinyin', '')
        self.meanings = kwargs.get('meanings', '')
        self.raw_line = kwargs.get('raw_line', '')

    @classmethod
    def make(cls, line):
        """ Generates an entry from a Cedict file line data """
        hanzis = line.partition('[')[0].split(' ', 1)
        keywords = dict(
            meanings=line.partition('/')[2].replace("\"", "'").rstrip("/").strip().split("/"),
            traditional=hanzis[0].strip(" "),
            simplified=hanzis[1].strip(" "),
            # Take the content in between the two brackets
            pinyin=line.partition('[')[2].partition(']')[0],
            raw_line=line
        )
        return cls(**keywords)
