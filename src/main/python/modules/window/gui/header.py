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
from PyQt5 import QtCore

from PyQt5.QtCore import Qt


class WidgetHeaderFactory(object):

    def __init__(self):
        self.widgets = []

    def addWidget(self, widget):
        self.widgets.append(widget)

    @property
    def widget(self):
        widget = WindowHeader()
        for header_widget in self.widgets:
            if isinstance(header_widget, QtWidgets.QAction):
                widget.header.addAction(header_widget)
            if isinstance(header_widget, QtWidgets.QWidget):
                widget.header.addWidget(header_widget)
        return widget


class WindowHeader(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(WindowHeader, self).__init__(parent)

        self.setContentsMargins(0, 0, 0, 0)

        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.setLayout(layout)
