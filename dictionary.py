#!/usr/bin/python

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
import optparse
import logging
import inject

from PyQt5 import QtWidgets
from PyQt5 import QtWebEngineWidgets
from lib.kernel import Kernel


class Application(QtWidgets.QApplication):
    def __init__(self, options=None, args=None):
        """
        
        :param options: 
        :param args: 
        """
        QtWidgets.QApplication.__init__(self, sys.argv)
        # self.setQuitOnLastWindowClosed(False)

        self.kernel = Kernel(options, args)

        self.main = MainWindow(None, self.kernel, options, args)
        self.main.setWindowTitle('Dictionary')

    @inject.params(dispatcher='event_dispatcher', logger='logger')
    def exec_(self, dispatcher=None, logger=None):
        """
        
        :param dispather: 
        :param logger: 
        :return: 
        """
        dispatcher.add_listener('window.show', self.onActionOpen)
        dispatcher.add_listener('window.hide', self.onActionHide)
        dispatcher.add_listener('window.exit', self.onActionExit)
        dispatcher.dispatch('app.start', self)

        return super(Application, self).exec_()

    def onActionOpen(self, event, dispatcher):
        """

        :param event: 
        :return: 
        """
        self.main.show()

    def onActionHide(self, event, dispatcher):
        """

        :param event: 
        :return: 
        """
        self.main.hide()

    def onActionExit(self, event, dispatcher):
        """

        :param event: 
        :return: 
        """

        self.exit()


class MainWindow(QtWidgets.QFrame):
    @inject.params(dispatcher='event_dispatcher', logger='logger')
    def __init__(self, parent=None, kernel=None, options=None, args=None, dispatcher=None, logger=None):
        """

        :param parent: 
        """

        super(MainWindow, self).__init__(parent)

        self.setMinimumHeight(400)
        self.setMinimumWidth(400)

        dispatcher.dispatch('kernel_event.window', self)

        self.tab = QtWidgets.QTabWidget(self)
        self.tab.setTabPosition(QtWidgets.QTabWidget.West)
        self.tab.setFixedSize(self.size())

        dispatcher.dispatch('window.tab', self.tab)

        self.show()

    @inject.params(dispatcher='event_dispatcher', logger='logger')
    def closeEvent(self, event, dispatcher=None, logger=None):
        """
        
        :param event: 
        :return: 
        """
        dispatcher.dispatch('window.hide')

    def resizeEvent(self, event):
        """

        :param event: 
        :return: 
        """
        self.tab.setFixedSize(event.size())


if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-t", "--tray", action="store_true", default=False, dest="tray", help="enable grafic user interface")
    parser.add_option("-g", "--gui", action="store_true", default=True, dest="gui", help="enable grafic user interface")
    parser.add_option("-w", "--word", default="baum", dest="word", help="word to translate")

    (options, args) = parser.parse_args()

    log_format = '[%(relativeCreated)d][%(name)s] %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=log_format)

    application = Application(options, args)
    sys.exit(application.exec_())
