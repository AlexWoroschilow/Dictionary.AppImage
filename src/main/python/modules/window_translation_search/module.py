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

from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5.Qt import Qt

from lib.plugin import Loader

from .gui.widget import SearchField


class Loader(Loader):

    @property
    def enabled(self):
        return True

    def config(self, binder=None):
        binder.bind_to_constructor('widget.translator_search', self._widget)

    @inject.params(window='window', widget='widget.translator_search')
    def boot(self, options=None, args=None, window=None, widget=None):
        if window is not None and widget is not None: 
            window.header.addWidget(widget)
    
    @inject.params(window='window')
    def _widget(self, window=None):
        
        widget = SearchField()
        widget.returnPressed.connect(functools.partial(
            self.onActionSearchRequest, widget=widget
        ))
        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+f"), widget)
        shortcut.activated.connect(functools.partial(
            self.onActionSearchShortcut, widget=widget
        ))
        
        return widget
    
    @inject.params(kernel='kernel')    
    def onActionSearchRequest(self, widget=None, kernel=None):
        kernel.dispatch('translate_text', widget.text())        

    @inject.params(kernel='kernel')  
    def onActionSearchShortcut(self, widget=None, kernel=None):
        widget.setFocusPolicy(Qt.StrongFocus)
        widget.setFocus()