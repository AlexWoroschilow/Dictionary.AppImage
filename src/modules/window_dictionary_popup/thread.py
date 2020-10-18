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
    translated = QtCore.pyqtSignal(object)

    string = None

    def __del__(self):
        self.wait()

    def translate(self, string=None, priority=QtCore.QThread.NormalPriority):
        self.string = string
        super(TranslatorThread, self).start(priority)

    @inject.params(dictionary='dictionary', config='config')
    def run(self, dictionary, config):
        if not self.string:
            return None

        count = dictionary.translation_count(self.string)
        if not count: return None

        generator = dictionary.translate(self.string)
        if not generator: return None

        self.translated.emit(generator)
