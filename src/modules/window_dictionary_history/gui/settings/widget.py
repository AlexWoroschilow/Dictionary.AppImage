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
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5 import QtGui

from . import SettingsTitle
from . import WidgetSettings

from .button import PictureButtonFlat


class SettingsWidget(WidgetSettings):
    collection = []

    @inject.params(config='config')
    def __init__(self, config=None):
        super(SettingsWidget, self).__init__()

        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(Qt.AlignLeft)
        self.setLayout(layout)

        self.layout().addWidget(SettingsTitle('History'))

        database = config.get('history.database')
        database = database.replace(os.path.expanduser('~'), '~')

        self.database = PictureButtonFlat(QtGui.QIcon('icons/save'), ' {}'.format(database))
        self.database.setToolTip("Choose history database folder")
        self.database.clicked.connect(self.onActionHistoryChoose)
        self.layout().addWidget(self.database)

    @inject.params(config='config')
    def reload(self, QEvent=None, config=None):

        database = config.get('history.database')
        database = database.replace(os.path.expanduser('~'), '~')

        self.database.setText(' {}'.format(database))

    @inject.params(config='config')
    def onActionHistoryToggle(self, event, config):
        value = '{}'.format(int(event))
        config.set('history.enabled', value)

    @inject.params(config='config', history='history.widget')
    def onActionHistoryChoose(self, event, config=None, history=None):
        selector = QtWidgets.QFileDialog()
        if not selector.exec_():
            return None

        for path in selector.selectedFiles():
            if path is None:
                continue

            if os.path.exists(path):
                message = self.tr("Are you sure you want to use the existed file '%s' ?" % path)
                reply = QtWidgets.QMessageBox.question(self, 'Are you sure?', message, QtWidgets.QMessageBox.Yes,
                                                       QtWidgets.QMessageBox.No)
                if reply == QtWidgets.QMessageBox.No:
                    continue

            config.set('history.database', '{}'.format(path))

        self.database.setText(' {}'.format(path))

        if history is not None:
            history.reload()
