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
from kernel import Kernel


class Console(object):
    _kernel = None
    _notebook = None

    def __init__(self, options=None, args=None):
        self._kernel = Kernel(options, args)

    def MainLoop(self, options=None, args=None):
        dispatcher = self._kernel.get('event_dispatcher')
        dispatcher.dispatch('kernel_event.start', options)

