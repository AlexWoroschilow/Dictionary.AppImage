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

    def configure(self, binder, options=None, args=None):
        return None

    @inject.params(window='window')
    def boot(self, options=None, args=None, window=None):
        window.translationClipboardRequest.connect(self.onClipboardRequest)
        window.suggestionClipboardRequest.connect(self.onClipboardRequest)

    @inject.params(dictionary='dictionary', window='window', config='config')
    def onClipboardRequest(self, word, config, dictionary, window):
        if word is None: return None

        if not dictionary.translation_count(word):
            return None

        translation = dictionary.translate(word)

        event = (word, translation)
        if int(config.get('clipboard.suggestions')):
            window.translationClipboardResponse.emit(event)
            popup = self.widget(translation)
            self.collection.append(popup)

            animation = QtCore.QPropertyAnimation(popup, b'size')
            animation.setEasingCurve(QtCore.QEasingCurve.Linear)
            animation.setStartValue(QtCore.QSize(50, 50))
            animation.setEndValue(QtCore.QSize(500, 300))
            animation.setDuration(100)
            animation.start()

            return popup.exec_()

        window.suggestionClipboardResponse.emit(event)
        popup = self.widget(translation)
        self.collection.append(popup)

        animation = QtCore.QPropertyAnimation(popup, b'size')
        animation.setEasingCurve(QtCore.QEasingCurve.Linear)
        animation.setStartValue(QtCore.QSize(50, 50))
        animation.setEndValue(QtCore.QSize(500, 300))
        animation.setDuration(100)
        animation.start()

        return popup.exec_()

    def widget(self, content):

        dialog = TranslationDialog()
        dialog.activated.connect(self.cleanup)
        dialog.setText(content)

        return dialog

    def cleanup(self, event=None):
        try:
            while len(self.collection):
                widget = self.collection.pop()
                if widget is None:
                    continue
                widget.close()

            if event is None:
                return None
            return event.accept()
        except Exception as ex:
            if event is None:
                return None
            return event.accept()
