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
import event
from .widget.notebook import StatisticPage


class KernelEventSubscriber(event.EventSubscriberInterface):
    _container = None

    @property
    def container(self):
        return self._container

    def set_container(self, container):
        self._container = container

    @property
    def subscribed_events(self):
        yield ('kernel_event.window_tab', ['on_window_tab', 2])
        yield ('kernel_event.notebook_changed', ['on_window_tab_changed', 1])

    def on_window_tab(self, event, dispatcher):
        layout = self._container.get('crossplatform.layout')
        service_history = self.container.get('history')

        statistic = StatisticPage(layout, event.data)
        statistic.history = service_history.history

        event.data.AddPage(statistic, "Translation statistic")

    # Perform some actions if notebook
    # have been changed somehow
    def on_window_tab_changed(self, event, dispatcher):
        (previous, current) = event.data
        if current.__class__.__name__.find('StatisticPage') != -1:
            current.history = self.container.get('history').history
