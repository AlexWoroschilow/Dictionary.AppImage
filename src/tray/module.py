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
from gettext import gettext as _
from .gui.tray import DictionaryTray


class Loader(Loader):
    @property
    def enabled(self):
        """
        
        :return: 
        """
        return True

    def config(self, binder):
        """

        :param binder: 
        :return: 
        """

    @inject.params(dispatcher='event_dispatcher', logger='logger')
    def boot(self, dispatcher=None, logger=None):
        """

        :param event_dispatcher: 
        :return: 
        """
        dispatcher.add_listener('app.start', self.OnAppStart, 0)
        dispatcher.add_listener('window.hide', self.OnWindowHide, 0)
        dispatcher.add_listener('window.show', self.OnWindowShow, 0)

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

    @inject.params(dispatcher='event_dispatcher', logger='logger')
    def onActionScan(self, event, dispatcher=None, logger=None):
        """

        :param event:
        :return:
        """
        dispatcher.dispatch('window.clipboard.scan', event)

    @inject.params(dispatcher='event_dispatcher', logger='logger')
    def onActionToggle(self, event, status, dispatcher=None, logger=None):
        """

        :param event:
        :return:
        """
        if status == True:
            dispatcher.dispatch('window.show')
            return True

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

    @inject.params(dispatcher='event_dispatcher', logger='logger')
    def onActionExit(self, event, dispatcher=None, logger=None):
        """

        :param event:
        :return:
        """
        dispatcher.dispatch('window.exit')
