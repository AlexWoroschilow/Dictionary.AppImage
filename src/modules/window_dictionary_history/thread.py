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

from .service import SQLiteHistory


class HistoryThread(QtCore.QThread):
    actionCount = QtCore.pyqtSignal(object)
    actionProgress = QtCore.pyqtSignal(object)
    actionRow = QtCore.pyqtSignal(object)

    def __del__(self):
        self.wait()

    def reload(self, event=None):
        return super(HistoryThread, self).start()

    @inject.params(history='history')
    def run(self, history: SQLiteHistory):
        self.actionProgress.emit(0)

        count = history.count()
        self.actionCount.emit(count)
        for index, (date, word, text) in enumerate(history.history, start=0):
            self.actionProgress.emit((index / count) * 100)
            self.actionRow.emit((index, date, word, text))

        self.actionProgress.emit(100)
