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

from lib.plugin import Loader

from .services import ConfigService


class Loader(Loader):

    @property
    def enabled(self):
        return True
    
    def config(self, binder=None):
        binder.bind_to_constructor('config', self._construct)

    @inject.params(kernel='kernel')
    def _construct(self, kernel=None):
        return ConfigService(kernel.options.config)

