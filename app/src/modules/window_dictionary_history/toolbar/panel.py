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
from PyQt5.QtCore import Qt


class ToolbarWidget(QtWidgets.QFrame):

    @inject.params(config='config', actions='history.actions')
    def __init__(self, config=None, actions=None):
        super(ToolbarWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        from .button import ToolbarButton

        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.layout().setSpacing(0)

        self.history = ToolbarButton(self, "...", QtGui.QIcon('icons/history'))
        self.history.clicked.connect(self.onActionHistoryToggle)
        self.history.clicked.connect(self.reload)
        self.layout().addWidget(self.history, -1)

        database = config.get('history.database')
        database = os.path.basename(database)

        self.database = ToolbarButton(self, database, QtGui.QIcon('icons/open'))
        self.database.setToolTip("Choose history database folder")
        self.database.clicked.connect(self.onActionHistoryChoose)
        self.database.clicked.connect(self.reload)
        self.database.setCheckable(False)
        self.layout().addWidget(self.database, -1)

        self.export_csv = ToolbarButton(self, "Export as CSV", QtGui.QIcon('icons/csv'))
        self.export_csv.clicked.connect(self.onExportCsv)
        self.export_csv.clicked.connect(self.reload)
        self.export_csv.setCheckable(False)
        self.layout().addWidget(self.export_csv, -1)

        self.export_anki = ToolbarButton(self, "Export as Anki", QtGui.QIcon('icons/anki'))
        self.export_anki.clicked.connect(self.onExportAnki)
        self.export_anki.clicked.connect(self.reload)
        self.export_anki.setCheckable(False)
        self.layout().addWidget(self.export_anki, -1)

        self.cleanup = ToolbarButton(self, "Cleanup", QtGui.QIcon('icons/trash'))
        self.cleanup.clicked.connect(self.onActionCleanup)
        self.cleanup.clicked.connect(self.reload)
        self.cleanup.setCheckable(False)
        self.layout().addWidget(self.cleanup, -1)

        self.reload()

    @inject.params(config='config')
    def reload(self, event=None, config=None):
        database = config.get('history.database')
        self.database.setText(os.path.basename(database))
        self.database.setChecked(False)

        self.history.setChecked(int(config.get('history.enabled', 1)))
        self.history.setText('Enabled' if self.history.isChecked() else 'Disabled')

        self.export_csv.setChecked(False)
        self.export_csv.setCheckable(False)
        self.export_csv.setCheckable(False)

    @inject.params(config='config')
    def onActionHistoryToggle(self, event, config):
        config.set('history.enabled', '{}'.format(int(event)))

    @inject.params(config='config')
    def onActionHistoryChoose(self, event, config=None):
        database = config.get('history.database')

        selector = QtWidgets.QFileDialog()
        selector.setDirectory(os.path.expanduser(database))
        if not selector.exec_(): return None

        for path in selector.selectedFiles():
            if path is None: continue

            if os.path.exists(path):
                message = self.tr("Are you sure you want to use the existed file '{}' ?".format(path))
                reply = QtWidgets.QMessageBox.question(self, 'Are you sure?', message, QtWidgets.QMessageBox.Yes,
                                                       QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.No:
                    continue

            config.set('history.database', '{}'.format(path))

        self.database.setText(' {}'.format(path))

    @inject.params(config='config', history='history')
    def onExportCsv(self, event, config=None, history=None):
        selector = QtWidgets.QFileDialog()
        selector.setDirectory(os.path.expanduser('~'))
        if not selector.exec_(): return None

        for path in selector.selectedFiles():
            if len(path) and os.path.exists(path):
                message = self.tr("Are you sure you want to overwrite the file '%s' ?" % path)
                reply = QtWidgets.QMessageBox.question(self, 'Are you sure?', message, QtWidgets.QMessageBox.Yes,
                                                       QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.No:
                    break

            path = '{}.csv'.format(path.replace('.csv', ''))
            with open(path, 'w+') as stream:
                stream.write("\"Date\";\"Word\";\"Translation\"\n")
                for row in history.history:
                    date, word, description = row
                    stream.write("\"{}\";\"{}\";\"{}\"\n".format(date, word, description))
                stream.close()

    @inject.params(config='config', history='history')
    def onExportAnki(self, event, config=None, history=None):
        selector = QtWidgets.QFileDialog()
        selector.setDirectory(os.path.expanduser('~'))
        if not selector.exec_(): return None

        for path in selector.selectedFiles():
            if len(path) and os.path.exists(path):
                message = self.tr("Are you sure you want to overwrite the file '%s' ?" % path)
                reply = QtWidgets.QMessageBox.question(self, 'Are you sure?', message, QtWidgets.QMessageBox.Yes,
                                                       QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.No:
                    break

            path = '{}.csv'.format(path.replace('.csv', ''))
            print(path)
            with open(path, 'w+') as stream:
                stream.write("front,back\n")
                for row in history.history:
                    date, word, description = row
                    stream.write("{},{}\n".format(word, description))
                stream.close()

    @inject.params(config='config', history='history', widget='history.widget')
    def onActionCleanup(self, event, config=None, history=None, widget=None):

        message = self.tr("Are you sure you want to clean up the history?")
        reply = QtWidgets.QMessageBox.question(self, 'clean up the history?', message, QtWidgets.QMessageBox.Yes,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.No:
            return None

        history.clean()

        widget.history(history.history, history.count())
