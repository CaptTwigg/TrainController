from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class TrainLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.arduino = None
        self.trainList = TrainList(self.arduino)
        self.topMenu = TopMenu(self.trainList, self.arduino)
        self.addLayout(self.topMenu)
        self.addWidget(self.trainList)

class TrainList(QListWidget):
    def __init__(self, arduino):
        super().__init__()
        self.arduino = arduino

        #self.addTrain()
        self.setStyleSheet('color: black')
        # self.itemClicked.connect(self.addTrain)
        #self.setStyleSheet("background-color: rgb(244,244,244), color: white")

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
            train.addItem(str(i+1))

        train.setStyleSheet("QComboBox { combobox-popup: 0; }; color: rgb(255,0,0)")

        slider = QSlider(Qt.Horizontal)
        slider.setFocusPolicy(Qt.StrongFocus)
        slider.setTickPosition(QSlider.TicksBothSides)
        slider.setTickInterval(2)
        slider.setSingleStep(2)
        slider.setMinimum(-15)
        slider.setMaximum(15)
        slider.valueChanged[int].connect(self.speedvalue)
        #slider.setStyleSheet("QSlider::groove:horizontal {background-color:rgba(255, 255, 255, 10);}")

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
        if value % 2 == 0 :
            value -= 1
        self.speed = value
        self.widgetText.setText("Train speed: " + str(self.speed))

class TopMenu(QHBoxLayout):
    def __init__(self, trainlist, arduino):
        super().__init__()
        self.trainlist = trainlist
        self.arduino = arduino
        trainTopMenu = self
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
            lambda: self.arduino.sendCommand("EStop") if self.arduino is not None else print(self.arduino))

        trainTopMenu.addWidget(addTrainButton)
        trainTopMenu.addWidget(removeTrainButton)
        trainTopMenu.addWidget(stopAllTrainsBtn)