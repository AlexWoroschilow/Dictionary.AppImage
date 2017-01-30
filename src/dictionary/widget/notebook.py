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
import shutil

import wx
import wx.lib.mixins.listctrl  as  listmix


class ListCtrlAutoWidth(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, wx.ID_ANY, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        self.setResizeColumn(0)


class DictionaryPage(wx.Panel):
    _dictionaries = []

    def __init__(self, layout, parent):
        wx.Panel.__init__(self, parent)

        style = wx.LC_REPORT | wx.BORDER_NONE | wx.LC_EDIT_LABELS | wx.LC_SORT_ASCENDING
        self._list = ListCtrlAutoWidth(self, style=style)
        self._list.InsertColumn(0, 'Dictionary')

        self._label = wx.StaticText(self, -1, label='loading...')

        sizer3 = wx.BoxSizer(wx.VERTICAL)
        sizer3.Add(self._list, proportion=30, flag=wx.ALL | wx.EXPAND, border=layout.empty)
        sizer3.Add(self._label, proportion=1, flag=wx.ALL | wx.EXPAND, border=layout.border)

        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(self._button_panel, proportion=1, flag=wx.EXPAND | wx.ALL, border=layout.empty)
        sizer4.Add(sizer3, proportion=40, flag=wx.EXPAND | wx.ALL, border=layout.empty)

        self.SetSizer(sizer4)

    @property
    def _button_panel(self):
        self._toolbar = wx.ToolBar(self, style=wx.TB_FLAT | wx.TB_NOICONS | wx.TB_VERTICAL)
        self._toolbar.Bind(wx.EVT_TOOL, self._OnExport)
        self._toolbar.AddLabelTool(2014, 'DICT', wx.EmptyBitmap(32, 32))
        self._toolbar.Realize()
        return self._toolbar

    @property
    def dictionaries(self):
        pass

    @dictionaries.setter
    def dictionaries(self, collection):
        for index, dictionary in enumerate(collection):
            self._dictionaries.append(dictionary)
            self._list.InsertStringItem(index, 'line', 1)
            self._list.SetStringItem(index, 0, dictionary.name)

        message = "%s dictionaries found" % self._list.GetItemCount()
        self._label.SetLabelText(message)

    def GetSelectedItems(self):
        selection = []
        index = self._list.GetFirstSelected()
        selection.append(index)
        while len(selection) != self._list.GetSelectedItemCount():
            index = self._list.GetNextSelected(index)
            selection.append(index)
        return selection

    def _OnExport(self, event):
        if event.GetId() in [2014]:
            return self._OnExportDat(event)

    def _OnExportDat(self, event):
        dialog = wx.DirDialog(self, "Export to", "./", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if dialog.ShowModal() == wx.ID_OK:
            for index in self.GetSelectedItems():
                dictionary = self._dictionaries[index]
                if dictionary is None:
                    continue
                sources = dictionary.source
                if type(sources) in [list, tuple]:
                    for source in sources:
                        self._ExportDat(source, dialog.GetPath())
                    continue
                self._ExportDat(sources, dialog.GetPath())
        dialog.Destroy()

    def _ExportDat(self, source, destination):
        shutil.copy2(source, '%s/%s' % (destination, os.path.basename(source)))

