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
        self._connection = sqlite3.connect(database, check_same_thread=False)
        self._connection.text_factory = str
        self._connection.execute("CREATE TABLE history (id INTEGER PRIMARY KEY, date TEXT, word TEXT, description TEXT)")
        self._connection.execute("CREATE INDEX IDX_DATE ON history(date)")

    @property
    def history(self):
        query = "SELECT * FROM history ORDER BY date DESC"
        cursor = self._connection.cursor()
        for row in cursor.execute(query):
            index, date, word, description = row
            yield [str(index).encode("utf-8"), date, word, description]

    @history.setter
    def history(self, collection):
        pass

    def count(self):
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


class CSVFileHistory(object):
    _logger = None
    _logger_handler = None
    _logfile = None
    _dispatcher = None

    def __init__(self, logfile=None):
        self._logfile = logfile.replace('~', expanduser('~'))
        location = os.path.dirname(self._logfile)
        if not os.path.exists(location):
            os.makedirs(location, "0744")

        self._logger = logging.Logger("history")
        self._logger.setLevel(logging.INFO)
        self._logger.addHandler(self.handler)

    @property
    def handler(self):
        self._logger_handler = logging.FileHandler(filename=self._logfile)
        self._logger_handler.setFormatter(logging.Formatter('%(asctime)s;%(message)s', "%Y.%m.%d %H:%M:%S"))
        return self._logger_handler

    def add(self, word, translation=None):
        self._logger.info(word)

    @property
    def history(self):
        with open(self._logfile, 'r') as stream:
            for line in reversed(stream.readlines()):
                yield line.rstrip().split(';')
        stream.close()

    @history.setter
    def history(self, collection):
        history = []
        for record in collection:
            line = string.join(record, ';')
            history.append("%s\n" % line)

        with open(self._logfile, 'w+') as stream:
            stream.writelines(reversed(history))
            stream.close()
