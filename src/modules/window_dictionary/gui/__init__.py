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


@inject.params(window='window')
def tab(*args, **kwargs):
    name = kwargs.get('name', 'New Tab')
    position = kwargs.get('position', 0)
    focus = kwargs.get('focus', True)

    from .window import MainWindow
    window: MainWindow = kwargs.get('window')

    def wrapper1(*args, **kwargs):
        assert (callable(args[0]))

        widget = args[0](parent=window)
        window.addTab(position, widget, name, focus)

        return args[0]

    return wrapper1
