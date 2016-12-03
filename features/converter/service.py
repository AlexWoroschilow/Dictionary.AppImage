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
import sys
import sqlite3


class DictionaryConverter(object):
    def convert(self, dictionary, destination):
        destination = '%s/%s.dat' % (destination, dictionary.name)
        if os.path.isfile(destination):
            os.remove(destination)

        connection = sqlite3.connect(destination, check_same_thread=False)
        connection.text_factory = str
        connection.execute("CREATE TABLE dictionary (word text, translation text)")
        connection.execute("CREATE INDEX IDX_WORD ON dictionary(word)")

        i = 1
        for response in dictionary.words():
            word, translation = response
            connection.execute("INSERT INTO dictionary VALUES (?, ?)", (word, translation))
            sys.stdout.write('\r%s - %4f %%' % (dictionary.name, float(float(i * 100) / len(dictionary))))
            i += 1
        connection.commit()
        sys.stdout.write('\n%s - done\n' % dictionary.name)

