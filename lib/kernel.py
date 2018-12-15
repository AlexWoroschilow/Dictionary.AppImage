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

import importlib
from lib.event import Dispatcher


class Kernel(object):

    def __init__(self, application=None, options=None, args=None, sources="modules/**/module.py"):
        self._application = application
        self._options = options
        self._sources = sources
        self._args = args
        self._loaders = []

        inject.configure(self.__configure_dependencies)

        for loader in self._loaders:
            if hasattr(loader.__class__, 'boot') and \
            callable(getattr(loader.__class__, 'boot')):
                loader.boot(options, args)

        dispatcher = self.get('event_dispatcher')
        dispatcher.dispatch('kernel.start')

    @property
    def options(self):
        return self._options

    @property
    def args(self):
        return self._args

    def __configure_dependencies(self, binder):
        
        binder.bind('logger', logging.getLogger('app'))
        
        logger = logging.getLogger('dispatcher')
        binder.bind('event_dispatcher', Dispatcher(logger))

        logger = logging.getLogger('kernel')
        for module_source in self.__modules(self._sources):
            try:
                module = importlib.import_module(module_source, False)
                with module.Loader(self._options, self._args) as loader:
                    if not loader.enabled:
                        continue
                    
                    if hasattr(loader.__class__, 'config') and \
                    callable(getattr(loader.__class__, 'config')):
                            binder.install(loader.config)
                            
                    self._loaders.append(loader)
                    
            except (SyntaxError, RuntimeError) as err:
                logger.critical("%s: %s" % (module_source, err))
                continue

        binder.bind('application', self._application)
        binder.bind('kernel', self)

    def __modules(self, mask=None):
        logger = logging.getLogger('kernel')
        for source in glob.glob(mask):
            if os.path.exists(source):
                logger.debug("config: %s" % source)
                yield source[:-3].replace('/', '.')

    def get(self, name=None):
        container = inject.get_injector()
        return container.get_instance(name)

    def dispatch(self, name=None, event=None):
        dispatcher = self.get('event_dispatcher')
        dispatcher.dispatch(name, event)
        
    def listen(self, name=None, action=None, priority=0):
        dispatcher = self.get('event_dispatcher')
        dispatcher.add_listener(name, action, priority)

    def unlisten(self, name=None, action=None):
        dispatcher = self.get('event_dispatcher')
        dispatcher.remove_listener(name, action)

