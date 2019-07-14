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
import os
import inject
import functools
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from .button import PictureButtonFlat
from . import SettingsTitle


class SettingsWidget(QtWidgets.QWidget):
    collection = []

    @inject.params(config='config')
    def __init__(self, config=None):
        super(SettingsWidget, self).__init__()

        layout = QtWidgets.QGridLayout()
        layout.setAlignment(Qt.AlignLeft)
        self.setLayout(layout)

        self.layout().addWidget(SettingsTitle('Dictionary'), 0, 0)
        self.layout().addWidget(QtWidgets.QLabel('Dictionaries:'), 1, 0)

        database = config.get('dictionary.database')
        database = database.replace(os.path.expanduser('~'), '~')

        self.database = PictureButtonFlat(None, database)
        self.database.clicked.connect(self.onActionDictionary)
        self.database.setToolTip("Choose dictionary location folder")
        self.layout().addWidget(self.database, 1, 1)

        self.reload()

    @inject.params(config='config', dictionary='dictionary')
    def reload(self, config=None, dictionary=None):
        for widget in self.collection:
            self.layout().removeWidget(widget)

        self.collection = []
        for index, entity in enumerate(dictionary.dictionaries, start=6):
            checkbox_label = entity.name
            checkbox_label = checkbox_label.replace(os.path.expanduser('~'), '~')
            checkbox = QtWidgets.QCheckBox(checkbox_label)
            self.collection.append(checkbox)

            checkbox.setChecked(int(config.get('dictionary.%s' % entity.unique)))
            checkbox.stateChanged.connect(functools.partial(
                self.onActionCheck, entity=entity
            ))

            self.layout().addWidget(checkbox, index, 0, 1, 2)

    @inject.params(config='config', dictionary='dictionary')
    def onActionCheck(self, index, entity, config, dictionary):
        if entity is None or not entity:
            return None

        var_value = int(index > 0)
        var_name = 'dictionary.{}'.format(entity.unique)
        if var_value == int(config.get(var_name)):
            return None

        config.set(var_name, var_value)

        if dictionary is not None:
            dictionary.reload()

    @inject.params(config='config', dictionary='dictionary')
    def onActionDictionary(self, event, widget=None, config=None, dictionary=None):
        database = config.get('dictionary.database')
        path = str(QtWidgets.QFileDialog.getExistingDirectory(None, 'Select Directory', database))
        if path is None or len(path) == 0:
            return None

        config.set('dictionary.database', '{}'.format(path))
        self.database.setText('{}'.format(path))

        if dictionary is not None:
            dictionary.reload()
