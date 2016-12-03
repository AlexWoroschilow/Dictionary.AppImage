'''
Created on Oct 28, 2016

@author: sensey
'''


class Loader(object):
    _options = None

    def __init__(self, options=None):
        self._options = options

    @property
    def options(self):
        return self._options

    def __enter__(self):
        return self

    def on_loaded(self, container):
        pass

    def __exit__(self, type, value, traceback):
        pass
