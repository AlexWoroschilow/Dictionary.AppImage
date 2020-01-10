#!/usr/bin/python

# -*- coding: utf-8 -*-
#coding: utf8
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
# yaml,
import logging
import optparse
from app import console

if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-w", "--wiktionary", action="store_true", default=True, dest="wiktionary", help="Work with wiktionary")
    parser.add_option("-c", "--converter", action="store_true", default=True, dest="converter", help="Display convertor window")
    parser.add_option("-a", "--process", action="store_true", default=False, dest="process", help="Convert database to dictionary")
    parser.add_option("-o", "--output", default=None, dest="output", help="Output dictionary file")
    parser.add_option("-l", "--list", action="store_true", default=False, dest="list", help="Show all words")
    parser.add_option("-q", "--query", default=None, dest="query", help="Query word")
    parser.add_option("--host", default=None, dest="host", help="Database host")
    parser.add_option("--port", default=None, dest="port", help="Database port")
    parser.add_option("--database", default=None, dest="database", help="Database name")
    parser.add_option("--user", default=None, dest="user", help="Database user")
    parser.add_option("--password", default=None, dest="password", help="Database user password")

    (options, args) = parser.parse_args()

    log_format = '[%(relativeCreated)d][%(name)s] %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.DEBUG, format=log_format)

    application = console.Console(options, args)
    application.MainLoop()
