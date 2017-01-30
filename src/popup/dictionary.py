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
import gi
import string
from di import container

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from .widget.popup import TranslationPopup


class AppListener(container.ContainerAware):
    _all = False
    _dictionary = None
    _window = None

    def __init__(self, container=None):
        self._window = TranslationPopup()
        self._window.connect("delete-event", Gtk.main_quit)
        self._window.hide()

    def OnTranslateAll(self, event, dispatcher):
        self._all = event.data

    def OnClipboard(self, event, dispatcher):
        dictionary = self.container.get('dictionary')
        word = self._text_clean(event.data)
        if not word:
            return None

        if self._all:
            translations = dictionary.translate(word)
            if translations is not None:
                return self._popup(word, translations)

        translation = dictionary.translate_one(word)
        if translation is not None:
            return self._popup(word, [translation])

    def _popup(self, word, translations):
        dispatcher = self.container.get('event_dispatcher')

        event = dispatcher.new_event([word, translations])
        dispatcher.dispatch('dictionary.translation', event)

        with open("%s/themes/popup.html" % os.getcwd(), 'r') as stream:
            self._window.content = stream.read() % string.join(translations, '')
        self._window.show_all()

    @staticmethod
    def _text_clean(text):
        if len(text) > 32:
            return None
        return ''.join(e for e in text if e.isalnum())
