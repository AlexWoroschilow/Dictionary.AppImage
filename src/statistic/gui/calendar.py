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

        if collection is not None:
            for entity in collection:
                index, date, word, translation = entity
                date = datetime.strptime(date, '%Y.%m.%d %H:%M:%S')
                hash = date.strftime('%Y%m%d')
                if not hash in self._collection:
                    self._collection[hash] = 1
                    continue
                self._collection[hash] += 1

    def has(self, date):
        """
        
        :param date: 
        :return: 
        """
        date = datetime.strptime(date, '%Y.%m.%d')
        return date.strftime('%Y%m%d') in self._collection


class StatisticCalendar(QtWidgets.QCalendarWidget):
    @inject.params(historyManager='history', logger='logger')
    def __init__(self, parent=None, historyManager=None, logger=None):
        """
        
        :param parent: 
        """
        self._container = ContainerHistory(
            historyManager.history
        )

        QtWidgets.QCalendarWidget.__init__(self, parent)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setDateEditEnabled(False)

    @inject.params(historyManager='history', logger='logger')
    def refresh(self, historyManager=None, logger=None):
        """

        :param history: 
        :return: 
        """
        self._container = ContainerHistory(
            historyManager.history
        )
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
