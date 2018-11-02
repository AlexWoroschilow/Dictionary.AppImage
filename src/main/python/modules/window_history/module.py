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
        binder.bind('history', SQLiteHistory('~/.dictionaries/history.dhf'))
        binder.bind_to_provider('widget.history', self._provider)

    @inject.params(history='history')
    def _provider(self, history):

        widget = HistoryWidget()
#                 
        widget.toolbar.csv.triggered.connect(functools.partial(
            self.actions.onActionExportCsv, widget=widget
        ))
        
        widget.toolbar.anki.triggered.connect(functools.partial(
            self.actions.onActionExportAnki, widget=widget
        ))
        
        widget.toolbar.clean.triggered.connect(functools.partial(
            self.actions.onActionHistoryClean, widget=widget
        ))

        widget.table.itemChanged.connect(functools.partial(
            widget.table.onActionHistoryUpdate, action=self.actions.onActionUpdate
        ))
        
        widget.table.keyReleaseEvent = (functools.partial(
            widget.table.keyReleaseEvent, action_remove=self.actions.onActionUpdate
        ))
        
        widget.table.clean.triggered.connect(functools.partial(
            widget.table.onActionMenuClean, action=self.actions.onActionUpdate
        ))
        
        widget.table.remove.triggered.connect(functools.partial(
            widget.table.onActionMenuRemove, action=self.actions.onActionRemove
        ))
        
        widget.setHistory(history.history, history.count())
        
        return widget

    @inject.params(kernel='kernel', window='window', widget='widget.history')
    def boot(self, options=None, args=None, window=None, kernel=None, widget=None):
        
        kernel.listen('window.translation.request', functools.partial(
            self.actions.onActionTranslationRequest, widget=widget
        ), 10)
        
        if widget is not None and window is not None:
            window.addTab('History', widget, False)
