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


class TranslatorActions(object):

    @inject.params(config='config')
    def onActionSettingsClipboard(self, event=None, config=None):
        config.set('clipboard.scan', int(event))

    @inject.params(config='config')
    def onActionSettingsLowercase(self, event=None, config=None):
        config.set('clipboard.uppercase', int(event))

    @inject.params(config='config')
    def onActionSettingsSimilarities(self, event=None, config=None):
        config.set('clipboard.suggestions', int(event))

    @inject.params(config='config')
    def onActionSettingsCleaner(self, event=None, config=None):
        config.set('clipboard.extrachars', int(event))

    @inject.params(config='config')
    def onActionSettingsAllsources(self, event=None, config=None):
        config.set('translator.all', int(event))
