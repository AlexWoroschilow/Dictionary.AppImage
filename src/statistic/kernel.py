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
from di import container

from src.statistic.widget import StatisticPage
from gettext import gettext as _


class AppListener(container.ContainerAware):
    def OnTab(self, event, dispatcher):
        layout = self.container.get('crossplatform.layout')
        service_history = self.container.get('history')

        statistic = StatisticPage(layout, event.data)
        statistic.history = service_history.history

        event.data.AddPage(statistic, _('Statistic'))

    # Perform some actions if notebook
    # have been changed somehow
    def OnTabSwitched(self, event, dispatcher):
        (previous, current) = event.data
        if current.__class__.__name__.find('StatisticPage') != -1:
            current.history = self.container.get('history').history
