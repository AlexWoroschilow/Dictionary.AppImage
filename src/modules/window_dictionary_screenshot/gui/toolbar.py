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

import functools


class ToolbarWidget(QtWidgets.QWidget):
    actionClipboard = QtCore.pyqtSignal(object)
    actionLowercase = QtCore.pyqtSignal(object)
    actionCleaner = QtCore.pyqtSignal(object)

    @inject.params(config='config')
    def __init__(self, config=None):
        super(ToolbarWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setContentsMargins(0, 0, 0, 0)

        from .button import ToolbarButton

        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setAlignment(Qt.AlignLeft)

        self.screenshot = ToolbarButton(self, "...", QtGui.QIcon('icons/screenshot'))
        self.screenshot.clicked.connect(self.onToggleScreenshot)
        self.screenshot.clicked.connect(self.reload)
        self.layout().addWidget(self.screenshot, -1)

        self.english = ToolbarButton(self, "English", QtGui.QIcon('icons/english'))
        self.english.clicked.connect(functools.partial(self.onLanguageChanged, lang='eng'))
        self.english.clicked.connect(self.reload)
        self.layout().addWidget(self.english, -1)

        self.german = ToolbarButton(self, "German", QtGui.QIcon('icons/german'))
        self.german.clicked.connect(functools.partial(self.onLanguageChanged, lang='deu'))
        self.german.clicked.connect(self.reload)
        self.layout().addWidget(self.german, -1)

        self.spanish = ToolbarButton(self, "Spanish", QtGui.QIcon('icons/spanish'))
        self.spanish.clicked.connect(functools.partial(self.onLanguageChanged, lang='spa'))
        self.spanish.clicked.connect(self.reload)
        self.layout().addWidget(self.spanish, -1)

        self.russian = ToolbarButton(self, "Russian", QtGui.QIcon('icons/russian'))
        self.russian.clicked.connect(functools.partial(self.onLanguageChanged, lang='rus'))
        self.russian.clicked.connect(self.reload)
        self.layout().addWidget(self.russian, -1)

        self.ukrainian = ToolbarButton(self, "Ukrainian", QtGui.QIcon('icons/ukrainian'))
        self.ukrainian.clicked.connect(functools.partial(self.onLanguageChanged, lang='ukr'))
        self.ukrainian.clicked.connect(self.reload)
        self.layout().addWidget(self.ukrainian, -1)

        self.belarusian = ToolbarButton(self, "Belarusian", QtGui.QIcon('icons/belarusian'))
        self.belarusian.clicked.connect(self.reload)
        self.belarusian.clicked.connect(functools.partial(self.onLanguageChanged, lang='bel'))
        self.layout().addWidget(self.belarusian, -1)

        self.reload()

    @inject.params(config='config')
    def reload(self, event=None, config=None):
        self.screenshot.setChecked(int(config.get('screenshot.enabled', 1)))
        self.screenshot.setText('Enabled' if self.screenshot.isChecked() else 'Disabled')

        self.english.setChecked(config.get('screenshot.language') == 'eng')
        self.german.setChecked(config.get('screenshot.language') == 'deu')
        self.spanish.setChecked(config.get('screenshot.language') == 'spa')
        self.russian.setChecked(config.get('screenshot.language') == 'rus')
        self.ukrainian.setChecked(config.get('screenshot.language') == 'ukr')
        self.belarusian.setChecked(config.get('screenshot.language') == 'bel')

    @inject.params(config='config')
    def onLanguageChanged(self, event=None, lang=None, config=None):
        config.set('screenshot.language', lang)
        self.reload()

    @inject.params(config='config')
    def onToggleScreenshot(self, event=None, config=None):
        config.set('screenshot.enabled', int(event))
