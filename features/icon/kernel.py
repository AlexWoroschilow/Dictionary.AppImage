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
import wx
import event


class KernelEventSubscriber(event.EventSubscriberInterface):
    _container = None

    @property
    def container(self):
        return self._container

    def set_container(self, container):
        self._container = container

    @property
    def subscribed_events(self):
        yield ('kernel_event.window', ['on_window', 2])

    def on_window(self, event, dispatcher):
        layout = self._container.get('crossplatform.layout')
        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(wx.Bitmap(layout.icon, wx.BITMAP_TYPE_ANY))

        if event.data.SetIcon is not None:
            event.data.SetIcon(icon)
