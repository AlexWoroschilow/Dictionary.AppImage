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

from .menu.container import MenuContainerWidget


class ToolbarWidget(QtWidgets.QScrollArea):

    @inject.params(config='config', dictionary='dictionary')
    def __init__(self, config=None, dictionary=None):
        super(ToolbarWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)

        self.setContentsMargins(0, 0, 0, 0)

        from .button import ToolbarButton

        self.container = QtWidgets.QWidget()
        self.container.setLayout(QtWidgets.QHBoxLayout())
        self.container.layout().setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.setWidget(self.container)

        self.database = ToolbarButton(self, "Location", QtGui.QIcon('icons/dictionaries'))
        self.database.setToolTip(config.get('dictionary.database'))
        self.database.clicked.connect(self.onSelectDatabase)
        self.database.setChecked(False)
        self.addWidget(self.database)

        self.dropdown = ToolbarButton(self, "Dictionaries", QtGui.QIcon('icons/book'))
        self.dropdown.setToolTip('dropdown menu')
        self.dropdown.clicked.connect(self.onToggleMenu)
        self.dropdown.setChecked(False)
        self.addWidget(self.dropdown)

    def addWidget(self, widget):
        self.container.layout().addWidget(widget, -1)

    @inject.params(themes='themes')
    def onToggleMenu(self, event, themes):

        widget = MenuContainerWidget()
        widget.setStyleSheet(themes.get_stylesheet())
        widget.toggleDictionary.connect(self.onToggleDictionary)

        container = QtWidgets.QWidgetAction(self)
        container.setDefaultWidget(widget)

        menu = QtWidgets.QMenu()
        menu.addAction(container)
        menu.aboutToHide.connect(lambda x=None: self.dropdown.setChecked(False))
        menu.setStyleSheet(themes.get_stylesheet())

        menu.exec_(QtGui.QCursor.pos())

    @inject.params(config='config', dictionary='dictionary')
    def onToggleDictionary(self, event, entity, config, dictionary):

        var_name = 'dictionary.{}'.format(entity.unique)
        print(event, var_name, int(event), int(config.get('dictionary.{}'.format(entity.unique))))
        if int(event) == int(config.get(var_name)):
            return None

        config.set(var_name, int(event))
        dictionary.reload()

    @inject.params(config='config', dictionary='dictionary')
    def onSelectDatabase(self, event, widget=None, config=None, dictionary=None):
        database = config.get('dictionary.database')
        database = os.path.expanduser(database)
        path = str(QtWidgets.QFileDialog.getExistingDirectory(None, 'Select Directory', database))
        if not path: return self.database.setChecked(False)

        config.set('dictionary.database', '{}'.format(path))
        if dictionary: dictionary.reload()
