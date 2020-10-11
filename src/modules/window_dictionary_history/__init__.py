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

from .gui.widget import HistoryWidget
from .service import SQLiteHistory
from .actions import HistoryActions


class Loader(object):

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def configure(self, binder, options=None, args=None):
        """
        Configure module services and internal objects structure
        :param binder:
        :param options:
        :param args:
        :return:
        """

        @inject.params(history='history', actions='history.actions')
        def HistoryWidget(history=None, actions: HistoryActions = None):
            from .gui.widget import HistoryWidget

            widget = HistoryWidget()

            action = functools.partial(actions.onActionReload, widget=widget)
            widget.reloadHistory.connect(action)

            action = functools.partial(actions.onActionExportCsv, widget=widget)
            widget.csv.connect(action)

            action = functools.partial(actions.onActionExportAnki, widget=widget)
            widget.anki.connect(action)

            action = functools.partial(actions.onActionHistoryClean, widget=widget)
            widget.clean.connect(action)

            widget.update.connect(actions.onActionUpdate)
            widget.cleanRow.connect(actions.onActionUpdate)
            widget.remove.connect(actions.onActionRemove)

            widget.history(history.history, history.count())

            return widget

        binder.bind_to_constructor('history', SQLiteHistory)
        binder.bind_to_constructor('history.widget', HistoryWidget)
        binder.bind_to_constructor('history.actions', HistoryActions)

    def boot(self, options, args):
        from .gui.widget import HistoryWidget

        from modules.window_dictionary import gui as window
        from modules.window_dictionary_settings import gui as settings

        @settings.element()
        @inject.params(parent='settings.widget')
        def window_settings(parent=None):
            from .gui.settings.widget import SettingsWidget
            return SettingsWidget()

        @window.tab(name='History', focus=False, position=3)
        @inject.params(widget='history.widget', actions='history.actions')
        def tab(parent=None, widget: HistoryWidget = None, actions: HistoryActions = None):
            action = functools.partial(actions.onActionTranslationRequest, widget=widget)
            parent.translationClipboardResponse.connect(action)

            action = functools.partial(actions.onActionTranslationRequest, widget=widget)
            parent.suggestionClipboardResponse.connect(action)

            action = functools.partial(actions.onActionTranslationRequest, widget=widget)
            parent.translationResponse.connect(action)

            action = functools.partial(actions.onActionTranslationRequest, widget=widget)
            parent.suggestionResponse.connect(action)

            return widget
