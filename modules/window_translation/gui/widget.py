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
import functools
import inject

from PyQt5 import QtWidgets as QtGui

from .bar import StatusbarWidget
from .suggestions import TranslationListWidget
from .browser import TranslationWidget


class TranslatorWidget(QtGui.QWidget):
    _bright = False
    _actions = False

    def __init__(self):
        super(TranslatorWidget, self).__init__()
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.setContentsMargins(0, 0, 0, 0)
        self.setObjectName('TranslatorWidget')

        self.translation = TranslationWidget(self)
        self.translations = TranslationListWidget(self)

        self.layout = QtGui.QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        splitter = QtGui.QSplitter(self)
        splitter.setContentsMargins(0, 0, 0, 0)
        splitter.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)

        splitter.addWidget(self.translations)
        splitter.addWidget(self.translation)

        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        
        self.layout.addWidget(splitter, 1, 0)

    def clearTranslation(self):
        self.translation.clear()

    def addTranslation(self, translation):
        self.translation.addTranslation(translation)

    def setTranslation(self, collection):
        self.translation.setTranslation(collection)

    @inject.params(statusbar='widget.statusbar')
    def clearSuggestion(self, statusbar):
        self.translations.clear()
        statusbar.text('Total: %s words' % 0)

    @inject.params(statusbar='widget.statusbar')
    def addSuggestion(self, suggestion, statusbar):
        self.translations.append(suggestion)
        statusbar.text('Total: %s words' % self.translations.model().rowCount())

    @inject.params(statusbar='widget.statusbar')
    def setSuggestions(self, suggestions, statusbar):
        self.translations.setSuggestions(suggestions)
        statusbar.text('Total: %s words' % self.translations.model().rowCount())

    def onSuggestionSelected(self, action):
        self.translations.selectionChanged = functools.partial(
            self._onSuggestionSelected, action=(action)
        )

    def _onSuggestionSelected(self, current, previous, action=None):
        for index in self.translations.selectedIndexes():
            entity = self.translations.model().itemFromIndex(index)
            if action is not None:
                action(entity.text())
