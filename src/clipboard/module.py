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
from PyQt5 import QtGui
from lib.plugin import Loader


class Loader(Loader):
    _scan = False

    @property
    def enabled(self):
        """
        
        :return: 
        """
        if hasattr(self._options, 'converter'):
            return not self._options.converter
        return True

    def config(self, binder):
        """
        
        :return: 
        """

    @inject.params(dispatcher='event_dispatcher', logger='logger')
    def boot(self, dispatcher=None, logger=None):
        """

        :param event_dispatcher: 
        :return: 
        """
        dispatcher.add_listener('app.start', self.OnAppStart, 0)
        dispatcher.add_listener('window.clipboard.scan', self.OnClipboardScan, 0)

    def OnAppStart(self, event, dispatcher):
        """

        :param event:
        :param dispatcher:
        :return:
        """
        self.clipboard = event.data.clipboard()
        self.clipboard.dataChanged.connect(self.OnDataChanged)
        self.clipboard.selectionChanged.connect(self.OnSeletionChanged)

    @inject.params(dispatcher='event_dispatcher', logger='logger')
    def OnDataChanged(self, dispatcher=None, logger=None):
        """

        :return:
        """
        if not self._scan:
            return None

        string = self.clipboard.text()
        dispatcher.dispatch('window.clipboard.request', string)

    @inject.params(dispatcher='event_dispatcher', logger='logger')
    def OnSeletionChanged(self, dispatcher=None, logger=None):
        """

        :return:
        """
        if not self._scan:
            return None

        string = self.clipboard.text(QtGui.QClipboard.Selection)
        dispatcher.dispatch('window.clipboard.request', string)

    def OnClipboardScan(self, event, dispatcher):
        """

        :param event:
        :param dispatcher:
        :return:
        """
        self._scan = event.data
