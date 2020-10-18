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

from .actions import HistoryActions
from .gui.widget import HistoryWidget
from .service import SQLiteHistory


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

            widget.reloadHistory.connect(functools.partial(actions.onActionReload, widget=widget))
            widget.csv.connect(functools.partial(actions.onActionExportCsv, widget=widget))
            widget.anki.connect(functools.partial(actions.onActionExportAnki, widget=widget))
            widget.clean.connect(functools.partial(actions.onActionHistoryClean, widget=widget))

            widget.update.connect(actions.onActionUpdate)
            widget.cleanRow.connect(actions.onActionUpdate)
            widget.remove.connect(actions.onActionRemove)

            widget.history(history.history, history.count())

            return widget

        binder.bind_to_constructor('history', SQLiteHistory)
        binder.bind_to_constructor('history.actions', HistoryActions)
        binder.bind_to_constructor('history.widget', HistoryWidget)

    def boot(self, options, args):
        from .gui.widget import HistoryWidget

        from modules.window_dictionary import gui as window

        @window.toolbar(name='History', position=10)
        def window_toolbar(parent=None):
            from .toolbar.panel import ToolbarWidget
            widget = ToolbarWidget()
            parent.actionReload.connect(widget.reload)
            return widget

        @window.tab(name='History', focus=False, position=3)
        @inject.params(widget='history.widget', actions='history.actions')
        def injector_window_tab(parent=None, widget: HistoryWidget = None, actions: HistoryActions = None):
            parent.translationClipboardResponse.connect(actions.onActionTranslationRequest)
            parent.suggestionClipboardResponse.connect(actions.onActionTranslationRequest)
            parent.translationResponse.connect(actions.onActionTranslationRequest)
            parent.suggestionResponse.connect(actions.onActionTranslationRequest)

            return widget
