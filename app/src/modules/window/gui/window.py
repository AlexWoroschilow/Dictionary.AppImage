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
import inject

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

from PyQt5.QtCore import Qt

from .content import WindowContent


class MainWindow(QtWidgets.QMainWindow):
    translationRequest = QtCore.pyqtSignal(object)
    translationScreenshotRequest = QtCore.pyqtSignal(object)
    translationClipboardRequest = QtCore.pyqtSignal(object)

    translationResponse = QtCore.pyqtSignal(object)
    translationClipboardResponse = QtCore.pyqtSignal(object)

    suggestionClipboardRequest = QtCore.pyqtSignal(object)
    suggestionClipboardResponse = QtCore.pyqtSignal(object)
    suggestionResponse = QtCore.pyqtSignal(object)
    suggestionRequest = QtCore.pyqtSignal(object)
    resizeAction = QtCore.pyqtSignal(object)

    settings = QtCore.pyqtSignal(object)
    tabAppend = QtCore.pyqtSignal(object)
    tabClose = QtCore.pyqtSignal(object)
    exit = QtCore.pyqtSignal(object)

    @inject.params(themes='themes')
    def __init__(self, parent=None, themes=None):
        super(MainWindow, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setWindowTitle('Dictionary')

        if os.path.exists('icons/dictionary.svg'):
            self.setWindowIcon(QtGui.QIcon("icons/dictionary"))

        self.setStyleSheet(themes.get_stylesheet())

    def resizeEvent(self, event):
        self.resizeAction.emit(event)
