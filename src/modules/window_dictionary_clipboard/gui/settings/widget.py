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

        self.layout().addWidget(SettingsTitle('Clipboard'), 0, 0)

        self.scan = QtWidgets.QCheckBox('Scan and translate the clipboard')
        self.scan.setChecked(int(config.get('clipboard.scan')))
        self.scan.stateChanged.connect(self.onActionScan)
        self.layout().addWidget(self.scan, 1, 0)

        self.suggestions = QtWidgets.QCheckBox('Show the similar words for the clipboard translations')
        self.suggestions.setChecked(int(config.get('clipboard.suggestions')))
        self.suggestions.stateChanged.connect(self.onActionSuggestions)
        self.layout().addWidget(self.suggestions, 2, 0)

    @inject.params(config='config')
    def reload(self, event=None, config=None):
        self.suggestions.setChecked(int(config.get('clipboard.suggestions')))
        self.scan.setChecked(int(config.get('clipboard.scan')))

    @inject.params(config='config')
    def onActionScan(self, event, config):
        value = '{}'.format(int(event))
        config.set('clipboard.scan', value)

    @inject.params(config='config')
    def onActionSuggestions(self, event, config):
        value = '{}'.format(int(event))
        config.set('clipboard.suggestions', value)
