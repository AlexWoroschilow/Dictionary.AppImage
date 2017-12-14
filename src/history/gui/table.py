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
import inject
import functools

from PyQt5.Qt import Qt
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets


class HistoryTable(QtWidgets.QTableWidget):
    @inject.params(historyManager='history', logger='logger')
    def __init__(self, parent=None, historyManager=None, logger=None):
        """

        :param actions: 
        """
        super(HistoryTable, self).__init__(parent)
        self._active_item = None
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers | QtWidgets.QAbstractItemView.DoubleClicked)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.mouseRightClickEvent)

        self.menu = QtWidgets.QMenu()
        self.remove = QtWidgets.QAction(self.tr("remove"), self.menu)
        self.menu.addAction(self.remove)

        self.clean = QtWidgets.QAction(self.tr("clean"), self.menu)
        self.menu.addAction(self.clean)

        self.clean.triggered.connect(self._onMenuCleanAction)
        self.remove.triggered.connect(self._onMenuRemoveAction)
        self.itemChanged.connect(self._onEntityUpdated)
        self.update = None

        self.setColumnCount(4)
        self.setRowCount(historyManager.count())
        for i, entity in enumerate(historyManager.history):
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
        width_total = size.width()
        width_column = float(width_total) / 4
        self.setColumnWidth(0, 0)
        self.setColumnWidth(1, width_column)
        self.setColumnWidth(2, width_column)
        self.setColumnWidth(3, width_total - (width_column * 2))

    @inject.params(historyManager='history', logger='logger')
    def keyReleaseEvent(self, event=None, historyManager=None, logger=None):
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
                if self._active_item == None:
                    item.setText(None)

                    index = self.item(current.row(), 0)
                    date = self.item(current.row(), 1)
                    word = self.item(current.row(), 2)
                    text = self.item(current.row(), 3)

                    historyManager.update(
                        index.text(), date.text(),
                        word.text(), text.text()
                    )

            return None

        if event.key() in [Qt.Key_Return, Qt.Key_F2]:
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
        for current in self.selectedItems():
            item = self.item(current.row(), current.column())
            if self._active_item == item:
                self._active_item = None
                return None
            self._active_item = item
            self.editItem(item)

    def mouseRightClickEvent(self, event=None):
        """
        
        :param event: 
        :return: 
        """

        self.menu.exec_(self.viewport().mapToGlobal(event))

    @inject.params(historyManager='history', logger='logger')
    def _onMenuRemoveAction(self, event=None, historyManager=None, logger=None):
        """
        
        :param event: 
        :param action: 
        :return: 
        """
        for current in self.selectedItems():
            index = self.item(current.row(), 0)
            date = self.item(current.row(), 1)
            word = self.item(current.row(), 2)
            text = self.item(current.row(), 3)

            historyManager.remove(
                index.text(), date.text(),
                word.text(), text.text()
            )

            self.removeRow(current.row())

    @inject.params(historyManager='history', logger='logger')
    def _onMenuCleanAction(self, event=None, historyManager=None, logger=None):
        """
        
        :param event: 
        :param action: 
        :return: 
        """
        for current in self.selectedItems():
            item = self.item(current.row(), current.column())
            item.setText(None)

            index = self.item(current.row(), 0)
            date = self.item(current.row(), 1)
            word = self.item(current.row(), 2)
            text = self.item(current.row(), 3)

            historyManager.update(
                index.text(), date.text(),
                word.text(), text.text()
            )

    @inject.params(historyManager='history', logger='logger')
    def _onEntityUpdated(self, item=None, historyManager=None, logger=None):
        """
        
        :param event: 
        :param action: 
        :return: 
        """
        for current in self.selectedItems():
            index = self.item(current.row(), 0)
            date = self.item(current.row(), 1)
            word = self.item(current.row(), 2)
            text = self.item(current.row(), 3)

            historyManager.update(
                index.text(), date.text(),
                word.text(), text.text()
            )

    @inject.params(historyManager='history', logger='logger')
    def refresh(self, historyManager=None, logger=None):
        """
        
        :param historyManager: 
        :param logger: 
        :return: 
        """
        self.setRowCount(historyManager.count())
        for i, entity in enumerate(historyManager.history):
            index, date, word, translation = entity
            self.setItem(i, 0, QtWidgets.QTableWidgetItem(index))
            self.setItem(i, 1, QtWidgets.QTableWidgetItem(date))
            self.setItem(i, 2, QtWidgets.QTableWidgetItem(word))
            self.setItem(i, 3, QtWidgets.QTableWidgetItem(translation))
