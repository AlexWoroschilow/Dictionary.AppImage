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
from datetime import datetime

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui


class ContainerHistory(object):
    def __init__(self, collection=None):
        """
        
        :param collection: 
        """
        self._collection = {}

        # if collection is not None:
        #     for entity in collection:
        #         index, date, word, translation = entity
        #
        #         date = datetime.strptime(date, '%Y.%m.%d %H:%M:%S')
        #         hash = date.strftime('%Y%m%d')
        #         if not self._collection.has_key(hash):
        #             self._collection[hash] = 1
        #             continue
        #         self._collection[hash] += 1

    def has(self, date):
        """
        
        :param date: 
        :return: 
        """
        date = datetime.strptime(date, '%Y.%m.%d')
        # return self._collection.has_key(date.strftime('%Y%m%d'))


class StatisticCalendar(QtWidgets.QCalendarWidget):
    def __init__(self, parent=None, history=None):
        """
        
        :param parent: 
        """
        self._container = ContainerHistory(history)

        QtWidgets.QCalendarWidget.__init__(self, parent)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setDateEditEnabled(False)

    def setHistory(self, history):
        """

        :param history: 
        :return: 
        """
        self._container = ContainerHistory(history)
        self.updateCells()

    def paintCell(self, painter, rect, date):
        """
        
        :param painter: 
        :param rect: 
        :param date: 
        :return: 
        """
        QtWidgets.QCalendarWidget.paintCell(self, painter, rect, date)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)

        if self._container.has(date.toString('yyyy.MM.dd')):
            painter.setPen(QtGui.QPen(QtGui.QColor(63, 171, 243, 100), 1))
            painter.setBrush(QtGui.QBrush(QtGui.QColor(63, 171, 243, 100)))
            painter.drawRect(rect)
