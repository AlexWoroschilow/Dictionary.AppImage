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

    @inject.params(config='config')
    def _clean(self, text=None, config=None):

        if len(text) >= 32:
            return None

        if int(config.get('clipboard.extrachars')):
            text = ''.join(e for e in text if e.isalnum())

        if int(config.get('clipboard.uppercase')):
            text = text.lower()

        return text

    def configure(self, binder, options=None, args=None):
        binder.bind_to_constructor('clipboard', QtWidgets.QApplication.clipboard)

    @inject.params(clipboard='clipboard')
    def boot(self, options=None, args=None, clipboard=None):
        from modules.window_dictionary import gui as window

        @window.toolbar(name='Clipboard', position=1)
        @inject.params(translator='translator.widget')
        def window_toolbar(parent=None, translator=None):
            from .toolbar.panel import ToolbarWidget
            widget = ToolbarWidget()
            translator.actionReload.connect(widget.reload)
            return widget

        if not clipboard.selectionChanged: return None
        clipboard.selectionChanged.connect(self.onChangedSelection)

        # if not clipboard.dataChanged: return None
        # clipboard.dataChanged.connect(self.onChangedSelection)

    @inject.params(window='window', config='config', clipboard='clipboard')
    def onChangedSelection(self, window, config, clipboard: QtGui.QClipboard):
        if not int(config.get('clipboard.scan')):
            return None

        string = clipboard.text(QtGui.QClipboard.Selection)
        clipboard.clear(QtGui.QClipboard.Selection)
        if not string: return None

        string = self._clean(string)
        if not string: return None

        if int(config.get('clipboard.suggestions')):
            window.suggestionClipboardRequest.emit(string)
        return window.translationClipboardRequest.emit(string)
