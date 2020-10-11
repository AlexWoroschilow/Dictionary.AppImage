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


class Loader(object):

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def configure(self, binder, options=None, args=None):
        binder.bind_to_constructor('translator.widget', TranslatorWidget)
        binder.bind_to_constructor('translator.thread', TranslatorThread)

    def boot(self, options, args):
        from modules.window_dictionary import gui as window
        from modules.window_dictionary_settings import gui as settings

        @settings.element()
        @inject.params(parent='settings.widget')
        def window_settings(parent=None):
            from .gui.settings.widget import SettingsWidget

            widget = SettingsWidget()
            parent.actionReload.connect(widget.reload)
            return widget

        @window.tab(name='Translation', focus=True, position=0)
        @inject.params(widget='translator.widget', thread='translator.thread')
        def window_tab(parent=None, widget: TranslatorWidget = None, thread: TranslatorThread = None):
            thread.startedSuggesting.connect(widget.suggestionClean.emit)
            thread.suggestion.connect(widget.suggestionAppend.emit)
            thread.startedTranslating.connect(widget.translationClear.emit)
            thread.translation.connect(widget.translationAppend.emit)
            thread.finishedTranslating.connect(parent.translationResponse.emit)
            thread.finished.connect(widget.finished)

            widget.settings.connect(lambda button: parent.settings.emit(button))
            widget.translationRequest.connect(lambda word: thread.translate(word))
            widget.translationSuggestion.connect(lambda word: thread.suggest(word))
            parent.translationClipboardRequest.connect(lambda word: thread.translate(word))
            parent.suggestionClipboardRequest.connect(lambda word: thread.suggest(word))

            thread.translate('test')

            return widget
