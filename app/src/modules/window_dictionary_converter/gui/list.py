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

    @inject.params(cleaner='dictionary.cleaner')
    def _preview(self, event, content, cleaner=None):
        content = base64.b64decode(content)

        dialog = TranslationDialog()
        dialog.setText(cleaner.cleanup(content.decode('utf-8')))
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
        self.model().removeRows(0, self.model().rowCount())
