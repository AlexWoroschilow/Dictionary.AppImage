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


class DictionaryCreator(object):
    def __int__(self, ):
        """
        
        :return: 
        """
        pass

    def create(self, output):
        """
        
        :param output: 
        :return: 
        """
        destination = '%s' % (output)
        if os.path.isfile(destination):
            os.remove(destination)

        self.connection = sqlite3.connect(destination, check_same_thread=False)
        self.connection.text_factory = str
        self.connection.execute("CREATE TABLE dictionary (word TEXT, translation TEXT)")
        self.connection.execute("CREATE INDEX IDX_WORD ON dictionary(word)")

        return self

    def append(self, word, translation):
        """
        
        :param word: 
        :param translation: 
        :return: 
        """

        self.connection.execute("INSERT INTO dictionary VALUES (?, ?)", (word, translation))

        return self

    def flush(self):
        """
        
        :return: 
        """
        self.connection.commit()
        return self


class DictionaryConverter(object):
    _creator = None

    def __int__(self):
        """
        
        :return: 
        """
        self._creator = DictionaryCreator()

    def convert(self, dictionary, destination):
        """
        
        :param dictionary: 
        :param destination: 
        :return: 
        """
        self._creator.create('%s/%s.dat' % (destination, dictionary.name))
        for index, response in enumerate(dictionary.words(), start=1):
            word, translation = response
            self._creator.append(word, translation)
            if index % 1000 == 0:
                self._creator.flush()
            yield float(float(index * 100) / len(dictionary))
            self._creator.flush()
