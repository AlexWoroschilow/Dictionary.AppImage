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

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

gi.require_version('Gdk', '3.0')
from gi.repository import Gdk

gi.require_version('WebKit', '3.0')
from gi.repository import WebKit


class TranslationPopup(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, Gtk.WindowType.POPUP)
        self.set_position(Gtk.WindowPosition.MOUSE)
        self.connect("event", self.on_popup_hide)
        self.set_default_size(400, 400)
        self.set_keep_above(True)
        self.add(self.scrolled_area)

    @property
    def content(self):
        pass

    @content.setter
    def content(self, value):
        self._web_view.load_html_string(value, 'text/html')

    @property
    def scrolled_area(self):
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.NEVER)
        scrolled_window.add(self.web_view)
        return scrolled_window

    @property
    def web_view(self):
        self._web_view = WebKit.WebView()
        self._web_view.can_go_back()
        return self._web_view

    def on_popup_hide(self, popup, event):
        if event.type in [
            Gdk.EventType.FOCUS_CHANGE,
            Gdk.EventType.LEAVE_NOTIFY,
            Gdk.EventType.BUTTON_RELEASE,
        ]:
            self.hide()
        return True