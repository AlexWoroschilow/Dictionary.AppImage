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


class ToolbarWidget(QtWidgets.QWidget):

    @inject.params(config='config')
    def __init__(self, config=None):
        super(ToolbarWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setContentsMargins(0, 0, 0, 0)

        from .button import ToolbarButton

        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setAlignment(Qt.AlignLeft)

        self.clipboard = ToolbarButton(self, "...", QtGui.QIcon('icons/clipboard'))
        self.clipboard.clicked.connect(self.onToggleClipboard)
        self.clipboard.clicked.connect(self.reload)
        self.layout().addWidget(self.clipboard, -1)

        self.cleaner = ToolbarButton(self, "Letters", QtGui.QIcon('icons/letters'))
        self.cleaner.clicked.connect(self.onToggleCleaner)
        self.cleaner.clicked.connect(self.reload)
        self.layout().addWidget(self.cleaner, -1)

        self.lowercase = ToolbarButton(self, "Lowercase", QtGui.QIcon('icons/lowercase'))
        self.lowercase.clicked.connect(self.onToggleLowercase)
        self.lowercase.clicked.connect(self.reload)
        self.layout().addWidget(self.lowercase, -1)

        self.reload()

    @inject.params(config='config')
    def reload(self, event=None, config=None):
        self.clipboard.setChecked(int(config.get('clipboard.scan')))
        self.clipboard.setText('Enabled' if self.clipboard.isChecked() else 'Disabled')

        self.lowercase.setChecked(int(config.get('clipboard.uppercase')))
        self.cleaner.setChecked(int(config.get('clipboard.extrachars')))

    @inject.params(config='config')
    def onToggleCleaner(self, event, config=None):
        config.set('clipboard.extrachars', int(event))

    @inject.params(config='config')
    def onToggleLowercase(self, event, config=None):
        config.set('clipboard.uppercase', int(event))

    @inject.params(config='config')
    def onToggleClipboard(self, event, config=None):
        config.set('clipboard.scan', int(event))
