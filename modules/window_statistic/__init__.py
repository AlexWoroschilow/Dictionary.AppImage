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

    def enabled(self, options=None, args=None):
        if hasattr(self._options, 'converter'):
            return not self._options.converter
        return True

    def configure(self, binder, options=None, args=None):
        binder.bind_to_constructor('widget.statistic', self._construct)

    @inject.params(window='window', widget='widget.statistic')
    def boot(self, options, args, window=None, widget=None):
        window.addTab(2, widget, 'Statistic', False)

    @inject.params(history='history')
    def _construct(self, history):
        return StatisticWidget(history)
