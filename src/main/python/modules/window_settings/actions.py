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
    def onActionShowAll(self, event, config, widget):
        config.set('translator.all', '%s' % int(event))

    @inject.params(config='config')
    def onActionDictionaryChoose(self, event, config, widget):
        selector = QtWidgets.QFileDialog()
        if not selector.exec_():
            return None
        
        for path in selector.selectedFiles():
            if len(path) and os.path.exists(path):
                message = widget.tr("Are you sure you want to overwrite the file '%s' ?" % path)
                reply = QtWidgets.QMessageBox.question(widget, 'Are you sure?', message, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.No:
                    break
        
            print(path, event, config, widget)

    @inject.params(config='config')
    def onActionHistoryToggle(self, event, config, widget):
        config.set('history.enabled', '%s' % int(event))

    @inject.params(config='config')
    def onActionHistoryChoose(self, event, config, widget):
        selector = QtWidgets.QFileDialog()
        if not selector.exec_():
            return None
        
        for path in selector.selectedFiles():
            if len(path) and os.path.exists(path):
                message = widget.tr("Are you sure you want to overwrite the file '%s' ?" % path)
                reply = QtWidgets.QMessageBox.question(widget, 'Are you sure?', message, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.No:
                    break
                
            print(path, event, config, widget)

