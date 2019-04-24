from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class ConsoleLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.title = QLabel("Console")
        self.console = QPlainTextEdit()
        self.console.setStyleSheet("color : black")
        self.console.setDocumentTitle("Console")
        self.console.setReadOnly(True)
        self.clearButton = QPushButton("Clear")
        self.clearButton.clicked.connect(lambda: self.console.clear())

        self.autoScroll = QCheckBox("Auto Scroll")


        self.addWidget(self.title)
        self.addWidget(self.console)
        btnLay = QHBoxLayout()
        btnLay.addWidget(self.autoScroll)
        btnLay.addWidget(self.clearButton)
        self.addLayout(btnLay, Qt.RightEdge)
