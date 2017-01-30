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

gi.require_version('AppIndicator3', '0.1')
from gi.repository import AppIndicator3 as appindicator

from kernel import Kernel


class IndicatorGtk(object):

    _kernel = None
    _notebook = None

    def __init__(self, options=None, args=None):

        self._kernel = Kernel(options, args)
        dispatcher = self._kernel.get('event_dispatcher')

        self.__indicator = appindicator.Indicator.new(
                "Indicator Popup Dictionary",
                "/home/sensey/Projects/DictionaryIndicator/img/dictionary.svg",
                appindicator.IndicatorCategory.SYSTEM_SERVICES
        )
        self.__indicator.set_status(appindicator.IndicatorStatus.ACTIVE)

        event = dispatcher.new_event(Gtk.Menu())
        dispatcher.dispatch('indicator.menu', event)

        self.__indicator.set_menu(event.data)
        Gtk.main()

    def Destroy(self, event=None):
        dispatcher = self._kernel.get('event_dispatcher')
        dispatcher.dispatch('kernel.stop', dispatcher.new_event())
