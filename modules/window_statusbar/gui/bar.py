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
from PyQt5 import QtWidgets
from PyQt5 import QtCore


class StatusbarWidget(QtWidgets.QStatusBar):

    def __init__(self):
        super(StatusbarWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.status = QtWidgets.QLabel()

        self.status.setAlignment(QtCore.Qt.AlignCenter)
        self.addWidget(self.status)

        self.progress = QtWidgets.QProgressBar()
        self.progress.hide()

    def text(self, text):
        self.status.setText(text)

    def start(self, progress):
        if self.status is not None:
            self.status.hide()
            self.removeWidget(self.status)

        if self.progress is not None:
            self.progress.setValue(progress)
            self.addWidget(self.progress, 1)
            self.progress.show()

    def setProgress(self, progress):
        if self.progress is not None:
            self.progress.setValue(progress)

    def stop(self, progress):
        if self.progress is not None:
            self.progress.setValue(progress)
            self.progress.hide()
            self.removeWidget(self.progress)

        if self.status is not None:
            self.addWidget(self.status, 1)
            self.status.show()
