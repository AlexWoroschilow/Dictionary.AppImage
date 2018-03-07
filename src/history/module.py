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
from .service import SQLiteHistory
from .gui.widget import HistoryWidget


class Loader(Loader):
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

        :param binder: 
        :return: 
        """

        binder.bind('history', SQLiteHistory("~/.dictionaries/history.dhf"))

    @inject.params(dispatcher='event_dispatcher', logger='logger')
    def boot(self, dispatcher=None, logger=None):
        """
        
        :param dispatcher: 
        :param logger: 
        :return: 
        """
        dispatcher.add_listener('window.tab', self.OnWindowTab, 10)
        dispatcher.add_listener('window.translation.request', self.OnWindowTranslationRequest, 10)
        dispatcher.add_listener('window.history.export', self.OnWindowHistoryExport)
        dispatcher.add_listener('window.history.clean', self.OnWindowHistoryClean)

    @inject.params(logger='logger')
    def OnWindowTab(self, event, dispatcher, logger=None):
        """

        :param event:
        :param dispatcher:
        :return:
        """

        self._widget = HistoryWidget()
        event.data.addTab(self._widget, self._widget.tr('History'))

    @inject.params(history='history', logger='logger')
    def OnWindowTranslationRequest(self, event, dispatcher, history=None, logger=None):
        """

        :param event:
        :param dispatcher:
        :return:
        """
        history.add(event.data)
        self._widget.refresh()

    @inject.params(history='history', logger='logger')
    def OnWindowHistoryExport(self, event, dispatcher, history=None, logger=None):
        """
        
        :param event: 
        :param dispatcher: 
        :param history: 
        :param logger: 
        :return: 
        """
        path, type = event.data
        history.export(path, type)

    @inject.params(history='history', logger='logger')
    def OnWindowHistoryClean(self, event, dispatcher, history=None, logger=None):
        """
        
        :param event: 
        :param dispatcher: 
        :param history: 
        :param logger: 
        :return: 
        """
        history.clean()
        self._widget.refresh()
