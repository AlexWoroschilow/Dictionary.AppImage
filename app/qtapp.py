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
import sys
import glob
from os.path import expanduser
from PyQt5 import QtWidgets as QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets



from kernel import Kernel


class Application(QtWidgets.QApplication):
    def __init__(self, options=None, args=None):
        QtWidgets.QApplication.__init__(self, sys.argv)

        self.kernel = Kernel(options, args)

        self.main = MainWindow(None, options, args)
        self.main.setWindowTitle('Dictionary')


        dispatcher = self.kernel.get('event_dispatcher')
        dispatcher.dispatch('kernel_event.window', self.main)


        tab = QtGui.QTabWidget(self.main)
        tab.setFixedWidth(self.main.width())
        tab.setFixedHeight(self.main.height())


        dispatcher.dispatch('window.tab', tab)

        self.main.show()


class MainWindow(QtWidgets.QFrame):
    def __init__(self, parent=None, options=None, args=None):
        """

        :param parent: 
        """

        QtGui.QWidget.__init__(self, parent)
        self.setMinimumWidth(1000)
        self.setMinimumHeight(800)

