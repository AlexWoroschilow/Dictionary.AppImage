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
import inject
from PyQt5 import QtGui
from PyQt5 import QtWidgets


class Loader(object):

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def configure(self, binder, options=None, args=None):
        from .screenshot.screenshot import Screenshot
        binder.bind('screenshot', Screenshot)

    @inject.params(parent='window', config='config')
    def boot(self, options=None, args=None, parent=None, config=None):
        from modules import window

        shortcut = QtWidgets.QShortcut("Ctrl+G", parent)
        shortcut.activated.connect(self.onScreenshot)

        @window.toolbar(name='Screenshot', focus=False, position=0)
        @inject.params(window='window')
        def window_toolbar(parent=None, window=None):
            from .toolbar.panel import ToolbarWidget
            widget = ToolbarWidget()

            if not widget.actionScreenshot: return widget
            widget.actionScreenshot.connect(self.onScreenshot)

            if not parent.actionReload: return widget
            parent.actionReload.connect(widget.reload)

            window.translationScreenshotRequest.connect(lambda x: widget.setText(x))

            return widget

    @inject.params(window='window', config='config', screenshot='screenshot', cleaner='cleaner')
    def onScreenshot(self, event=None, window=None, config=None, screenshot=None, cleaner=None):
        if not int(config.get('screenshot.enabled')):
            return None

        import logging
        import pytesseract
        from PIL import Image
        logger = logging.getLogger('screenshot')
        logger.info('processing...')

        pixmap: QtGui.QPixmap = screenshot.take_screenshot()
        logger.info('processing pixmap...')
        if not pixmap: return None

        language = config.get('screenshot.language', 'eng')
        logger.info('processing pixmap with language: {}...'.format(language))
        if not language: return None

        image = Image.fromqpixmap(pixmap)
        if not image: return None

        string = pytesseract.image_to_string(image, lang=language)
        logger.info('ocr: {}'.format(string))
        if not string: return None

        string = cleaner(string)
        logger.info('ocr cleaned: {}'.format(string))
        if not string: return None

        if not window.translationScreenshotRequest: return None
        window.translationScreenshotRequest.emit(string)
