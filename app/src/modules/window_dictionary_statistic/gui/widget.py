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

from .calendar import StatisticCalendar


class StatisticWidget(QtWidgets.QFrame):
    _bright = False
    _actions = False

    @inject.params(history='history')
    def __init__(self, history):
        super(StatisticWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.calendar = StatisticCalendar(self, history.history)
        self.calendar.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

    def resizeEvent(self, event):
        self.calendar.setFixedSize(self.size())

    def setHistory(self, history):
        self.calendar.setHistory(history)
