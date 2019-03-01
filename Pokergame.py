from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import *
from PyQt5.QtWidgets import *
import sys
from cardlib import *


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
        # widgets
        cardLabels = QLabel("Flop, River, Turn")
        # arrange horizontally
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(cardLabels)
        # arrange vertically
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)


class TexasHoldEm:
    def __init__(self):
        # init players
        self.players = ['P1', 'P2']
        # init deck
        self.deck = StandardDeck()
        # init flop (3 cards)
        self.table_cards = [self.deck.pop_card() for _ in range(3)]
        self.pot = 0



    def active_player(self):
        # Whos turn is it?
        pass

    def cards_on_table(self):
        # Which cards are on the table?
        pass

    def the_pot(self):
        # add money to pot when betting, call
        pass

    def fold(self):
        #
        pass

    def call(self):
        # call previous players decision
        pass

    def bet(self, bet_amount):
        # bet a specific ammount, add it to the pot
        pass


class Player:
    def __init__(self, name):
        self.name = name
        self.credits = 1000
        self.cards = Hand()
        self.folded = False


    def active(self):
        return self.credits > 0 and not self.folded




app = QApplication(sys.argv)
win = MainWindow()
win.show()
app.exec_()
