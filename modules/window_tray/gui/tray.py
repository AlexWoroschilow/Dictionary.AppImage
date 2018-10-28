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
from PyQt5 import QtWidgets
from PyQt5 import QtGui


class DictionaryTray(QtWidgets.QSystemTrayIcon):

    def __init__(self, app=None):
        icon = QtGui.QIcon('icons/dictionary.svg')
        QtWidgets.QApplication.__init__(self, icon, app)
        self.activated.connect(self.onActionClick)

        self.menu = QtWidgets.QMenu()
        self.scan = QtWidgets.QAction('Scan clipboard', self.menu, checkable=True)
        self.menu.addAction(self.scan)

        self.exit = QtWidgets.QAction('Exit', self.menu)
        self.menu.addAction(self.exit)

        self.setContextMenu(self.menu)

        self.show()

    def onActionClick(self, value):
        if value == self.Trigger:  # left click!
            self.menu.exec_(QtGui.QCursor.pos())
