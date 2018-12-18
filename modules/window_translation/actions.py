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


class TranslatorActions(object):
    
    def __init__(self, wiget, thread):
        self.thread = thread
        self.widget = wiget
    
    @inject.params(kernel='kernel')
    def onSearchString(self, string, kernel=None):
        if not len(string):
            return None

        self.thread.translate(string)
        
        kernel.dispatch('window.translation.request', string)

    @inject.params(kernel='kernel', widget='widget.translator_search')
    def onActionTranslate(self, event, kernel, widget=None):
        string = event.data
        if not len(string):
            return None
         
        self.thread.translate(string)
            
        kernel.dispatch('window.translation.request', string)
        if widget is not None and widget:
            return widget.setText(string)

    @inject.params(kernel='kernel', widget='widget.translator_search', dictionary='dictionary', config='config')
    def onActionTranslateClipboard(self, event, kernel, widget, dictionary, config):
        kernel.dispatch('window.translation.request', event.data)
        
        if widget is not None and widget:
            widget.setText(event.data)

        if int(config.get('clipboard.suggestions')):
            return self.thread.translate(event.data)
        
        for translation in dictionary.translate(event.data):
            self.widget.addTranslation(translation)
            if not int(config.get('translator.all')):
                break
        return None

    @inject.params(dictionary='dictionary', config='config')
    def onSuggestionSelected(self, string, dictionary, config):
        self.widget.clearTranslation()
        for translation in dictionary.translate(string):
            self.widget.addTranslation(translation)
            if not int(config.get('translator.all')):
                break

    @inject.params(statusbar='widget.statusbar')
    def onTranslationStarted(self, progress=None, statusbar=None):
        self.widget.clearTranslation()
        self.widget.clearSuggestion()
        
        if statusbar is not None and statusbar:
            return statusbar.start(progress)

    @inject.params(statusbar='widget.statusbar')
    def onTranslationProgress(self, progress=None, translation=None, statusbar=None):
        self.widget.addTranslation(translation)
        if statusbar is not None and statusbar:
            return statusbar.setProgress(progress)

    @inject.params(statusbar='widget.statusbar')
    def onTranslationProgressSuggestion(self, progress=None, string=None, statusbar=None):
        self.widget.addSuggestion(string)
        if statusbar is not None and statusbar:
            return statusbar.setProgress(progress)

    @inject.params(statusbar='widget.statusbar')
    def onTranslationFinished(self, progress=None, statusbar=None):
        if statusbar is not None and statusbar:
            statusbar.stop(progress)
