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
# from .gui.dialog import TranslationDialog
from lib.plugin import Loader


class Loader(Loader):
    def config(self, binder):
        """
        
        :return: 
        """

    @property
    def enabled(self):
        if hasattr(self._options, 'converter'):
            return not self._options.converter
        return True

    # @property
    # def subscribed_events(self):
    #     """
    #
    #     :return:
    #     """
    #     yield ('app.start', ['onAppStart', 0])
    #     yield ('window.clipboard.request', ['onClipboardRequest', 0])
    #
    # def init(self, container):
    #     """
    #
    #     :param container_builder:
    #     :param container:
    #     :return:
    #     """
    #     self.container = container
    #
    # def onAppStart(self, event, dispatcher):
    #     """
    #
    #     :param event:
    #     :param dispatcher:
    #     :return:
    #     """
    #     self.application = event.data
    #
    # def onClipboardRequest(self, event, dispatcher):
    #     """
    #
    #     :param event:
    #     :param dispatcher:
    #     :return:
    #     """
    #     word = self._text_clean(event.data)
    #     if word is None:
    #         return None
    #
    #     dictionary = self.container.get('dictionary')
    #     if dictionary.translation_count(word):
    #         dialog = TranslationDialog()
    #         dialog.setTranslation(dictionary.translate(word))
    #         dialog.exec_()
    #
    # @staticmethod
    # def _text_clean(text):
    #     if len(text) > 32:
    #         return None
    #     return ''.join(e for e in text if e.isalnum())
