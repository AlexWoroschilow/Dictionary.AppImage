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
from PyQt5 import QtCore


class TranslationListWidget(QtWidgets.QListView):
    selected = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        super(TranslationListWidget, self).__init__(parent)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setMinimumWidth(200)

        self.clicked.connect(self.onItemClicked)

        self.collection = []

    def onItemClicked(self, index=None):
        model = self.model()
        for index in self.selectedIndexes():
            entity = model.itemFromIndex(index)
            if entity is None:
                continue

            text = entity.text()
            if text is not None and len(text) > 0:
                self.selected.emit(text)

    def append(self, string, progress=None):
        if self.model() is None:
            model = QtGui.QStandardItemModel()
            self.setModel(model)

        item = QtGui.QStandardItem(string)
        # item.setIcon(QtGui.QIcon("icons/folder"))

        self.model().appendRow(item)

    def setSuggestions(self, collection):
        if self.model() is None:
            model = QtGui.QStandardItemModel()
            self.setModel(model)

        self.model().clear()
        for string in collection:
            item = QtGui.QStandardItem(string)
            self.model().appendRow(item)

    def clean(self):
        if self.model() is not None:
            self.model().clear()
