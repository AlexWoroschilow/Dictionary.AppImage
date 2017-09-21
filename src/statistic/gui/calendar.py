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
import functools

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui


class StatisticCalendar(QtWidgets.QCalendarWidget):
    def __init__(self, parent=None):
        QtWidgets.QCalendarWidget.__init__(self, parent)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setDateEditEnabled(False)

    def paintCell(self, painter, rect, date):
        QtWidgets.QCalendarWidget.paintCell(self, painter, rect, date)

        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        # painter.setBrush(QtGui.QBrush(QtGui.QColor("#17a81a")))
        # painter.drawRect(rect)

        # painter.translate(self.width() / 2.0, self.height() / 2.0)
        # painter.rotate(45)
        # painter.setBrush(QtGui.QBrush(self.gradient))
        # painter.drawPath(self.path)

        # painter.drawText(rect.center(), date.toString('d'))
