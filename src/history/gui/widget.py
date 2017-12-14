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

        self.table = HistoryTable()
        self.status = StatusbarWidget()
        self.toolbar = ToolbarbarWidget()

        container = QtWidgets.QWidget()

        layout = QtWidgets.QHBoxLayout(container)
        layout.setContentsMargins(0,0,0,0)
        layout.addWidget(self.table, -1)
        layout.addWidget(self.toolbar, -1)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(container, -1)

        self.layout.addWidget(self.status, -1)

        self.setLayout(self.layout)

    def resizeEvent(self, event):
        """

        :param event: 
        :return: 
        """
        self.table.setFixedSize(self.size())

    def refresh(self):
        """
        
        :param collection: 
        :return: 
        """
        self.table.refresh()