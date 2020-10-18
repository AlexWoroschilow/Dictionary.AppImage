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
from PyQt5 import QtCore
from PyQt5 import QtWidgets

from .table import HistoryTable


class HistoryWidget(QtWidgets.QFrame):
    csv = QtCore.pyqtSignal(object)
    clean = QtCore.pyqtSignal(object)
    anki = QtCore.pyqtSignal(object)

    remove = QtCore.pyqtSignal(object)
    cleanRow = QtCore.pyqtSignal(object)
    update = QtCore.pyqtSignal(object)
    reloadHistory = QtCore.pyqtSignal(object)

    @inject.params(window='window')
    def __init__(self, window=None):
        super(HistoryWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setContentsMargins(0, 0, 0, 0)

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.table = HistoryTable()
        self.table.remove.connect(self.remove.emit)
        self.table.update.connect(self.update.emit)
        layout.addWidget(self.table)

    def history(self, collection, count):
        self.table.history(collection, count)

    def reload(self):
        self.reloadHistory.emit(())

    def resizeEvent(self, event):
        self.table.setFixedSize(self.size())

    def event(self, QEvent):
        if type(QEvent) == QtCore.QEvent:
            if QEvent.type() == QtCore.QEvent.ShowToParent:
                self.reloadHistory.emit(())
        return super(HistoryWidget, self).event(QEvent)
