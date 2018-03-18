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
from PyQt5 import QtCore
from PyQt5 import QtWidgets


class StatusbarWidget(QtWidgets.QStatusBar):
    def __init__(self):
        super(StatusbarWidget, self).__init__()

        self.status = QtWidgets.QLabel()
        self.status.setAlignment(QtCore.Qt.AlignLeft)
        self.status.setFixedWidth(self.width())

        font = self.status.font()
        font.setPixelSize(10)
        self.status.setFont(font)

        self.addWidget(self.status)

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

    def setProgress(self, progress):
        """

        :param progress: 
        :return: 
        """

    def stop(self, progress):
        """

        :param progress: 
        :return: 
        """
