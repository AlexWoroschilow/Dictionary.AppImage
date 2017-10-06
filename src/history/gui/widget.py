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

from .bar import StatusbarWidget
from .bar import ToolbarbarWidget
from .table import HistoryTable


class HistoryWidget(QtWidgets.QWidget):
    _bright = False
    _actions = False

    def __init__(self):
        """

        :param actions: 
        """
        super(HistoryWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        container = QtWidgets.QWidget()

        layout = QtWidgets.QVBoxLayout(container)

        self.table = HistoryTable()
        self.status = StatusbarWidget()
        self.toolbar = ToolbarbarWidget()


        layout.addWidget(self.table, -1)
        layout.addWidget(self.status, -1)

        self.layout = QtWidgets.QHBoxLayout(container)
        self.layout.addWidget(container, 10)
        self.layout.addWidget(self.toolbar, -1)


        self.setLayout(self.layout)

    def resizeEvent(self, event):
        """

        :param event: 
        :return: 
        """
        self.table.setFixedSize(self.size())

    def setHistory(self, collection, count):
        """
        
        :param collection: 
        :return: 
        """
        self.table.history(collection, count)
        self.status.text(self.tr('Total: %s words') % count)

    def onMenuRemoveAction(self, action=None):
        """

        :param event: 
        :return: 
        """
        self.table.onMenuRemoveAction(action)

    def onMenuCleanAction(self, action=None):
        """

        :param event: 
        :return: 
        """
        self.table.onMenuCleanAction(action)

    def onHistoryUpdateAction(self, action=None):
        """

        :param event: 
        :return: 
        """
        self.table.onHistoryUpdateAction(action)
