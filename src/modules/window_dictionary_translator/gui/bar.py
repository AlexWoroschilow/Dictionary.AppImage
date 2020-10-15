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
from PyQt5.QtCore import Qt
from PyQt5.QtCore import Qt
import inject


class SearchLine(QtWidgets.QLineEdit):

    def __init__(self):
        super(SearchLine, self).__init__()
        font = self.font()  # lineedit current font
        font.setPointSize(20)  # change it's size
        self.setFont(font)  # set font

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.setText('')
        return super(SearchLine, self).keyPressEvent(event)


class ToolbarWidget(QtWidgets.QWidget):
    actionClipboard = QtCore.pyqtSignal(object)
    actionLowercase = QtCore.pyqtSignal(object)
    actionSimilarities = QtCore.pyqtSignal(object)
    actionAllsources = QtCore.pyqtSignal(object)
    actionCleaner = QtCore.pyqtSignal(object)
    actionReload = QtCore.pyqtSignal(object)

    @inject.params(config='config')
    def __init__(self, config=None):
        super(ToolbarWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.setContentsMargins(0, 0, 0, 0)

        from .button import ToolbarButton

        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setAlignment(Qt.AlignLeft)

        self.clipboard = ToolbarButton("Clipboard", self)
        self.clipboard.setChecked(int(config.get('clipboard.scan')))
        self.clipboard.clicked.connect(self.actionClipboard.emit)
        self.layout().addWidget(self.clipboard, -1)

        self.allsources = ToolbarButton("All dictionaries", self)
        self.allsources.setChecked(int(config.get('translator.all')))
        self.allsources.clicked.connect(self.actionAllsources.emit)
        self.layout().addWidget(self.allsources, -1)

        self.similarities = ToolbarButton("Suggestions", self)
        self.similarities.setChecked(int(config.get('clipboard.suggestions')))
        self.similarities.clicked.connect(self.actionSimilarities.emit)
        self.layout().addWidget(self.similarities, -1)

        self.cleaner = ToolbarButton("Letters only", self)
        self.cleaner.setChecked(int(config.get('clipboard.extrachars')))
        self.cleaner.clicked.connect(self.actionCleaner.emit)
        self.layout().addWidget(self.cleaner, -1)

        self.lowercase = ToolbarButton("Lowercase", self)
        self.lowercase.setChecked(int(config.get('clipboard.uppercase')))
        self.lowercase.clicked.connect(self.actionLowercase.emit)
        self.layout().addWidget(self.lowercase, -1)

    @inject.params(config='config')
    def reload(self, event=None, config=None):
        self.clipboard.setChecked(int(config.get('clipboard.scan')))
        self.similarities.setChecked(int(config.get('clipboard.suggestions')))
        self.lowercase.setChecked(int(config.get('clipboard.uppercase')))
        self.cleaner.setChecked(int(config.get('clipboard.extrachars')))
        self.allsources.setChecked(int(config.get('translator.all')))


class StatusbarWidget(QtWidgets.QStatusBar):

    def __init__(self):
        super(StatusbarWidget, self).__init__()

        self.status = QtWidgets.QLabel()

        self.status.setAlignment(QtCore.Qt.AlignCenter)
        self.addWidget(self.status)

        self.progress = QtWidgets.QProgressBar()
        self.progress.hide()

    def text(self, text):
        self.status.setText(text)

    def start(self, progress):
        if self.status is not None:
            self.status.hide()
            self.removeWidget(self.status)

        if self.progress is not None:
            self.progress.setValue(progress)
            self.addWidget(self.progress, 1)
            self.progress.show()

    def setProgress(self, progress):
        if self.progress is not None:
            self.progress.setValue(progress)

    def stop(self, progress):
        if self.progress is not None:
            self.progress.setValue(progress)
            self.progress.hide()
            self.removeWidget(self.progress)

        if self.status is not None:
            self.addWidget(self.status, 1)
            self.status.show()
