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
import inject
import functools

from PyQt5 import QtWidgets

from lib.plugin import Loader

from .gui.widget import SettingsWidget
from .actions import SettingsActions


class Loader(Loader):

    actions = SettingsActions()

    @property
    def enabled(self):
        if hasattr(self._options, 'converter'):
            return not self._options.converter
        return True

    def config(self, binder=None):
        binder.bind_to_provider('widget.settings', self._provider)

    @inject.params(window='window', widget='widget.settings')
    def boot(self, options, args, window=None, widget=None):
        window.addTab(3, widget, 'Settings', False)

    @inject.params(window='window')
    def _provider(self, window):
        
        widget = SettingsWidget()

        action = functools.partial(self.actions.onActionShowAll, widget=widget) 
        widget.dictionary.showall.stateChanged.connect(action)

        action = functools.partial(self.actions.onActionDictionaryChoose, widget=widget.dictionary)
        widget.dictionary.database.clicked.connect(action)

        action = functools.partial(self.actions.onActionHistoryChoose, widget=widget.dictionary.history)
        widget.dictionary.history.clicked.connect(action)
        
        action = functools.partial(self.actions.onActionScan, widget=widget) 
        widget.clipboard.scan.stateChanged.connect(action)
        
        action = functools.partial(self.actions.onActionSuggestions, widget=widget) 
        widget.clipboard.suggestions.stateChanged.connect(action)

        action = functools.partial(self.actions.onActionUpperCase, widget=widget)
        widget.clipboard.uppercase.stateChanged.connect(action)

        action = functools.partial(self.actions.onActionExtraChars, widget=widget)
        widget.clipboard.extrachars.stateChanged.connect(action)

        return widget
