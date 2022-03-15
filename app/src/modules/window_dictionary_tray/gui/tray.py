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
from PyQt5 import QtGui

from .checkbox import MenuCheckbox


class DictionaryTray(QtWidgets.QSystemTrayIcon):

    @inject.params(config='config')
    def __init__(self, app=None, config=None):
        icon = QtGui.QIcon('icons/dictionary')
        QtWidgets.QApplication.__init__(self, icon, app)
        self.setVisible(True)

        self.activated.connect(self.onActionClick)

        self.menu = QtWidgets.QMenu()

        self.window = QtWidgets.QAction('Show window', self.menu)
        self.menu.addAction(self.window)

        self.scan = MenuCheckbox('Translate clipboard', self.menu)
        self.scan.setChecked(int(config.get('clipboard.scan')))
        self.menu.addAction(self.scan)
        self.menu.addSeparator()

        self.suggestions = MenuCheckbox('Show the similar words', self.menu)
        self.suggestions.setChecked(int(config.get('clipboard.suggestions')))
        self.menu.addAction(self.suggestions)

        self.showall = MenuCheckbox('Use all dictionaries', self.menu)
        self.showall.setChecked(int(config.get('translator.all')))
        self.menu.addAction(self.showall)

        self.menu.addSeparator()

        self.exit = QtWidgets.QAction('Quit', self.menu)
        self.menu.addAction(self.exit)

        self.show()

    @inject.params(config='config')
    def onActionClick(self, value, config):
        self.scan.setChecked(int(config.get('clipboard.scan')))
        self.suggestions.setChecked(int(config.get('clipboard.suggestions')))
        self.showall.setChecked(int(config.get('translator.all')))

        self.menu.exec_(QtGui.QCursor.pos())
