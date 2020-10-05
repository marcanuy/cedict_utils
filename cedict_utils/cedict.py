#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Parser class for cedict Chinese-English dictionary files
"""

import os
import os.path
import io
import logging
import pickle

from os import path

BASE_PATH = path.abspath(path.dirname(__file__))
DATA_DIR = os.path.join(BASE_PATH, "data")
CEDICT_PATH = os.path.join(DATA_DIR, "cedict_ts.u8")
DATA_PATH = os.path.join(DATA_DIR, "dump.dat")

class CedictParser:
    """Parser class. Reads a cedict file and return a list of
    CedictEntry instances with each line processed.
    """

    filters = ["_filter_comments", "_filter_new_lines", "_filter_empty_entries"]

    def __init__(self, lines=None, file_path=None, lines_count=None):
        self.lines = lines or []
        self.lines_count = lines_count
        
        if not file_path and os.path.isfile(DATA_PATH):
            self.lines = pickle.load( open( DATA_PATH, "rb" ) )
        elif file_path:
            self.read_file(file_path)
        else:
            self.read_file(file_path=CEDICT_PATH)

    def read_file(self, file_path):
        """Import the cedict file sanitizing each entry"""
        with io.open(
            file_path, "r", encoding="utf-8"
        ) as file_handler:
            if self.lines_count:
                logging.info("Loaded %s lines of the dictionary", self.lines_count)
            self.lines = file_handler.readlines()
            self._sanitize()
            pickle.dump( self.lines, open( DATA_PATH, "wb" ) )

    def _sanitize(self):
        from operator import methodcaller

        # f = methodcaller('_filter_comments')
        # f(b) returns b._filter_comments().
        for fun in self.filters:
            caller = methodcaller(fun)
            caller(self)

    def _filter_comments(self):
        """ remove lines starting with # or #! """
        self.lines = [line for line in self.lines if not line.startswith(("#"))]

    def _filter_new_lines(self):
        self.lines = [line.rstrip("\n") for line in self.lines]

    def _filter_empty_entries(self):
        self.lines = [line for line in self.lines if line.strip()]

    def parse(self):
        """ Parse Cedict lines and return a list of CedictEntry items """
        result = []
        for line in self.lines[: self.lines_count]:
            entry = CedictEntry.make(line)
            result.append(entry)
        return result


class CedictEntry:  # pylint: disable=too-few-public-methods
    """A representation of a cedict entry

    Keyword arguments:
    traditional -- entry in traditional hanzi
    simplified -- entry in simplified hanzi
    pinyin -- entry pronunciation with tone numbers
    meanings -- list of different meanings for an entry
    raw_line -- the original full line
    """

    def __init__(self, **kwargs):
        self.traditional = kwargs.get("traditional", "")
        self.simplified = kwargs.get("simplified", "")
        self.pinyin = kwargs.get("pinyin", "")
        self.meanings = kwargs.get("meanings", "")
        self.raw_line = kwargs.get("raw_line", "")

    @classmethod
    def make(cls, line):
        """ Generates an entry from a Cedict file line data """
        hanzis = line.partition("[")[0].split(" ", 1)
        keywords = dict(
            meanings=line.partition("/")[2]
            .replace('"', "'")
            .rstrip("/")
            .strip()
            .split("/"),
            traditional=hanzis[0].strip(" "),
            simplified=hanzis[1].strip(" "),
            # Take the content in between the two brackets
            pinyin=line.partition("[")[2].partition("]")[0],
            raw_line=line,
        )
        return cls(**keywords)

    def __str__(self):
        return "{} ({}) - {}".format(self.simplified, self.traditional, self.pinyin)
