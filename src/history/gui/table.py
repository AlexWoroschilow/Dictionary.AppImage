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
import functools

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui

from PyQt5.Qt import Qt


class HistoryTable(QtWidgets.QTableWidget):
    def __init__(self, parent=None):
        """

        :param actions: 
        """
        super(HistoryTable, self).__init__(parent)
        self._active_item = None
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers |
                             QtWidgets.QAbstractItemView.DoubleClicked)

    def history(self, collection, count):
        """
        
        :param collection: 
        :param count: 
        :return: 
        """
        self.setColumnCount(4)
        self.setRowCount(count)
        for i, entity in enumerate(collection):
            index, date, word, translation = entity
            self.setItem(i, 0, QtWidgets.QTableWidgetItem(index))
            self.setItem(i, 1, QtWidgets.QTableWidgetItem(date))
            self.setItem(i, 2, QtWidgets.QTableWidgetItem(word))
            self.setItem(i, 3, QtWidgets.QTableWidgetItem(translation))

    def setFixedSize(self, size):
        """
        
        :param size: 
        :return: 
        """
        # super(HistoryTable, self).setFixedSize(size)

        width_total = size.width()
        width_column = float(width_total) / 4
        self.setColumnWidth(0, 0)
        self.setColumnWidth(1, width_column)
        self.setColumnWidth(2, width_column)
        self.setColumnWidth(3, width_total - (width_column * 2))

    def keyReleaseEvent(self, event=None):
        """
        
        :param event: 
        :return: 
        """
        if event.key() == Qt.Key_Escape:
            self._active_item = None
            return None

        if event.key() in [Qt.Key_Delete, Qt.Key_Backspace]:
            for current in self.selectedItems():
                item = self.item(current.row(), current.column())
                item.setText(None)
            return None

        if event.key() == Qt.Key_Return:
            for current in self.selectedItems():
                item = self.item(current.row(), current.column())
                if self._active_item == item:
                    self._active_item = None
                    return None
                self._active_item = item
                self.editItem(item)
            return None

    def mouseDoubleClickEvent(self, event=None):
        """
        
        :param event: 
        :return: 
        """
        for currentQTableWidgetItem in self.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
