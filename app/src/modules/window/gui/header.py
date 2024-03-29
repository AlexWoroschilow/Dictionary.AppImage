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


class HeaderWidget(QtWidgets.QTabWidget):
    actionReload = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        super(HeaderWidget, self).__init__(parent)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.setContentsMargins(0, 0, 0, 0)

    def insertTab(self, index, widget, name, focus=False):
        response = super(HeaderWidget, self).insertTab(index, widget, name)
        if not focus: return response

        index = self.indexOf(widget)
        self.setCurrentIndex(index)

        return response

    def event(self, QEvent):
        if type(QEvent) == QtCore.QEvent:
            if QEvent.type() == QtCore.QEvent.ShowToParent:
                self.actionReload.emit(())
        return super(HeaderWidget, self).event(QEvent)
