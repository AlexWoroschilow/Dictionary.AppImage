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
from PyQt5 import QtWidgets


class SettingsActions(object):

    @inject.params(config='config')
    def onActionScan(self, event, config, widget):
        config.set('clipboard.scan', '%s' % int(event))
        
    @inject.params(config='config')
    def onActionSuggestions(self, event, config, widget):
        config.set('clipboard.suggestions', '%s' % int(event))

    @inject.params(config='config')
    def onActionUpperCase(self, event, config, widget):
        config.set('clipboard.uppercase', '%s' % int(event))

    @inject.params(config='config')
    def onActionExtraChars(self, event, config, widget):
        config.set('clipboard.extrachars', '%s' % int(event))

    @inject.params(config='config')
    def onActionShowAll(self, event, config, widget):
        config.set('translator.all', '%s' % int(event))

    @inject.params(config='config')
    def onActionHistoryToggle(self, event, config, widget):
        config.set('history.enabled', '%s' % int(event))

    @inject.params(config='config', dictionary='dictionary')
    def onActionDictionaryChoose(self, event, widget=None, config=None, dictionary=None):
        path = str(QtWidgets.QFileDialog.getExistingDirectory(None, 'Select Directory'))
        
        if config is not None and len(path):
            config.set('dictionary.database', '%s' % path)
            
        if widget is not None and len(path):
            widget.setText(config.get('dictionary.database'))

        if dictionary is not None:
            dictionary.reload()

    @inject.params(config='config', history='widget.history')
    def onActionHistoryChoose(self, event, widget, config=None, history=None):
        path, mask = QtWidgets.QFileDialog.getOpenFileName(None, 'Select Directory')
        if config is not None and len(path):
            config.set('history.database', '%s' % path)
            
        if widget is not None and len(path):
            widget.setText(config.get('history.database'))

        if history is not None:
            history.reload()

