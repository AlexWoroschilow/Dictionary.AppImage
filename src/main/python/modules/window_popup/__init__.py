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

from .gui.dialog import TranslationDialog


class Loader(object):

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def configure(self, binder, options=None, args=None):
        return None

    def enabled(self, options=None, args=None):
        if hasattr(self._options, 'converter'):
            return not self._options.converter
        return True

    @inject.params(window='window')
    def boot(self, options=None, args=None, window=None):
        window.translationClipboardRequest.connect(self.onClipboardRequest)
        window.suggestionClipboardRequest.connect(self.onClipboardRequest)

    @inject.params(dictionary='dictionary', window='window', config='config')
    def onClipboardRequest(self, word, config, dictionary, window):
        if word is None:
            return None

        if not dictionary.translation_count(word):
            return self.widget(['Nothing found'])

        translation = dictionary.translate(word)

        event = (word, translation)
        if int(config.get('clipboard.suggestions')):
            window.translationClipboardResponse.emit(event)
            return self.widget(translation)

        window.suggestionClipboardResponse.emit(event)
        return self.widget(translation)

    def widget(self, content):
        dialog = TranslationDialog()
        dialog.setText(content)
        return dialog.exec_()
