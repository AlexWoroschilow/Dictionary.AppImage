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
import functools


class ToolbarWidget(QtWidgets.QWidget):

    @inject.params(config='config', themes='themes')
    def __init__(self, config=None, themes=None):
        super(ToolbarWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setContentsMargins(0, 0, 0, 0)

        from .button import ToolbarButton

        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setAlignment(Qt.AlignLeft)

        self.buttons = []
        for theme in themes.get_stylesheets():
            button = ToolbarButton(self, theme.name, QtGui.QIcon(QtGui.QPixmap(theme.preview)))
            button.clicked.connect(functools.partial(self.onToggleTheme, theme=theme))
            button.theme = theme
            self.layout().addWidget(button, -1)

            self.buttons.append(button)

        self.reload()

    @inject.params(config='config')
    def reload(self, event=None, config=None):
        for button in self.buttons:
            if not button.theme:
                continue
            button.setChecked(button.theme.name == config.get('themes.theme'))

    @inject.params(config='config', window='window')
    def onToggleTheme(self, event, theme=None, config=None, window=None):
        if not theme: return None
        config.set('themes.theme', theme.name)
        window.setStyleSheet(theme.stylesheet)
        self.reload()
