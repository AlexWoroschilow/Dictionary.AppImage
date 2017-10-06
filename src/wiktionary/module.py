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
import services
import lib.di as di
from markup import WikiMarkup


class Loader(di.component.Extension):
    @property
    def config(self):
        """
        get etc file with initialized
        services for this module

        :return: 
        """
        return None

    @property
    def enabled(self):
        """
        check if system needs to enable this module

        :return: 
        """
        if hasattr(self._options, 'wiktionary'):
            return self._options.wiktionary
        return False

    @property
    def subscribed_events(self):
        """

        :return: 
        """
        yield ('app.start', ['OnAppStart', 0])

    def init(self, container):
        """

        :param container_builder: 
        :param container: 
        :return: 
        """
        self.container = container

    def post_build(self, container_builder, container):
        """

        :param container_builder: 
        :param container: 
        :return: 
        """
        container.add('wiktionary', services.Wiktionary(
            container.getOption('host'), container.getOption('port'),
            container.getOption('database'), container.getOption('user'),
            container.getOption('password')
        ))

    def OnAppStart(self, event, dispatcher):
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
        print(entity.revision.text.old_text)
        # print convertor.parse(entity.revision.text.old_text.replace("\n", ' '))

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
