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
import functools

from lib.plugin import Loader

from .gui.widget import HistoryWidget
from .service import SQLiteHistory


class Loader(Loader):

    def config(self, binder=None):
        binder.bind('history', SQLiteHistory('~/.dictionaries/history.dhf'))
        binder.bind_to_constructor('widget.history', self._construct)

    @property
    def enabled(self):
        if hasattr(self._options, 'converter'):
            return not self._options.converter
        return True

    @inject.params(kernel='kernel', window='window', widget='widget.history')
    def boot(self, options=None, args=None, window=None, kernel=None, widget=None):
        kernel.listen('window.translation.request', self.onActionTranslationRequest, 10)
        
        if widget is not None and window is not None:
            window.addTab('History', widget, False)
        
    @inject.params(history='history')
    def _construct(self, history):

        self._widget = HistoryWidget()
        self._widget.table.itemChanged.connect(functools.partial(
            self._widget.table.onActionHistoryUpdate, action=self.onActionUpdate
        ))
        
        self._widget.table.keyReleaseEvent = (functools.partial(
            self._widget.table.keyReleaseEvent, action_remove=self.onActionUpdate
        ))
        
        self._widget.table.clean.triggered.connect(functools.partial(
            self._widget.table.onActionMenuClean, action=self.onActionUpdate
        ))
        
        self._widget.table.remove.triggered.connect(functools.partial(
            self._widget.table.onActionMenuRemove, action=self.onActionRemove
        ))
        
        self._widget.setHistory(history.history, history.count())
        
        return self._widget

    @inject.params(history='history')
    def onActionTranslationRequest(self, event, history):
        history.add(event.data)
        self._widget.setHistory(history.history, history.count())

    @inject.params(history='history')
    def onActionRemove(self, entity=None, history=None):
        index, data, word, translation = entity
        history.remove(index, data, word, translation)

    @inject.params(history='history')
    def onActionUpdate(self, entity=None, history=None):
        index, data, word, translation = entity
        history.update(index, data, word, translation)
