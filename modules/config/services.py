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
import configparser


class ConfigService(object):
    _parser = None

    def __init__(self, file=None):
        self._file = file
        self._parser = configparser.ConfigParser()
        if os.path.exists(self._file):
            self._parser.read(self._file)
            return None
                    
        folder = os.path.dirname(self._file)
        if not os.path.exists(folder):
            os.makedirs(folder)

        with open(self._file, 'w') as stream:
            self._parser.add_section('window')
            self._parser.set('window', 'width', '950')
            self._parser.set('window', 'height', '600')

            self._parser.add_section('folders')
            self._parser.set('folders', 'toolbar', '1')
            self._parser.set('folders', 'keywords', '1')

            self._parser.add_section('editor')
            self._parser.set('editor', 'leftbar', '1')
            self._parser.set('editor', 'formatbar', '1')
            self._parser.set('editor', 'rightbar', '1')
            self._parser.set('editor', 'name', '1')

            self._parser.add_section('storage')
            self._parser.set('storage', 'location', '~/owncloud/CloudNotes/')
            
            self._parser.write(stream)
            stream.close()
            
        self._parser.read(self._file)
        return None

    def get(self, name, default=None):
        section, option = name.split('.')
        if not self._parser.has_section(section):
            return None
        if self._parser.has_option(section, option):
            return self._parser.get(section, option)
        return None

    def set(self, name, value=None):
        section, option = name.split('.')
        
        if not self._parser.has_section(section):
            self._parser.add_section(section)
        
        self._parser.set(section, option, value)
        with open(self._file, 'w') as stream:
            self._parser.write(stream)
            stream.close()

