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
from datetime import datetime

from PyQt5 import QtWidgets
from PyQt5 import QtGui


class ContainerHistory(object):

    def __init__(self, collection=None):
        self._collection = {}

        if collection is None:
            return None

        for entity in collection:
            date, word, text = entity

            date = datetime.strptime(date, '%Y.%m.%d %H:%M:%S')
            hash = date.strftime('%Y%m%d')

            if hash not in self._collection.keys():
                self._collection[hash] = 1
                continue

            self._collection[hash] += 1

    def has(self, date):
        date = datetime.strptime(date, '%Y.%m.%d')
        return date.strftime('%Y%m%d') in self._collection.keys()


class StatisticCalendar(QtWidgets.QCalendarWidget):
    container = None

    def __init__(self, parent=None, history=None):
        self.container = ContainerHistory(history)

        QtWidgets.QCalendarWidget.__init__(self, parent)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setHorizontalHeaderFormat(QtWidgets.QCalendarWidget.ShortDayNames)
        self.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.NoVerticalHeader)
        self.setNavigationBarVisible(True)
        self.setDateEditEnabled(False)
        self.setGridVisible(True)

    def setHistory(self, history):
        self.container = ContainerHistory(history)
        self.updateCells()

    def paintCell(self, painter, rect, date):
        QtWidgets.QCalendarWidget.paintCell(self, painter, rect, date)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        if self.container.has(date.toString('yyyy.MM.dd')):
            painter.setPen(QtGui.QPen(QtGui.QColor(63, 171, 243, 100), 1))
            painter.setBrush(QtGui.QBrush(QtGui.QColor(63, 171, 243, 100)))
            painter.drawRect(rect)
