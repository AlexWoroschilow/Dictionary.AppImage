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

    def configure(self, binder, options=None, args=None):
        binder.bind_to_constructor('clipboard', QtWidgets.QApplication.clipboard)

    @inject.params(clipboard='clipboard')
    def boot(self, options=None, args=None, clipboard=None):
        from modules.window_dictionary_settings import gui as settings

        @settings.element()
        def window_settings(parent=None):
            from .gui.settings.widget import SettingsWidget
            return SettingsWidget()

        clipboard.selectionChanged.connect(self.onChangedSelection)
        clipboard.dataChanged.connect(self.onChangedData)

    @inject.params(config='config')
    def _clean(self, text, config=None):
        if len(text) >= 32:
            return None

        if int(config.get('clipboard.extrachars')):
            text = ''.join(e for e in text if e.isalnum())

        if int(config.get('clipboard.uppercase')):
            text = text.lower()

        return text

    @inject.params(window='window', config='config', clipboard='clipboard')
    def onChangedData(self, window, config, clipboard):
        if not int(config.get('clipboard.scan')):
            return None

        string = clipboard.text(QtGui.QClipboard.Selection)
        string = self._clean(string)
        if len(string) == 0:
            return None

        if int(config.get('clipboard.suggestions')):
            return window.translationClipboardRequest.emit(string)
        window.suggestionClipboardRequest.emit(string)

    @inject.params(window='window', config='config', clipboard='clipboard')
    def onChangedSelection(self, window, config, clipboard):
        if not int(config.get('clipboard.scan')):
            return None

        string = clipboard.text(QtGui.QClipboard.Selection)
        string = self._clean(string)

        if string is None or not len(string):
            return None

        if int(config.get('clipboard.suggestions')):
            return window.translationClipboardRequest.emit(string)
        return window.suggestionClipboardRequest.emit(string)
