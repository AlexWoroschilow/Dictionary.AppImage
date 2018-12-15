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
        self._connection.execute("CREATE TABLE history (id INTEGER PRIMARY KEY, date TEXT, word TEXT, description TEXT)")
        self._connection.execute("CREATE INDEX IDX_DATE ON history(date)")
        return None

    @inject.params(config='config')
    def reload(self, config=None):
        database = os.path.expanduser(config.get('history.database'))
        return self.__init_database(database)
        
    @property
    def history(self):
        cursor = self._connection.cursor()
        for row in cursor.execute("SELECT * FROM history ORDER BY date DESC"):
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
        time = datetime.now()
        fields = (time.strftime("%Y.%m.%d %H:%M:%S"), word, '')
        self._connection.execute("INSERT INTO history VALUES (NULL, ?, ?, ?)", fields)
        self._connection.commit()

    def update(self, index=None, date=None, word=None, description=None):
        fields = (date, word, description, index)
        self._connection.execute("UPDATE history SET date=?, word=?, description=? WHERE id=?", fields)
        self._connection.commit()

    def remove(self, index=None, date=None, word=None, description=None):
        self._connection.execute("DELETE FROM history WHERE id=?", [index])
        self._connection.commit()
        
    def clean(self):
        self._connection.execute("DELETE FROM history")
        self._connection.commit()

