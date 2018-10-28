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
from di import container
from pyparsing import *
from markup import WikiMarkup


class Console(container.ContainerAware):
    def OnStart(self, event, dispatcher):
        """
        
        :param event: 
        :param dispatcher: 
        :return: 
        """
        if self.container.getOption('query') is not None:
            return self.OnQuery(self.container.getOption('query'))

        if self.container.getOption('list') is True:
            return self.OnList()

        if self.container.getOption('process') is True \
                and self.container.getOption('output') is not None:
            return self.OnConvert(self.container.getOption('output'))

    def OnQuery(self, string):
        """
        
        :param string: 
        :return: 
        """
        wiktionary = self.container.get('wiktionary')
        entity = wiktionary.find(string)
        # print (entity.page_title, wikitextparser.parse(entity.revision.text.old_text))
        # print (entity.page_title, entity.revision.text.old_text.replace("\n",' '))

        convertor = WikiMarkup()
        print convertor.parse(entity.revision.text.old_text.replace("\n",' '))

    def OnList(self):
        """
        
        :return: 
        """
        wiktionary = self.container.get('wiktionary')
        for entity in wiktionary.all():
            print (entity.page_title, entity.revision.text.old_text)

    def OnConvert(self, output):
        """
        
        :return: 
        """
        convertor = WikiMarkup()
        creator = self.container.get('dictionary_creator')
        wiktionary = self.container.get('wiktionary')

        creator.create(output)
        for index, entity in enumerate(wiktionary.all()):
            if entity.revision is None:
                continue
            text = entity.revision.text
            creator.append(entity.page_title, convertor.parse(text.old_text))
            if index % 10000 == 0:
                creator.flush()
        creator.flush()
