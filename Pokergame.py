from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtSvg import *
from PyQt5.QtWidgets import *
import sys
from cardlib import *


class MainWindow(QGroupBox):
    def __init__(self, game):
        super().__init__("Main window")  # Call the QWidget initialization as well!

        # creates widgets
        cv = ControlView(game.pot)
        pv1 = PlayerView(game.players[0])
        pv2 = PlayerView(game.players[1])
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

        # Model
        self.game = game
        self.update_pot()


    def update_pot(self):
        pass

class ControlView(QGroupBox):
    def __init__(self, pot):
        super().__init__("Control View")  # Call the QWidget initialization as well!
        self.pot = pot
        #Create buttons
        betButton = QPushButton("Bet")
        foldButton = QPushButton("Fold")
        raiseButton = QPushButton("Raise")
        checkButton = QPushButton("Check")
        betAmmount = QLineEdit()
        self.potLabel = QLabel()

        # arrange widgets vertically
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        # add widgets
        vbox.addWidget(self.potLabel)
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

        self.update_pot()

    def update_pot(self):
            self.potLabel.setText("Pot: ${}".format(self.pot))


class PlayerView(QGroupBox):
    def __init__(self, player):
        super().__init__()
        self.player = player
        # widgets
        self.valueLabel = QLabel()
        cardView = QLabel("Two Cards")
        # arrange vertically
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.valueLabel)
        vbox.addWidget(cardView)
        # arrange horizontally
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addLayout(vbox)

        self.setLayout(hbox)
        # Model
        self.update_credits()

    def update_credits(self):
        self.valueLabel.setText("Credits: ${}".format(self.player.credits))


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


class TexasHoldEm(QObject):
    new_pot = pyqtSignal()

    def __init__(self):
        super().__init__()
        # init players, should be represented by player class ?
        self.players = [Player("Janne"), Player("Fia")]
        # init deck
        self.deck = StandardDeck()
        # init flop (3 cards)
        self.table_cards = [self.deck.pop_card() for _ in range(3)]
        self.pot = 0

    def active_player(self):
        return self.players[0]

    def cards_on_table(self):
        # Which cards are on the table?
        pass

    def the_pot(self):
        pass

    def fold(self):
        # if active player press fold, then other player win!
        pass

    def call(self):
        # call previous players decision
        pass

    def bet(self, amount):
        self.active_player().bet(amount)
        self.pot += amount
        self.new_pot.emit()


class Player:
    new_credits = pyqtSignal()

    def __init__(self, name: str):
        self.name = name
        self.credits = 1000
        self.hand = Hand()

    def active(self):
        return self.credits > 0

    def bet(self, amount):
        self.credits -= amount
        self.new_credits.emit()




app = QApplication(sys.argv)
win = MainWindow(TexasHoldEm())
win.show()
app.exec_()
