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
import string
import sqlite3
import logging

from datetime import datetime
from os.path import expanduser

from jinja2 import Environment
from jinja2 import FileSystemLoader
from jinja2 import select_autoescape


class HistoryExporterSpm(object):
    def __init__(self, history=None):
        """

        :param path: 
        """
        self._history = history

    def export(self, path=None):
        """

        :param path: 
        :return: 
        """


class HistoryExporterCsv(object):
    def __init__(self, history=None):
        """

        :param path: 
        """
        self._history = history

    def export(self, path=None):
        """

        :param path: 
        :return: 
        """
        with open(path, 'w') as stream:
            stream.write('"Date";"Word";"Translation"\n')
            for row in self._history.history:
                index, date, word, description = row
                stream.write('"%s";"%s";"%s"\n' % (date, word, description))
            stream.close()


class SQLiteHistory(object):
    _connection = None

    def __init__(self, database=None):
        """
        
        :param database: 
        """
        database = database.replace('~', expanduser('~'))
        if not os.path.isfile(database):
            self.__init_database(database)
        if self._connection is None:
            self._connection = sqlite3.connect(database, check_same_thread=False)
            self._connection.text_factory = str

    def __init_database(self, database=None):
        """
        
        :param database: 
        :return: 
        """
        self._connection = sqlite3.connect(database, check_same_thread=False)
        self._connection.text_factory = str
        self._connection.execute("CREATE TABLE history (id INTEGER PRIMARY KEY, date TEXT, word TEXT, description TEXT)")
        self._connection.execute("CREATE INDEX IDX_DATE ON history(date)")

    @property
    def history(self):
        """
        
        :return: 
        """
        query = "SELECT * FROM history ORDER BY date DESC"
        cursor = self._connection.cursor()
        for row in cursor.execute(query):
            index, date, word, description = row
            yield [str(index), str(date), str(word), str(description)]

    @history.setter
    def history(self, collection):
        """
        
        :param collection: 
        :return: 
        """
        pass

    def count(self):
        """
        
        :return: 
        """
        query = "SELECT COUNT(*) FROM history ORDER BY date DESC"
        cursor = self._connection.cursor()
        for row in cursor.execute(query):
            count, = row
            return count

    def add(self, word, translation=None):
        """
        
        :param word: 
        :param translation: 
        :return: 
        """
        time = datetime.now()
        fields = (time.strftime("%Y.%m.%d %H:%M:%S"), word, '')
        self._connection.execute("INSERT INTO history VALUES (NULL, ?, ?, ?)", fields)
        self._connection.commit()

    def update(self, index=None, date=None, word=None, description=None):
        """
        
        :param index: 
        :param date: 
        :param word: 
        :param description: 
        :return: 
        """
        fields = (date, word, description, index)
        self._connection.execute("UPDATE history SET date=?, word=?, description=? WHERE id=?", fields)
        self._connection.commit()

    def remove(self, index=None, date=None, word=None, description=None):
        """
        
        :param index: 
        :param date: 
        :param word: 
        :param description: 
        :return: 
        """
        self._connection.execute("DELETE FROM history WHERE id=?", [index])
        self._connection.commit()

    def clean(self):
        """

        :param path: 
        :return: 
        """
        self._connection.execute("DELETE FROM history")
        self._connection.commit()

    def export(self, path=None, type=None):
        """
        
        :param path: 
        :return: 
        """
        if path is None:
            return None

        if type in ['CSV']:
            exporter = HistoryExporterCsv(self)
            exporter.export(path)

        if type in ['SPM']:
            exporter = HistoryExporterSpm(self)
            exporter.export(path)
