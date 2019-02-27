from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import *
from PyQt5.QtWidgets import *
import sys
# import cardlib as pc


class MyWindow(QGroupBox):
    def __init__(self):
        super().__init__("My window content")  # Call the QWidget initialization as well!

        betButton = QPushButton("Bet")
        foldButton = QPushButton("Fold")
        flopCard1 = QLabel("Card 1")
        flopCard2 = QLabel("Card 2")
        flopCard3 = QLabel("Card 3")
        turnCard = QLabel("Turn")
        riverCard = QLabel("River")

        # Bet and fold button
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        # add widgets
        hbox.addWidget(betButton)
        hbox.addWidget(foldButton)
        # Flop, turn, river cards
        hbox1 = QHBoxLayout()
        hbox1.addStretch(1)

        #add widgets
        boardCards = QGroupBox("board cards")
        hbox1.addWidget(flopCard1)
        hbox1.addWidget(flopCard2)
        hbox1.addWidget(flopCard3)
        hbox1.addWidget(turnCard)
        hbox1.addWidget(riverCard)

        # Arrange vertical
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.setGeometry(500, 300, 1000, 500)
        self.setWindowTitle('Poker Game')


app = QApplication(sys.argv)
win = MyWindow()

win.show()
app.exec_()