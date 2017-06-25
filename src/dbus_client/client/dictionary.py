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
import dbus
import logging

class DictionaryClient(object):
    _bus = None
    _translate = None
    
    def __init__(self):
        self._bus = dbus.SessionBus()

    
    def translate(self, word):
        logger = logging.getLogger('dbus-client')
        logger.debug('translate: %s' % word)
        try:
            service = self._bus.get_object('org.sensey.Dictionary', "/org/sensey/Dictionary")
            self._translate = service.get_dbus_method('translate', 'org.sensey.Dictionary.Translate')
            self._translate(word)
        except dbus.exceptions.DBusException as exception:
            logger.error(exception.get_dbus_message())

