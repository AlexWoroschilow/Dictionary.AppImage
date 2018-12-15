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
        kernel.listen('translate_clipboard', self.onClipboardRequest, 40)

    @inject.params(dictionary='dictionary')
    def onClipboardRequest(self, event, dictionary):
        if event.data is not None:
            if not dictionary.translation_count(event.data):
                return self.widget(['Nothing found'])
            
            translation = dictionary.translate(event.data)
            return self.widget(translation)

        return self.widget(['Nothing found'])

    def widget(self, content):
        dialog = TranslationDialog()
        dialog.setTranslation(content)
        return dialog.exec_()
        
