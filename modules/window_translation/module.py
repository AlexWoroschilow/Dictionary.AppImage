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

from PyQt5 import QtCore
from gettext import gettext as _
from lib.plugin import Loader
from .gui.widget import TranslatorWidget


class DictionaryThread(QtCore.QThread):
    started = QtCore.pyqtSignal(int)
    progress = QtCore.pyqtSignal(int, str)
    translation = QtCore.pyqtSignal(int, str)
    suggestion = QtCore.pyqtSignal(int, str)
    finished = QtCore.pyqtSignal(int)

    def __init__(self, parent, dictionary):
        super(DictionaryThread, self).__init__()
        self.parent = parent
        self.dictionary = dictionary
        self.string = None

    def __del__(self):
        self.wait()

    def translate(self, string=None, priority=QtCore.QThread.NormalPriority):
        super(DictionaryThread, self).start(priority)
        self.string = string

    def run(self):
        self.started.emit(0)
        count = self.dictionary.suggestions_count(self.string)
        for index, suggestion in enumerate(self.dictionary.suggestions(self.string), start=1):
            self.suggestion.emit((index / float(count) * 100), suggestion)
        self.finished.emit(100)

        count = self.dictionary.translation_count(self.string)
        for index, translation in enumerate(self.dictionary.translate(self.string), start=1):
            self.translation.emit((index / float(count) * 100), translation)
        self.finished.emit(100)


class Loader(Loader):

    @property
    def enabled(self):
        if hasattr(self._options, 'converter'):
            return not self._options.converter
        if hasattr(self._options, 'tray'):
            return not self._options.tray
        return False

    def config(self, binder=None):
        binder.bind_to_constructor('widget.translator', self._widget)

    @inject.params(kernel='kernel', window='window', widget='widget.translator')
    def boot(self, options=None, args=None, kernel=None, window=None, widget=None):
        kernel.listen('window.clipboard.request', self.onActionTranslate)
        kernel.listen('translate_text', self.onActionTranslate)

        if widget is not None and window is not None:
            window.addTab('Translation', widget)
        
    @inject.params(dictionary='dictionary')
    def _widget(self, dictionary=None):
        
        self.translator_thread = DictionaryThread(self, dictionary)
        self.translator_thread.started.connect(self.onTranslationStarted)
        self.translator_thread.translation.connect(self.onTranslationProgress)
        self.translator_thread.suggestion.connect(self.onTranslationProgressSuggestion)
        self.translator_thread.finished.connect(self.onTranslationFinished)

        self.translator = TranslatorWidget()
        self.translator.onSuggestionSelected(self.onSuggestionSelected)

        self.translator_thread.translate('welcome')
        
        return self.translator

    @inject.params(kernel='kernel', dictionary='dictionary')
    def onSearchString(self, string, dictionary, kernel):
        kernel.dispatch('window.translation.request', string)
        self.translator_thread.translate(string)

    @inject.params(kernel='kernel', widget='widget.translator_search')
    def onActionTranslate(self, event, kernel, widget):
        kernel.dispatch('window.translation.request', event.data)
        self.translator_thread.translate(event.data)
        if widget is not None and widget:
            widget.setText(event.data)

    @inject.params(dictionary='dictionary')
    def onSuggestionSelected(self, string, dictionary):
        translations = dictionary.translate(string) 
        self.translator.setTranslation(translations)

    @inject.params(statusbar='widget.statusbar')
    def onTranslationStarted(self, progress=None, statusbar=None):
        statusbar.start(progress)
        self.translator.clearTranslation()
        self.translator.clearSuggestion()

    @inject.params(statusbar='widget.statusbar')
    def onTranslationProgress(self, progress=None, translation=None, statusbar=None):
        self.translator.addTranslation(translation)
        statusbar.setProgress(progress)

    @inject.params(statusbar='widget.statusbar')
    def onTranslationProgressSuggestion(self, progress=None, string=None, statusbar=None):
        self.translator.addSuggestion(string)
        statusbar.setProgress(progress)

    @inject.params(statusbar='widget.statusbar')
    def onTranslationFinished(self, progress=None, statusbar=None):
        statusbar.stop(progress)
