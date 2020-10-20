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
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5 import QtGui


class HistoryTable(QtWidgets.QTableWidget):
    remove = QtCore.pyqtSignal(object)
    update = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        super(HistoryTable, self).__init__(parent)
        self._active_item = None
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setContentsMargins(0, 0, 0, 0)

        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers | QtWidgets.QAbstractItemView.DoubleClicked)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.mouseRightClickEvent)

        self.setColumnCount(3)
        self.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem('Date'))
        self.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem('Word'))
        self.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem('Text'))

        self.itemChanged.connect(self.onActionHistoryUpdate)

    def setCount(self, count):
        self.setRowCount(count)
        return self

    def addRow(self, entity=None):
        index, date, word, text = entity
        self.setItem(index, 0, QtWidgets.QTableWidgetItem(date))
        self.setItem(index, 1, QtWidgets.QTableWidgetItem(word))
        self.setItem(index, 2, QtWidgets.QTableWidgetItem(text))
        return self

    def setFixedSize(self, size):
        width_total = size.width()
        width_column = float(width_total) / 3
        self.setColumnWidth(0, width_column)
        self.setColumnWidth(1, width_column)
        self.setColumnWidth(2, width_total - (width_column * 2))

    def mouseDoubleClickEvent(self, event=None):
        for current in self.selectedItems():
            item = self.item(current.row(), current.column())
            if self._active_item == item:
                self._active_item = None
                return None
            self._active_item = item
            self.editItem(item)

    def mouseRightClickEvent(self, event=None):
        menu = QtWidgets.QMenu()

        remove = QtWidgets.QAction(self.tr("remove"), menu)
        remove.triggered.connect(self.onActionMenuRemove)
        menu.addAction(remove)

        clean = QtWidgets.QAction(self.tr("clean"), menu)
        clean.triggered.connect(self.onActionMenuClean)

        menu.addAction(clean)

        menu.exec_(self.viewport().mapToGlobal(event))

    def keyReleaseEvent(self, event=None, action_remove=None):
        if event.key() == Qt.Key_Escape:
            self._active_item = None
            return None

        if event.key() in [Qt.Key_Delete, Qt.Key_Backspace]:
            for current in self.selectedItems():
                item = self.item(current.row(), current.column())
                if self._active_item == None:
                    item.setText(None)

                    data = self.item(current.row(), 0)
                    word = self.item(current.row(), 1)
                    text = self.item(current.row(), 2)

                    self.remove.emit((
                        data.text(),
                        word.text(),
                        text.text(),
                    ))

            return super(HistoryTable, self).keyReleaseEvent(event)

        if event.key() in [Qt.Key_Return, Qt.Key_F2]:
            for current in self.selectedItems():
                item = self.item(current.row(), current.column())
                if self._active_item == item:
                    self._active_item = None
                    return None
                self._active_item = item
                self.editItem(item)
            return None

    def onActionMenuRemove(self, event=None, action=None):

        for current in self.selectedItems():

            try:

                data = self.item(current.row(), 0)
                word = self.item(current.row(), 1)
                text = self.item(current.row(), 2)

                self.remove.emit((data.text(), word.text(), text.text()))

                self.removeRow(current.row())

            except Exception as ex:
                print(ex)
                continue

    def onActionMenuClean(self, event=None):

        for current in self.selectedItems():
            try:

                item = self.item(current.row(), current.column())
                item.setText(None)

                data = self.item(current.row(), 0)
                word = self.item(current.row(), 1)
                text = self.item(current.row(), 2)

                self.update.emit((data.text(), word.text(), text.text()))

            except Exception as ex:
                print(ex)
                continue

    def onActionHistoryUpdate(self, event=None):

        for current in self.selectedItems():
            try:

                data = self.item(current.row(), 0)
                word = self.item(current.row(), 1)
                text = self.item(current.row(), 2)

                self.update.emit((data.text(), word.text(), text.text()))

            except Exception as ex:
                print(ex)
                continue
