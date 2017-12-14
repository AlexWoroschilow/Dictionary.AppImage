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
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from gettext import gettext as _
import functools


class DictionaryTray(QtWidgets.QSystemTrayIcon):
    def __init__(self, app=None):
        """
        
        :param app: 
        """
        icon = QtGui.QIcon(os.path.abspath(os.path.curdir) + "/img/dictionary.svg")
        QtWidgets.QApplication.__init__(self, icon, app)
        self.activated.connect(self.onActionClick)

        self.menu = QtWidgets.QMenu()
        self.scan = QtWidgets.QAction(_("Scan clipboard"), self.menu, checkable=True)
        self.menu.addAction(self.scan)

        self.toggle = QtWidgets.QAction(_("Hide main window"), self.menu)
        self.menu.addAction(self.toggle)

        self.exit = QtWidgets.QAction(_("Exit"), self.menu)
        self.menu.addAction(self.exit)

        self.setContextMenu(self.menu)

        self.hidden = False

        self.show()

    def onActionClick(self, value):
        """
        
        :param value: 
        :return: 
        """
        if value == self.Trigger:  # left click!
            self.menu.exec_(QtGui.QCursor.pos())

    def onActionScan(self, action):
        """

        :param event: 
        :return: 
        """
        self.scan.triggered.connect(functools.partial(
            self._onActionScan, action=action
        ))

    def _onActionScan(self, event, action=None):
        """

        :param event: 
        :return: 
        """
        if action is not None:
            action(event)

    def onActionToggle(self, action):
        """
        
        :param event: 
        :return: 
        """
        self.toggle.triggered.connect(functools.partial(
            self._onActionToggle, action=action
        ))

    def _onActionToggle(self, event, action=None):
        """
        
        :param event: 
        :return: 
        """
        if action is not None:
            action(event, self.hidden)

    def onActionExit(self, action):
        """
        
        :param event: 
        :return: 
        """
        self.exit.triggered.connect(functools.partial(
            self._onActionExit, action=action
        ))

    def _onActionExit(self, event, action=None):
        """

        :param event: 
        :return: 
        """
        if action is not None:
            action(event)
