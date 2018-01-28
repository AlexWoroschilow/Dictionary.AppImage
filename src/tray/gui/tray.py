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
from gettext import gettext as _


class DictionaryTray(QtWidgets.QSystemTrayIcon):
    def __init__(self, app=None):
        """
        
        :param app: 
        """
        icon = QtGui.QIcon("themes/img/dictionary.svg")
        QtWidgets.QApplication.__init__(self, icon, app)
        self.activated.connect(self._onActionClick)

        self.menu = QtWidgets.QMenu()
        self.scan = QtWidgets.QAction(_("Scan clipboard"), self.menu, checkable=True)
        self.scan.triggered.connect(self._onActionScan)

        self.menu.addAction(self.scan)

        self.exit = QtWidgets.QAction(_("Exit"), self.menu)
        self.exit.triggered.connect(self._onActionExit)
        self.menu.addAction(self.exit)

        self.setContextMenu(self.menu)

        self.hidden = False

        self.show()

    @inject.params(dispatcher='event_dispatcher')
    def _onActionClick(self, value=None, dispatcher=None):
        """
        
        :param value: 
        :return: 
        """
        if dispatcher is None:
            return None

        if value == self.Trigger:
            dispatcher.dispatch('window.toggle')

    @inject.params(dispatcher='event_dispatcher')
    def _onActionScan(self, event=None, dispatcher=None):
        """

        :param event: 
        :return: 
        """
        dispatcher.dispatch('window.clipboard.scan', event)

    @inject.params(dispatcher='event_dispatcher')
    def _onActionExit(self, event=None, dispatcher=None):
        """

        :param event: 
        :return: 
        """
        dispatcher.dispatch('window.exit')
