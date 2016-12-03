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
import time
import threading


class ClipboardEvent(wx.PyEvent):
    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(100)
        self.data = data


class Clipboard(object):
    _timeout = 0.4
    _event = None
    _thread = None
    _application = None
    _callback = None
    __current = None
    __previous = None

    def __init__(self, application, callback):
        self._callback = callback
        self._application = application
        self._application.Connect(-1, -1, 100, self._scan)

    def start_scan(self, callback):
        while wx.TheClipboard.IsOpened():
            time.sleep(self._timeout)

        self._event = threading.Event()
        self._thread = threading.Thread(target=self.scan, args=[
            callback, self._event
        ])

        self._thread.start()

    def scan(self, callback, event):
        while not event.is_set():
            wx.PostEvent(self._application, ClipboardEvent(None))
            event.wait(self._timeout)

    def stop_scan(self):
        if self._event is not None:
            self._event.set()
        if self._thread is not None:
            self._thread.join()

    def _scan(self, event):
        '''
        Scan clipboard for changes
        '''
        data = wx.TextDataObject()
        if not data:
            return None

        wx.TheClipboard.Open()
        success = wx.TheClipboard.GetData(data)
        wx.TheClipboard.Close()
        if not success:
            return None

        self.__current = data.GetText()
        if self.__current is None or not len(self.__current):
            return None

        if self.__current == self.__previous:
            return None

        self._callback(self.__current)

        self.__previous = self.__current
