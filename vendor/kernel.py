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
import di
import glob
import logging


class Kernel(object):
    _logger = None
    _container = None

    def __init__(self, options=None, args=None, config="config/*.yml"):
        container = di.build(options, self.__configs(config))
        dispatcher = container.get('event_dispatcher')

        event = dispatcher.new_event()
        dispatcher.dispatch('kernel_event.load', event)

        self._container = container

    def __configs(self, mask):
        collection = []
        logger = logging.getLogger('app')
        for source in glob.glob(mask):
            if os.path.exists(source):
                logger.debug("config: %s" % source)
                collection.append(source)
        return collection

    def get(self, name):
        if self._container.has(name):
            return self._container.get(name)
        return None

