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
import glob
import os

from di import container
from pystardict import Dictionary

from src.converter.widget import DictionaryPage


class AppListener(container.ContainerAware):
    def OnTab(self, event, dispatcher):
        layout = self.container.get('crossplatform.layout')
        converter = self.container.get('dictionary_converter')

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
