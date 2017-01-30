# -*- coding: utf-8 -*-
# Copyright 2015 Alex Woroschilow (alex.woroschilow@gmail.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import os
import glob
import sqlite3


class Dictionary(object):
    _connection = None
    _source = None

    def __init__(self, source):
        self._source = source
        self._connection = sqlite3.connect(source, check_same_thread=False)
        self._connection.text_factory = str

    @property
    def name(self):
        return self._source

    @property
    def source(self):
        return self._source

    def has(self, word):
        query = "SELECT COUNT(*) FROM dictionary WHERE word = ?"
        cursor = self._connection.cursor()
        for row in cursor.execute(query, [word]):
            count, = row
            return count > 0
        return False

    def get(self, word):
        query = "SELECT * FROM dictionary WHERE word = ?"
        cursor = self._connection.cursor()
        for response in cursor.execute(query, [word]):
            if response is None:
                continue
            word, translation = response
            return translation
        return None

    def matches(self, word, limit=10):
        query = "SELECT * FROM dictionary WHERE word LIKE ? LIMIT ?"
        cursor = self._connection.cursor()
        for row in cursor.execute(query, [word + "%", limit]):
            yield row


class DictionaryManager(object):
    _dictionaries = []

    def __init__(self, sources):
        while len(sources):
            source = sources.pop()
            for path in glob.glob(source):
                if os.path.isdir(path):
                    sources.append(path)
                    continue
                dictionary = Dictionary(path)
                self._dictionaries.append(dictionary)

    @property
    def dictionaries(self):
        for dictionary in self._dictionaries:
            yield dictionary

    def suggestions(self, match):
        matches = {}
        for dictionary in self._dictionaries:
            for word, translation in dictionary.matches(match):
                if word not in matches.keys():
                    matches[word] = True
                    yield word

    def translate(self, word):
        for dictionary in self.dictionaries:
            translation = dictionary.get(word)
            if translation is None:
                continue
            yield translation

    def translate_one(self, word):
        for dictionary in self.dictionaries:
            translation = dictionary.get(word)
            if translation is None:
                continue
            return translation
