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

import platform
from PyQt5 import QtGui

from lib.plugin import Loader


class Loader(Loader):

    @property
    def config(self):
        return None

    @property
    def enabled(self):
        if hasattr(self._options, 'converter'):
            return not self._options.converter
        if platform.system() in ["Linux"]:
            return True
        return False

    @inject.params(window='window')
    def boot(self, options=None, args=None, window=None):
        icon = QtGui.QIcon("icons/dictionary.svg")
        if not icon.isNull():
            window.setWindowIcon(icon)
