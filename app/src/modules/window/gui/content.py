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


class WindowContent(QtWidgets.QTabWidget):

    def __init__(self, parent=None):
        super(WindowContent, self).__init__(parent)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setTabPosition(QtWidgets.QTabWidget.West)
        self.setContentsMargins(0, 0, 0, 0)

    def insertTab(self, index, widget, name, focus=True):
        response = super(WindowContent, self).insertTab(index, widget, name)

        index = self.indexOf(widget)
        self.setCurrentIndex(index)

        return response
