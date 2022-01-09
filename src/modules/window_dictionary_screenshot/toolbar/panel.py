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
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from .button import ToolbarButton, PictureButtonDisabled
from .label import OCRField
from .menu.container import MenuContainerWidget


class ToolbarWidget(QtWidgets.QFrame):
    actionScreenshot = QtCore.pyqtSignal(object)

    @inject.params(config='config')
    def __init__(self, config=None):
        super(ToolbarWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)

        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.layout().setSpacing(0)

        self.screenshot = ToolbarButton(self, "...", QtGui.QIcon('icons/monitor'))
        self.screenshot.clicked.connect(self.onToggleScreenshot)
        self.screenshot.clicked.connect(self.reload)
        self.layout().addWidget(self.screenshot)

        self.grabber = ToolbarButton(self, "Grab text", QtGui.QIcon('icons/screenshot'))
        self.grabber.clicked.connect(self.actionScreenshot.emit)
        self.grabber.setCheckable(False)
        self.layout().addWidget(self.grabber)

        self.layout().addWidget(PictureButtonDisabled(QtGui.QIcon("icons/folder")), -1)

        self.ocr = OCRField('...')
        self.layout().addWidget(self.ocr)

        self.dropdown = ToolbarButton(self, "Language", QtGui.QIcon('icons/eng'))
        self.dropdown.setToolTip('dropdown menu')
        self.dropdown.clicked.connect(self.onToggleMenu)
        self.dropdown.setChecked(False)
        self.layout().addWidget(self.dropdown)

        self.reload()

    def setText(self, string):
        self.ocr.setText(string)

    @inject.params(themes='themes')
    def onToggleMenu(self, event, themes):
        widget = MenuContainerWidget()
        widget.setStyleSheet(themes.get_stylesheet())
        widget.language.connect(self.reload)

        container = QtWidgets.QWidgetAction(self)
        container.setDefaultWidget(widget)

        menu = QtWidgets.QMenu()
        menu.addAction(container)
        menu.aboutToHide.connect(lambda x=None: self.dropdown.setChecked(False))
        menu.setStyleSheet(themes.get_stylesheet())

        menu.exec_(QtGui.QCursor.pos())

    @inject.params(config='config')
    def reload(self, event=None, config=None):
        self.screenshot.setChecked(int(config.get('screenshot.enabled', 1)))
        self.screenshot.setText('Enabled' if self.screenshot.isChecked() else 'Disabled')

        language = config.get('screenshot.language', 'eng')
        self.dropdown.setIcon(QtGui.QIcon('icons/{}'.format(language)))

    @inject.params(config='config')
    def onToggleScreenshot(self, event=None, config=None):
        config.set('screenshot.enabled', int(event))
