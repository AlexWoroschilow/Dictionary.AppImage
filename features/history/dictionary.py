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


class HistoryEventSubscriber(event.EventSubscriberInterface):
    _container = None

    @property
    def container(self):
        return self._container

    def set_container(self, container):
        self._container = container

    @property
    def subscribed_events(self):
        yield ('dictionary.translation', ['on_dictionary_translation', 0])

    def on_dictionary_translation(self, event, dispatcher):
        word, translation = event.data
        self.container.get('history').add(word, translation)
