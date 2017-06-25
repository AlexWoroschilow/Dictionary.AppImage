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
import string

import wx.lib.mixins.listctrl as listmix
import wx.grid
from gettext import gettext as _


class ListCtrlAutoWidth(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin):
    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        self.setResizeColumn(2)


class EditableListCtrl(ListCtrlAutoWidth, listmix.TextEditMixin):
    def __init__(self, parent, ID=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
        ListCtrlAutoWidth.__init__(self, parent, ID, pos, size, style)
        listmix.TextEditMixin.__init__(self)


class HistoryPage(wx.Panel):
    _OnUpdate = None
    _OnDelete = None
    _SelectedRows = None
    _parent = None

    def __init__(self, layout, parent, OnUpdate=None, OnDelete=None):
        self._OnUpdate = OnUpdate
        self._OnDelete = OnDelete
        self._SelectedRows = []
        self._parent = parent

        wx.Panel.__init__(self, parent, style=wx.TEXT_ALIGNMENT_LEFT)
        # Create a wxGrid object
        self._history = wx.grid.Grid(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0)

        # Then we call CreateGrid to set the dimensions of the grid
        # (100 rows and 10 columns in this example)
        self._history.CreateGrid(1, 4)
        self._history.HideCol(0)

        size_row = self._history.GetRowLabelSize()
        self._history.SetRowLabelSize(size_row / 1.8)

        size_col = self._history.GetColLabelSize()
        self._history.SetColLabelSize(size_col / 1.4)

        self._history.Bind(wx.EVT_SIZE, self._OnResize)
        self._history.Bind(wx.grid.EVT_GRID_CELL_CHANGED, self._OnChanged)
        self._history.Bind(wx.grid.EVT_GRID_SELECT_CELL, self._OnSelectedCell)
        self._history.Bind(wx.grid.EVT_GRID_RANGE_SELECT, self._OnSelectedRange)
        self._history.Bind(wx.EVT_KEY_DOWN, self._OnKeyDown)

        sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer3.Add(self._button_panel, 0, wx.ALL | wx.EXPAND)
        sizer3.Add(self._history, 1, wx.ALL | wx.EXPAND)
        self.SetSizer(sizer3)

    @property
    def history(self):
        for row in range(0, self._history.GetNumberRows()):
            collection = []
            for column in range(0, self._history.GetNumberCols()):
                collection.append(self._history.GetCellValue(row, column))
            yield collection

    @history.setter
    def history(self, value=None):
        self._history.DeleteRows(numRows=self._history.GetNumberRows())
        for row, line in enumerate(value):
            if self._history.GetNumberRows() == row:
                self._history.AppendRows(1)
            for column, field in enumerate(line):
                if self._history.GetNumberCols() == column:
                    self._history.AppendCols(1)
                self._history.SetCellValue(row, column, field)
        self._history.HideCol(0)
        self._OnResize(None)

    @property
    def _button_panel(self):
        self._toolbar = wx.ToolBar(self, style=wx.TB_FLAT | wx.TB_NOICONS | wx.TB_VERTICAL)
        self._toolbar.Bind(wx.EVT_TOOL, self._OnExport)
        self._toolbar.AddLabelTool(1013, _('CSV'), wx.EmptyBitmap(32, 32))
        self._toolbar.AddLabelTool(1014, _('TXT'), wx.EmptyBitmap(32, 32))
        self._toolbar.Realize()
        return self._toolbar

    def _OnKeyDown(self, event):
        if self._OnDelete is None:
            return event.Skip()

        removed = 0
        if event.GetKeyCode() in [wx.WXK_DELETE, wx.WXK_BACK]:
            for index in sorted(self._history.GetSelectedRows()):
                index -= removed
                self._OnDelete(self._history.GetCellValue(index, 0))
                self._history.DeleteRows(index, 1)
                removed += 1
            return False
        return event.Skip()

    def _OnSelectedCell(self, event):
        """Internal update to the selection tracking list"""
        if event.GetRow() not in self._history.GetSelectedRows():
            self._history.SelectRow(event.GetRow(), True)
            return event.Skip()
        self._history.DeselectRow(event.GetRow())
        return event.Skip()

    def _OnSelectedRange(self, event):
        """Internal update to the selection tracking list"""
        if event.Selecting():
            for index in range(event.GetTopRow(), event.GetBottomRow() + 1):
                if index not in self._history.GetSelectedRows():
                    self._history.SelectRow(index, True)
            return event.Skip()
        for index in range(event.GetTopRow(), event.GetBottomRow() + 1):
            if index in self._history.GetSelectedRows():
                self._history.DeselectRow(index)
        return event.Skip()

    def _OnExport(self, event):
        if event.GetId() in [1013]:
            return self._OnExportCsv(event)
        if event.GetId() in [1014]:
            return self._OnExportText(event)

    def _OnResize(self, event=None):
        width, height = self._parent.GetClientSizeTuple()
        self._history.SetColSize(1, width / 4)
        self._history.SetColSize(2, width / 4)
        self._history.SetColSize(3, width / 2)

    def _OnChanged(self, event):
        collection = []
        row = event.GetRow()
        for column in range(0, self._history.GetNumberCols()):
            collection.append(self._history.GetCellValue(row, column))
        if self._OnUpdate is not None:
            self._OnUpdate(collection)

    def _OnExportCsv(self, event):
        dialog = wx.FileDialog(self, _('Save As'), '', '', '', wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if dialog.ShowModal() == wx.ID_OK:
            with open(dialog.GetPath(), 'w+') as stream:
                for fields in self.history:
                    stream.write("%s\n" % string.join(fields, ';'))
                stream.close()
        dialog.Destroy()

    def _OnExportText(self, event):
        dialog = wx.FileDialog(self, _('Save As'), '', '', '', wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if dialog.ShowModal() == wx.ID_OK:
            with open(dialog.GetPath(), 'w+') as stream:
                for fields in self.history:
                    stream.write("%s\n" % string.join(fields, "\t"))
                stream.close()
        dialog.Destroy()
