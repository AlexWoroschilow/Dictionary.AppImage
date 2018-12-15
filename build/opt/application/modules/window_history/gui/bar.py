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
from PyQt5.Qt import Qt


class ToolbarRightWidget(QtWidgets.QToolBar):

    def __init__(self):
        super(ToolbarRightWidget, self).__init__()

        self.setOrientation(Qt.Vertical)

        icon = QtGui.QIcon('icons/csv.svg')
        self.csv = QtWidgets.QAction(icon, self.tr('Export to CSV'), self)
        self.addAction(self.csv)
        
        icon = QtGui.QIcon('icons/anki.svg')
        self.anki = QtWidgets.QAction(icon, self.tr('Export to Anki'), self)
        self.addAction(self.anki)
        self.addSeparator()
        icon = QtGui.QIcon('icons/trash.svg')
        self.clean = QtWidgets.QAction(icon, self.tr('Cleanup the history'), self)
        self.addAction(self.clean)
