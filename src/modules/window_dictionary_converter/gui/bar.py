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
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

from .button import ProgressBarButton


class DictionaryConverterHeader(QtWidgets.QFrame):
    loadAction = QtCore.pyqtSignal(object)

    def __init__(self):
        super(DictionaryConverterHeader, self).__init__()

        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignCenter)

        load = ProgressBarButton(QtGui.QIcon("icons/import"), ' Load dump')
        load.clicked.connect(self.loadAction.emit)

        self.layout().addWidget(load)

    def close(self):
        super(DictionaryConverterHeader, self).deleteLater()
        return super(DictionaryConverterHeader, self).close()


class DictionaryConverterToolbar(QtWidgets.QFrame):
    exportAction = QtCore.pyqtSignal(object)
    progressAction = QtCore.pyqtSignal(object)

    def __init__(self):
        super(DictionaryConverterToolbar, self).__init__()

        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignCenter)

        export = ProgressBarButton(QtGui.QIcon("icons/export"), ' Create dictionary')
        export.clicked.connect(self.exportAction.emit)

        self.layout().addWidget(export)

        self.progressAction.connect(export.progress.emit)

    def close(self):
        super(DictionaryConverterToolbar, self).deleteLater()
        return super(DictionaryConverterToolbar, self).close()
