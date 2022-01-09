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
        from modules import window

        @window.toolbar(name='Clipboard', focus=False, position=3)
        @inject.params(translator='translator.widget')
        def window_toolbar(parent=None, translator=None):
            from .toolbar.panel import ToolbarWidget
            widget = ToolbarWidget()
            translator.actionReload.connect(widget.reload)
            return widget

        if not clipboard.selectionChanged: return None
        clipboard.selectionChanged.connect(self.onChangedSelection)

    @inject.params(window='window', config='config', clipboard='clipboard', cleaner='cleaner')
    def onChangedSelection(self, window, config, clipboard: QtGui.QClipboard, cleaner):
        if not int(config.get('clipboard.scan')):
            return None

        string = clipboard.text(QtGui.QClipboard.Selection)
        if not string: return None
        string = cleaner(string)
        if not string: return None

        clipboard.clear(QtGui.QClipboard.Selection)

        if int(config.get('clipboard.suggestions')):
            window.suggestionClipboardRequest.emit(string)
        return window.translationClipboardRequest.emit(string)
