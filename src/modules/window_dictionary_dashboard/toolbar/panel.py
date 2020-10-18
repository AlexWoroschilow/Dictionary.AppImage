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
import os
import functools


class ToolbarWidget(QtWidgets.QScrollArea):

    @inject.params(config='config', dictionary='dictionary')
    def __init__(self, config=None, dictionary=None):
        super(ToolbarWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        self.setContentsMargins(0, 0, 0, 0)

        from .button import ToolbarButton

        self.container = QtWidgets.QWidget()
        self.container.setLayout(QtWidgets.QHBoxLayout())
        self.container.layout().setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.setWidget(self.container)

        database = config.get('dictionary.database')
        database = os.path.basename(os.path.expanduser(database))

        self.database = ToolbarButton(self, database, QtGui.QIcon('icons/dictionaries'))
        self.database.setToolTip(config.get('dictionary.database'))
        self.database.clicked.connect(self.onSelectDatabase)
        self.database.clicked.connect(self.reload)
        self.database.setChecked(False)
        self.addWidget(self.database)

        self.collection = []
        for entity in dictionary.dictionaries:
            checkbox_label = os.path.basename(entity.name)

            dictionary_button = ToolbarButton(self, checkbox_label, QtGui.QIcon('icons/book'))
            dictionary_button.setChecked(int(config.get('dictionary.{}'.format(entity.unique))))
            dictionary_button.clicked.connect(functools.partial(self.onToggleDictionary, entity=entity))
            dictionary_button.clicked.connect(self.reload)
            dictionary_button.setToolTip(entity.name)
            self.addWidget(dictionary_button)

        self.reload()

    def addWidget(self, widget):
        self.container.layout().addWidget(widget, -1)

    @inject.params(config='config')
    def reload(self, event=None, config=None):
        database = config.get('dictionary.database')
        database = os.path.basename(os.path.expanduser(database))
        self.database.setChecked(False)
        self.database.setText(database)

    @inject.params(config='config', dictionary='dictionary')
    def onToggleDictionary(self, event, entity, config, dictionary):
        if not entity: return None

        var_name = 'dictionary.{}'.format(entity.unique)
        if int(event) == int(config.get(var_name)):
            return None

        config.set(var_name, int(event))
        dictionary.reload()

    @inject.params(config='config', dictionary='dictionary')
    def onSelectDatabase(self, event, widget=None, config=None, dictionary=None):
        database = config.get('dictionary.database')
        database = os.path.expanduser(database)
        path = str(QtWidgets.QFileDialog.getExistingDirectory(None, 'Select Directory', database))
        if not path: return self.database.setChecked(False)

        config.set('dictionary.database', '{}'.format(path))
        if dictionary: dictionary.reload()
