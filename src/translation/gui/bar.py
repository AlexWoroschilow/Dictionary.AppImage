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
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.Qt import Qt


class SearchLine(QtWidgets.QLineEdit):
    def __init__(self):
        super(SearchLine, self).__init__()
        self.setClearButtonEnabled(True)
        font = self.font()  # lineedit current font
        font.setPointSize(20)  # change it's size
        self.setFont(font)  # set font

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.setText('')
        return super(SearchLine, self).keyPressEvent(event)


class ToolbarWidget(QtWidgets.QStatusBar):
    def __init__(self):
        super(ToolbarWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.setContentsMargins(0, 0, 0, 0)

        self.search = SearchLine()
        self.search.setPlaceholderText(self.tr('Type the word to find a translation...'))
        self.addWidget(self.search, 1)

        self.action = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+f"), self)
        self.action.activated.connect(self.onShortcutSearch)

        self.action = QtWidgets.QShortcut(QtGui.QKeySequence("ESC"), self)
        self.action.activated.connect(self.onShortcutClean)

    def setText(self, text):
        """
        
        :param text: 
        :return: 
        """
        self.search.setText(text)

    def onShortcutClean(self):
        """
        
        :return: 
        """
        self.search.setText("")

    def onShortcutSearch(self):
        """
        
        :return: 
        """
        self.search.setFocusPolicy(Qt.StrongFocus)
        self.search.setFocus()

    def onActionSearch(self, action):
        """
        
        :param action: 
        :return: 
        """
        if self.search is None:
            return None

        self.search.returnPressed.connect(action)


class StatusbarWidget(QtWidgets.QStatusBar):
    def __init__(self):
        super(StatusbarWidget, self).__init__()

        self.status = QtWidgets.QLabel()
        self.status.setAlignment(QtCore.Qt.AlignLeft)

        font = self.status.font()
        font.setPixelSize(10)
        self.status.setFont(font)

        self.addWidget(self.status)

        self.progress = QtWidgets.QProgressBar()
        self.progress.hide()

    def text(self, text):
        """

        :param text: 
        :return: 
        """
        self.status.setText(text)

    def start(self, progress):
        """

        :param progress: 
        :return: 
        """
        if self.status is not None:
            self.status.hide()
            self.removeWidget(self.status)

        if self.progress is not None:
            self.progress.setValue(progress)
            self.addWidget(self.progress, 1)
            self.progress.show()

    def setProgress(self, progress):
        """

        :param progress: 
        :return: 
        """
        if self.progress is not None:
            self.progress.setValue(progress)

    def stop(self, progress):
        """

        :param progress: 
        :return: 
        """
        if self.progress is not None:
            self.progress.hide()
            self.removeWidget(self.progress)

        if self.status is not None:
            self.addWidget(self.status, 1)
            self.status.show()
