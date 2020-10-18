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
    frameless = None
    framed = None

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

    @inject.params(config='config')
    def _popup_frameless(self, text, popup: TranslationDialog = None, config=None):
        try:
            self.clear()
        except RuntimeError as ex:
            pass

        popup: TranslationDialog = self._popup(text)
        popup.activated.connect(popup.close)
        if not int(config.get('popup.position')):
            return popup

        x = int(config.get('popup.x', 0))
        y = int(config.get('popup.y', 0))
        popup.move(x, y)
        return popup

    @inject.params(config='config')
    def _popup_framed(self, text, popup: TranslationDialog = None, config=None):
        try:
            if not popup: self.clear()
            if popup: popup.setText(text)
            if popup: return popup
        except RuntimeError as ex:
            self.clear()

        popup: TranslationDialog = self._popup(text)
        if not int(config.get('popup.position')):
            return popup

        x = int(config.get('popup.x', 0))
        y = int(config.get('popup.y', 0))
        popup.move(QtCore.QPoint(x, y))

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
            self.frameless = self._popup_frameless(translation, self.frameless)
            return self.frameless.exec_()

        self.framed = self._popup_framed(translation, self.framed)
        return self.framed.show()

    def clear(self):
        try:
            if self.frameless: self.frameless.close()
            if self.frameless: self.frameless = None
        except RuntimeError as ex:
            pass

        try:
            if self.framed: self.framed.close()
            if self.framed: self.framed = None
        except RuntimeError as ex:
            pass
