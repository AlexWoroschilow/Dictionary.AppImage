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
from .gui.scroll import SettingsScrollArea


class SettingsFactory(object):
    collection = []

    def addWidget(self, bundle=None):
        self.collection.append(bundle)

    @property
    def widget(self):
        widget = SettingsScrollArea()
        for bundle in sorted(self.collection, key=lambda x: x[1]):
            constructor, priority = bundle
            print(constructor, priority)
            if not callable(constructor):
                continue
            widget.addWidget(constructor())
        return widget
