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
import event

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from .widget.popup import TranslationPopup


class PopupEventSubscriber(event.EventSubscriberInterface):
    _all = False
    _container = None
    _dictionary = None
    _window = None

    def __init__(self, container=None):
        '''
        Class constructor create instance
        of our popup window here and hide
        this window a this time, show it
        only if some translations found
        '''
        self._window = TranslationPopup()
        self._window.connect("delete-event", Gtk.main_quit)
        self._window.hide()

    @property
    def container(self):
        return self._container

    def set_container(self, container):
        self._container = container

    @property
    def subscribed_events(self):
        '''
        Get a list with all subscribed
        events and theirs callbacks
        '''
        yield ('kernel_event.window_clipboard', ['on_clipboard', 10])
        yield ('kernel_event.window_translate_all', ['on_translate_all', 10])

    def on_translate_all(self, event, dispatcher):
        '''
        Enable or disable all
        translations in popup window
        '''
        self._all = event.data

    def on_clipboard(self, event, dispatcher):
        '''
        Catch clipboard event (clipboard text has been changed)
        and display popup with a translation,
        if it has been found
        '''
        dictionary = self._container.get('dictionary')
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
        '''
        Show popup with given content
        '''
        dispatcher = self._container.get('event_dispatcher')

        event = dispatcher.new_event([word, translations])
        dispatcher.dispatch('dictionary.translation', event)

        with open("%s/themes/popup.html" % os.getcwd(), 'r') as stream:
            self._window.content = stream.read() % string.join(translations, '')
        self._window.show_all()

    @staticmethod
    def _text_clean(text):
        '''
        Remove special characters, empty spaces
        and check for maximal word 
        Limit to translate Tree
        '''
        if len(text) > 32:
            return None

        return ''.join(e for e in text if e.isalnum())
