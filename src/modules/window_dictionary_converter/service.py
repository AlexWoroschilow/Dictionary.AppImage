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
from pyquery import PyQuery as pq


class DictionaryContentCleaner(object):

    def cleanup(self, content):

        test = pq(content)

        test.find('.noprint').remove()
        test.find('.Übersetzungen').remove()
        test.find('.Übersetzungen_0').remove()
        test.find('.Übersetzungen_1').remove()
        test.find('.Übersetzungen_2').remove()
        test.find('#Übersetzungen').remove()
        test.find('#Übersetzungen_0').remove()
        test.find('#Übersetzungen_1').remove()
        test.find('#Übersetzungen_2').remove()

        test.find('.mw-jump-link').remove()
        test.find('.mw-editsection-bracket').remove()
        test.find('.mw-collapsible-content').remove()
        test.find('.mw-editsection').remove()
        test.find('.fmbox-editnotice').remove()
        test.find('.mw-empty-elt').remove()

        test.find('#Vorlage_Siehe_auch').remove()
        test.find('noscript').remove()
        test.find('.visualClear').remove()
        test.find('.catlinks').remove()
        test.find('#catlinks').remove()
        test.find('.printfooter').remove()
        test.find('video').remove()
        test.find('audio').remove()
        test.find('img').remove()
        test.find('script').remove()
        test.find('style').remove()
        test.find('#toc').remove()

        test.find('table').attr('border', '1')
        test.find('table').attr('width', '100%')
        test.find('table').attr('align', 'center')
        test.find('table').attr('cellspacing', '0')
        test.find('table').attr('cellpadding', '5')

        for a in test.find('a'):
            pq(a).remove_attr('style')
            if pq(a).text() in ['Edit', 'Bearbeiten']:
                pq(a).remove()
                continue
            href = pq(a).attr('href')
            if href is None:
                continue
            if href.find('http') != -1 and href.find('https') != -1:
                continue
            pq(a).attr('href', 'https://de.wiktionary.org{}'.format(href))

        for table in test.find('table'):
            pq(table).remove_attr('style')
            if pq(table).attr('title') in ['Übersetzungen in andere Sprachen']:
                pq(table).remove()
                continue

        for div in test.find('div'):
            pq(div).remove_attr('style')
            if not len(pq(div).text()):
                pq(div).remove()
                continue

        for span in test.find('span'):
            pq(span).remove_attr('style')
            if not len(pq(span).text()):
                pq(span).remove()
                continue

        for p in test.find('p'):
            pq(p).remove_attr('style')
            if not len(pq(p).text()):
                pq(p).remove()
                continue

        for tr in test.find('tr'):
            pq(tr).remove_attr('style')
            if not len(pq(tr).text()):
                pq(tr).remove()
                continue

        for td in test.find('td'):
            pq(td).remove_attr('style')
            if not len(pq(td).text()):
                pq(td).remove()
                continue

        for td in test.find('th'):
            pq(td).remove_attr('style')
            if not len(pq(td).text()):
                pq(td).remove()
                continue

        for element in test.find('ol'):
            pq(element).remove_attr('style')
            if not len(pq(element).text()):
                pq(element).remove()
                continue

        for element in test.find('ul'):
            pq(element).remove_attr('style')
            if not len(pq(element).text()):
                pq(element).remove()
                continue

        for element in test.find('li'):
            pq(element).remove_attr('style')
            if not len(pq(element).text()):
                pq(element).remove()
                continue

        return test.html()


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
