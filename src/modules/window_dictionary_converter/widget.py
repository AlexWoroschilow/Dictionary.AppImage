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
from gettext import gettext as _


class ListCtrlAutoWidth(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, wx.ID_ANY, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        self.setResizeColumn(0)


class DictionaryPage(wx.Panel):
    _dictionaries = []
    _converter = None

    def __init__(self, layout, parent, converter):
        self._converter = converter
        wx.Panel.__init__(self, parent)

        style = wx.LC_REPORT | wx.BORDER_NONE | wx.LC_EDIT_LABELS | wx.LC_SORT_ASCENDING
        self._list = ListCtrlAutoWidth(self, style=style)
        self._list.InsertColumn(0, _('Dictionary'))

        self._label = wx.StaticText(self, -1, label=_('loading...'))

        sizer3 = wx.BoxSizer(wx.VERTICAL)
        sizer3.Add(self._list, 1, wx.ALL | wx.EXPAND)
        sizer3.Add(self._label, 0, wx.ALL | wx.EXPAND)

        sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer4.Add(self._button_panel, 0, wx.ALL | wx.EXPAND)
        sizer4.Add(sizer3, 1, wx.ALL | wx.EXPAND)

        self.SetSizer(sizer4)

    @property
    def _button_panel(self):
        self._toolbar = wx.ToolBar(self, style=wx.TB_FLAT | wx.TB_NOICONS | wx.TB_VERTICAL)
        self._toolbar.Bind(wx.EVT_TOOL, self._OnExport)
        self._toolbar.AddLabelTool(3014, _('ORIG'), wx.EmptyBitmap(32, 32))
        self._toolbar.AddLabelTool(3015, _('DICT'), wx.EmptyBitmap(32, 32))
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

        message = "%s %s" % (self._list.GetItemCount(), _('dictionaries found'))
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
        if event.GetId() in [3014]:
            return self._OnExportOrig(event)
        if event.GetId() in [3015]:
            return self._OnExportDat(event)

    # Process export original dictionary button
    def _OnExportOrig(self, event):
        dialog = wx.DirDialog(self, _("Export to"), "./", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if dialog.ShowModal() == wx.ID_OK:
            for index in self.GetSelectedItems():
                dictionary = self._dictionaries[index]
                if dictionary is None:
                    continue
                sources = dictionary.source
                if type(sources) in [list, tuple]:
                    for source in sources:
                        self._ExportOrig(source, dialog.GetPath())
                    continue
                self._ExportOrig(sources, dialog.GetPath())
        dialog.Destroy()

    # Export single dictionary file
    def _ExportOrig(self, source, destination):
        if not os.path.isfile(source):
            return None
        destination = '%s/%s' % (destination, os.path.basename(source))
        if os.path.isfile(destination):
            os.remove(destination)
        shutil.copy2(source, destination)

    # Process export sqlite dictionary button
    def _OnExportDat(self, event):
        dialog = wx.DirDialog(self, _("Export to"), "./", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if dialog.ShowModal() == wx.ID_OK:
            for index in self.GetSelectedItems():
                dictionary = self._dictionaries[index]
                if dictionary is None:
                    continue
                self._ExportDat(dictionary, dialog.GetPath())
        dialog.Destroy()

    # Export single dictionary
    def _ExportDat(self, dictionary, destination):
        dlg = wx.ProgressDialog("%s - %s" % (_('Create dictionary'), dictionary.name), '...',
                                style=wx.PD_APP_MODAL | wx.PD_CAN_ABORT | wx.PD_REMAINING_TIME | wx.PD_AUTO_HIDE,
                                maximum=100, parent=self)

        for percent in self._converter.convert(dictionary, destination):
            (keepGoing, skip) = dlg.Update(float(percent), "%s: %.2f %%" % (dictionary.name, percent))
            if keepGoing == False:
                break
        dlg.Destroy()
