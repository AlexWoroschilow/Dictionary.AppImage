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
import functools

from lib.plugin import Loader

from .service import DictionaryManager
from .gui.widget import DictionaryWidget


class Loader(Loader):

    @property
    def enabled(self):
        if hasattr(self._options, 'converter'):
            return self._options.converter
        return True

    def config(self, binder=None):
        binder.bind_to_constructor('dictionary', self._service)
        binder.bind_to_provider('widget.dictionary', self._widget)

    @inject.params(window='window', widget='widget.dictionary')
    def boot(self, options=None, args=None, window=None, widget=None):
        if widget is not None and window is not None:
            window.addTab('Dictionaries', widget, False)

    @inject.params(config='config')
    def _service(self, config=None):
        print([
            config.get('dictionary.sources_system'),
            config.get('dictionary.sources_default'),
            config.get('dictionary.sources_user'),
        ])
        return DictionaryManager([
            config.get('dictionary.sources_system'),
            config.get('dictionary.sources_default'),
            config.get('dictionary.sources_user'),
        ])        

    @inject.params(dictionary='dictionary', config='config', statusbar='widget.statusbar')
    def _widget(self, dictionary=None, config=None, statusbar=None):
        widget = DictionaryWidget()
        for index, entity in enumerate(dictionary.dictionaries, start=1):
            widget.append(entity, int(config.get('dictionary.%s' % entity.unique)))

        widget.list.clicked.connect(functools.partial(
            self.onActionCheck, widget=widget.list
        ))
            
        if statusbar is not None and statusbar:
            statusbar.text('Total: %s dictionaries' % index)
            
        return widget

    @inject.params(config='config', dictionary='dictionary')
    def onActionCheck(self, index, widget, config, dictionary):
        item = widget.model().item(index.row())
        if item is None or not item:
            return None
        entity = item.data()
        if entity is None or not entity:
            return None
        
        var_name = 'dictionary.%s' % entity.unique
        var_value = int(item.checkState() > 0)
        if var_value == int(config.get(var_name)):
            return None
         
        config.set(var_name, var_value)
        dictionary.reload()
            
