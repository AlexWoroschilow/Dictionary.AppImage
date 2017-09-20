#
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

import yaml

import di.helper
import di.exceptions
from di.misc import OrderedDictYAMLLoader
from di.component import Definition, Reference, WeakReference


class Loader(object):
    def fix_config(self, config):
        for key, value in config.items():
            if isinstance(value, dict):
                config[key] = self.fix_config(value)
        return di.helper.Dict(config)


class YamlLoader(Loader):
    def support(self, source):
        return source[-3:] == 'yml'

    def load(self, source, container_builder):

        try:
            data = yaml.load(open(source).read(), OrderedDictYAMLLoader)
        except yaml.scanner.ScannerError as e:
            raise di.exceptions.LoadingError("file %s, \nerror: %s" % (source, e))

        for extension, config in data.items():
            if extension in ['parameters', 'services']:
                continue

            if config is None:
                config = {}

            container_builder.add_extension(extension, self.fix_config(config.copy()))

        if 'parameters' in data:
            for key, value in data['parameters'].items():
                container_builder.parameters.set(key, value)

        if 'services' in data:
            for index, meta in data['services'].items():

                if 'arguments' not in meta:
                    meta['arguments'] = []

                if 'class' not in meta:
                    meta['class'] = None

                if 'kwargs' not in meta:
                    meta['kwargs'] = {}

                if 'calls' not in meta:
                    meta['calls'] = []

                if 'tags' not in meta:
                    meta['tags'] = {}

                if 'abstract' not in meta:
                    meta['abstract'] = False

                definition = Definition(
                    clazz=meta['class'],
                    arguments=self.set_references(meta['arguments']),
                    kwargs=self.set_references(meta['kwargs']),
                    abstract=meta['abstract']
                )

                for call in meta['calls']:
                    if len(call) == 0:
                        continue

                    if len(call) == 2:
                        call.append({})

                    if len(call) == 1:
                        call.append([])
                        call.append({})

                    definition.method_calls.append(
                        (call[0], self.set_references(call[1]), self.set_references(call[2]))
                    )

                for tag, options in meta['tags'].items():
                    if options is None:
                        definition.add_tag(tag, None)
                        continue

                    for option in options:
                        definition.add_tag(tag, option)

                container_builder.add(index, definition)

    def set_reference(self, value):
        if di.helper.is_scalar(value) and value[0:1] == '@':
            if '#' in value:
                index, method = value.split("#")
                return Reference(index[1:], method)

            return Reference(value[1:])

        if di.helper.is_scalar(value) and value[0:2] == '#@':
            return WeakReference(value[2:])

        if di.helper.is_iterable(value):
            return self.set_references(value)

        return value

    def set_references(self, arguments):
        for pos in di.helper.get_keys(arguments):
            arguments[pos] = self.set_reference(arguments[pos])

        return arguments
