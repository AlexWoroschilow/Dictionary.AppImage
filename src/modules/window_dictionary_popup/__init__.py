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

    @inject.params(parent='window', thread='translator.thread')
    def boot(self, options=None, args=None, parent=None, thread=None):
        from modules import window

        @window.toolbar(name='Pop-up', focus=True, position=0)
        @inject.params(translator='translator.widget')
        def window_toolbar(parent=None, translator=None):
            from .toolbar.panel import ToolbarWidget
            widget = ToolbarWidget()

            if not parent.actionReload: return widget
            parent.actionReload.connect(widget.reload)

            return widget

        if not parent.translationClipboardRequest: return None
        parent.translationClipboardRequest.connect(thread.translate)

        if not parent.translationScreenshotRequest: return None
        parent.translationScreenshotRequest.connect(thread.translate)

        if not thread.translated: return None
        thread.translated.connect(self.onTranslationFound)

    @inject.params(config='config')
    def onTranslationFound(self, translations, config):

        try:
            if self.popup: self.popup.close()
            if self.popup: self.popup = None
        except RuntimeError as ex:
            pass

        if not int(config.get('popup.enabled', 1)):
            return None

        if not translations:
            return None

        self.popup = TranslationDialog()
        self.popup.setText(translations)
        self.popup.show()

        if int(config.get('popup.frameless', 1)):
            self.popup.activated.connect(self.popup.close)

        if not int(config.get('popup.position', 0)):
            return None

        x = int(config.get('popup.x', 0))
        y = int(config.get('popup.y', 0))
        self.popup.move(x, y)
