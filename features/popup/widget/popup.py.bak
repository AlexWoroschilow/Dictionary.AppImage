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
import wx.lib.scrolledpanel as scrolled


class TranslationPopup(wx.PopupWindow):
    _transformation = {
        '<k>': '<span foreground="#006400" size="x-large">',
        '</k>': '</span>',
        '<kref>': '<span foreground="grey">',
        '</kref>': '</span>',
        '<dtrn>': '<small>',
        '</dtrn>': '</small>',
        '<co>': '<i>',
        '</co>': '</i>',
        '<abr>': '<span foreground="blue">',
        '</abr>': '</span>',
        '<ex>': '<span foreground="#a0a0a0">',
        '</ex>': '</span>',
        '<tr>': '<i>',
        '</tr>': '</i>',
        '<c>': '<i>',
        '</c>': '</i>',
    }

    def __init__(self):
        wx.PopupWindow.__init__(self, None, wx.STAY_ON_TOP | wx.FRAME_SHAPED)
        self.SetBackgroundColour("#f0f0f0")
        self.SetTransparent(240)
        self.SetSize(wx.Size(280, 300))

        self.Bind(wx.EVT_CHAR_HOOK, self.OnKeyUP)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnKeyUP)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnKeyUP)

        self._panel = scrolled.ScrolledPanel(self, -1, style=wx.VSCROLL)
        self._panel.SetAutoLayout(1)
        self._panel.SetupScrolling()
        self._panel.SetSize(wx.Size(280, 300))

        self._panel.Bind(wx.EVT_CHAR_HOOK, self.OnKeyUP)
        self._panel.Bind(wx.EVT_LEAVE_WINDOW, self.OnKeyUP)
        self._panel.Bind(wx.EVT_LEFT_DOWN, self.OnKeyUP)

        self._browser = wx.StaticText(self._panel, style=wx.TE_WORDWRAP)
        self._browser.SetMinSize(wx.Size(260, 1500))
        self._browser.Wrap(240)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self._browser, 1, wx.EXPAND, border=30)
        self._panel.SetSizer(sizer)

        sizer_panel = wx.BoxSizer(wx.HORIZONTAL)
        sizer_panel.Add(self._panel)

    @property
    def translations(self):
        pass

    @translations.setter
    def translations(self, text):
        if not len(text):
            return None

        for replace, to in self._transformation.iteritems():
            text = text.replace(replace, to)
        self._browser.SetLabelMarkup(text)
        self._panel.Scroll(0, 0)

    def OnKeyUP(self, event):
        self.Hide()
