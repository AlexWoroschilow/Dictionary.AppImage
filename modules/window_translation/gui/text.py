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
from PyQt5.Qt import Qt
from PyQt5 import QtGui


class SearchField(QtWidgets.QLineEdit):

    def __init__(self, parent=None):
        super(SearchField, self).__init__(parent)
        self.setPlaceholderText('Enter the search string...')

        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+f"), self)
        shortcut.activated.connect(self.on_shortcut_activated)

        effect = QtWidgets.QGraphicsDropShadowEffect()
        effect.setBlurRadius(5)
        effect.setOffset(0)

        self.setGraphicsEffect(effect)

    def on_shortcut_activated(self, event=None):
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()
