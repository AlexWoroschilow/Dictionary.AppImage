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
import logging
import inject

import importlib.util
from lib.event import Dispatcher


class Kernel(object):
    def __init__(self, options=None, args=None, sources="src/**/module.py"):
        """
        
        :param self: 
        :param options: 
        :param args: 
        :param config: 
        :return: 
        """
        self._options = options
        self._sources = sources
        self._args = args
        self._loaders = []

        inject.configure(self.__init)

        for loader in self._loaders:
            loader.boot()

    def __init(self, binder):
        """
        
        :param binder: 
        :return: 
        """
        binder.bind('logger', logging.getLogger('app'))
        binder.bind('event_dispatcher', Dispatcher(logging.getLogger('ed')))

        for module_source in self.__modules(self._sources):
            module = importlib.import_module(module_source, True)
            with module.Loader(self._options, self._args) as loader:
                self._loaders.append(loader)
                if not loader.enabled:
                    continue
                binder.install(loader.config)

    def __modules(self, mask=None):
        """
        
        :param mask: 
        :return: 
        """
        collection = []
        logger = logging.getLogger('app')
        for source in glob.glob(mask):
            if os.path.exists(source):
                logger.debug("config: %s" % source)
                yield source[:-3].replace('/', '.')
