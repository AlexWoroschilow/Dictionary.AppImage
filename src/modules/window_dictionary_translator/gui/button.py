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
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui


class ToolbarButton(QtWidgets.QPushButton):
    def __init__(self, text=None, parent=None):
        super(ToolbarButton, self).__init__(text, parent)
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setCheckable(True)
        self.setFlat(True)


class PictureButtonFlat(QtWidgets.QPushButton):

    def __init__(self, icon=None, parent=None):
        super(PictureButtonFlat, self).__init__(parent)
        self.setFlat(True)
        self.setIcon(icon)

    def event(self, QEvent):
        if QEvent.type() == QtCore.QEvent.Enter:
            effect = QtWidgets.QGraphicsDropShadowEffect()
            effect.setColor(QtGui.QColor('#6cccfc'))
            effect.setBlurRadius(30)
            effect.setOffset(0)
            self.setGraphicsEffect(effect)

        if QEvent.type() == QtCore.QEvent.Leave:
            self.setGraphicsEffect(None)

        return super(PictureButtonFlat, self).event(QEvent)


class PictureButtonDisabled(PictureButtonFlat):

    def __init__(self, icon=None, parent=None):
        super(PictureButtonDisabled, self).__init__(icon, parent)
        self.setIconSize(QtCore.QSize(24, 24))
        self.setDisabled(True)
        self.setIcon(icon)

    def event(self, QEvent):
        return super(QtWidgets.QPushButton, self).event(QEvent)
