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
from PyQt5 import QtWidgets as QtGui
from PyQt5 import QtCore
from gettext import gettext as _

from .gui.widget import StatisticWidget
import lib.di as di


class Loader(di.component.Extension):
    @property
    def config(self):
        return None

    @property
    def enabled(self):
        if hasattr(self._options, 'converter'):
            return not self._options.converter
        if hasattr(self._options, 'tray'):
            return not self._options.tray
        return False

    @property
    def subscribed_events(self):
        """

        :return: 
        """
        yield ('window.tab', ['OnWindowTab', 30])
        yield ('window.translation.request', ['OnWindowTranslationRequest', -10])

    # - {name: 'window.tab_switch', method: 'OnTabSwitched', priority: 1}
    # - {name: 'window.tab', method: 'OnTab', priority: 0}
    # - {name: 'clipboard_event.changed', method: 'OnClipboard', priority: 0}
    # - {name: 'kernel_event.service_transate', method: 'OnClipboard', priority: 0}

    def init(self, container):
        """

        :param container_builder: 
        :param container: 
        :return: 
        """
        self.container = container

    def OnWindowTab(self, event, dispatcher):
        """

        :param event: 
        :param dispatcher: 
        :return: 
        """

        self._widget = StatisticWidget()

        manager = self.container.get('history')
        self._widget.setHistory(manager.history)

        event.data.addTab(self._widget, _('Statistic'))

    def OnWindowTranslationRequest(self, event, dispatcher):
        """
        
        :param event: 
        :param dispatcher: 
        :return: 
        """
        manager = self.container.get('history')
        self._widget.setHistory(manager.history)
