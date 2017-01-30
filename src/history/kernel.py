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
from .widget.notebook import HistoryPage


class KernelEventSubscriber(container.ContainerAware):

    # Append custom page to common notebook
    def OnTab(self, event, dispatcher):
        layout = self.container.get('crossplatform.layout')
        page = HistoryPage(layout, event.data, self.OnHistoryChanged,
                           self.OnHistoryRemoved)
        event.data.AddPage(page, "Translation history")

    # Perform some actions if notebook
    # have been changed somehow
    def OnTabSwitched(self, event, dispatcher):
        (previous, current) = event.data
        if current.__class__.__name__.find('HistoryPage') != -1:
            current.history = self.container.get('history').history

    def OnHistoryChanged(self, values):
        index, date, word, description = values
        history = self.container.get('history')
        history.update(index, date, word, description)

    def OnHistoryRemoved(self, index):
        self.container.get('history').remove(index)
