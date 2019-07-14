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


class TranslatorThread(QtCore.QThread):
    started = QtCore.pyqtSignal(int)
    startedSuggesting = QtCore.pyqtSignal(int)
    startedTranslating = QtCore.pyqtSignal(int)
    progress = QtCore.pyqtSignal(int, str)
    translation = QtCore.pyqtSignal(str, int)
    suggestion = QtCore.pyqtSignal(str, int)
    finished = QtCore.pyqtSignal(int)
    finishedSuggesting = QtCore.pyqtSignal(object)
    finishedTranslating = QtCore.pyqtSignal(object)

    stringSuggestions = None
    stringTranslations = None

    @inject.params(dictionary='dictionary', config='config')
    def _run_suggestions(self, word=None, dictionary=None, config=None):
        if word is None or not len(word):
            return None

        count = dictionary.suggestions_count(word)
        generator = dictionary.suggestions(word)
        if count is None or generator is None:
            return None

        self.startedSuggesting.emit(0)
        for index, suggestion in enumerate(generator, start=1):
            progress = index / float(count) * 100
            self.suggestion.emit(suggestion, progress)
        self.finishedSuggesting.emit((
            word, generator
        ))

    @inject.params(dictionary='dictionary', config='config')
    def _run_translations(self, word=None, dictionary=None, config=None):
        if word is None or not len(word):
            return None

        generator = dictionary.translate(word)
        count = dictionary.translation_count(word)
        if count is None or generator is None:
            return None

        self.startedTranslating.emit(0)
        for index, translation in enumerate(generator, start=1):
            progress = index / float(count) * 100
            self.translation.emit(translation, progress)
            if not int(config.get('translator.all')):
                break
        self.finishedTranslating.emit((
            word, generator
        ))

    def __del__(self):
        self.wait()

    def suggest(self, word=None, priority=QtCore.QThread.NormalPriority):
        super(TranslatorThread, self).start(priority)
        self.stringTranslations = word
        self.stringSuggestions = None

    def translate(self, string=None, priority=QtCore.QThread.NormalPriority):
        super(TranslatorThread, self).start(priority)
        self.stringTranslations = string
        self.stringSuggestions = string

    @inject.params(dictionary='dictionary', config='config')
    def run(self, dictionary, config):
        self.started.emit(0)

        if self.stringTranslations is not None:
            self._run_translations(self.stringTranslations)

        if self.stringSuggestions is not None:
            self._run_suggestions(self.stringSuggestions)

        self.finished.emit(100)
