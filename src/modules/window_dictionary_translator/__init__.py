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

from .thread import TranslatorThread
from .gui.widget import TranslatorWidget
from .actions import TranslatorActions


class Loader(object):

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def configure(self, binder, options=None, args=None):
        binder.bind_to_constructor('translator.widget', TranslatorWidget)
        binder.bind_to_constructor('translator.thread', TranslatorThread)
        binder.bind_to_constructor('translator.actions', TranslatorActions)

    def boot(self, options, args):
        from modules.window_dictionary import gui as window

        @window.toolbar(name='Translation', focus=True, position=0)
        @inject.params(translator='translator.widget')
        def window_header(parent=None, translator=None):
            from .gui.toolbar import ToolbarWidgetTab
            widget = ToolbarWidgetTab()
            widget.actionClipboard.connect(translator.actionClipboard.emit)
            widget.actionLowercase.connect(translator.actionLowercase.emit)
            widget.actionSimilarities.connect(translator.actionSimilarities.emit)
            widget.actionAllsources.connect(translator.actionAllsources.emit)
            widget.actionCleaner.connect(translator.actionCleaner.emit)

            translator.actionReload.connect(widget.reload)
            return widget

        @window.tab(name='Translation', focus=True, position=0)
        @inject.params(widget='translator.widget', thread='translator.thread', actions='translator.actions')
        def window_content(parent=None, widget: TranslatorWidget = None, thread: TranslatorThread = None, actions: TranslatorActions = None):
            thread.startedSuggesting.connect(widget.suggestionClean.emit)
            thread.startedTranslating.connect(widget.translationClear.emit)
            thread.suggestion.connect(widget.suggestionAppend.emit)
            thread.translation.connect(widget.translationAppend.emit)
            thread.finishedTranslating.connect(parent.translationResponse.emit)
            thread.finished.connect(widget.finished)

            widget.actionPopup.connect(actions.onActionSettingsPopup)
            widget.actionClipboard.connect(actions.onActionSettingsClipboard)
            widget.actionLowercase.connect(actions.onActionSettingsLowercase)
            widget.actionSimilarities.connect(actions.onActionSettingsSimilarities)
            widget.actionAllsources.connect(actions.onActionSettingsAllsources)
            widget.actionCleaner.connect(actions.onActionSettingsCleaner)

            widget.translationRequest.connect(thread.translate)
            widget.translationSuggestion.connect(thread.suggest)

            parent.translationRequest.connect(thread.translate)
            parent.translationRequest.connect(widget.word)

            parent.translationClipboardRequest.connect(thread.translate)
            parent.translationClipboardRequest.connect(widget.word)

            parent.translationScreenshotRequest.connect(thread.translate)
            parent.translationScreenshotRequest.connect(widget.word)

            thread.translate('test')

            return widget
