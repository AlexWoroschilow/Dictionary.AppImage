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
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from . import SettingsTitle
from . import WidgetSettings


class SettingsWidget(WidgetSettings):

    @inject.params(config='config')
    def __init__(self, config=None):
        super(SettingsWidget, self).__init__()

        layout = QtWidgets.QGridLayout()
        layout.setAlignment(Qt.AlignLeft)
        self.setLayout(layout)

        self.layout().addWidget(SettingsTitle('Translation'), 0, 0)

        self.showall = QtWidgets.QCheckBox('Show translations from all dictionaries')
        self.showall.setChecked(int(config.get('translator.all')))
        self.showall.stateChanged.connect(self.onActionShowAll)
        self.layout().addWidget(self.showall, 1, 0)

        self.lowercase = QtWidgets.QCheckBox('Convert to lowercase before translate')
        self.lowercase.setChecked(int(config.get('clipboard.uppercase')))
        self.lowercase.stateChanged.connect(self.onActionUpperCase)
        self.layout().addWidget(self.lowercase, 2, 0)

        self.extrachars = QtWidgets.QCheckBox('Remove extra characters before translate')
        self.extrachars.setChecked(int(config.get('clipboard.extrachars')))
        self.extrachars.stateChanged.connect(self.onActionExtraChars)
        self.layout().addWidget(self.extrachars, 3, 0)

    @inject.params(config='config')
    def onActionUpperCase(self, event, config):
        value = '{}'.format(int(event))
        config.set('clipboard.uppercase', value)

    @inject.params(config='config')
    def onActionExtraChars(self, event, config):
        value = '{}'.format(int(event))
        config.set('clipboard.extrachars', value)

    @inject.params(config='config')
    def onActionShowAll(self, event, config):
        value = '{}'.format(int(event))
        config.set('translator.all', value)
