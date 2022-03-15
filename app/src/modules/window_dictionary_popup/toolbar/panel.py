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
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5 import QtGui


class ToolbarWidget(QtWidgets.QFrame):
    actionPopup = QtCore.pyqtSignal(object)
    actionReload = QtCore.pyqtSignal(object)

    @inject.params(config='config')
    def __init__(self, config=None):
        super(ToolbarWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        from .button import ToolbarButton

        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.layout().setSpacing(0)

        self.popup = ToolbarButton(self, "...", QtGui.QIcon('icons/popup'))
        self.popup.clicked.connect(self.onTogglePopup)
        self.popup.clicked.connect(self.reload)
        self.layout().addWidget(self.popup, -1)

        self.frameless = ToolbarButton(self, "Frameless", QtGui.QIcon('icons/frameless'))
        self.frameless.clicked.connect(self.onToggleFrameless)
        self.frameless.clicked.connect(self.reload)
        self.layout().addWidget(self.frameless, -1)

        self.position = ToolbarButton(self, "Fixed position", QtGui.QIcon('icons/position'))
        self.position.clicked.connect(self.onTogglePosition)
        self.position.clicked.connect(self.reload)
        self.layout().addWidget(self.position, -1)

        self.size = ToolbarButton(self, "Size", QtGui.QIcon('icons/size'))
        self.size.clicked.connect(self.onToggleSize)
        self.size.clicked.connect(self.reload)
        self.layout().addWidget(self.size, -1)

        self.reload()

    @inject.params(config='config')
    def reload(self, event=None, config=None):
        self.popup.setChecked(int(config.get('popup.enabled', 1)))
        self.popup.setText('Enabled' if self.popup.isChecked() else 'Disabled')

        self.frameless.setChecked(int(config.get('popup.frameless', 1)))
        self.position.setChecked(int(config.get('popup.position', 1)))
        self.size.setChecked(int(config.get('popup.size', 1)))

    @inject.params(config='config')
    def onTogglePopup(self, event=None, config=None):
        config.set('popup.enabled', int(event))

    @inject.params(config='config')
    def onToggleFrameless(self, event=None, config=None):
        config.set('popup.frameless', int(event))

    @inject.params(config='config')
    def onTogglePosition(self, event=None, config=None):
        config.set('popup.position', int(event))

    @inject.params(config='config')
    def onToggleSize(self, event=None, config=None):
        config.set('popup.size', int(event))
