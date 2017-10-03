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
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from gettext import gettext as _
from .gui.widget import TranslatorWidget
import lib.di as di


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

    def start(self, string=None, priority=QtCore.QThread.NormalPriority):
        super(DictionaryThread, self).start(priority)
        self.string = string

    def run(self):
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


class Loader(di.component.Extension):
    @property
    def config(self):
        return None

    @property
    def enabled(self):
        if hasattr(self._options, 'converter'):
            return not self._options.converter
        if hasattr(self._options, 'tray'):
            return not self._options.tray
        return False

    @property
    def subscribed_events(self):
        """

        :return: 
        """
        yield ('window.tab', ['OnWindowTab', 0])
        yield ('window.clipboard.request', ['onClipboardRequest', 0])

    def init(self, container):
        """

        :param container_builder: 
        :param container: 
        :return: 
        """
        self.container = container

    def OnWindowTab(self, event, dispatcher):
        """
        
        :param event: 
        :param dispatcher: 
        :return: 
        """

        self.loader = DictionaryThread(self, self.container.get('dictionary'))
        self.loader.started.connect(self._onTranslationStart)
        self.loader.translation.connect(self._onTranslationProgress)
        self.loader.suggestion.connect(self._onTranslationSuggestionProgress)
        self.loader.finished.connect(self._onTranslationDone)

        self.translator = TranslatorWidget()
        self.translator.onSearchString(self.onSearchString)
        self.translator.onSuggestionSelected(self.onSuggestionSelected)

        self.loader.start("welcome")

        event.data.addTab(self.translator, self.translator.tr('Translation'))

    def onSearchString(self, string):
        """
        
        :param string: 
        :return: 
        """
        self.loader.start(string)

        dispatcher = self.container.get('event_dispatcher')
        dispatcher.dispatch('window.translation.request', string)

    def onClipboardRequest(self, event, dispatcher):
        """

        :param event: 
        :param dispatcher: 
        :return: 
        """
        self.loader.start(event.data)
        self.translator.setText(event.data)

        dispatcher = self.container.get('event_dispatcher')
        dispatcher.dispatch('window.translation.request', event.data)

    def onSuggestionSelected(self, string):
        """
        
        :param string: 
        :return: 
        """
        dictionary = self.container.get('dictionary')
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
        self.translator.addTranslation(translation.encode('utf8'))
        self.translator.status.setProgress(progress)

    def _onTranslationSuggestionProgress(self, progress=None, string=None):
        """
        
        :param progress: 
        :param translation: 
        :return: 
        """
        self.translator.addSuggestion(string.encode('utf8'))
        self.translator.status.setProgress(progress)

    def _onTranslationDone(self, progress=None):
        """

        :param progress: 
        :return: 
        """
        self.translator.status.stop(progress)
