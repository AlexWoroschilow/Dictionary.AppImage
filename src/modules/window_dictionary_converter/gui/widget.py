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
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import Qt

from .bar import DictionaryConverterToolbar
from .list import DictionaryConverterList
from .thread import TranslatorThread


class DictionaryConverterWidget(QtWidgets.QFrame):
    exportAction = QtCore.pyqtSignal(object)
    progressAction = QtCore.pyqtSignal(object)

    def __init__(self):
        super(DictionaryConverterWidget, self).__init__()
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        source = 'wiki.csv'

        thread = TranslatorThread(source)
        thread.wordAction.connect(self.wordActionEvent)
        thread.start()

        self.list_view = DictionaryConverterList()

        self.toolbar = DictionaryConverterToolbar()
        self.toolbar.exportAction.connect(lambda x: self.exportAction.emit(source))
        self.progressAction.connect(self.toolbar.progressAction.emit)

        self.layout().addWidget(self.list_view)
        self.layout().addWidget(self.toolbar)

        self.show()

    def wordActionEvent(self, event):
        word, content = event
        self.list_view.append(word, content)
