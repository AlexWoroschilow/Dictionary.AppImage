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

from .gui.tray import DictionaryTray


class Loader(object):

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def enabled(self, options=None, args=None):
        return True

    def configure(self, binder, options=None, args=None):
        return None

    @inject.params(window='window')
    def boot(self, options=None, args=None, window=None):
        widget = DictionaryTray(window)
        widget.scan.triggered.connect(self.onActionScan)
        widget.suggestions.triggered.connect(self.onActionSuggestions)
        widget.showall.triggered.connect(self.onActionShowAll)
        widget.exit.triggered.connect(self.onActionExit)

    @inject.params(config='config')
    def onActionScan(self, event, config):
        config.set('clipboard.scan', '%s' % int(event))

    @inject.params(config='config')
    def onActionSuggestions(self, event, config):
        config.set('clipboard.suggestions', '%s' % int(event))

    @inject.params(config='config')
    def onActionShowAll(self, event, config):
        config.set('translator.all', '%s' % int(event))

    @inject.params(kernel='kernel')
    def onActionExit(self, event, kernel):
        kernel.dispatch('window.exit')
