from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QPushButton

from .constant import *


class MyToolBar(QWidget):
    """ ToolBar widget """

    # signal
    trigger = pyqtSignal(int)

    def __init__(self, flags, parent=None):
        super(MyToolBar, self).__init__(parent)

        self.setWindowFlags(Qt.ToolTip)
        self.paddingX = 5
        self.paddingY = 2
        self.iconWidth = self.iconHeight = 28
        self.setFixedHeight(self.iconHeight + 2 * self.paddingY)

        self.cancelButton = None
        self.okButton = None

        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setContentsMargins(10, 2, 10, 2)
        self.layout().setSpacing(2)

        self.cancelButton = QPushButton(self)
        self.cancelButton.setFlat(True)
        self.cancelButton.setIcon(QIcon("icons/close"))
        self.cancelButton.setFixedSize(self.iconWidth, self.iconHeight)
        self.cancelButton.clicked.connect(self.otherButtonsClicked)

        self.okButton = QPushButton(self)
        self.okButton.setFlat(True)
        self.okButton.setIcon(QIcon("icons/check"))
        self.okButton.setFixedSize(self.iconWidth, self.iconHeight)
        self.okButton.clicked.connect(self.otherButtonsClicked)

        self.layout().addWidget(self.okButton)
        self.layout().addWidget(self.cancelButton)

    def otherButtonsClicked(self):
        if self.sender() == self.cancelButton:
            self.trigger.emit(ACTION_CANCEL)
        elif self.sender() == self.okButton:
            self.trigger.emit(ACTION_SURE)
