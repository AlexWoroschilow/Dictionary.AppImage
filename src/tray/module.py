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
import lib.di as di
from .gui.tray import DictionaryTray
from gettext import gettext as _


class Loader(di.component.Extension):
    @property
    def config(self):
        return None

    @property
    def enabled(self):
        return True

    @property
    def subscribed_events(self):
        """

        :return: 
        """
        yield ('app.start', ['OnAppStart', 0])
        yield ('window.hide', ['OnWindowHide', 0])
        yield ('window.show', ['OnWindowShow', 0])

    def init(self, container):
        """

        :param container_builder: 
        :param container: 
        :return: 
        """
        self.container = container

    def OnAppStart(self, event, dispatcher):
        """
        
        :param event: 
        :param dispatcher: 
        :return: 
        """
        self.tray = DictionaryTray(event.data)
        self.tray.onActionScan(self.onActionScan)
        self.tray.onActionToggle(self.onActionToggle)
        self.tray.onActionExit(self.onActionExit)

    def onActionScan(self, event):
        """
        
        :param event: 
        :return: 
        """
        dispatcher = self.container.get('event_dispatcher')
        dispatcher.dispatch('window.clipboard.scan', event)

    def onActionToggle(self, event, status):
        """

        :param event: 
        :return: 
        """
        if status == True:
            dispatcher = self.container.get('event_dispatcher')
            dispatcher.dispatch('window.show')
            return True

        dispatcher = self.container.get('event_dispatcher')
        dispatcher.dispatch('window.hide')
        return True

    def OnWindowShow(self, event, dispatcher):
        """
        
        :param event: 
        :param dispatcher: 
        :return: 
        """
        self.tray.toggle.setText(_("Hide window"))
        self.tray.hidden = False

    def OnWindowHide(self, event, dispatcher):
        """

        :param event: 
        :param dispatcher: 
        :return: 
        """
        self.tray.toggle.setText(_("Show window"))
        self.tray.hidden = True

    def onActionExit(self, event):
        """

        :param event: 
        :return: 
        """
        dispatcher = self.container.get('event_dispatcher')
        dispatcher.dispatch('window.exit')
