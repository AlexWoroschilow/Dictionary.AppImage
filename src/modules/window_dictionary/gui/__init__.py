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


@inject.params(window='window', content='window.content')
def tab(*args, **kwargs):
    name = kwargs.get('name', 'New Tab')
    position = kwargs.get('position', 0)
    focus = kwargs.get('focus', True)

    from .window import MainWindow
    from .content import WindowContent
    content: WindowContent = kwargs.get('content')
    window: MainWindow = kwargs.get('window')

    def wrapper1(*args, **kwargs):
        assert (callable(args[0]))

        widget = args[0](parent=window)
        content.insertTab(position, widget, name, focus)

        return args[0]

    return wrapper1


@inject.params(window='window', header='window.header')
def toolbar(*args, **kwargs):
    name = kwargs.get('name', 'New Tab')
    position = kwargs.get('position', 0)
    focus = kwargs.get('focus', True)

    from .window import MainWindow
    from .header import ToolbarWidget
    header: ToolbarWidget = kwargs.get('header')

    def wrapper1(*args, **kwargs):
        assert (callable(args[0]))

        widget_class = args[0]
        if not widget_class: return None

        widget = widget_class(parent=header)
        header.insertTab(position, widget, name, focus)

        return widget_class

    return wrapper1
