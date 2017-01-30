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
from di import container

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk


class AppListener(container.ContainerAware):
    _clipboard = None
    _application = None
    _scan = False

    def OnMenuIndicator(self, event, dispatcher):
        event.data.append(self._menu_checkbox('Scan clipboard', self.OnClipboardScan))
        event.data.append(self._menu_checkbox('Show all translations', self.OnTranslationsAll))
        event.data.append(self._menu_separator())

        service_translator = self.container.get('dictionary')
        for dictionary in service_translator.dictionaries:
            event.data.append(self._menu_item(dictionary.name))

    def OnMenuClipboard(self, event, dispatcher):
        self._clipboard = Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY)
        self._clipboard.connect("owner-change", self.OnClipboardChange)

    def OnClipboardChange(self, clipboard, event):
        client = self.container.get('dbus.dictionary.client')
        dispatcher = self.container.get('event_dispatcher')

        if not self._scan:
            return None

        text = clipboard.wait_for_text()
        text = text.decode('utf-8')
        if text is None or not len(text):
            return None

        event = dispatcher.new_event(text.strip())
        dispatcher.dispatch('kernel_event.window_clipboard', event)

        client.translate(text)

    def OnClipboardScan(self, item=None):
        self._scan = item.get_active()
        dispatcher = self.container.get('event_dispatcher')

        event = dispatcher.new_event(self._scan)
        dispatcher.dispatch('kernel_event.window_toggle_scanning', event)

    def OnTranslationsAll(self, item=None):
        dispatcher = self.container.get('event_dispatcher')

        event = dispatcher.new_event(item.get_active())
        dispatcher.dispatch('kernel_event.window_translate_all', event)

    def _menu_item(self, name):
        entity = Gtk.MenuItem(name)
        entity.show()
        return entity

    def _menu_checkbox(self, name, callback=None):
        entity = Gtk.CheckMenuItem(name)
        entity.connect("activate", callback)
        entity.set_active(False)
        entity.show()
        return entity

    def _menu_separator(self):
        element = Gtk.SeparatorMenuItem()
        element.show()
        return element
