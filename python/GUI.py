import sys
import glob

import serial, time

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ConsoleLayout import ConsoleLayout
from TrainLayout import TrainList, TrainLayout
from arduino import Arduino


def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    start = time.time()
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    print(time.time() - start)
    return result


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'Train - C Programming'
        self.left = 10
        self.top = 10
        self.width = 1000
        self.height = 600
        self.initUI()
        self.serial_ports = serial_ports()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.mainWidget = MainWidget(self)
        # center point of screen
        FG = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        FG.moveCenter(cp)
        self.move(FG.topLeft())

        mainMenu = self.menuBar()
        mainMenu.setNativeMenuBar(False)
        fileMenu = mainMenu.addMenu('File')
        # editMenu = mainMenu.addMenu('Edit')
        # viewMenu = mainMenu.addMenu('View')
        # searchMenu = mainMenu.addMenu('Search')
        self.ports = mainMenu.addMenu('Ports')
        # helpMenu = mainMenu.addMenu('Help')

        exitButton = QAction(QIcon('exit24.png'), 'Exit', self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip('Exit application')
        exitButton.triggered.connect(self.close)
        fileMenu.addAction(exitButton)

        self.ports.aboutToShow.connect(lambda: self.updateAvailablePorts())

        self.setCentralWidget(self.mainWidget)

    def call(self, port):
        self.mainWidget.setConnection(port)

    def updateAvailablePorts(self):
        self.ports.clear()
        for port in serial_ports():
            portButton = QAction(port, self)
            portButton.setStatusTip('Choose serial port')
            portButton.triggered.connect(lambda checked, port=port: self.call(port))
            self.ports.addAction(portButton)


class MainWidget(QWidget):
    def __init__(self, parent):
        super(MainWidget, self).__init__(parent)
        self.arduino = None
        self.trainLayout = TrainLayout()
        self.consoleLayout = ConsoleLayout()

        mainHboxLayout = QHBoxLayout()

        mainHboxLayout.addLayout(self.trainLayout)
        mainHboxLayout.addLayout(self.consoleLayout)

        self.setLayout(mainHboxLayout)

    def setConnection(self, port):
        self.arduino = Arduino(port, self.consoleLayout)
        self.trainLayout.trainList.arduino = self.arduino
        self.trainLayout.topMenu.arduino = self.arduino


def run():
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())


run()
