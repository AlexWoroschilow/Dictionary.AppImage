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

from PyQt5 import QtGui
from PyQt5 import QtWidgets


class Loader(object):
    clipboard = None

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def enabled(self, options=None, args=None):
        if hasattr(self._options, 'converter'):
            return not self._options.converter
        return True

    def configure(self, binder, options=None, args=None):
        return None

    def boot(self, options=None, args=None):

        self.clipboard = QtWidgets.QApplication.clipboard()
        self.clipboard.selectionChanged.connect(self.onChangedSelection)
        self.clipboard.dataChanged.connect(self.onChangedData)

    @inject.params(config='config')
    def _clean(self, text, config=None):
        if len(text) >= 32:
            return None

        if int(config.get('clipboard.extrachars')):
            text = ''.join(e for e in text if e.isalnum())

        if int(config.get('clipboard.uppercase')):
            text = text.lower()

        return text

    @inject.params(window='window', config='config')
    def onChangedData(self, window, config):
        if not int(config.get('clipboard.scan')):
            return None

        string = self.clipboard.text(QtGui.QClipboard.Selection)
        window.translationClipboardRequest.emit(self._clean(string))

    @inject.params(window='window', config='config')
    def onChangedSelection(self, window, config):
        if not int(config.get('clipboard.scan')):
            return None

        string = self.clipboard.text(QtGui.QClipboard.Selection)
        window.translationClipboardRequest.emit(self._clean(string))
