# -*- coding: utf-8 -*-
# Copyright 2015 Alex Woroschilow (alex.woroschilow@gmail.com)
# !!
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,!
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import os
import inject
import base64
import functools

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import Qt


class TranslatorThread(QtCore.QThread):
    progressAction = QtCore.pyqtSignal(object)
    wordAction = QtCore.pyqtSignal(object)

    def __init__(self, source=None):
        super(TranslatorThread, self).__init__()
        self.source = source

    def start(self, source=None, priority=None):
        super(TranslatorThread, self).start()
        self.source = source

    def run(self):
        if not os.path.exists(self.source):
            return None

        with open(self.source, 'r') as stream:
            index = 0
            limit = 200

            line = stream.readline()
            self.progressAction.emit(0)
            while len(line):
                line = line.strip("\n")
                if index is not None and index > 0:
                    self.wordAction.emit(line.split(','))
                line = stream.readline()
                if index > limit:
                    break
                index += 1
            self.progressAction.emit(index / limit * 200)
            stream.close()
