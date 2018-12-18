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
    progress = QtCore.pyqtSignal(int, str)
    translation = QtCore.pyqtSignal(int, str)
    suggestion = QtCore.pyqtSignal(int, str)
    finished = QtCore.pyqtSignal(int)

    string = None

    def translate(self, string=None, priority=QtCore.QThread.NormalPriority):
        super(TranslatorThread, self).start(priority)
        self.string = string

    @inject.params(dictionary='dictionary', config='config')
    def run(self, dictionary, config):
        self.started.emit(0)

        count = dictionary.translation_count(self.string)
        generator = dictionary.translate(self.string)
        if count is not None and generator is not None: 
            for index, translation in enumerate(generator, start=1):
                self.translation.emit((index / float(count) * 100), translation)
                if not int(config.get('translator.all')):
                    break
        self.finished.emit(100)

        count = dictionary.suggestions_count(self.string)
        generator = dictionary.suggestions(self.string)
        if count is not None and generator is not None: 
            for index, suggestion in enumerate(generator, start=1):
                self.suggestion.emit((index / float(count) * 100), suggestion)
        self.finished.emit(100)

    def __del__(self):
        self.wait()
