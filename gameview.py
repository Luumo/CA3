from PyQt5.QtGui import *
from PyQt5.QtSvg import *
from PyQt5.QtWidgets import *
import sys



class MainWindow(QGroupBox):
    def __init__(self, game):
        super().__init__("Main window")

        # creates widgets
        cv = ControlView(game)
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
        game.winner.connect(self.alert_winner)

    def alert_winner(self, text):
        msg = QMessageBox()
        msg.setText(text)
        msg.exec()


class ControlView(QGroupBox):
    def __init__(self, game):
        super().__init__("Control View")
        self.game = game

        #widgets
        self.betButton = QPushButton("Bet")
        self.betAmmount = QLineEdit()
        self.betButton.clicked.connect(self.bet_ammount)

        foldButton = QPushButton("Fold")
        foldButton.clicked.connect(game.fold)
        raiseButton = QPushButton("Raise")
        checkButton = QPushButton("Check")
        self.potLabel = QLabel()

        # arrange widgets vertically
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        # add widgets
        vbox.addWidget(self.potLabel)
        vbox.addWidget(self.betAmmount)
        vbox.addWidget(self.betButton)
        vbox.addWidget(foldButton)
        vbox.addWidget(raiseButton)
        vbox.addWidget(checkButton)

        # Arrange horizontally
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addLayout(vbox)

        self.setLayout(hbox)

        game.new_pot.connect(self.update_pot)
        self.update_pot()

    def update_pot(self):
        self.potLabel.setText("Pot: ${}".format(self.game.pot))

    def bet_ammount(self):
        self.game.bet(int(self.betAmmount.text()))


class PlayerView(QGroupBox):
    def __init__(self, player):
        super().__init__("{}".format(player.name))
        self.player = player

        # widgets
        self.creditLabel = QLabel()
        cardView = QLabel("Two Cards")

        # arrange vertically
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.creditLabel)
        vbox.addWidget(cardView)

        # arrange horizontally
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addLayout(vbox)

        self.setLayout(hbox)

        # Model
        player.new_credits.connect(self.update_credits)
        self.update_credits()

    def update_credits(self):
        self.creditLabel.setText("Credits: ${}".format(self.player.credits))


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

