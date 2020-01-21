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
import os
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import Qt

from .bar import DictionaryConverterHeader
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

        self.source = None

        self.header = DictionaryConverterHeader()
        self.header.loadAction.connect(self.loadActionEvent)

        self.list_view = DictionaryConverterList()

        self.footer = DictionaryConverterToolbar()
        self.footer.exportAction.connect(self.exportActionEvent)
        self.progressAction.connect(self.footer.progressAction.emit)

        self.layout().addWidget(self.header)
        self.layout().addWidget(self.list_view)
        self.layout().addWidget(self.footer)

        self.thread = TranslatorThread()
        self.thread.progressAction.connect(self.footer.progressAction.emit)
        self.thread.wordAction.connect(self.wordActionEvent)

        self.show()

    def exportActionEvent(self, event):
        self.exportAction.emit(self.source)

    def loadActionEvent(self, event):
        selector = QtWidgets.QFileDialog()
        if not selector.exec_():
            return None

        for path in selector.selectedFiles():
            if not os.path.exists(path):
                return None
            self.source = path
            self.list_view.clear()
            self.thread.start(path)

    def wordActionEvent(self, event):
        word, content = event
        self.list_view.append(word, content)
