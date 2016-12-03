'''
Created on Oct 6, 2016

@author: sensey
'''
import os
import platform


class Layout(object):

    @property
    def icon(self):
        if platform.system() in ["Darwin"]:
            return os.path.abspath(os.path.curdir) + "/img/icon_osx.png"
        return os.path.abspath(os.path.curdir) + "/img/dictionary.svg"

    @property
    def empty(self):
        return 0

    @property
    def text(self):
        if platform.system() in ["Darwin"]:
            return 40
        return 80

    @property
    def border(self):
        if platform.system() in ["Darwin"]:
            return 0
        return 15

    @property
    def width(self):
        if platform.system() in ["Darwin"]:
            return 600
        return 800

    @property
    def height(self):
        if platform.system() in ["Darwin"]:
            return 600
        return 900

    @property
    def grid_label_column(self):
        if platform.system() in ["Darwin"]:
            return 20
        return None

