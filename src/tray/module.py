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
        self.tray.onActionOpen(self.onActionOpen)
        self.tray.onActionScan(self.onActionScan)
        self.tray.onActionHide(self.onActionHide)
        self.tray.onActionExit(self.onActionExit)

    def onActionScan(self, event):
        """
        
        :param event: 
        :return: 
        """
        dispatcher = self.container.get('event_dispatcher')
        dispatcher.dispatch('window.clipboard.scan', event)

    def onActionOpen(self, event):
        """

        :param event: 
        :return: 
        """
        dispatcher = self.container.get('event_dispatcher')
        dispatcher.dispatch('window.show')

    def onActionHide(self, event):
        """

        :param event: 
        :return: 
        """
        dispatcher = self.container.get('event_dispatcher')
        dispatcher.dispatch('window.hide')

    def onActionExit(self, event):
        """

        :param event: 
        :return: 
        """
        dispatcher = self.container.get('event_dispatcher')
        dispatcher.dispatch('window.exit')
