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
import inject

from os.path import expanduser


class Dictionary(object):

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

    @property
    def unique(self):
        return self._source. \
            replace(':', '/'). \
            replace(' ', '')

    def has(self, word):
        query = "SELECT COUNT(*) FROM dictionary WHERE word = ? COLLATE NOCASE"
        cursor = self._connection.cursor()
        for row in cursor.execute(query, [word]):
            count, = row
            return count > 0
        return False

    def get(self, word):
        query = "SELECT * FROM dictionary WHERE word = ? COLLATE NOCASE"
        cursor = self._connection.cursor()
        for response in cursor.execute(query, [word]):
            if response is None:
                continue
            word, translation = response
            return translation
        return None

    def matches(self, word, limit=20):
        query = "SELECT * FROM dictionary WHERE word LIKE ? LIMIT ? COLLATE NOCASE"
        cursor = self._connection.cursor()
        for row in cursor.execute(query, [word + "%", limit]):
            yield row

    def matches_count(self, word):
        query = "SELECT COUNT(*) FROM dictionary WHERE word LIKE ? COLLATE NOCASE"
        cursor = self._connection.cursor()
        for row in cursor.execute(query, [word + "%"]):
            count, = row
            return count


class DictionaryManager(object):
    sources = []
    collection = []

    @inject.params(config='config')
    def __init__(self, config=None):
        self.collection = self.load([
            os.path.expanduser(config.get('dictionary.database')),
            'default/'
        ])

    @property
    def dictionaries(self):
        for entity in self.collection:
            yield entity

    @inject.params(config='config')
    def reload(self, config=None):
        self.collection = self.load([
            os.path.expanduser(config.get('dictionary.database')),
            'default/'
        ])

    @inject.params(logger='logger', config='config')
    def load(self, sources, logger, config):
        collection = []
        if not len(sources):
            return collection

        while len(sources):
            source = sources.pop()
            for path in glob.glob('{}/*.dat'.format(source)):
                if os.path.isdir(path):
                    sources.append(path)
                    continue
                logger.info('dictionary found: {}'.format(path))
                entity = Dictionary(path)

                variable = 'dictionary.{}'.format(entity.unique)
                if not config.has(variable):
                    config.set(variable, '1')
                collection.append(entity)
        return collection

    @inject.params(config='config')
    def suggestions(self, match, config=None):
        matches = {}
        for dictionary in self.collection:
            if not int(config.get('dictionary.{}'.format(dictionary.unique))):
                continue
            for word, translation in dictionary.matches(match):
                if word not in matches.keys():
                    matches[word] = True
                    yield word

    @inject.params(config='config')
    def suggestions_count(self, word, config=None, start=0):
        for dictionary in self.collection:
            if int(config.get('dictionary.%s' % dictionary.unique)):
                start += dictionary.matches_count(word)
        return start

    @inject.params(config='config')
    def translate(self, word, config=None):
        for dictionary in self.collection:
            if not int(config.get('dictionary.%s' % dictionary.unique)):
                continue
            translation = dictionary.get(word)
            if translation is not None:
                yield translation

    @inject.params(config='config')
    def translation_count(self, word, config=None, start=0):
        for dictionary in self.collection:
            if int(config.get('dictionary.%s' % dictionary.unique)):
                if dictionary.get(word) is not None:
                    start += 1
        return start

    @inject.params(config='config')
    def translate_one(self, word, config=None):
        for dictionary in self.collection:
            if not int(config.get('dictionary.%s' % dictionary.unique)):
                continue
            translation = dictionary.get(word)
            if translation is not None:
                return translation
