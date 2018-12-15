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

from .browser import TranslationWidget


class TranslationDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        """
        
        :param parent: 
        """
        super(TranslationDialog, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setContentsMargins(0, 0, 0, 0)



        self.resize(500, 300)

        self.translation = TranslationWidget(self)
        self.translation.setContentsMargins(0, 0, 0, 0)
        self.translation.mousePressEvent = self.onDialogHideEvent
        self.translation.focusOutEvent = self.onDialogHideEvent

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.translation, -1)

        self.setLayout(self.layout)

    def onDialogHideEvent(self, event):
        self.hide()
        event.accept()

    def setTranslation(self, collection):
        self.translation.setTranslation(collection)

    def showEvent(self, event):
        geom = self.frameGeometry()
        geom.moveCenter(QtGui.QCursor.pos())
        self.setGeometry(geom)
        super(TranslationDialog, self).showEvent(event)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.hide()
            event.accept()
        else:
            super(TranslationDialog, self).keyPressEvent(event)
            