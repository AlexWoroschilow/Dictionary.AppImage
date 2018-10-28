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
import os
import inject

from lib.plugin import Loader

from .gui.dialog import TranslationDialog


class Loader(Loader):

    @property
    def config(self):
        return None

    @property
    def enabled(self):
        if hasattr(self._options, 'converter'):
            return not self._options.converter
        return True

    @inject.params(kernel='kernel')
    def boot(self, options=None, args=None, kernel=None):
        kernel.listen('window.clipboard.request', self.onClipboardRequest, 40)

    @staticmethod
    def _text_clean(text):
        if len(text) > 32:
            return None
        return ''.join(e for e in text if e.isalnum())

    @inject.params(dictionary='dictionary')
    def onClipboardRequest(self, event, dictionary):
        word = self._text_clean(event.data)
        if word is None:
            return None

        if dictionary.translation_count(word):
            dialog = TranslationDialog()
            dialog.setTranslation(dictionary.translate(word))
            dialog.exec_()

    
