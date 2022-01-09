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
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from .button import PictureButtonDisabled
from .text import SearchField


class ToolbarWidget(QtWidgets.QFrame):
    actionClipboard = QtCore.pyqtSignal(object)
    actionLowercase = QtCore.pyqtSignal(object)
    actionSimilarities = QtCore.pyqtSignal(object)
    actionAllsources = QtCore.pyqtSignal(object)
    actionCleaner = QtCore.pyqtSignal(object)
    actionReload = QtCore.pyqtSignal(object)
    translationRequest = QtCore.pyqtSignal(object)

    @inject.params(config='config')
    def __init__(self, config=None):
        super(ToolbarWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        from .button import ToolbarButton

        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.layout().setSpacing(0)

        self.cleaner = ToolbarButton(self, "Letters", QtGui.QIcon('icons/letters'))
        self.cleaner.setToolTip('Remove extra characters from the text')
        self.cleaner.clicked.connect(self.actionCleaner.emit)
        self.layout().addWidget(self.cleaner, -1)

        self.lowercase = ToolbarButton(self, "Lowercase", QtGui.QIcon('icons/lowercase'))
        self.lowercase.clicked.connect(self.actionLowercase.emit)
        self.layout().addWidget(self.lowercase, -1)

        self.layout().addWidget(PictureButtonDisabled(QtGui.QIcon("icons/folder")), -1)

        self.text = SearchField(self)
        self.text.returnPressed.connect(lambda: self.translationRequest.emit(self.text.text()))
        self.layout().addWidget(self.text, -1)

        self.allsources = ToolbarButton(self, "All sources", QtGui.QIcon('icons/dictionaries'))
        self.allsources.clicked.connect(self.actionAllsources.emit)
        self.layout().addWidget(self.allsources, -1)

        self.reload()

    @inject.params(config='config')
    def reload(self, event=None, config=None):
        self.lowercase.setChecked(int(config.get('clipboard.uppercase')))
        self.cleaner.setChecked(int(config.get('clipboard.extrachars')))
        self.allsources.setChecked(int(config.get('translator.all')))
