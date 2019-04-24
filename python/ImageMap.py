import sys
import math
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class ImageMap(QWidget):
    def __init__(self):
        super().__init__()
        self.x, self.y = 400, 300
        self.showFullScreen()
        #self.setGeometry(0, 0, self.x, self.y)
        # self.setStyleSheet("background-image: url(images/switchs.jpg);")
        self.setStyleSheet("QPushButton {background : blue}")

        layout = QVBoxLayout()

        image = QImage("images/Signals.png")
        transform = QTransform()
        transform.translate(image.width()/2, image.height()/2)
        transform.rotate(90)
        image.transformed(transform)

        image = image.scaled(self.width(), self.height(), Qt.KeepAspectRatioByExpanding)
        pallet = QPalette()
        pallet.setBrush(10, QBrush(image))
        self.setPalette(pallet)

        btn = SignalButton()

        layout.addWidget(btn)

        self.setLayout(layout)


class SignalButton(QPushButton):
    def __init__(self, *__args):
        super().__init__(*__args)
        self.blockSignal = True

        self.setFixedSize(40, 100)
        self.setFlat(True)
        self.setIcon(QIcon("images/trainSignalRed.png"))
        self.setIconSize(QSize(100, 100))
        self.blockSignal = True

    def toggleSignalIcon(self):

        if self.blockSignal:
            self.setIcon(QIcon("images/trainSignalGreen.png"))
            self.blockSignal = False
        else:
            self.setIcon(QIcon("images/trainSignalRed.png"))
            self.blockSignal = True

    def mousePressEvent(self, QMouseEvent):
        self.toggleSignalIcon()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ImageMap()
    ex.show()
    sys.exit(app.exec_())
