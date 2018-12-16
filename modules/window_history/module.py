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
from .actions import HistoryActions


class Loader(Loader):

    actions = HistoryActions()

    @property
    def enabled(self):
        if hasattr(self._options, 'converter'):
            return not self._options.converter
        return True

    def config(self, binder=None):
        binder.bind_to_constructor('history', self._constructor)
        binder.bind_to_constructor('widget.history', self._provider)

    @inject.params(kernel='kernel', window='window', widget='widget.history')
    def boot(self, options, args, kernel, window=None, widget=None):
        action = functools.partial(self.actions.onActionTranslationRequest, widget=widget)
        kernel.listen('window.translation.request', action, 10)
        window.addTab(1, widget, 'History', False)

    @inject.params(config='config')
    def _constructor(self, config=None):
        return SQLiteHistory()
    
    @inject.params(history='history', window='window')
    def _provider(self, history, window):

        widget = HistoryWidget()
        
        widget.reload = functools.partial(self.actions.onActionReload, widget=widget) 
        widget.table.keyReleaseEvent = functools.partial(widget.table.keyReleaseEvent, action_remove=self.actions.onActionUpdate)

        action = functools.partial(self.actions.onActionExportCsv, widget=widget) 
        widget.toolbar.csv.triggered.connect(action)
        
        action = functools.partial(self.actions.onActionExportAnki, widget=widget) 
        widget.toolbar.anki.triggered.connect(action)
        
        action = functools.partial(self.actions.onActionHistoryClean, widget=widget) 
        widget.toolbar.clean.triggered.connect(action)

        action = functools.partial(widget.table.onActionHistoryUpdate, action=self.actions.onActionUpdate) 
        widget.table.itemChanged.connect(action)
        
        action = functools.partial(widget.table.onActionMenuClean, action=self.actions.onActionUpdate) 
        widget.table.clean.triggered.connect(action)
        
        action = functools.partial(widget.table.onActionMenuRemove, action=self.actions.onActionRemove)
        widget.table.remove.triggered.connect(action)
        
        widget.history(history.history, history.count())
        
        return widget

