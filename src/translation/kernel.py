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

from src.translation.widget import TranslationPage


class KernelEventSubscriber(container.ContainerAware):
    _page = None

    def OnTab(self, event, dispatcher):
        layout = self.container.get('crossplatform.layout')
        dictionary = self.container.get('dictionary')

        self._page = TranslationPage(layout, event.data, self.OnSearch, self.OnSuggestion, self.OnScaningToggle)
        event.data.AddPage(self._page, "Translation")

        self._page.translations = dictionary.translate("welcome")
        self._page.suggestions = dictionary.suggestions("welcome")

    # Catch clipboard event (clipboard text has been changed)
    # and display popup with a translation, if it has been found
    def OnClipboard(self, event, dispatcher):
        self._page.word = event.data
        self.OnSearch(event.data)

    # Enable or disable clipboard scanning
    def OnScaningToggle(self, scan=False):
        dispatcher = self.container.get('event_dispatcher')
        dispatcher.dispatch('kernel_event.window_toggle_scanning', scan)

    # Search event, fired if user
    # typped a word in search box and
    # pressed enter, or without enter
    def OnSearch(self, word=None):
        dictionary = self.container.get('dictionary')
        dispatcher = self.container.get('event_dispatcher')
        if self._page is None:
            return None

        suggestions = dictionary.suggestions(word)
        self._page.suggestions = suggestions
        if not len(word):
            return None

        translations = dictionary.translate(word)
        if translations is None:
            return None

        self._page.translations = translations

        dispatcher.dispatch('dictionary.translation', [word, translations])

    # Suggestion event, fired of user
    # found a similar word in left side panel
    # and clicked on it
    def OnSuggestion(self, word=None):
        dictionary = self.container.get('dictionary')
        dispatcher = self.container.get('event_dispatcher')
        if self._page is None:
            return None

        translations = dictionary.translate(word)
        if translations is None:
            return None

        self._page.translations = translations

        dispatcher.dispatch('dictionary.translation', [word, translations])