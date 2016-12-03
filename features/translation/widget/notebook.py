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
import sys
import string

import wx
import wx.html2 as webview
import wx.lib.mixins.listctrl as listmix


class ListCtrlAutoWidth(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, wx.ID_ANY, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        self.setResizeColumn(0)


class TranslationPage(wx.Panel):
    _show_all = False

    _callback_on_select = None
    _callback_on_search = None

    def __init__(self, layout=None, parent=None, on_search=None, on_select=None, on_scan=None):
        self._callback_on_scan = on_scan
        self._callback_on_search = on_search
        self._callback_on_select = on_select
        wx.Panel.__init__(self, parent)

        self._search = wx.TextCtrl(self, size=(layout.text, layout.text), style=wx.TE_PROCESS_ENTER)
        self._search.Bind(wx.EVT_TEXT_ENTER, self.on_search_selected)
        self._search.SetFont(wx.Font(26, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Consolas'))

        self._scan_clipboard = wx.CheckBox(self, label='Scan and translate clipboard')
        self._scan_clipboard.Bind(wx.EVT_CHECKBOX, self.on_scan_checked)

        self._checkbox_show_all = wx.CheckBox(self, label='Show results from all available dictionaries')
        self._checkbox_show_all.Bind(wx.EVT_CHECKBOX, self.on_show_all)

        self._browser = webview.WebView.New(self)

        self._suggestions = ListCtrlAutoWidth(self, size=(20,200), style=wx.LC_REPORT | wx.BORDER_NONE)
        self._suggestions.InsertColumn(0, 'Similar words')

        self._suggestions.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_suggestion_selected)
        self._suggestions.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.on_suggestion_selected)

        translations = wx.BoxSizer(wx.HORIZONTAL)
        translations.Add(self._suggestions, proportion=1, flag=wx.ALL | wx.EXPAND, border=layout.empty)
        translations.Add(self._browser, proportion=3, flag=wx.ALL | wx.EXPAND, border=layout.empty)

        sizer3 = wx.BoxSizer(wx.VERTICAL)
        sizer3.Add(self._search, proportion=1, flag=wx.ALL | wx.EXPAND, border=layout.border)
        sizer3.Add(self._checkbox_show_all, proportion=1, flag=wx.ALL | wx.EXPAND, border=layout.border)
        sizer3.Add(translations, proportion=20, flag=wx.ALL | wx.EXPAND, border=layout.empty)
        sizer3.Add(self._scan_clipboard, proportion=1, flag=wx.ALL | wx.EXPAND, border=layout.border)

        self.SetSizer(sizer3)

    @property
    def suggestions(self):
        pass

    @suggestions.setter
    def suggestions(self, value):
        if self._suggestions.GetItemCount():
            self._suggestions.DeleteAllItems()
        for index, word in enumerate(value):
            self._suggestions.InsertStringItem(sys.maxint, word)

    @property
    def word(self):
        self._search.GetValue()

    @word.setter
    def word(self, value):
        self._search.SetValue(value)

    @property
    def translations(self):
        pass

    @translations.setter
    def translations(self, translations):

        collection = []
        for translation in translations:
            if translation is not None:
                collection.append(translation)
                if self._show_all is False:
                    break

        with open("%s/themes/translation.html" % os.getcwd(), 'r') as stream:
            content = stream.read() % string.join(collection, '')
            self._browser.SetPage(content, "text/html")

    def on_show_all(self, event):
        checkbox = event.GetEventObject()
        self._show_all = checkbox.GetValue()

    def on_scan_checked(self, event):
        if self._callback_on_scan is not None:
            checkbox = event.GetEventObject()
            self._callback_on_scan(checkbox.GetValue())

    def on_search_selected(self, event):
        if self._callback_on_search is not None:
            word = self._search.GetValue()
            self._callback_on_search(word.encode('utf-8'))

    def on_suggestion_selected(self, event):
        if self._callback_on_select is not None:
            index = self._suggestions.GetFocusedItem()
            word = self._suggestions.GetItemText(index)
            self._callback_on_select(word.encode('utf-8'))
