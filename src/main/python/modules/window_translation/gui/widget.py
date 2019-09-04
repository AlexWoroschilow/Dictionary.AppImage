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
from PyQt5 import QtCore
from PyQt5 import QtGui

from .suggestions import TranslationListWidget
from .browser import TranslationWidget
from .text import SearchField
from .button import PictureButtonFlat
from .button import PictureButtonDisabled


class TranslatorContainerDescription(QtWidgets.QFrame):
    settings = QtCore.pyqtSignal(object)
    search = QtCore.pyqtSignal(object)

    def __init__(self):
        super(TranslatorContainerDescription, self).__init__()
        self.setLayout(QtWidgets.QGridLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        test = PictureButtonDisabled(QtGui.QIcon("icons/folder"))
        self.layout().addWidget(test, 0, 0, 1, 1, QtCore.Qt.AlignTop)

        self.text = SearchField(self)
        self.text.returnPressed.connect(lambda x=None: self.search.emit(self.text.text()))
        self.layout().addWidget(self.text, 0, 1, 1, 18)

        settings = PictureButtonFlat(QtGui.QIcon("icons/settings"))
        settings.clicked.connect(lambda event=None: self.settings.emit(settings))
        self.layout().addWidget(settings, 0, 19, 1, 1, QtCore.Qt.AlignTop)

        self.translation = TranslationWidget(self)
        self.translation.setMinimumWidth(300)

        self.layout().addWidget(self.translation, 1, 0, 1, 20)

    def clean(self):
        self.translation.clear()

    def append(self, translation=None, progress=None):
        self.translation.addTranslation(translation)

    def replace(self, collection):
        self.translation.setTranslation(collection)


class TranslatorWidget(QtWidgets.QWidget):
    translationClear = QtCore.pyqtSignal(object)
    translationReplace = QtCore.pyqtSignal(object)
    translationAppend = QtCore.pyqtSignal(str, int)
    translationRequest = QtCore.pyqtSignal(object)
    translationSuggestion = QtCore.pyqtSignal(object)

    suggestionClean = QtCore.pyqtSignal(object)
    suggestionFinished = QtCore.pyqtSignal(object)
    suggestionAppend = QtCore.pyqtSignal(object)

    settings = QtCore.pyqtSignal(object)

    def __init__(self):
        super(TranslatorWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setContentsMargins(0, 0, 0, 0)

        self.suggestions = TranslationListWidget(self)
        self.suggestions.selected.connect(self.translationSuggestion.emit)

        self.translations = TranslatorContainerDescription()
        self.translations.search.connect(self.translationRequest.emit)
        self.translations.settings.connect(self.settings.emit)

        self.translationClear.connect(self.translations.clean)
        self.suggestionClean.connect(self.suggestions.clean)
        self.translationAppend.connect(self.translations.append)
        self.suggestionAppend.connect(self.suggestions.append)
        self.translationReplace.connect(self.translations.replace)

        self.layout = QtWidgets.QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        splitter = QtWidgets.QSplitter(self)
        splitter.setContentsMargins(0, 0, 0, 0)
        splitter.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        splitter.addWidget(self.suggestions)
        splitter.addWidget(self.translations)

        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 4)

        self.layout.addWidget(splitter, 1, 0)

    def finished(self, progress=None):
        model = self.suggestions.model()
        if model is None:
            return None
