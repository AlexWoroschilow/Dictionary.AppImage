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

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import Qt

from .browser import TranslationWidget


class TranslationDialog(QtWidgets.QDialog):
    activated = QtCore.pyqtSignal(object)

    @inject.params(config='config', themes='themes')
    def __init__(self, parent=None, config=None, themes=None):
        super(TranslationDialog, self).__init__(parent)

        self.setContentsMargins(0, 0, 0, 0)
        self.keyPressEvent = self.activated.emit

        self.translation = TranslationWidget(self)
        self.translation.setContentsMargins(0, 0, 0, 0)
        self.translation.mousePressEvent = self.activated.emit
        self.translation.focusOutEvent = self.activated.emit
        self.translation.keyPressEvent = self.activated.emit

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.translation, -1)

        self.setLayout(self.layout)

        self.setStyleSheet(themes.get_stylesheet())

        if int(config.get('popup.frameless')):
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        width = int(config.get('popup.width', 400))
        height = int(config.get('popup.height', 400))
        self.resize(width, height)

    def onDialogHideEvent(self, event):
        self.close()
        return event.accept()

    def setText(self, collection):
        self.translation.setText(collection)

    def showEvent(self, event):
        geom = self.frameGeometry()
        geom.moveCenter(QtGui.QCursor.pos())
        self.setGeometry(geom)

        super(TranslationDialog, self).showEvent(event)

    def keyPressEvent(self, event):
        return self.close()

    def close(self, event=None):
        self.deleteLater()
        self.hide()
        return super(TranslationDialog, self).close()

    @inject.params(config='config')
    def moveEvent(self, event: QtGui.QMoveEvent, config):
        if not int(config.get('popup.position')):
            return event.ignore()

        position_old: QtCore.QPoint = event.oldPos()
        if not position_old.x(): return None
        if not position_old.y(): return None

        position_new: QtCore.QPoint = event.pos()
        if not position_new.x(): return None
        if not position_new.y(): return None

        config.set('popup.x', position_new.x())
        config.set('popup.y', position_new.y())

        return event.ignore()

    @inject.params(config='config')
    def resizeEvent(self, event, config):
        if not int(config.get('popup.size')):
            return event.accept()

        config.set('popup.width', event.size().width())
        config.set('popup.height', event.size().height())
        return event.accept()
