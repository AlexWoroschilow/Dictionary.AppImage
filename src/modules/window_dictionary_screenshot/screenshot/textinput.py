from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QHBoxLayout, QPushButton


class ToolbarWidget(QtWidgets.QFrame):
    okPressed = pyqtSignal()
    cancelPressed = pyqtSignal()

    def __init__(self, parent=None):
        super(ToolbarWidget, self).__init__(parent)

        self.setWindowFlags(Qt.FramelessWindowHint)

        self.setLayout(QHBoxLayout())

        self.cancelButton = QPushButton('Cancel', self)
        self.cancelButton.clicked.connect(self.cancelPressed)

        self.okButton = QPushButton('Ok', self)
        self.okButton.clicked.connect(self.okButtonClicked)

        self.layout().addWidget(self.cancelButton)
        self.layout().addWidget(self.okButton)

    def cancelButtonClicked(self):
        self.cancelPressed.emit()

    def okButtonClicked(self):
        self.okPressed.emit()
