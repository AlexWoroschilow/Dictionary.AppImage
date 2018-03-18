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


class TranslationWidget(QtWidgets.QTextEdit):
    def __init__(self, parent):
        """

        :param actions: 
        """
        super(TranslationWidget, self).__init__(parent)
        self.setStyleSheet(''' QTextEdit{ border: none; }; QLineEdit{ border: none; }''')

        self.resize(self.sizeHint())

        self.content = []

    def _format(self, text=None):
        """
        
        :param text: 
        :return: 
        """
        text = text.replace('<k>', '<h1 style="color:green">')
        text = text.replace('</k>', '</h1>')

        text = text.replace('<kref>', '<small>')
        text = text.replace('</kref>', '</small>')

        text = text.replace('<ex>', '<p>')
        text = text.replace('</ex>', '</p>')

        text = text.replace('<abr>', '<i>')
        text = text.replace('</abr>', '</i>')

        text = text.replace('<tr>', '&nbsp;<span style="color:#535353">')
        text = text.replace('</tr>', '</span><br/>')

        text = text.replace('<kref>', '<small>')
        text = text.replace('</kref>', '</small><br/>')

        text = text.replace('<dtrn>', '<span style="color:#000000">')
        text = text.replace('</dtrn>', '</span>')

        text = text.replace('<co>', '<span style="color:#535353">')
        text = text.replace('</co>', '</span>')

        return text

    def addTranslation(self, translation=None):
        """

        :param translation: 
        :return: 
        """
        self.content.append(self._format(translation))
        self.setHtml(''.join(self.content))

    def setTranslation(self, collection):
        """
        
        :param collection: 
        :return: 
        """
        self.content = []
        for translation in collection:
            self.content.append(self._format(translation))
        self.setHtml(str(''.join(self.content)))

    def clear(self):
        self.content = []
        self.setHtml('')
