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
import os
import glob

import event
from pystardict import Dictionary
from .widget.notebook import DictionaryPage


class KernelEventSubscriber(event.EventSubscriberInterface):
    _container = None

    @property
    def container(self):
        return self._container

    def set_container(self, container):
        self._container = container

    @property
    def subscribed_events(self):
        yield ('kernel_event.window_tab', ['on_window_tab', 5])

    def on_window_tab(self, event, dispatcher):
        layout = self._container.get('crossplatform.layout')
        converter = self._container.get('dictionary_converter')

        page = DictionaryPage(layout, event.data, converter)
        page.dictionaries = self._dictionaries()

        event.data.AddPage(page, "External dictionaries")

    def _dictionaries(self):
        sources = [('~/.dictionary').replace('~', os.path.expanduser('~'))]
        while len(sources):
            source = sources.pop()
            for path in glob.glob(source):
                if os.path.isdir(path):
                    sources.append("%s/*" % path)
                    continue
                if path.find('.ifo') is not -1:
                    yield Dictionary(path.replace('.ifo', ''))

#     def on_started(self, event, dispatcher):
#         options = event.data
#         if options is None:
#             return None
# 
#         dictionaries = []
#         sources = [options.source.replace('~', os.path.expanduser('~'))]
#         while len(sources):
#             source = sources.pop()
#             for path in glob.glob(source):
#                 if os.path.isdir(path):
#                     sources.append("%s/*" % path)
#                     continue
#                 if path.find('.ifo') is not -1:
#                     dictionary = Dictionary(path.replace('.ifo', ''))
#                     dictionaries.append(dictionary)
# 
#         if options.list and not options.convert:
#             for dictionary in dictionaries:
#                 print(dictionary.name)
#             return None
# 
#         if options.source is None:
#             return None
# 
#         dictionary_converter = self._container.get('dictionary_converter')
#         for dictionary in dictionaries:
#             dictionary_converter.convert(dictionary)
#         return None



