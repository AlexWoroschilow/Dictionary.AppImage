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

from .widget import clipboard


class KernelEventSubscriber(event.EventSubscriberInterface):
    _container = None
    _clipboard = None
    _application = None

    @property
    def container(self):
        return self._container

    def set_container(self, container):
        self._container = container

    @property
    def subscribed_events(self):
        '''
        Get a list with all subscribed 
        events and theirs callbacks

        '''

        yield ('kernel_event.stop', ['on_stop', 0])
        yield ('kernel_event.window_toggle_scanning', ['on_toggle_scanning', 0])
        yield ('kernel_event.window_tab', ['on_notebook', 10])

    def on_notebook(self, event, dispatcher):
        '''
        Application is ready here
        to accept notebok pages from modules
        all servicea are initialized

        '''
 
        self._clipboard = clipboard.Clipboard(event.data, self.on_text)

    def on_toggle_scanning(self, event, dispatcher):
        '''
        Enable or disable clipboard scanning

        '''

        if event.data is not None and event.data:
            return self._clipboard.start_scan(self.on_text)
        return self._clipboard.stop_scan()

    def on_text(self, text):
        '''
        Get text from clipboard and fire
        an event to show an popup and son on

        '''
        dispatcher = self._container.get('event_dispatcher')
        if text is None or not len(text):
            return None

        event = dispatcher.new_event(text.strip())
        dispatcher.dispatch('clipboard_event.changed', event)

    def on_stop(self, event, dispatcher):
        '''
        Disable clipboard scanning

        '''

        self._clipboard.stop_scan()
