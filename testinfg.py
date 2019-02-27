from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import *
from PyQt5.QtWidgets import *
import sys


# import cardlib as pc


class MyWindow(QGroupBox):
    def __init__(self):
        super().__init__("My window content")  # Call the QWidget initialization as well!

        grid = QGridLayout()
        grid.addWidget(self.firstButtons(), 0, 0)
        grid.addWidget(self.firstButtons(), 1, 0)
        self.setLayout(grid)

        self.setGeometry(500, 300, 1000, 500)
        self.setWindowTitle('Poker Game')

    def firstButtons(self):
        groupBox = QGroupBox()

        betButton = QPushButton("Bet")
        foldButton = QPushButton("Fold")

        hbox = QHBoxLayout()
        hbox.addWidget(betButton)
        hbox.addWidget(foldButton)
        hbox.addStretch(1)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        groupBox.setLayout(vbox)

        return groupBox

    def cardButtons(self):
        groupBox = QGroupBox()
        flopCard1 = QLabel("Card 1")
        flopCard2 = QLabel("Card 2")
        flopCard3 = QLabel("Card 3")
        turnCard = QLabel("Turn")
        riverCard = QLabel("River")

        # Bet and fold button
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        # add widgets
        hbox.addWidget(flopCard1)
        hbox.addWidget(flopCard2)
        hbox.addWidget(flopCard3)
        hbox.addWidget(turnCard)
        hbox.addWidget(riverCard)

        groupBox.setLayout(hbox)

        return groupBox


app = QApplication(sys.argv)
win = MyWindow()

win.show()
app.exec_()
