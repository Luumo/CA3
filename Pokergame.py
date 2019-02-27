from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import *
from PyQt5.QtWidgets import *
import sys
# import cardlib as pc


class MyWindow(QGroupBox):
    def __init__(self):
        super().__init__("My window content")  # Call the QWidget initialization as well!
        car = TableCards()
        betButton = QPushButton("Bet")
        foldButton = QPushButton("Fold")


        # creates horizontal objects
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(betButton)
        hbox.addWidget(foldButton)

        # uses the horizontal objects, and aligns them vertically
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.setGeometry(500, 300, 1000, 500)
        self.setWindowTitle('POKER GAME')


class TableCards(QGroupBox):
    def __init__(self):
        super().__init__("Table Cards")

        Flop1 = QLabel("Card 1")
        Flop2 = QLabel("Card 2")
        Flop3 = QLabel("Card 3")
        Turn = QLabel("Turn")
        River = QLabel("River")

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(Flop1)
        hbox.addWidget(Flop2)
        hbox.addWidget(Flop3)
        hbox.addWidget(Turn)
        hbox.addWidget(River)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        self.setLayout(vbox)


app = QApplication(sys.argv)
win = MyWindow()
table = TableCards()

win.show()
table.show()
app.exec_()
