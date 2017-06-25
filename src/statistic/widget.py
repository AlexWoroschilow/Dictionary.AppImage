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
from gettext import gettext as _

class Statistic(object):
    _collection = None

    def __init__(self, history):
        if history is None:
            return None

        self._collection = {}
        for fields in history:
            index, date, word, description = fields
            timestamp = self._timestamp(date)
            if timestamp in self._collection:
                self._collection[timestamp] += 1
                continue
            self._collection[timestamp] = 1

    @property
    def labels(self):
        return ["" for i in self.collection.keys()]

    @property
    def values(self):
        return self.collection.values()

    @property
    def collection(self):
        return OrderedDict(sorted(
            self._collection.items()
        ))

    @staticmethod
    def _timestamp(string, hours=0, minutes=0, seconds=0):
        try:
            date = parser.parse(string).replace(hour=hours, minute=minutes, second=seconds)
            return int(date.strftime("%s"))
        except ValueError as error:
            logger = logging.getLogger('statistic')
            logger.error(error.message)
        return 0


class StatisticPage(wx.Panel):
    _template = None

    def __init__(self, layout, parent):
        wx.Panel.__init__(self, parent)

        self.figure = Figure(facecolor='white')
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)

        self._label = wx.StaticText(self, -1, label=_('loading...'))
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.canvas, 1, wx.ALL | wx.EXPAND)
        sizer.Add(self._label, 0, wx.ALL | wx.EXPAND)

        self.SetSizer(sizer)

    @property
    def history(self):
        pass

    @history.setter
    def history(self, history):
        statistic = Statistic(history)
        if statistic.collection is None:
            return None

        self.axes.clear()
        self.axes.set_xticklabels(statistic.labels, rotation=23, fontdict={'size': 18})
        self.axes.grid(b=True, which='major', color='#c0c0c0', linestyle='-')
        self.axes.plot([i for i in range(0, len(statistic.values))], statistic.values, linewidth=5.0, color='green')
        self._label.SetLabelText("%s %s" % (len(statistic.labels), _('days history statistic')))

        self.canvas.draw()
