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
import os

import inject

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.QtCore import Qt

from .button import ToolbarButton


class MenuContainerWidget(QtWidgets.QScrollArea):
    toggleDictionary = QtCore.pyqtSignal(int, object)

    @inject.params(config='config', dictionary='dictionary')
    def __init__(self, config=None, dictionary=None, themes=None):
        super(MenuContainerWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setContentsMargins(0, 0, 0, 0)
        self.setWidgetResizable(True)

        self.container = QtWidgets.QFrame()

        self.container.setLayout(QtWidgets.QVBoxLayout())
        self.container.layout().setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.setWidget(self.container)

        self.collection = []
        for entity in dictionary.dictionaries:
            checkbox_label = os.path.basename(entity.name)

            dictionary_button = ToolbarButton(self, checkbox_label, QtGui.QIcon('icons/book'))
            dictionary_button.setChecked(int(config.get('dictionary.{}'.format(entity.unique))))
            dictionary_button.clicked.connect(functools.partial(self.onDictionaryToggle, entity=entity))

            dictionary_button.setToolTip(entity.name)
            self.addWidget(dictionary_button)

    def addWidget(self, widget):
        self.container.layout().addWidget(widget, -1)

    def onDictionaryToggle(self, event, entity):
        self.toggleDictionary.emit(event, entity)
