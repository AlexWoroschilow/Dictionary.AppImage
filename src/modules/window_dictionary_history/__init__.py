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
from .thread import HistoryThread


class Loader(object):

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    @inject.params(actions='history.actions')
    def _costructor(self, actions: HistoryActions):
        from .gui.widget import HistoryWidget

        widget = HistoryWidget()

        widget.csv.connect(functools.partial(actions.onActionExportCsv, widget=widget))
        widget.clean.connect(functools.partial(actions.onActionHistoryClean, widget=widget))
        widget.anki.connect(functools.partial(actions.onActionExportAnki, widget=widget))

        widget.update.connect(actions.onActionUpdate)
        widget.cleanRow.connect(actions.onActionUpdate)
        widget.remove.connect(actions.onActionRemove)

        return widget

    def configure(self, binder, options=None, args=None):

        binder.bind_to_constructor('history', SQLiteHistory)
        binder.bind_to_constructor('history.actions', HistoryActions)
        binder.bind_to_constructor('history.thread', HistoryThread)
        binder.bind_to_constructor('history.widget', self._costructor)

    @inject.params(widget='history.widget', thread='history.thread')
    def boot(self, options, args, widget, thread: HistoryThread):
        from .gui.widget import HistoryWidget
        from modules import window

        @window.toolbar(name='History', position=10)
        def window_toolbar(parent=None):
            from .toolbar.panel import ToolbarWidget
            widget = ToolbarWidget()
            parent.actionReload.connect(widget.reload)
            return widget

        @window.workspace(name='History', focus=False, position=3)
        @inject.params(widget='history.widget', actions='history.actions')
        def injector_window_tab(parent=None, widget: HistoryWidget = None, actions: HistoryActions = None):
            parent.translationClipboardResponse.connect(actions.onActionTranslationRequest)
            parent.suggestionClipboardResponse.connect(actions.onActionTranslationRequest)
            parent.translationResponse.connect(actions.onActionTranslationRequest)
            parent.suggestionResponse.connect(actions.onActionTranslationRequest)

            return widget

        if not widget.actionReload: return None
        widget.actionReload.connect(thread.reload)

        if not thread.actionProgress: return None
        thread.actionProgress.connect(widget.setProgress)

        if not thread.actionCount: return None
        thread.actionCount.connect(widget.setCount)

        if not thread.actionRow: return None
        thread.actionRow.connect(widget.addRow)
