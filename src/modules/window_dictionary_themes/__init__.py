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
import inject
import functools

from .actions import ModuleActions
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
        binder.bind_to_constructor('themes.action', ModuleActions)

    @inject.params(themes='themes')
    def boot(self, options=None, args=None, themes=None):
        from modules.window_dictionary_settings import gui as settings

        @settings.element()
        @inject.params(parent='settings.widget', actions='themes.action')
        def window_settings(parent=None, actions: ModuleActions = None):
            from .gui.settings.themes import WidgetSettingsThemes
            widget = WidgetSettingsThemes()

            action = functools.partial(actions.onActionTheme, widget=widget)
            widget.theme.connect(action)

            return widget
