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

from .service import ServiceTheme


class Loader(object):

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def configure(self, binder, options, args):
        @inject.params(config='config')
        def themes_service(config=None):
            themes_default = config.get('themes.default', 'themes/')
            themes_custom = config.get('themes.custom', '~/.config/AOD-Dictionary/themes')

            return ServiceTheme([themes_default, themes_custom])

        binder.bind_to_constructor('themes', themes_service)

    @inject.params(themes='themes')
    def boot(self, options=None, args=None, themes=None):
        from modules import window

        @window.toolbar(name='Themes', focus=False, position=6)
        def window_toolbar(parent=None):
            from .toolbar.panel import ToolbarWidget
            widget = ToolbarWidget()
            parent.actionReload.connect(widget.reload)
            return widget
