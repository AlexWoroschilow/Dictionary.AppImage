'''
Created on Oct 6, 2016

@author: sensey
'''
import os
import platform


class Linux(object):
    @property
    def icon(self):
        return os.path.abspath(os.path.curdir) + \
               "/img/dictionary.svg"

    @property
    def empty(self):
        return 0

    @property
    def text(self):
        return 55

    @property
    def border(self):
        return 0

    @property
    def width(self):
        return 600

    @property
    def height(self):
        return 650

    @property
    def grid_label_column(self):
        return None


class Darwin(object):
    @property
    def icon(self):
        return os.path.abspath(os.path.curdir) + \
               "/img/icon_osx.png"

    @property
    def empty(self):
        return 0

    @property
    def text(self):
        return 40

    @property
    def border(self):
        return 0

    @property
    def width(self):
        return 600

    @property
    def height(self):
        return 600

    @property
    def grid_label_column(self):
        return 20


class Layout(object):
    def platform(self):
        if platform.system() in ["Darwin"]:
            return Darwin()
        return Linux()

    @property
    def icon(self):
        return self.platform().icon

    @property
    def empty(self):
        return self.platform().empty

    @property
    def text(self):
        return self.platform().text

    @property
    def border(self):
        return self.platform().border

    @property
    def width(self):
        return self.platform().width

    @property
    def height(self):
        return self.platform().height

    @property
    def grid_label_column(self):
        return self.platform().grid_label_column
