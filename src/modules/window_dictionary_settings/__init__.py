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

from .gui.widget import SettingsWidget
from .actions import SettingsActions


class Loader(object):

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    actions = SettingsActions()

    def enabled(self, options=None, args=None):
        if hasattr(self._options, 'converter'):
            return not self._options.converter
        return True

    def configure(self, binder, options=None, args=None):
        from .factory import SettingsFactory
        binder.bind('settings.factory', SettingsFactory())

    @inject.params(window='window')
    def boot(self, options, args, window):
        window.settings.connect(functools.partial(
            self.actions.onActionSettings, widget=window
        ))

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
