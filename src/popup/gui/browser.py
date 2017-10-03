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
from PyQt5.QtWebKitWidgets import QWebView
import string


class TranslationWidget(QWebView):
    def __init__(self, parent):
        """

        :param actions: 
        """
        super(TranslationWidget, self).__init__(parent)
        self.resize(self.sizeHint())

        self.content = []

    def addTranslation(self, translation):
        """

        :param translation: 
        :return: 
        """
        with open("%s/themes/translation.html" % os.getcwd(), 'r') as stream:
            self.content.append(stream.read() % translation)
        self.setContent(string.join(self.content, ''))

    def setTranslation(self, collection):
        """
        
        :param collection: 
        :return: 
        """
        self.content = []
        with open("%s/themes/translation.html" % os.getcwd(), 'r') as stream:
            template = stream.read()
            for translation in collection:
                self.content.append(template % translation)
        self.setContent(string.join(self.content, ''))

    def clear(self):
        self.content = []
        self.setContent(string.join(self.content, ''))
