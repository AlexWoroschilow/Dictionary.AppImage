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
# distributed under the License is distributed on an "AS IS" BASIS, AAA
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import inject

from PyQt5 import QtCore

from .gui.dialog import TranslationDialog


class Loader(object):
    popup = None

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    @inject.params(config='config')
    def _popup(self, text, config):
        if not int(config.get('popup.enabled', 1)):
            return None

        popup = TranslationDialog()
        popup.setText(text)
        popup.show()

        return popup

    @inject.params(parent='window')
    def boot(self, options=None, args=None, parent=None):
        from modules.window_dictionary import gui as window

        @window.toolbar(name='Popup', focus=True, position=0)
        @inject.params(translator='translator.widget')
        def window_toolbar(parent=None, translator=None):
            from .toolbar.panel import ToolbarWidget
            widget = ToolbarWidget()
            parent.actionReload.connect(widget.reload)
            return widget

        parent.translationClipboardRequest.connect(self.onClipboardRequest)
        parent.translationScreenshotRequest.connect(self.onClipboardRequest)

    @inject.params(dictionary='dictionary', window='window', config='config')
    def onClipboardRequest(self, word, config, dictionary, window):
        if not int(config.get('popup.enabled', 1)):
            return None

        count = dictionary.translation_count(word)
        if not count: return None

        translation = dictionary.translate(word)
        if not translation: return None

        if int(config.get('popup.frameless', 1)):
            try:
                if self.popup: self.popup.close()
                if self.popup: self.popup = None
            except RuntimeError as ex:
                if self.popup: self.popup = None

            self.popup = self._popup(translation)
            self.popup.activated.connect(self.popup.close)
            if int(config.get('popup.position')):
                x = int(config.get('popup.x', 0))
                y = int(config.get('popup.y', 0))
                self.popup.move(x, y)
            return self.popup.exec_()

        if self.popup is not None:
            try:
                self.popup.setText(translation)
                self.popup.finished.connect(self.popup.close)
                self.popup.finished.connect(self.clear)
                return self.popup
            except RuntimeError as ex:
                pass

        self.popup = self._popup(translation)
        if int(config.get('popup.position')):
            x = int(config.get('popup.x', 0))
            y = int(config.get('popup.y', 0))
            self.popup.move(QtCore.QPoint(x, y))
        self.popup.finished.connect(self.popup.close)
        self.popup.finished.connect(self.clear)
        return self.popup.show()

    def clear(self):
        self.popup = None
