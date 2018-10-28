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

from PyQt5 import QtGui
from lib.plugin import Loader


class Loader(Loader):
    isScanActiated = False

    @property
    def enabled(self):
        if hasattr(self._options, 'converter'):
            return not self._options.converter
        return True

    def config(self, binder=None):
        return None

    @inject.params(kernel='kernel', application='application')
    def boot(self, options=None, args=None, kernel=None, application=None):
        kernel.listen('window.clipboard.scan', self.onClipboardScan, 40)
        
        self.clipboard = application.clipboard()
        self.clipboard.selectionChanged.connect(self.onChangedSeletion)
        self.clipboard.dataChanged.connect(self.onChangedData)

    @inject.params(kernel='kernel')
    def onChangedData(self, kernel):
        if not self.isScanActiated:
            return None

        string = self.clipboard.text(QtGui.QClipboard.Selection)
        kernel.dispatch('window.clipboard.request', string)

    @inject.params(kernel='kernel')
    def onChangedSeletion(self, kernel):
        if not self.isScanActiated:
            return None

        string = self.clipboard.text(QtGui.QClipboard.Selection)
        kernel.dispatch('window.clipboard.request', string)

    @inject.params(kernel='kernel')
    def onClipboardScan(self, event, kernel):
        self.isScanActiated = event.data
