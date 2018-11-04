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
import functools
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


class SettingsClipboardWidget(QtWidgets.QWidget):

    @inject.params(config='config')
    def __init__(self, config=None):
        super(SettingsClipboardWidget, self).__init__()
        self.setObjectName('SettingsClipboardWidget')
        layout = QtWidgets.QGridLayout()
        self.setLayout(layout)
        
        layout.addWidget(QtWidgets.QLabel('Clipboard'), 0, 0, 1, 2)
        
        self.scan = QtWidgets.QCheckBox('Scan and translate the clipboard')
        self.scan.setChecked(int(config.get('clipboard.scan')))
        layout.addWidget(self.scan, 1, 0)

        self.suggestions = QtWidgets.QCheckBox('Show the suggestions for the clipboard translations')
        self.suggestions.setChecked(int(config.get('clipboard.suggestions')))
        layout.addWidget(self.suggestions, 2, 0)

        self.uppercase = QtWidgets.QCheckBox('Convert to lowercase before translate')
        self.uppercase.setChecked(int(config.get('clipboard.uppercase')))
        layout.addWidget(self.uppercase, 3, 0)

        self.extrachars = QtWidgets.QCheckBox('Remove extra characters before translate')
        self.extrachars.setChecked(int(config.get('clipboard.extrachars')))
        layout.addWidget(self.extrachars, 4, 0)


class SettingsDictionaryWidget(QtWidgets.QWidget):

    @inject.params(config='config', dictionary='dictionary')
    def __init__(self, config=None, dictionary=None):
        super(SettingsDictionaryWidget, self).__init__()
        self.setObjectName('SettingsDictionaryWidget')
        
        layout = QtWidgets.QGridLayout()
        layout.setAlignment(Qt.AlignLeft)
        self.setLayout(layout)

        layout.addWidget(QtWidgets.QLabel('Dictionary'), 0, 0, 1, 3)
        layout.addWidget(self.spacer, 0, 1)
        
        self.showall = QtWidgets.QCheckBox('Show translations from all dictionaries')
        self.showall.setChecked(int(config.get('translator.all')))

        layout.addWidget(self.showall, 1, 0)

        layout.addWidget(self.spacer, 2, 0)

        label = QtWidgets.QLabel('Dictionary location:')
        label.setObjectName('LabelDictionaryDatabase')
        layout.addWidget(label, 3, 0)
        
        self.database = self.button(config.get('dictionary.database'), "Choose dictionary location folder")
        layout.addWidget(self.database, 3, 2)

        label = QtWidgets.QLabel('History database location:')
        label.setObjectName('LabelHistoryDatabase')
        layout.addWidget(label, 4, 0)
        
        self.history = self.button(config.get('history.database'), "Choose history database folder")
        layout.addWidget(self.history, 4, 2)
        
        layout.addWidget(self.spacer, 5, 0)
 
        for index, entity in enumerate(dictionary.dictionaries, start=6):
            checkbox = QtWidgets.QCheckBox(entity.name)
            checkbox.setChecked(int(config.get('dictionary.%s' % entity.unique)))
            checkbox.stateChanged.connect(functools.partial(
                self.onActionCheck, entity=entity
            ))

            layout.addWidget(checkbox, index, 0, 1, 3)

    def button(self, name, description):
        button = QtWidgets.QPushButton(name)
        button.setToolTip(description)
        button.setFlat(True)
        return button

    @property
    def spacer(self):
        spacer = QtWidgets.QWidget();
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        return spacer

    @inject.params(config='config', dictionary='dictionary')
    def onActionCheck(self, index, entity, config, dictionary):
        if entity is None or not entity:
            return None
        
        var_name = 'dictionary.%s' % entity.unique
        var_value = int(index > 0)
        if var_value == int(config.get(var_name)):
            return None
         
        config.set(var_name, var_value)
        dictionary.reload()


class SettingsWidget(QtWidgets.QScrollArea):

    @inject.params(config='config')
    def __init__(self, config=None):
        super(SettingsWidget, self).__init__()
        self.setObjectName('SettingsWidget')
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setAlignment(Qt.AlignHCenter)
        self.setWidgetResizable(True)        

        scrollContent = QtWidgets.QWidget(self)
        
        layout = QtWidgets.QVBoxLayout()
        scrollContent.setLayout(layout)
        self.setWidget(scrollContent)

        self.clipboard = SettingsClipboardWidget(config)
        layout.addWidget(self.clipboard)
        self.dictionary = SettingsDictionaryWidget(config)
        layout.addWidget(self.dictionary)
        
        spacer = QtWidgets.QWidget();
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        layout.addWidget(spacer)
