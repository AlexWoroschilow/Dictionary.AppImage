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
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.Qt import Qt


class ToolbarbarWidget(QtWidgets.QToolBar):
    def __init__(self):
        super(ToolbarbarWidget, self).__init__()

        self.setOrientation(Qt.Vertical)

        icon = QtGui.QIcon('themes/img/csv.png')
        self.csv = QtWidgets.QAction(icon, self.tr('Export to CSV'), self)
        self.csv.triggered.connect(self.OnExportCsv)
        self.addAction(self.csv)

        icon = QtGui.QIcon('themes/img/supermemo.png')
        self.superMemo = QtWidgets.QAction(icon, self.tr('Export to SuperMemo'), self)
        self.superMemo.triggered.connect(self.OnExportSuperMemo)
        self.addAction(self.superMemo)

        icon = QtGui.QIcon('themes/img/trash.png')
        self.clean = QtWidgets.QAction(icon, self.tr('Cleanup the history'), self)
        self.clean.triggered.connect(self.OnCleanHistory)
        self.addAction(self.clean)

    @inject.params(dispatcher='event_dispatcher', logger='logger')
    def OnExportSuperMemo(self, event=None, dispatcher=None, logger=None):
        """

        :param event: 
        :return: 
        """
        fileChooser = QtWidgets.QFileDialog()
        if fileChooser.exec_():
            for path in fileChooser.selectedFiles():

                if not os.path.exists(path):
                    dispatcher.dispatch('window.history.export', (path, 'SPM'))
                    continue

                message = self.tr("Are you sure you want to overwrite the file '%s' ?" % path)
                reply = QtWidgets.QMessageBox.question(self, 'Message', message, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.No:
                    continue

                dispatcher.dispatch('window.history.export', (path, 'SPM'))

    @inject.params(dispatcher='event_dispatcher', logger='logger')
    def OnExportCsv(self, event=None, dispatcher=None, logger=None):
        """
        
        :param event: 
        :return: 
        """
        fileChooser = QtWidgets.QFileDialog()
        if fileChooser.exec_():
            for path in fileChooser.selectedFiles():

                if not os.path.exists(path):
                    dispatcher.dispatch('window.history.export', (path, 'CSV'))
                    continue

                message = self.tr("Are you sure you want to overwrite the file '%s' ?" % path)
                reply = QtWidgets.QMessageBox.question(self, 'Message', message, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.No:
                    continue

                dispatcher.dispatch('window.history.export', (path, 'CSV'))

    @inject.params(dispatcher='event_dispatcher', logger='logger')
    def OnCleanHistory(self, event=None, dispatcher=None, logger=None):
        """

        :param event: 
        :return: 
        """
        message = self.tr("Are you sure you want to clean the history up?")
        reply = QtWidgets.QMessageBox.question(self, 'Message', message, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            dispatcher.dispatch('window.history.clean')


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
