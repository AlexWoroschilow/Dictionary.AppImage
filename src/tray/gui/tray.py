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
import di
import os
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from gettext import gettext as _
import platform
import functools


class DictionaryTray(QtWidgets.QSystemTrayIcon):
    def __init__(self, app=None):
        icon = QtGui.QIcon(os.path.abspath(os.path.curdir) + "/img/dictionary.svg")
        QtWidgets.QApplication.__init__(self, icon, app)
        self.activated.connect(self.onActionClick)

        self.menu = QtWidgets.QMenu()
        self.scan = QtWidgets.QAction(_("Scan clipboard"), self.menu, checkable=True)
        self.menu.addAction(self.scan)

        self.open = QtWidgets.QAction(_("Open main window"), self.menu)
        self.menu.addAction(self.open)

        self.hide = QtWidgets.QAction(_("Hide main window"), self.menu)
        self.menu.addAction(self.hide)

        self.exit = QtWidgets.QAction(_("Exit"), self.menu)
        self.menu.addAction(self.exit)

        self.setContextMenu(self.menu)

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

    def onActionOpen(self, action):
        """
        
        :param event: 
        :return: 
        """
        self.open.triggered.connect(functools.partial(
            self._onActionOpen, action=action
        ))

    def _onActionOpen(self, event, action=None):
        """
        
        :param event: 
        :return: 
        """
        if action is not None:
            action(event)

    def onActionHide(self, action):
        """

        :param event: 
        :return: 
        """
        self.hide.triggered.connect(functools.partial(
            self._onActionHide, action=action
        ))

    def _onActionHide(self, event, action=None):
        """

        :param event: 
        :return: 
        """
        if action is not None:
            action(event)

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
