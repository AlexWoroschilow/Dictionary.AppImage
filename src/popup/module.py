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
from lib.plugin import Loader
from .gui.dialog import TranslationDialog


class Loader(Loader):
    @property
    def enabled(self):
        """
        
        :return: 
        """
        if hasattr(self._options, 'converter'):
            return not self._options.converter
        return True

    def config(self, binder):
        """
        
        :return: 
        """

    @inject.params(dispatcher='event_dispatcher', logger='logger')
    def boot(self, dispatcher=None, logger=None):
        """

        :param event_dispatcher: 
        :return: 
        """
        dispatcher.add_listener('window.clipboard.request', self.OnClipboardRequest, 0)

    @inject.params(dictionary='dictionary', logger='logger')
    def OnClipboardRequest(self, event, dispatcher, dictionary=None, logger=None):
        """

        :param event:
        :param dispatcher:
        :return:
        """
        word = self._text_clean(event.data)
        if word is None:
            return None

        if not dictionary.translation_count(word):
            return None

        dialog = TranslationDialog()
        dialog.setTranslation(dictionary.translate(word))
        dialog.exec_()

    @staticmethod
    def _text_clean(text):
        if len(text) > 32:
            return None
        return ''.join(e for e in text if e.isalnum())
