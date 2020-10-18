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

    @inject.params(config='config')
    def _clean(self, text, config=None):
        if len(text) >= 32:
            return None

        if int(config.get('clipboard.extrachars')):
            text = ''.join(e for e in text if e.isalnum())

        if int(config.get('clipboard.uppercase')):
            text = text.lower()

        return text

    def configure(self, binder, options=None, args=None):
        from .screenshot.screenshot import Screenshot
        binder.bind('screenshot', Screenshot)

    @inject.params(parent='window', config='config')
    def boot(self, options=None, args=None, parent=None, config=None):
        from modules.window_dictionary import gui as window

        shortcut = QtWidgets.QShortcut("Ctrl+K", parent)
        shortcut.activated.connect(self.onScreenshot)

        @window.toolbar(name='Screenshot', focus=False, position=3)
        @inject.params(translator='translator.widget')
        def window_toolbar(parent=None, translator=None):
            from .toolbar.panel import ToolbarWidget
            widget = ToolbarWidget()

            if not widget.actionScreenshot: return widget
            widget.actionScreenshot.connect(self.onScreenshot)

            if not parent.actionReload: return widget
            parent.actionReload.connect(widget.reload)

            return widget

    @inject.params(window='window', config='config', screenshot='screenshot')
    def onScreenshot(self, event=None, window=None, config=None, screenshot=None):
        if not int(config.get('screenshot.enabled')):
            return None

        import logging
        import pytesseract
        from PIL import Image
        from .screenshot.screenshot import constant
        logger = logging.getLogger('screenshot')
        logger.info('processing...')

        pixmap: QtGui.QPixmap = screenshot.take_screenshot(constant.CLIPBOARD)
        logger.info('processing pixmap...')
        if not pixmap: return None

        language = config.get('screenshot.language', 'eng')
        logger.info('processing pixmap with language: {}...'.format(language))
        if not language: return None

        image = Image.fromqpixmap(pixmap)
        if not image: return None

        string = pytesseract.image_to_string(image, lang=language)
        logger.info('ocr: {}'.format(string))

        string = self._clean(string)
        logger.info('ocr cleaned: {}'.format(string))

        if not window.translationScreenshotRequest: return None
        window.translationScreenshotRequest.emit(string)
