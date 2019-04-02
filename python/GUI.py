import sys
import glob

import serial, time

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
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
        editMenu = mainMenu.addMenu('Edit')
        viewMenu = mainMenu.addMenu('View')
        searchMenu = mainMenu.addMenu('Search')
        self.ports = mainMenu.addMenu('Ports')
        helpMenu = mainMenu.addMenu('Help')

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
        self.trainlist = TrainList()

        mainHboxLayout = QHBoxLayout()
        commandLayout = QVBoxLayout()

        onbutton = QPushButton("ON")
        offbutton = QPushButton("OFF")
        self.consoleLayout = ConsoleLayout()

        onbutton.clicked.connect(self.onclick)
        offbutton.clicked.connect(self.offclick)

        trainTopMenu = QHBoxLayout()
        trainTopMenu.addWidget(QLabel("Trains"))

        addTrainButton = QPushButton()
        addTrainButton.setMaximumWidth(30)
        addTrainButton.setFlat(True)
        addTrainButton.setIcon(QIcon("icons/add.png"))
        addTrainButton.clicked.connect(self.trainlist.addTrain)

        removeTrainButton = QPushButton()
        removeTrainButton.setMaximumWidth(30)
        removeTrainButton.setFlat(True)
        removeTrainButton.setIcon(QIcon("icons/minus.png"))
        removeTrainButton.clicked.connect(self.trainlist.removeTrain)

        stopAllTrainsBtn = QPushButton("Emergency Stop All Trains")
        stopAllTrainsBtn.setIcon(QIcon("icons/stop.png"))
        stopAllTrainsBtn.clicked.connect(
            lambda: self.arduino.sendCommand("EStop") if self.arduino is not None else None)

        trainTopMenu.addWidget(addTrainButton)
        trainTopMenu.addWidget(removeTrainButton)
        trainTopMenu.addWidget(stopAllTrainsBtn)

        commandLayout.addLayout(trainTopMenu)
        commandLayout.addWidget(self.trainlist)
        commandLayout.addWidget(onbutton)
        commandLayout.addWidget(offbutton)

        mainHboxLayout.addLayout(commandLayout)
        mainHboxLayout.addLayout(self.consoleLayout)

        self.setLayout(mainHboxLayout)

    def onclick(self):
        print(self.arduino)
        try:
            self.arduino.write("blink".encode())
        except AttributeError as e:
            self.consoleLayout.console.appendPlainText(str(e))

    def offclick(self):
        print(self.arduino)
        print(self.arduino.reset_input_buffer())
        try:
            self.arduino.write("noblink".encode())
        except AttributeError as e:
            self.consoleLayout.console.appendPlainText(str(e))

    def setConnection(self, port):
        self.arduino = Arduino(port, self.consoleLayout)
        self.trainlist.arduino = self.arduino


class TrainList(QListWidget):
    def __init__(self):
        super().__init__()
        self.arduino = None

        #self.addTrain()
        self.setStyleSheet('color: black')
        # self.itemClicked.connect(self.addTrain)

    def Clicked(self, item):
        QMessageBox.information(self, "ListWidget", "You clicked: " + item.text())

    def addTrain(self):
        listWidget = QListWidgetItem()
        trainWidget = TrainListWidget(arduino=self.arduino)

        listWidget.setSizeHint(trainWidget.sizeHint())
        self.addItem(listWidget)
        self.setItemWidget(listWidget, trainWidget)

    def removeTrain(self):
        print(self.takeItem(self.currentRow()))




class TrainListWidget(QWidget):
    def __init__(self, arduino):
        super().__init__()
        self.speed = 0
        self.arduino = None

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
        slider.valueChanged[int].connect(self.speedvalue)

        textButtonLayout = QVBoxLayout()

        trainStatus = QLabel("Train status: stopped")

        self.widgetText = QLabel("Train speed: 0")
        self.widgetText.setMinimumWidth(20)

        buttonsLayout = QVBoxLayout()

        sendButton = QPushButton("Send")
        stopButton = QPushButton("stop")
        sendButton.clicked.connect(lambda: arduino.sendCommand(f"train start {train.currentText()} {self.speed}"))
        stopButton.clicked.connect(lambda: arduino.sendCommand(f"train stop {train.currentText()} {0}"))

        # Adding layouts
        textButtonLayout.addWidget(trainStatus)
        textButtonLayout.addWidget(self.widgetText)
        trainSpeedLayout.addWidget(train)
        trainSpeedLayout.addWidget(slider)
        buttonsLayout.addWidget(sendButton)
        buttonsLayout.addWidget(stopButton)

        layout = QHBoxLayout()
        layout.addLayout(trainSpeedLayout)
        layout.addSpacing(10)
        layout.addLayout(textButtonLayout)
        layout.addSpacing(20)
        # layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Expanding))
        layout.addLayout(buttonsLayout)

        # widgetLayout.addStretch(50)

        layout.setSizeConstraint(QLayout.SetFixedSize)

        self.setLayout(layout)

    def speedvalue(self, value=0):
        if value % 2 > 0:
            value += 1
        self.speed = value
        self.widgetText.setText("Train speed: " + str(self.speed))


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

        self.addWidget(self.title)
        self.addWidget(self.console)
        btnLay = QHBoxLayout()
        btnLay.addWidget(self.clearButton)
        self.addLayout(btnLay, Qt.RightEdge)


def run():
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())


run()
