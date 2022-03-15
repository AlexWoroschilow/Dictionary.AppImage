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
import functools


class Kernel(object):

    def __init__(self, options=None, args=None, sources=["plugins/**/__init__.py", "modules/**/__init__.py"]):

        self.modules = self.get_modules(sources, options, args)

        inject.configure(functools.partial(
            self.configure,
            modules=self.modules,
            options=options,
            args=args
        ))

        logger = logging.getLogger('kernel')
        for module in self.modules:
            if not hasattr(module, 'boot'):
                continue

            loader_boot = getattr(module, 'boot')
            if not callable(loader_boot):
                continue

            logger.debug("booting: {}".format(module))
            module.boot(options, args)

    @staticmethod
    def get_module_candidates(sources=None):
        for mask in sources:
            for source in glob.glob(mask):
                if not os.path.exists(source):
                    continue

                yield source.replace('/', '.') \
                    .replace('.py', '')

    def get_modules(self, sources=None, options=None, args=None):

        modules = []

        logger = logging.getLogger('kernel')
        for source in self.get_module_candidates(sources):
            try:

                module = importlib.import_module(source, False)
                logger.debug("found: {}".format(source))
                if not hasattr(module, 'Loader'):
                    continue

                module_class = getattr(module, 'Loader')
                with module_class() as loader:
                    if hasattr(loader, 'enabled'):
                        enabled = getattr(loader, 'enabled')
                        if callable(enabled) and not enabled(options, args):
                            continue

                    logger.debug("loading: {}".format(loader))
                    modules.append(loader)

            except (SyntaxError, RuntimeError) as err:
                logger.critical("{}: {}".format(source, err))
                continue

        return modules

    def configure(self, binder, modules, options=None, args=None):

        logger = logging.getLogger('kernel')
        for module in modules:

            try:

                if not hasattr(module, 'configure'):
                    continue

                configure = getattr(module, 'configure')
                if not callable(configure):
                    continue

                logger.debug("configuring: {}".format(module))

                binder.install(functools.partial(
                    module.configure,
                    options=options,
                    args=args
                ))

            except (SyntaxError, RuntimeError) as err:
                logger.critical("{}: {}".format(module, err))
                continue

        binder.bind('logger', logging.getLogger('app'))
        binder.bind('kernel', self)
