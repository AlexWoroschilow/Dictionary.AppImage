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
from PyQt5 import QtWidgets

from .actions import ModuleActions
from .gui import toolbar
from .gui import workspace
from .gui.window import MainWindow


class WindowTabFactory(object):

    def __init__(self):
        self.widgets = []

    def addWidget(self, widget=None):
        print(widget)


class CentralWidget(QtWidgets.QFrame):
    def __init__(self):
        super(CentralWidget, self).__init__()
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)


class Loader(object):
    actions = ModuleActions()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def configure(self, binder, options=None, args=None):

        binder.bind_to_constructor('window', self._widget)

        from .gui.content import WindowContent
        binder.bind_to_constructor('window.content', WindowContent)

        from .gui.header import HeaderWidget
        binder.bind_to_constructor('window.header', HeaderWidget)

        binder.bind_to_constructor('window.footer', self._widget_footer)

    @inject.params(config='config', content='window.content', header='window.header')
    def _widget(self, config=None, content=None, header=None):

        widget = MainWindow()

        widget.setCentralWidget(CentralWidget())
        widget.centralWidget().layout().addWidget(header)
        widget.centralWidget().layout().addWidget(content)

        widget.resizeAction.connect(self.actions.resizeActionEvent)

        width = int(config.get('window.width'))
        height = int(config.get('window.height'))
        widget.resize(width, height)

        return widget

    @inject.params(window='window')
    def _widget_header(self, window=None):
        if window.header is not None:
            return window.header
        return None

    @inject.params(window='window')
    def _widget_footer(self, window=None):
        if window.footer is not None:
            return window.footer
        return None
