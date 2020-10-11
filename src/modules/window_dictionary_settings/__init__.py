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
import functools

import inject

from .actions import SettingsActions
from .gui.scroll import SettingsScrollArea
from .gui.widget import SettingsWidget


class Loader(object):

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def configure(self, binder, options=None, args=None):
        binder.bind_to_constructor('settings.widget', SettingsScrollArea)
        binder.bind_to_constructor('settings.actions', SettingsActions)

    @inject.params(window='window')
    def boot(self, options, args, window):
        from modules.window_dictionary import gui as window

        @window.tab(name='Settings', focus=True, position=5)
        @inject.params(widget='settings.widget')
        def window_tab(parent=None, widget: SettingsScrollArea = None):
            return widget

    @inject.params(window='window', widget='settings.actions')
    def _provider(self, window, actions):
        widget = SettingsWidget()

        action = functools.partial(actions.onActionShowAll, widget=widget)
        widget.dictionary.showall.stateChanged.connect(action)

        action = functools.partial(actions.onActionDictionaryChoose, widget=widget.dictionary)
        widget.dictionary.database.clicked.connect(action)

        action = functools.partial(actions.onActionHistoryChoose, widget=widget.dictionary.history)
        widget.dictionary.history.clicked.connect(action)

        action = functools.partial(actions.onActionScan, widget=widget)
        widget.clipboard.scan.stateChanged.connect(action)

        action = functools.partial(actions.onActionSuggestions, widget=widget)
        widget.clipboard.suggestions.stateChanged.connect(action)

        action = functools.partial(actions.onActionUpperCase, widget=widget)
        widget.clipboard.uppercase.stateChanged.connect(action)

        action = functools.partial(actions.onActionExtraChars, widget=widget)
        widget.clipboard.extrachars.stateChanged.connect(action)

        return widget
