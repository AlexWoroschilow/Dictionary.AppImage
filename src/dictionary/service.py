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
from os.path import expanduser


class Dictionary(object):
    def __init__(self, source):
        """
        
        :param source: 
        """
        self._source = source
        self._connection = sqlite3.connect(source, check_same_thread=False)
        self._connection.text_factory = self._text_factory

    @property
    def name(self):
        """
        
        :return: 
        """
        return self._source

    @property
    def source(self):
        """
        
        :return: 
        """
        return self._source

    def _text_factory(self, x):
        """

        :param x: 
        :return: 
        """
        return str(x, 'utf-8')

    def has(self, word=None):
        """
        
        :param word: 
        :return: 
        """
        query = "SELECT COUNT(*) FROM dictionary WHERE word = ?"
        cursor = self._connection.cursor()
        for row in cursor.execute(query, [word]):
            count, = row
            return count > 0
        return False

    def get(self, word=None):
        """
        
        :param word: 
        :return: 
        """
        query = "SELECT * FROM dictionary WHERE word = ?"
        cursor = self._connection.cursor()
        for response in cursor.execute(query, [word]):
            if response is None:
                continue
            word, translation = response
            return translation
        return None

    def matches(self, word=None, limit=10):
        """
        
        :param word: 
        :param limit: 
        :return: 
        """
        query = "SELECT * FROM dictionary WHERE word LIKE ? LIMIT ?"
        cursor = self._connection.cursor()
        for row in cursor.execute(query, [word + "%", limit]):
            yield row

    def matches_count(self, word=None):
        """
        
        :param word: 
        :return: 
        """
        query = "SELECT COUNT(*) FROM dictionary WHERE word LIKE ?"
        cursor = self._connection.cursor()
        for row in cursor.execute(query, [word + "%"]):
            count, = row
            return count


class DictionaryManager(object):
    def __init__(self, sources):
        """
        
        :param sources: 
        """
        self._dictionaries = []

        while len(sources):
            source = sources.pop()
            for path in glob.glob(source.replace('~', expanduser("~"))):
                if os.path.isdir(path):
                    sources.append(path)
                    continue
                dictionary = Dictionary(path)
                self._dictionaries.append(dictionary)

    @property
    def dictionaries(self):
        """
        
        :return: 
        """
        for dictionary in self._dictionaries:
            yield dictionary

    def suggestions(self, match=None):
        """
        
        :param match: 
        :return: 
        """
        matches = {}
        for dictionary in self._dictionaries:
            for word, translation in dictionary.matches(match):
                if word not in matches.keys():
                    matches[word] = True
                    yield word

    def suggestions_count(self, word):
        """
        
        :param word: 
        :return: 
        """
        count = 0
        for dictionary in self._dictionaries:
            count += dictionary.matches_count(word)
        return count

    def translate(self, word):
        """
        
        :param word: 
        :return: 
        """
        for dictionary in self._dictionaries:
            translation = dictionary.get(word)
            if translation is not None:
                yield translation

    def translation_count(self, word=None):
        """
        
        :param word: 
        :return: 
        """
        count = 0
        for dictionary in self._dictionaries:
            translation = dictionary.get(word)
            if translation is not None:
                count += 1
        return count

    def translate_one(self, word=None):
        """
        
        :param word: 
        :return: 
        """
        for dictionary in self._dictionaries:
            translation = dictionary.get(word)
            if translation is not None:
                return translation
