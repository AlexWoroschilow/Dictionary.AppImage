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
import di
import os


class Loader(di.component.Extension):

    @property
    def config(self):
        location = os.path.dirname(os.path.abspath(__file__))
        return '%s/config/services.yml' % location

    @property
    def enabled(self):
        if hasattr(self._options, 'converter'):
            return not self._options.converter
        if hasattr(self._options, 'tray'):
            return self._options.tray
        return False
