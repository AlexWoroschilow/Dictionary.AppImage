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
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from .button import PictureButton


class HistoryToolbar(QtWidgets.QFrame):
    csv = QtCore.pyqtSignal(object)
    clean = QtCore.pyqtSignal(object)
    anki = QtCore.pyqtSignal(object)

    def __init__(self):
        super(HistoryToolbar, self).__init__()

        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        spacer = QtWidgets.QWidget()
        spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        layout.addWidget(spacer)

        self.buttonCsv = PictureButton(QtGui.QIcon('icons/csv'))
        self.buttonCsv.setToolTip('Export to CSV')
        self.buttonCsv.clicked.connect(self.csv.emit)
        layout.addWidget(self.buttonCsv)

        self.buttonAnki = PictureButton(QtGui.QIcon('icons/anki'))
        self.buttonAnki.setToolTip('Export to Anki')
        self.buttonAnki.clicked.connect(self.anki.emit)
        layout.addWidget(self.buttonAnki)

        self.buttonClean = PictureButton(QtGui.QIcon('icons/trash'))
        self.buttonClean.setToolTip('Cleanup the history')
        self.buttonClean.clicked.connect(self.clean.emit)
        layout.addWidget(self.buttonClean)
