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
import functools
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import Qt


class LabelTop(QtWidgets.QLabel):
    def __init__(self, parent=None):
        """

        :param parent: 
        """
        super(LabelTop, self).__init__(parent)
        self.setStyleSheet('color: #000')
        font = self.font()
        font.setPixelSize(14)
        self.setFont(font)


class QCustomQWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(QCustomQWidget, self).__init__(parent)
        self.textUpQLabel = LabelTop()
        self.allQHBoxLayout = QtWidgets.QVBoxLayout()
        self.allQHBoxLayout.addWidget(self.textUpQLabel)
        self.setLayout(self.allQHBoxLayout)

    def setTextUp(self, text=None):
        """
        
        :param text: 
        :return: 
        """
        self.textUpQLabel.setText(text)


class FolderListWidgetItem(QtWidgets.QListWidgetItem):
    def __init__(self, parent=None, text=None):
        """

        :param parent: 
        """
        super(FolderListWidgetItem, self).__init__(parent)
        self._text = text

    @property
    def text(self):
        """

        :return: 
        """
        return self._text


class TranslationListWidget(QtWidgets.QListWidget):
    def __init__(self, parent=None):
        """

        :param parent: 
        """
        super(TranslationListWidget, self).__init__(parent)
        self.setStyleSheet('''
            QListWidget{ border: none; }
            QListWidget::item{ background-color: #fcf9f6; padding: 0px 0px 0px 0px; }
            QListWidget::item:selected{ background-color: #fdfcf9 }
        ''')

    def append(self, string):
        """

        :param name: 
        :param descrption: 
        :return: 
        """

        myQCustomQWidget = QCustomQWidget()
        myQCustomQWidget.setTextUp(string)

        item = FolderListWidgetItem(self, string)
        item.setSizeHint(myQCustomQWidget.sizeHint())

        self.addItem(item)
        self.setItemWidget(item, myQCustomQWidget)

    def setSuggestions(self, collection):
        """

        :param collection: 
        :return: 
        """
        self.clear()
        for string in collection:
            self.append(string)
