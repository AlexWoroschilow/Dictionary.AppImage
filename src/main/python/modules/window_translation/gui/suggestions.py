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
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


class TranslationListWidget(QtWidgets.QListView):

    def __init__(self, parent):
        super(TranslationListWidget, self).__init__(parent)
        self.parent = parent
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)        
        self.setWindowTitle('Honey-Do List')
        self.setObjectName('TranslationListWidget')

        self.collection = []

    def clear(self):
        if self.model() is None:
            return None
        self.model().clear()

    def append(self, string):
        if self.model() is None:
            model = QtGui.QStandardItemModel()
            self.setModel(model)

        item = QtGui.QStandardItem(string)
        self.model().appendRow(item)

    def setSuggestions(self, collection):
        if self.model() is None:
            model = QtGui.QStandardItemModel()
            self.setModel(model)

        self.model().clear()
        for string in collection:
            item = QtGui.QStandardItem(string)
            self.model().appendRow(item)
