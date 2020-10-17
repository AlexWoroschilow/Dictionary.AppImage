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
    collection = []

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    @inject.params(window='window')
    def boot(self, options=None, args=None, window=None):
        from modules.window_dictionary_settings import gui as settings

        @settings.element()
        def window_settings(parent=None):
            from .gui.settings.widget import SettingsWidget

            widget = SettingsWidget()
            parent.actionReload.connect(widget.reload)
            return widget

        window.translationClipboardRequest.connect(self.onClipboardRequest)
        window.translationScreenshotRequest.connect(self.onClipboardRequest)

    @inject.params(dictionary='dictionary', window='window', config='config')
    def onClipboardRequest(self, word, config, dictionary, window):
        if not int(config.get('popup.enabled', 1)):
            return None

        count = dictionary.translation_count(word)
        if not count: return None

        translation = dictionary.translate(word)
        if not translation: return None

        popup = TranslationDialog()
        self.collection.append(popup)

        popup.activated.connect(popup.close)
        popup.setText(translation)

        animation = QtCore.QPropertyAnimation(popup, b'size')
        animation.setEasingCurve(QtCore.QEasingCurve.Linear)
        animation.setStartValue(QtCore.QSize(50, 50))
        animation.setEndValue(QtCore.QSize(500, 300))
        animation.setDuration(100)
        animation.start()

        return popup.exec_()

    def cleanup(self, event=None):
        try:
            while len(self.collection):
                widget = self.collection.pop()
                if not widget: continue
                widget.close()

            if not event: return None
            return event.accept()
        except Exception as ex:
            if not event: return None
            return event.accept()
