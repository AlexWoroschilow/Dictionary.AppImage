# -*- coding: utf-8 -*-
# Copyright 2014 Thomas Rabaix <thomas.rabaix@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import re
import os

import inspect
import importlib
import logging

from .exceptions import ParameterHolderIsFrozen
from .exceptions import UnknownParameter
from .exceptions import RecursiveParameterResolutionError
from .exceptions import UnknownService
from .exceptions import AbstractDefinitionInitialization
from .exceptions import CyclicReference
from .loader import YamlLoader
from .loader import Definition
from .loader import Reference
from .loader import WeakReference
from .helper import is_iterable
from .helper import get_keys
from .helper import deepcopy

from .proxy import Proxy


class Extension(object):
    def __init__(self, options=None):
        self._options = options

    @property
    def options(self):
        return self._options

    @property
    def config(self):
        return None

    @property
    def enabled(self):
        return False

    def __enter__(self):
        return self

    def load(self, config, container_builder):
        pass

    def post_load(self, container_builder):
        pass

    def pre_build(self, container_builder, container):
        pass

    def post_build(self, container_builder, container):
        pass

    def start(self, container):
        pass

    def __exit__(self, type, value, traceback):
        pass


class ParameterHolder(object):
    def __init__(self, parameters=None):
        self._parameters = parameters or {}
        self._frozen = False

    def set(self, key, value):
        if self._frozen:
            raise ParameterHolderIsFrozen(key)

        self._parameters[key] = value

    def get(self, key):
        if key in self._parameters:
            return self._parameters[key]

        raise UnknownParameter(key)

    def remove(self, key):
        del self._parameters[key]

    def has(self, key):
        return key in self._parameters

    def all(self):
        return self._parameters

    def freeze(self):
        self._frozen = True

    def is_frozen(self):
        return self._frozen == True


class ParameterResolver(object):
    def __init__(self, logger=None):
        self.re = re.compile("%%|%([^%\s]+)%")
        self.logger = logger
        self.stack = []

    def _resolve(self, parameter, parameter_holder):
        if isinstance(parameter, (tuple)):
            parameter = list(parameter)
            for key in get_keys(parameter):
                parameter[key] = self.resolve(parameter[key], parameter_holder)

            return tuple(parameter)

        if is_iterable(parameter):
            for key in get_keys(parameter):
                parameter[key] = self.resolve(parameter[key], parameter_holder)

            return parameter

        if not type(parameter) == str:
            return parameter

        if parameter[0:1] == '%' and parameter[-1] == '%' and parameter_holder.has(parameter[1:-1]):
            # if self.logger:
            #     self.logger.debug("   >> Match parameter: %s" % parameter[1:-1])

            return self.resolve(parameter_holder.get(parameter[1:-1]), parameter_holder)

        def replace(matchobj):
            if matchobj.group(0) == '%%':
                return '%'

            return self.resolve(parameter_holder.get(matchobj.group(1)), parameter_holder)

        # if self.logger:
        #     self.logger.debug("   >> Start resolving parameter: %s" % parameter)

        parameter, nums = re.subn(self.re, replace, parameter)

        # print parameter
        return parameter

    def resolve(self, parameter, parameter_holder):
        if parameter in self.stack:
            raise RecursiveParameterResolutionError(" -> ".join(self.stack) + " -> " + parameter)

        parameter = deepcopy(parameter)

        self.stack.append(parameter)
        value = self._resolve(parameter, parameter_holder)
        self.stack.pop()

        return value


class Container(object):
    _options = None

    def __init__(self):
        self.options = {}
        self.services = {}
        self.parameters = ParameterHolder()
        self.stack = []

    def has(self, index):
        return index in self.services

    def add(self, index, service):
        self.services[index] = service

    def get(self, index):
        if index not in self.services:
            raise UnknownService(index)

        return self.services[index]

    def setOptions(self, options):
        self._options = options

    def getOption(self, name, default=None):
        if hasattr(self._options, name):
            return getattr(self._options, name)
        return default


class ContainerBuilder(Container):
    _options = None

    def __init__(self, options=None):
        """
        
        :param options: 
        """
        logger = logging.getLogger('sc')
        self.parameter_resolver = ParameterResolver(logger)
        self.parameters = ParameterHolder()
        self._options = options
        self.extensions = {}
        self.services = {}
        self.stack = []

    def __load_configs(self, files):
        """
        
        :param files: 
        :return: 
        """
        logger = logging.getLogger('sc')
        for config in files:
            if os.path.isfile(config):
                for loader in [YamlLoader()]:
                    if loader.support(config):
                        logger.debug("Load file: %s" % config)
                        loader.load(config, self)

    def add_extension(self, name, config):
        self.extensions[name] = config

    def get_ids_by_tag(self, name):
        for index, definition in self.services.items():
            if definition.has_tag(name):
                yield index

    def build_container(self, files, container):
        """
        
        :param files: 
        :param container: 
        :return: 
        """
        logger = logging.getLogger('sc')
        logger.debug("Start building the container")
        container.setOptions(self._options)
        container.add("service_container", container)
        container.add("logger", logger)

        self.__load_configs(files)

        modules = []
        for name, config in self.extensions.items():
            logger.debug("Load extension: %s" % name)
            extension = self.get_class(Definition(name))(self._options)
            if not extension.enabled:
                continue
            extension.load(config, self)
            modules.append(extension)

        self.__load_configs([
            plugin.config for plugin in modules
            if plugin.config is not None
        ])

        for extension in modules:
            if hasattr(extension, 'post_load'):
                extension.post_load(self)

        for extension in modules:
            if hasattr(extension, 'pre_build'):
                extension.pre_build(self, container)

        for index, definition in self.services.items():
            if not definition.abstract:
                self.get_service(index, definition, container)

        dispatcher = container.get('event_dispatcher')
        for extension in modules:
            if hasattr(extension, 'subscribed_events'):
                dispatcher.add_subscriber(extension)

        for extension in modules:
            if hasattr(extension, 'post_build'):
                extension.post_build(self, container)
            if hasattr(extension, 'init'):
                extension.init(container)

        logger.debug("Building container is over")
        logger.debug("Starting resolving all parameters")
        for name, value in self.parameters.all().items():
            value = self.parameter_resolver.resolve(value, self.parameters)
            logger.debug("Resolve: %s" % name)
            container.parameters.set(name, value)
        return container

    def create_definition(self, index):
        """
        
        :param index: 
        :return: 
        """
        abstract = self.services[index]

        definition = Definition(
            clazz=abstract.clazz,
            arguments=deepcopy(abstract.arguments),
            kwargs=deepcopy(abstract.kwargs),
            abstract=False,
        )

        definition.method_calls = deepcopy(abstract.method_calls)
        definition.property_calls = deepcopy(abstract.property_calls)
        definition.tags = deepcopy(abstract.tags)

        return definition

    def get_class(self, definition):
        """
        
        :param definition: 
        :return: 
        """
        clazz = self.parameter_resolver.resolve(definition.clazz, self.parameters)

        if isinstance(clazz, list):
            module = clazz[0]
            function = clazz[1]
        else:
            module = ".".join(clazz.split(".")[0:-1])
            function = clazz.split(".")[-1]

        module = importlib.import_module(module)

        function = function.split(".")
        clazz = getattr(module, function[0])

        if len(function) == 2:
            return getattr(clazz, function[1])

        return clazz

    def get_instance(self, definition, container):
        """
        
        :param definition: 
        :param container: 
        :return: 
        """

        klass = self.get_class(definition)

        logger = logging.getLogger('sc')
        logger.debug("Create instance for %s" % klass)

        if inspect.isclass(klass) \
                or inspect.isfunction(klass) \
                or inspect.ismethod(klass):
            args = self.set_services(definition.arguments, container)
            kwargs = self.set_services(definition.kwargs, container)
            instance = klass(*args, **kwargs)
        else:
            # module object ...
            instance = klass

        for call in definition.method_calls:
            method, args, kwargs = call

            logger.debug("Call method: %s on class: %s" % (method, instance))

            attr = getattr(instance, method)

            if not attr:
                # handle property definition
                setattr(instance, method, self.set_services(args, container)[0])
            else:
                attr(*self.set_services(args, container), **self.set_services(kwargs, container))
            logger.debug("End creating instance %s" % instance)

        return instance

    def get_service(self, index, definition, container):
        """
        
        :param index: 
        :param definition: 
        :param container: 
        :return: 
        """
        logger = logging.getLogger('sc')
        if definition.abstract:
            message = "The ContainerBuilder try to build an abstract definition, index=%s, class=%s" % (
                index, definition.clazz)
            raise AbstractDefinitionInitialization(message)

        if container.has(index):
            return container.get(index)

        if index in self.stack:
            logger.error("CyclicReference: " + " -> ".join(self.stack) + " -> " + index)
            raise CyclicReference(" -> ".join(self.stack) + " -> " + index)

        self.stack.append(index)
        instance = self.get_instance(definition, container)
        container.add(index, instance)
        self.stack.pop()

        return instance

    def retrieve_service(self, value, container):
        """
        
        :param value: 
        :param container: 
        :return: 
        """
        if isinstance(value, (Reference, WeakReference)) \
                and not container.has(value.id) \
                and not self.has(value.id):
            raise UnknownService(value.id)

        if isinstance(value, (Reference)):
            service = None
            if container.has(value.id):
                service = container.get(value.id)
            if service is None:
                service = self.get_service(value.id, self.get(value.id), container)
            if value.method:
                return getattr(service, value.method)
            return service

        if isinstance(value, (WeakReference)):
            if container.has(value.id):
                return container.get(value.id)
            return Proxy(container, value.id)

        if isinstance(value, Definition):
            return self.get_instance(value, container)

        if is_iterable(value):
            return self.set_services(value, container)

        if isinstance(value, (tuple)):
            return tuple(self.set_services(list(value), container))

        return self.parameter_resolver.resolve(value, self.parameters)

    def set_services(self, arguments, container):
        """
        
        :param arguments: 
        :param container: 
        :return: 
        """
        for pos in get_keys(arguments):
            arguments[pos] = self.retrieve_service(arguments[pos], container)
        return arguments
