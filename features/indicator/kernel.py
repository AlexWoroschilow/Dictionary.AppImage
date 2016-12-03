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
import gi
import event

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


class KernelEventSubscriber(event.EventSubscriberInterface):
    _container = None
    _clipboard = None
    _application = None
    _scan = False

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
        yield ('kernel_event.indicator_menu', ['on_indicator_menu', 10])
        yield ('kernel_event.indicator_menu', ['on_indicator_clipboard', 10])

    def on_indicator_menu(self, event, dispatcher):
        '''
        Application is ready here
        to accept notebok pages from modules
        all servicea are initialized
        '''
        event.data.append(self._menu_checkbox('Scan clipboard', self.on_clipboard_scan))
        event.data.append(self._menu_checkbox('Show all translations', self.on_translations_all))
        event.data.append(self._menu_separator())

        service_translator = self._container.get('dictionary')
        for dictionary in service_translator.dictionaries:
            event.data.append(self._menu_item(dictionary.name))

    def on_indicator_clipboard(self, event, dispatcher):
        self._clipboard = Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY)
        self._clipboard.connect("owner-change", self.on_clipboard_change)

    def on_clipboard_change(self, clipboard, event):
        client = self._container.get('dbus.dictionary.client')
        dispatcher = self._container.get('event_dispatcher')

        if not self._scan:
            return None

        text = clipboard.wait_for_text()
        text = text.decode('utf-8')
        if text is None or not len(text):
            return None

        event = dispatcher.new_event(text.strip())
        dispatcher.dispatch('kernel_event.window_clipboard', event)

        client.translate(text)

    def on_clipboard_scan(self, item=None):
        '''
        Enable or disable clipboard scanning
        '''
        self._scan = item.get_active()
        dispatcher = self._container.get('event_dispatcher')

        event = dispatcher.new_event(self._scan)
        dispatcher.dispatch('kernel_event.window_toggle_scanning', event)

    def on_translations_all(self, item=None):
        '''
        Show all translations
        '''
        dispatcher = self._container.get('event_dispatcher')

        event = dispatcher.new_event(item.get_active())
        dispatcher.dispatch('kernel_event.window_translate_all', event)

    def _menu_item(self, name):
        '''
        Create indicator menu entry
        '''
        entity = Gtk.MenuItem(name)
        entity.show()
        return entity

    def _menu_checkbox(self, name, callback=None):
        '''
        Create indicator menu entry
        '''
        entity = Gtk.CheckMenuItem(name)
        entity.connect("activate", callback)
        entity.set_active(False)
        entity.show()
        return entity

    def _menu_separator(self):
        '''
        Create menu separator
        '''
        element = Gtk.SeparatorMenuItem()
        element.show()
        return element
