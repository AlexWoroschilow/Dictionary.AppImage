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
import platform
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore
import lib.di as di


class Loader(di.component.Extension):
    @property
    def config(self):
        return None

    @property
    def enabled(self):
        if hasattr(self._options, 'converter'):
            return not self._options.converter
        if platform.system() in ["Linux"]:
            return True
        return False

    @property
    def subscribed_events(self):
        """

        :return: 
        """
        yield ('kernel_event.window', ['OnWindow', 0])

    def init(self, container):
        """

        :param container_builder: 
        :param container: 
        :return: 
        """
        self.container = container

    def OnWindow(self, event, dispatcher):
        """
        
        :param event: 
        :param dispatcher: 
        :return: 
        """
        icon = QtGui.QIcon(os.path.abspath(os.path.curdir) + "/img/icon_osx.png")
        if not icon.isNull():
            event.data.setWindowIcon(icon)
