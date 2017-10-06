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
from PyQt5 import QtCore
from PyQt5.Qt import Qt


class ToolbarbarWidget(QtWidgets.QToolBar):
    def __init__(self):
        super(ToolbarbarWidget, self).__init__()

        self.setOrientation(Qt.Vertical)

        icon = QtGui.QIcon('img/anki.png')
        self.anki = QtWidgets.QAction(icon, self.tr('Export to Anki'), self)
        self.addAction(self.anki)

        icon = QtGui.QIcon('img/csv.png')
        self.csv = QtWidgets.QAction(icon, self.tr('Export to CSV'), self)
        self.addAction(self.csv)

        icon = QtGui.QIcon('img/supermemo.png')
        self.superMemo = QtWidgets.QAction(icon, self.tr('Export to SuperMemo'), self)
        self.addAction(self.superMemo)

        icon = QtGui.QIcon.fromTheme('user-trash')
        self.clean = QtWidgets.QAction(icon, self.tr('Cleanup the history'), self)
        self.addAction(self.clean)





class StatusbarWidget(QtWidgets.QStatusBar):
    def __init__(self):
        super(StatusbarWidget, self).__init__()

        self.status = QtWidgets.QLabel()

        self.status.setAlignment(QtCore.Qt.AlignCenter)
        self.addWidget(self.status)

        self.progress = QtWidgets.QProgressBar()
        self.progress.hide()

    def text(self, text):
        """

        :param text: 
        :return: 
        """
        self.status.setText(text)

    def start(self, progress):
        """

        :param progress: 
        :return: 
        """
        if self.status is not None:
            self.status.hide()
            self.removeWidget(self.status)

        if self.progress is not None:
            self.progress.setValue(progress)
            self.addWidget(self.progress, 1)
            self.progress.show()

    def setProgress(self, progress):
        """

        :param progress: 
        :return: 
        """
        if self.progress is not None:
            self.progress.setValue(progress)

    def stop(self, progress):
        """

        :param progress: 
        :return: 
        """
        if self.progress is not None:
            self.progress.setValue(progress)
            self.progress.hide()
            self.removeWidget(self.progress)

        if self.status is not None:
            self.addWidget(self.status, 1)
            self.status.show()
