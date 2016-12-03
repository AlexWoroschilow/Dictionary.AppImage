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
import logging
from datetime import datetime
from dateutil import parser
from collections import OrderedDict

import wx
import matplotlib

matplotlib.use('WXAgg')

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure


class StatisticPage(wx.Panel):
    _template = None

    def __init__(self, layout, parent):
        wx.Panel.__init__(self, parent)

        self.figure = Figure(facecolor='white')
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)

        self._label = wx.StaticText(self, -1, label='loading...')

        sizer1 = wx.BoxSizer(wx.VERTICAL)
        sizer1.Add(self.canvas, proportion=30, flag=wx.ALL | wx.EXPAND, border=layout.empty)
        sizer1.Add(self._label, proportion=1, flag=wx.ALL | wx.EXPAND, border=layout.border)

        self.SetSizer(sizer1)

    @staticmethod
    def _timestamp(string, hours=0, minutes=0, seconds=0):
        try:
            date = parser.parse(string).replace(hour=hours, minute=minutes, second=seconds)
            return int(date.strftime("%s"))
        except ValueError as error:
            logger = logging.getLogger('statistic')
            logger.error(error.message)
        return 0

    @property
    def history(self):
        pass

    @history.setter
    def history(self, history):
        collection = {}
        if history is None:
            return None

        for fields in history:
            index, date, word, description = fields
            timestamp = self._timestamp(date)
            if timestamp in collection:
                collection[timestamp] += 1
                continue
            collection[timestamp] = 1

        collection = OrderedDict(sorted(collection.items()))
        if collection is None:
            return None

        labels = [datetime.fromtimestamp(i).strftime("%d %b %y")
                  for i in collection.keys()]

        values = collection.values()
 
        positions = [i for i in range(0, len(labels))]
 
        self.axes.clear()
        if len(labels) > 1 and len(values) > 1:
            self.axes.plot(positions, values, linewidth=3.0)
 
        self.axes.set_xticks(positions)
        self.axes.set_xticklabels(labels, rotation=23, fontdict={'size': 9})
        self.axes.set_ylabel('Amount of words')
 
        message = "%s days history statistic" % len(labels)
        self._label.SetLabelText(message)
 
        self.canvas.draw()
