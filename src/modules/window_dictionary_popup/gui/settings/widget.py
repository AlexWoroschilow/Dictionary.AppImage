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

        self.layout().addWidget(SettingsTitle('Popup'), 0, 0)

        self.popup = QtWidgets.QCheckBox('Show translations in a popup')
        self.popup.setChecked(int(config.get('popup.enabled', 1)))
        self.popup.stateChanged.connect(self.onActionPopup)
        self.layout().addWidget(self.popup, 1, 0)

    @inject.params(config='config')
    def reload(self, event=None, config=None):
        self.popup.setChecked(int(config.get('popup.enabled', 1)))

    @inject.params(config='config')
    def onActionPopup(self, event, config):
        value = '{}'.format(int(event))
        config.set('popup.enabled', value)
