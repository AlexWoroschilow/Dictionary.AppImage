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
import functools
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore


class TranslationListWidget(QtWidgets.QListView):
    def __init__(self, parent):
        """

        :param actions: 
        """
        super(TranslationListWidget, self).__init__(parent)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.setWindowTitle('Honey-Do List')
        # self.selectionChanged = self.onSelectionChange

    def setSuggestions(self, collection):
        """
        
        :param collection: 
        :return: 
        """
        model = QtGui.QStandardItemModel(self)
        for suggestion in collection:
            item = QtGui.QStandardItem("%s" % suggestion)
            model.appendRow(item)

        self.setModel(model)
