# -*- coding: utf-8 -*-
# Copyright 2015 Alex Woroschilow (alex.woroschilow@gmail.com)
# !!
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,!
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import inject
import base64
import functools

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from pyquery import PyQuery as pq

from .dialog import TranslationDialog


class WordItem(QtWidgets.QListWidgetItem):

    def __init__(self, book=None):
        super(WordItem, self).__init__()
        self.setTextAlignment(Qt.AlignCenter)


class WordsWidget(QtWidgets.QWidget):

    def __init__(self, word=None, content=None):
        super(WordsWidget, self).__init__()
        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.layout().addWidget(QtWidgets.QLabel(word))
        button = QtWidgets.QPushButton('preview')
        button.clicked.connect(functools.partial(
            self._preview, content=content
        ))
        self.layout().addWidget(button)

    def _preview(self, event, content):
        content = base64.b64decode(content)

        test = pq(content.decode('utf-8'))
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

        content = test.html()

        dialog = TranslationDialog()
        dialog.setText(content)
        dialog.exec_()


class DictionaryConverterList(QtWidgets.QListWidget):

    def __init__(self):
        super(DictionaryConverterList, self).__init__()

    def append(self, word=None, content=None):
        item = WordItem(word)
        self.addItem(item)

        widget = WordsWidget(word, content)
        self.setItemWidget(item, widget)

    def clear(self):
        if self.model() is None:
            return None
        self.model().clear()
