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
from lib.plugin import Loader
from .gui.widget import StatisticWidget


class Loader(Loader):
    def config(self, binder):
        """

        :param binder: 
        :return: 
        """

    @property
    def enabled(self):
        if hasattr(self._options, 'converter'):
            return not self._options.converter
        if hasattr(self._options, 'tray'):
            return not self._options.tray
        return False

    @inject.params(dispatcher='event_dispatcher', logger='logger')
    def boot(self, dispatcher=None, logger=None):
        """

        :param event_dispatcher: 
        :return: 
        """
        dispatcher.add_listener('window.tab', self.OnWindowTab, 30)
        dispatcher.add_listener('window.translation.request', self.OnWindowTranslationRequest, -10)

    @inject.params(historyManager='history', logger='logger')
    def OnWindowTab(self, event, dispatcher, historyManager=None, logger=None):
        """

        :param event:
        :param dispatcher:
        :return:
        """

        self._widget = StatisticWidget()
        self._widget.setHistory(historyManager.history)
        event.data.addTab(self._widget, self._widget.tr('Statistic'))

    @inject.params(historyManager='history', logger='logger')
    def OnWindowTranslationRequest(self, event, dispatcher, historyManager=None, logger=None):
        """

        :param event:
        :param dispatcher:
        :return:
        """
        self._widget.setHistory(historyManager.history)
