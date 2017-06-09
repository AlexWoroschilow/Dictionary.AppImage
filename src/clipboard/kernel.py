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
from src.clipboard import widget


class AppListener(container.ContainerAware):
    _clipboard = None

    def OnTab(self, event, dispatcher):
        self._clipboard = widget.Clipboard(event.data, self.OnText)

    def OnScaningSwitch(self, event, dispatcher):
        if event.data is not None and event.data:
            return self._clipboard.start_scan(self.OnText)
        return self._clipboard.stop_scan()

    def OnText(self, text):
        if text is None or not len(text):
            return None
        dispatcher = self.container.get('event_dispatcher')
        dispatcher.dispatch('clipboard_event.changed', text.strip())

    def OnStop(self, event, dispatcher):
        self._clipboard.stop_scan()
