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
from PyQt5 import QtCore
from PyQt5 import QtWidgets


class DictionaryListWidget(QtWidgets.QListView):

    def __init__(self):
        super(DictionaryListWidget, self).__init__()
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setModel(QtGui.QStandardItemModel())
        self.setObjectName('DictionaryListWidget')

    def clear(self):
        if self.model() is None:
            return None
        self.model().clear()

    def append(self, entity, isChecked=True):

        item = QtGui.QStandardItem(entity.name)
        item.setCheckState(QtCore.Qt.Checked if isChecked else QtCore.Qt.Unchecked)
        item.setCheckable(True)
        item.setData(entity)

        self.model().appendRow(item)
