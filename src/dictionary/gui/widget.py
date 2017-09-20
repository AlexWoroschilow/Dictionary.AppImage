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

from PyQt5 import QtWidgets as QtGui
from PyQt5 import QtCore

from .bar import StatusbarWidget
from .list import DictionaryListWidget


class DictionaryWidget(QtGui.QWidget):
    _bright = False
    _actions = False

    def __init__(self):
        """

        :param actions: 
        """
        super(DictionaryWidget, self).__init__()
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)

        self.status = StatusbarWidget()

        self.dictionaries = DictionaryListWidget(self)

        self.layout = QtGui.QVBoxLayout(self)
        self.layout.addWidget(self.dictionaries, 1)
        self.layout.addWidget(self.status, -1)

    def clear(self):
        """
        
        :return: 
        """
        self.dictionaries.clear()

    def append(self, translation):
        """
        
        :param translation: 
        :return: 
        """
        self.dictionaries.append(translation)
        self.status.text('Total: %s words' % self.dictionaries.model().rowCount())

    def resizeEvent(self, event):
        """

        :param event: 
        :return: 
        """
        self.status.setFixedWidth(event.size().width())
