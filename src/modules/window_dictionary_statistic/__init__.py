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

from .gui.widget import StatisticWidget


class Loader(object):

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def configure(self, binder, options=None, args=None):
        binder.bind_to_constructor('statistic.widget', StatisticWidget)

    @inject.params(window='window', widget='statistic.widget')
    def boot(self, options, args, window=None, widget=None):
        from modules.window_dictionary import gui

        @gui.tab(name='Statistic', focus=False, position=1)
        @inject.params(widget='statistic.widget')
        def tab(parent=None, widget: StatisticWidget = None):
            return widget
