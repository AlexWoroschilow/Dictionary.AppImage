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

from PyQt5 import QtWidgets as QtGui
from .list import DictionaryListWidget


class DictionaryWidget(QtGui.QWidget):
    _bright = False
    _actions = False

    def __init__(self):
        super(DictionaryWidget, self).__init__()
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.setContentsMargins(0, 0, 0, 0)

        self.dictionaries = DictionaryListWidget(self)

        self.layout = QtGui.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.dictionaries, 1)

    def clear(self):
        self.dictionaries.clear()

    @inject.params(statusbar='widget.statusbar')
    def append(self, translation, statusbar):
        self.dictionaries.append(translation)
        if statusbar is not None and statusbar:
            statusbar.text('Total: %s dictionaries' % self.dictionaries.model().rowCount())

