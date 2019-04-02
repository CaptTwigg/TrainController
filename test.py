from PyQt5 import QtCore, uic, QtWidgets

import sys

from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import *
import GUI


class App(QDialog):

    def __init__(self):
        super().__init__()

        self.title = 'PyQt5 layout - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 320
        self.height = 100
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)

        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createGridLayout()

        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)

        self.show()

    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox()

        layout = QGridLayout()
        layout.setSpacing(1)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)

        layout.addWidget(QLabel("Train"), 0, 0)
        layout.addWidget(QPushButton('2'), 0, 1)
        layout.addWidget(QPushButton('3'), 0, 2)
        layout.addWidget(QComboBox(), 1, 0)
        layout.addWidget(QPushButton('5'), 1, 1)
        layout.addWidget(QPushButton('6'), 1, 2)
        # layout.addWidget(QPushButton('7'), 2, 0)
        layout.addWidget(QLabel("Train speed"), 2, 0)
        layout.addWidget(QPushButton('9'), 2, 2)
        layout.addWidget(QSlider(Qt.Horizontal), 3, 0)

        self.horizontalGroupBox.setLayout(layout)


class TrainListWidget(QWidget):
    def __init__(self):
        super().__init__()

        trainSpeedLayout = QVBoxLayout()
        train = QComboBox()
        train.setMinimumWidth(150)
        train.setMinimumHeight(20)
        for i in range(50):
            train.addItem(str(i))

        train.setStyleSheet("QComboBox { combobox-popup: 0; }; color: rgb(255,0,0)")

        slider = QSlider(Qt.Horizontal)
        slider.setFocusPolicy(Qt.StrongFocus)
        slider.setTickPosition(QSlider.TicksBothSides)
        slider.setTickInterval(2)
        slider.setSingleStep(2)
        slider.setMinimum(-16)
        slider.setMaximum(16)
        # slider.valueChanged[int].connect(self.speedvalue)

        textButtonLayout = QVBoxLayout()

        trainStatus = QLabel("stopped")

        self.widgetText = QLabel("0")
        self.widgetText.setMinimumWidth(20)

        buttonsLayout = QVBoxLayout()

        sendButton = QPushButton("Send")
        stopButton = QPushButton("stop")
        sendButton.clicked.connect(lambda: print("clicked"))

        # Adding layouts
        textButtonLayout.addWidget(trainStatus)
        textButtonLayout.addWidget(self.widgetText)
        trainSpeedLayout.addWidget(train)
        trainSpeedLayout.addWidget(slider)
        buttonsLayout.addWidget(sendButton)
        buttonsLayout.addWidget(stopButton)

        layout = QHBoxLayout()
        layout.addLayout(trainSpeedLayout)
        layout.addLayout(textButtonLayout)
        layout.addLayout(buttonsLayout)

        # widgetLayout.addStretch(50)

        layout.setSizeConstraint(QLayout.SetFixedSize)
        self.setFixedWidth(4000)
        # self.setFixedHeight(300)
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
