#!/usr/bin/python3

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
from importlib import util

abspath = sys.argv[0] \
    if len(sys.argv) else \
    os.path.abspath(__file__)
os.chdir(os.path.dirname(abspath))

import mmap
import PyQt5
import inject
from PyQt5 import QtWidgets

import optparse
import logging
import sqlite3
import configparser


class Application(QtWidgets.QApplication):
    kernel = None

    def __init__(self, options=None, args=None):
        super(Application, self).__init__(sys.argv)

        self.setApplicationName('Dictionary')

        spec = util.find_spec('lib.kernel')
        module = spec.loader.load_module()
        if module is None: return None

        self.kernel = module.Kernel(options, args)

    @inject.params(window='window')
    def exec_(self, options, args, window):
        if window is None:
            return None

        window.exit.connect(self.exit)
        window.show()

        return super(Application, self).exec_()


if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-t", "--tray", action="store_true", default=False, dest="tray")
    parser.add_option("-w", "--word", default="baum", dest="word", help="word to translate")

    logfile = os.path.expanduser('~/.config/AOD-Dictionary/dictionary.log')
    parser.add_option("--logfile", default=logfile, dest="logfile", help="Logfile location")
    parser.add_option("--loglevel", default=logging.DEBUG, dest="loglevel", help="Logging level")

    configfile = os.path.expanduser('~/.config/AOD-Dictionary/dictionary.conf')
    parser.add_option("--config", default=configfile, dest="config", help="Config file location")

    (options, args) = parser.parse_args()

    log_format = '[%(relativeCreated)d][%(name)s] %(levelname)s - %(message)s'
    logging.basicConfig(level=options.loglevel, format=log_format)

    application = Application(options, args)
    sys.exit(application.exec_(options, args))
