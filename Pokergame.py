from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import *
from PyQt5.QtWidgets import *
import sys
# import cardlib as pc


class MainWindow(QGroupBox):
    def __init__(self):
        super().__init__("Main window")  # Call the QWidget initialization as well!

        # creates widgets
        cv = ControlView()
        pv1 = PlayerView()
        pv2 = PlayerView()
        tv = TableView()

        # add horizontal widgets
        hbox = QHBoxLayout()
        hbox.addWidget(pv1)
        hbox.addWidget(pv2)
        hbox.addWidget(cv)
        # add vertical widgets
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(tv)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.setGeometry(500, 300, 1000, 500)
        self.setWindowTitle('Poker Game')


class ControlView(QGroupBox):
    def __init__(self):
        super().__init__("Control View")  # Call the QWidget initialization as well!

        #Create buttons
        betButton = QPushButton("Bet")
        foldButton = QPushButton("Fold")
        raiseButton = QPushButton("Raise")
        checkButton = QPushButton("Check")
        betAmmount = QLineEdit()

        # arrange widgets vertically
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        # add widgets
        vbox.addWidget(betAmmount)
        vbox.addWidget(betButton)
        vbox.addWidget(foldButton)
        vbox.addWidget(raiseButton)
        vbox.addWidget(checkButton)

        # Arrange horizontally
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addLayout(vbox)

        self.setLayout(hbox)


class PlayerView(QGroupBox):
    def __init__(self):
        super().__init__("Player 1")  # Call the QWidget initialization as well!

        # widgets
        valueLabel = QLabel("Value")
        cardView = QLabel("Two Cards")
        # arrange vertically
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(valueLabel)
        vbox.addWidget(cardView)
        # arrange horizontally
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addLayout(vbox)

        self.setLayout(hbox)


class TableView(QGroupBox):
    def __init__(self):
        super().__init__("Table View")

        cardLabels = QLabel("Flop, River, Turn")

        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(cardLabels)

        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)


app = QApplication(sys.argv)
win = MainWindow()

win.show()
app.exec_()
