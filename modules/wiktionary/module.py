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

from lib.plugin import Loader

from .services import Wiktionary


class Loader(Loader):

    @property
    def config(self):
        """
        get etc file with initialized
        services for this module

        :return: 
        """
        location = os.path.dirname(os.path.abspath(__file__))
        return '%s/config/services.yml' % location

    @property
    def enabled(self):
        """
        check if system needs to enable this module

        :return: 
        """
        if hasattr(self._options, 'wiktionary'):
            return self._options.wiktionary
        return False

    def post_build(self, container_builder, container):
        """

        :param container_builder: 
        :param container: 
        :return: 
        """
        container.add('wiktionary', Wiktionary(
            container.getOption('host'), container.getOption('port'),
            container.getOption('database'), container.getOption('user'),
            container.getOption('password')
        ))
