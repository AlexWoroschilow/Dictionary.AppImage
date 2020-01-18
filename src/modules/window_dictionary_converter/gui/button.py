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
import functools

from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui


class ButtonDisabled(QtWidgets.QPushButton):

    def __init__(self, icon=None, text=None):
        super(ButtonDisabled, self).__init__(icon, None)
        self.setCheckable(False)
        self.setFlat(True)
        self.setDisabled(True)


class PictureButton(QtWidgets.QPushButton):
    def __init__(self, icon=None, text=None):
        super(PictureButton, self).__init__(icon, None)
        self.setToolTipDuration(0)
        self.setToolTip(text)

    def event(self, QEvent):
        if QEvent.type() == QtCore.QEvent.Enter:
            effect = QtWidgets.QGraphicsDropShadowEffect()
            effect.setColor(QtGui.QColor('#6cccfc'))
            effect.setBlurRadius(5)
            effect.setOffset(0)
            self.setGraphicsEffect(effect)

        if QEvent.type() == QtCore.QEvent.Leave:
            self.setGraphicsEffect(None)

        return super(PictureButton, self).event(QEvent)


class PictureButtonFlat(PictureButton):
    def __init__(self, icon=None, text=None):
        super(QtWidgets.QPushButton, self).__init__(icon, None)
        self.setToolTipDuration(0)
        self.setToolTip(text)
        self.setText(text)
        self.setFlat(True)


class ProgressBarButton(QtWidgets.QWidget):
    clicked = QtCore.pyqtSignal(object)
    progress = QtCore.pyqtSignal(object)

    def __init__(self, icon=None, text=None):
        super(ProgressBarButton, self).__init__()
        self.progress.connect(self.progressActionEvent)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setAlignment(Qt.AlignCenter)

        self.button = PictureButtonFlat(icon, text)
        self.button.clicked.connect(self.clicked.emit)

        self.progressbar = QtWidgets.QProgressBar(self)

        self.progressbar.setVisible(False)

        self.layout().addWidget(self.progressbar)
        self.layout().addWidget(self.button)

    def progressActionEvent(self, value=None):
        if value is None or value >= 100:
            self.progressbar.setVisible(False)
            self.button.setVisible(True)
            return None

        self.progressbar.setVisible(True)
        self.progressbar.setValue(value)
        self.button.setVisible(False)
