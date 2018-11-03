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
import functools

from lib.plugin import Loader

from .service import DictionaryManager
from .gui.widget import DictionaryWidget


class Loader(Loader):

    @property
    def enabled(self):
        if hasattr(self._options, 'converter'):
            return self._options.converter
        return True

    def config(self, binder=None):
        binder.bind_to_constructor('dictionary', self._service)

    @inject.params(config='config')
    def _service(self, config=None):
        return DictionaryManager([config.get('dictionary.database'), ])        
