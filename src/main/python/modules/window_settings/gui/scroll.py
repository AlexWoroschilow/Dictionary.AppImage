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
import platform
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from .widget import SettingsWidget


class SettingsScrollArea(QtWidgets.QScrollArea):

    def __init__(self, parent=None):
        super(SettingsScrollArea, self).__init__(parent)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setAlignment(Qt.AlignTop)
        self.setWidgetResizable(True)

        self.container = SettingsWidget()
        self.setWidget(self.container)

        if os.path.exists('css/stylesheet.qss'):
            with open('css/stylesheet.qss') as stream:
                self.setStyleSheet(stream.read())

    def addWidget(self, widget):
        self.container.addWidget(widget)

    def close(self):
        super(SettingsScrollArea, self).deleteLater()
        return super(SettingsScrollArea, self).close()
