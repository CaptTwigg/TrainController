import time

import serial
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QThread


class Arduino:
    def __init__(self, port,consoleLayout):
        self.arduino = serial.Serial(port, 115200, timeout=0.1)

        print("Connected to port: " + str(port))
        self.arduino = serial.Serial(port, 115200, timeout=0.1)
        # self.arduino.read
        self.thread = ReadArduino(self.arduino, consoleLayout)
        self.thread.start()


    def sendCommand(self, command):
        self.arduino.write(command.encode())


class ReadArduino(QThread):
    sig = QtCore.pyqtSignal(int)

    def __init__(self, arduino, consoleLayout):
        QThread.__init__(self)
        self.arduino = arduino
        self.consoleLayout = consoleLayout
        self.sig.connect(self.read)

    def __del__(self):
        self.wait()

    def run(self):
        while True:
            time.sleep(.05)
            if self.arduino.in_waiting > 0:
                # Emit the signal
                self.sig.emit(1)

    def read(self):
        response = self.arduino.readline()
        print("read: " + str(response.decode()))
        print("inwait: " + str(self.arduino.in_waiting))
        # if "python" in str(response.decode()):
        if response:
            try:
                self.consoleLayout.console.insertPlainText(str(response.decode()))
                self.consoleLayout.console.moveCursor(QtGui.QTextCursor.End)
            except Exception as e:
                print(e)
        # self.arduino.flush()