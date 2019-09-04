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

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

from .content import WindowContent


class MainWindow(QtWidgets.QMainWindow):
    translationClipboardRequest = QtCore.pyqtSignal(object)
    translationClipboardResponse = QtCore.pyqtSignal(object)
    translationRequest = QtCore.pyqtSignal(object)
    translationResponse = QtCore.pyqtSignal(object)

    suggestionClipboardRequest = QtCore.pyqtSignal(object)
    suggestionClipboardResponse = QtCore.pyqtSignal(object)
    suggestionResponse = QtCore.pyqtSignal(object)
    suggestionRequest = QtCore.pyqtSignal(object)

    settings = QtCore.pyqtSignal(object)
    tabAppend = QtCore.pyqtSignal(object)
    tabClose = QtCore.pyqtSignal(object)
    exit = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setWindowTitle('AOD - Dictionary')

        if os.path.exists('icons/dictionary.svg'):
            self.setWindowIcon(QtGui.QIcon("icons/dictionary"))

        if os.path.exists('css/stylesheet.qss'):
            with open('css/stylesheet.qss') as stream:
                self.setStyleSheet(stream.read())

        self.content = WindowContent(self)
        self.setCentralWidget(self.content)

        # spacer = QtWidgets.QWidget()
        # spacer.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.statusBar().addWidget(QtWidgets.QWidget())

    def addTab(self, index, widget, name, focus=True):
        if self.content is not None and widget is not None:
            self.content.insertTab(index, widget, name)
            if focus is not None and focus == True:
                index = self.content.indexOf(widget)
                self.content.setCurrentIndex(index)
