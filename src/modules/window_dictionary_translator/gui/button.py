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
from PyQt5.QtCore import Qt


class ToolbarButton(QtWidgets.QToolButton):
    def __init__(self, parent=None, text=None, icon=None):
        super(ToolbarButton, self).__init__(parent)
        assert (text is not None)
        assert (icon is not None)

        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.setIconSize(QtCore.QSize(20, 20))
        self.setIcon(QtGui.QIcon(icon))
        self.setMinimumWidth(80)
        self.setCheckable(True)
        self.setText(text)


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
        self.setDisabled(False)
        self.setIcon(icon)

    def event(self, QEvent):
        return super(QtWidgets.QPushButton, self).event(QEvent)
