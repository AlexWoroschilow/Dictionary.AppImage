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
import inject
import sqlite3

from datetime import datetime


class SQLiteHistory(object):
    _connection = None

    @inject.params(config='config')
    def __init__(self, config=None):
        database = os.path.expanduser(config.get('history.database'))
        return self.__init_database(database)

    def __init_database(self, database=None):
        if database is not None and os.path.isfile(database):
            self._connection = sqlite3.connect(database, check_same_thread=False)
            self._connection.text_factory = str
            return None

        self._connection = sqlite3.connect(database, check_same_thread=False)
        self._connection.text_factory = str
        self._connection.execute(
            "CREATE TABLE history (word TEXT PRIMARY KEY, date TEXT, description TEXT)")
        self._connection.execute("CREATE INDEX IDX_DATE ON history(date)")
        self._connection.execute("CREATE INDEX IDX_WORD ON history(word)")
        return None

    @inject.params(config='config')
    def reload(self, config=None):
        database = os.path.expanduser(config.get('history.database'))
        return self.__init_database(database)

    @property
    def history(self):
        cursor = self._connection.cursor()
        for row in cursor.execute("SELECT * FROM history ORDER BY date DESC"):
            word, date, text = row
            yield (date, word, text)

    @history.setter
    def history(self, collection):
        pass

    def count(self):
        query = "SELECT COUNT(*) FROM history ORDER BY date DESC"
        cursor = self._connection.cursor()
        for row in cursor.execute(query):
            count, = row
            return count

    def has(self, word):
        query = "SELECT COUNT(*) FROM history WHERE word=?"
        cursor = self._connection.cursor()
        for row in cursor.execute(query, [word]):
            count, = row
            return count > 0

    def add(self, word=None, text=None):
        if word is None or not len(word):
            return None

        request_create = "INSERT INTO history VALUES (?, ?, ?)"
        request_update = "UPDATE history SET date=? WHERE word=?"

        date = datetime.now()
        date = date.strftime("%Y.%m.%d %H:%M:%S")

        if self.has(word):
            self._connection.execute(request_update, [date, word])
            return self._connection.commit()

        self._connection.execute(request_create, [word, date, ''])
        return self._connection.commit()

    def update(self, date=None, word=None, description=None):
        fields = (date, word, description, word)
        self._connection.execute("UPDATE history SET date=?, word=?, description=? WHERE word=?", fields)
        self._connection.commit()

    def remove(self, date=None, word=None, text=None):
        self._connection.execute("DELETE FROM history WHERE word=?", [word])
        self._connection.commit()

    def clean(self):
        self._connection.execute("DELETE FROM history")
        self._connection.commit()
