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


class HistoryActions(object):

    @inject.params(history='history')
    def onActionTranslationRequest(self, event, history, widget=None):
        history.add(event.data)
        if widget is None or not widget:
            return None
        
        widget.setHistory(history.history, history.count())

    @inject.params(history='history')
    def onActionRemove(self, entity=None, history=None):
        index, data, word, translation = entity
        history.remove(index, data, word, translation)

    @inject.params(history='history')
    def onActionUpdate(self, entity=None, history=None):
        index, data, word, translation = entity
        history.update(index, data, word, translation)
