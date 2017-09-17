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
import di
from gettext import gettext as _
from .gui.widget import TranslatorWidget
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui


class FinderThread(QtCore.QThread):
    started = QtCore.pyqtSignal(int)
    progress = QtCore.pyqtSignal(int, int, str)
    finished = QtCore.pyqtSignal(int)

    def __init__(self, parent, dictionary):
        super(FinderThread, self).__init__()
        self.parent = parent
        self.dictionary = dictionary
        self.string = None

    def __del__(self):
        self.wait()

    def start(self, string=None, priority=QtCore.QThread.NormalPriority):
        super(FinderThread, self).start(priority)
        self.string = string

    def run(self):
        self.started.emit(0)
        count = len(list(self.dictionary.translate(self.string)))
        for index, translation in enumerate(self.dictionary.translate(self.string), start=1):
            self.progress.emit(index, (index / float(count) * 100), translation)
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

    # - {name: 'window.tab', method: 'OnTab', priority: 0}
    # - {name: 'clipboard_event.changed', method: 'OnClipboard', priority: 0}
    # - {name: 'kernel_event.service_transate', method: 'OnClipboard', priority: 0}

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

        self.loader = FinderThread(self, self.container.get('dictionary'))
        self.loader.started.connect(self._onLoaderStart)
        self.loader.progress.connect(self._onLoaderProgress)
        self.loader.finished.connect(self._onLoaderDone)
        # self.connect(self.loader, QtCore.SIGNAL("start(int)"), c)
        # self.connect(self.loader, QtCore.SIGNAL("progress(int, int)"), self._onLoaderProgress)
        # self.connect(self.loader, QtCore.SIGNAL("done(int)"), self._onLoaderDone)

        self.translator = TranslatorWidget()
        self.translator.onSearchString(self.onSearchString)
        self.translator.onSuggestionSelected(self.onSuggestionSelected)

        dictionary = self.container.get('dictionary')
        self.translator.setTranslation(dictionary.translate("welcome"))
        self.translator.setSuggestions(dictionary.suggestions("welcome"))

        event.data.addTab(self.translator, _('Translation'))

    def onSearchString(self, string):
        """
        
        :param string: 
        :return: 
        """
        dictionary = self.container.get('dictionary')
        self.translator.setTranslation(dictionary.translate(string))
        self.translator.setSuggestions(dictionary.suggestions(string))

        self.loader.start(string)

    def onSuggestionSelected(self, string):
        """
        
        :param string: 
        :return: 
        """
        dictionary = self.container.get('dictionary')
        self.translator.setTranslation(dictionary.translate(string))

    def _onLoaderStart(self, progress=None):
        """
        
        :param progress: 
        :return: 
        """
        self.translator.status.start(progress)
        self.translator.cleanTranslation()

    def _onLoaderProgress(self, index=None, progress=None, translation=None):
        """

        :param progress: 
        :return: 
        """
        self.translator.addTranslation(translation.encode('utf8'))
        self.translator.status.setProgress(progress)

    def _onLoaderDone(self, progress=None):
        """

        :param progress: 
        :return: 
        """
        self.translator.status.stop(progress)
