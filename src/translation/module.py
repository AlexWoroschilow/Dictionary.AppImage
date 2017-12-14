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
from lib.plugin import Loader
from .gui.widget import TranslatorWidget


class DictionaryThread(QtCore.QThread):
    started = QtCore.pyqtSignal(int)
    progress = QtCore.pyqtSignal(int, str)
    translation = QtCore.pyqtSignal(int, str)
    suggestion = QtCore.pyqtSignal(int, str)
    finished = QtCore.pyqtSignal(int)

    def __init__(self, parent, dictionary):
        """
        
        :param parent: 
        :param dictionary: 
        """
        super(DictionaryThread, self).__init__()
        self.parent = parent
        self.dictionary = dictionary
        self.string = None

    def __del__(self):
        """
        
        :return: 
        """
        self.wait()

    def start(self, string=None, priority=QtCore.QThread.NormalPriority):
        """
        
        :param string: 
        :param priority: 
        :return: 
        """
        super(DictionaryThread, self).start(priority)
        self.string = string

    def run(self):
        """
        
        :return: 
        """
        self.started.emit(0)
        count = self.dictionary.translation_count(self.string)
        if count not in [0, None]:
            for index, translation in enumerate(self.dictionary.translate(self.string), start=1):
                self.translation.emit((index / float(count) * 100), translation)
        self.finished.emit(100)

        count = self.dictionary.suggestions_count(self.string)
        if count not in [0, None]:
            for index, suggestion in enumerate(self.dictionary.suggestions(self.string), start=1):
                self.suggestion.emit((index / float(count) * 100), suggestion)
        self.finished.emit(100)


class Loader(Loader):
    @property
    def enabled(self):
        """
        
        :return: 
        """
        if hasattr(self._options, 'converter'):
            return not self._options.converter
        if hasattr(self._options, 'tray'):
            return not self._options.tray
        return False

    def config(self, binder):
        """
        
        :param binder: 
        :return: 
        """

    @inject.params(dispatcher='event_dispatcher', logger='logger')
    def boot(self, dispatcher=None, logger=None):
        """

        :param event_dispatcher: 
        :return: 
        """
        dispatcher.add_listener('window.tab', self.OnWindowTab, 0)
        dispatcher.add_listener('window.clipboard.request', self.OnClipboardRequest, 0)

    @inject.params(dictionary='dictionary', logger='logger')
    def OnWindowTab(self, event, dispatcher, dictionary=None, logger=None):
        """

        :param event:
        :param dispatcher:
        :return:
        """

        self.loader = DictionaryThread(self, dictionary)
        self.loader.started.connect(self._onTranslationStart)
        self.loader.translation.connect(self._onTranslationProgress)
        self.loader.suggestion.connect(self._onTranslationSuggestionProgress)
        self.loader.finished.connect(self._onTranslationDone)

        self.translator = TranslatorWidget()
        self.translator.onSearchString(self.OnSearchString)
        self.translator.onSuggestionSelected(self.OnSuggestionSelected)

        self.loader.start("welcome")

        event.data.addTab(self.translator, self.translator.tr('Translation'))

    @inject.params(dispatcher='event_dispatcher', logger='logger')
    def OnSearchString(self, string, dispatcher=None, logger=None):
        """

        :param string:
        :return:
        """
        self.loader.start(string)

        dispatcher.dispatch('window.translation.request', string)

    def OnClipboardRequest(self, event, dispatcher=None):
        """

        :param event:
        :param dispatcher:
        :return:
        """
        self.loader.start(event.data)
        self.translator.setText(event.data)

        dispatcher.dispatch('window.translation.request', event.data)

    @inject.params(dictionary='dictionary', logger='logger')
    def OnSuggestionSelected(self, string, dictionary=None, logger=None):
        """

        :param string:
        :return:
        """
        self.translator.setTranslation(dictionary.translate(string))

    def _onTranslationStart(self, progress=None):
        """

        :param progress:
        :return:
        """
        self.translator.status.start(progress)
        self.translator.clearTranslation()
        self.translator.clearSuggestion()

    def _onTranslationProgress(self, progress=None, translation=None):
        """

        :param progress:
        :return:
        """
        self.translator.addTranslation(translation)
        self.translator.status.setProgress(progress)

    def _onTranslationSuggestionProgress(self, progress=None, string=None):
        """

        :param progress:
        :param translation:
        :return:
        """
        self.translator.addSuggestion(string)
        self.translator.status.setProgress(progress)

    def _onTranslationDone(self, progress=None):
        """

        :param progress:
        :return:
        """
        self.translator.status.stop(progress)
