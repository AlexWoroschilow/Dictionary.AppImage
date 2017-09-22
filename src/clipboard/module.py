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
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot
import lib.di as di


class Loader(di.component.Extension):
    _scan = False

    @property
    def config(self):
        return None

    @property
    def enabled(self):
        if hasattr(self._options, 'converter'):
            return not self._options.converter
        return True

    @property
    def subscribed_events(self):
        """

        :return: 
        """
        yield ('app.start', ['onAppStart', 0])
        yield ('window.clipboard.scan', ['onClipboardScan', 0])

    def init(self, container):
        """

        :param container_builder: 
        :param container: 
        :return: 
        """
        self.container = container

    def onAppStart(self, event, dispatcher):
        """

        :param event: 
        :param dispatcher: 
        :return: 
        """
        self.clipboard = event.data.clipboard()
        self.clipboard.dataChanged.connect(self.onDataChanged)
        self.clipboard.selectionChanged.connect(self.onSeletionChanged)

    def onDataChanged(self):
        """

        :return: 
        """
        if not self._scan:
            return None

        dispatcher = self.container.get('event_dispatcher')

        string = self.clipboard.text()
        dispatcher.dispatch('window.clipboard.request', string)

    def onSeletionChanged(self):
        """
        
        :return: 
        """
        if not self._scan:
            return None

        dispatcher = self.container.get('event_dispatcher')

        string = self.clipboard.text(QtGui.QClipboard.Selection)
        dispatcher.dispatch('window.clipboard.request', string)

    def onClipboardScan(self, event, dispatcher):
        """
        
        :param event: 
        :param dispatcher: 
        :return: 
        """
        self._scan = event.data
