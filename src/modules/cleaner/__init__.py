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


class Loader(object):

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    @staticmethod
    def provider():

        @inject.params(config='config')
        def clean(text=None, config=None):
            if not text: return None

            if len(text) >= 32:
                return None

            if int(config.get('clipboard.extrachars')):
                text = ''.join(e for e in text if e.isalnum())

            if int(config.get('clipboard.uppercase')):
                text = text.lower()

            return text

        return clean

    def configure(self, binder, options=None, args=None):
        binder.bind_to_provider('cleaner', self.provider)
