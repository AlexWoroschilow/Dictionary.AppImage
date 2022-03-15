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
import mmap
import inject
import base64
import functools

from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui


class ExportThread(QtCore.QThread):
    progress = QtCore.pyqtSignal(object)

    def __init__(self, source=None, destination=None):
        super(ExportThread, self).__init__()
        self.destination = destination
        self.source = source

    def start(self, source=None, destination=None, priority=None):
        self.destination = destination
        self.source = source
        return super(ExportThread, self).start()

    def get_count_lines(self, filename):
        f = open(filename, "r+")
        buf = mmap.mmap(f.fileno(), 0)
        lines = 0
        readline = buf.readline
        while readline():
            lines += 1
        return lines

    @inject.params(creator='dictionary.creator', cleaner='dictionary.cleaner')
    def run(self, creator=None, cleaner=None):
        creator = creator.create(self.destination)

        self.progress.emit(0)

        counter = 0
        total = self.get_count_lines(self.source)
        for index, line in enumerate(open(self.source), start=0):
            if index == 0: continue

            try:

                line = line.strip("\n")
                word, content = line.split(',')
                self.progress.emit(index / total * 100)

                content = base64.b64decode(content)
                creator.append(word, cleaner.cleanup(content.decode('utf-8')))
                counter += 1
                if counter == 200:
                    creator.flush()
                    counter = 0

            except Exception as ex:
                print(ex)

        creator.flush()
        self.progress.emit(100)


class Loader(object):

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def enabled(self, options=None, args=None):
        if hasattr(options, 'converter'):
            return options.converter
        return False

    def configure(self, binder, options=None, args=None):
        from .service import DictionaryCreator
        from .service import DictionaryContentCleaner
        binder.bind_to_constructor('dictionary.creator', DictionaryCreator)
        binder.bind_to_constructor('dictionary.cleaner', DictionaryContentCleaner)

    @inject.params(window='window')
    def boot(self, options=None, args=None, window=None):
        from .gui.widget import DictionaryConverterWidget

        self.thread = ExportThread()

        widget = DictionaryConverterWidget()
        widget.exportAction.connect(functools.partial(
            self.exportActionEvent, widget=widget
        ))

        window.addTab(0, widget, 'Converter')

    def exportActionEvent(self, source, widget=None):
        selector = QtWidgets.QFileDialog()
        if not selector.exec_():
            return None

        for path in selector.selectedFiles():
            if len(path) and os.path.exists(path):
                reply = QtWidgets.QMessageBox.question(
                    widget, 'Are you sure?', "Are you sure you want to overwrite the file '{}' ?".format(path),
                    QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No
                )

                if reply == QtWidgets.QMessageBox.No:
                    break

            self.thread.progress.connect(widget.progressAction.emit)
            self.thread.start(source, path)
