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

    @inject.params(window='window')
    def boot(self, options=None, args=None, window=None):
        widget = DictionaryTray(window)
        widget.window.triggered.connect(self.onActionWindow)
        widget.scan.triggered.connect(self.onActionScan)
        widget.suggestions.triggered.connect(self.onActionSuggestions)
        widget.showall.triggered.connect(self.onActionShowAll)
        widget.exit.triggered.connect(self.onActionExit)
        widget.show()

    @inject.params(window='window')
    def onActionWindow(self, event, window):
        window.show()

    @inject.params(config='config')
    def onActionScan(self, event, config):
        config.set('clipboard.scan', int(event))

    @inject.params(config='config')
    def onActionSuggestions(self, event, config):
        config.set('clipboard.suggestions', int(event))

    @inject.params(config='config')
    def onActionShowAll(self, event, config):
        config.set('translator.all', int(event))

    @inject.params(window='window')
    def onActionExit(self, event, window):
        window.exit.emit(event)
