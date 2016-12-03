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
from kernel import Kernel


class WxApplication(wx.App):
    _kernel = None
    _notebook = None

    def __init__(self, options=None, args=None):
        wx.App.__init__(self)
        self._kernel = Kernel(options, args)
        self.SetAppName("My App Name")

    def MainLoop(self, options=None, args=None):
        layout = self._kernel.get('crossplatform.layout')
        dispatcher = self._kernel.get('event_dispatcher')
        dispatcher.dispatch('kernel_event.start', dispatcher.new_event([]))

        window = wx.Frame(None)
        window.SetTitle("Dictionary")
        window.SetSize((layout.width, layout.height))
        window.SetMinSize((layout.width, layout.height))
        window.Bind(wx.EVT_CLOSE, self.Destroy)

        event = dispatcher.new_event(window)
        dispatcher.dispatch('kernel_event.window', event)

        panel = wx.Panel(window)
        self._area = wx.Notebook(panel, wx.ID_ANY)
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged, self._area)

        event = dispatcher.new_event(self._area)
        dispatcher.dispatch('kernel_event.window_tab', event)

        sizer = wx.BoxSizer()
        panel.SetSizer(sizer)

        expand = wx.ALL | wx.EXPAND
        sizer.Add(self._area, proportion=1, flag=expand, border=layout.border)
        window.Show()

        self.SetTopWindow(window)

        return wx.App.MainLoop(self)

    def OnPageChanged(self, event):
        dispatcher = self._kernel.get('event_dispatcher')
        if event.GetOldSelection() is -1:
            return None

        current = self._area.GetPage(event.GetSelection())
        previous = self._area.GetPage(event.GetOldSelection())

        event = dispatcher.new_event((previous, current))
        dispatcher.dispatch('kernel_event.notebook_changed', event)

    def Destroy(self, event=None):
        dispatcher = self._kernel.get('event_dispatcher')
        dispatcher.dispatch('kernel_event.stop', dispatcher.new_event())

        self.ExitMainLoop()
