from PyQt5.QtGui import *
from PyQt5.QtSvg import *
from PyQt5.QtWidgets import *
import sys


class TableScene(QGraphicsScene):
    """ A scene with a table cloth background """
    def __init__(self):
        super().__init__()
        self.tile = QPixmap('cards/table.png')
        self.setBackgroundBrush(QBrush(self.tile))


class CardSvgItem(QGraphicsSvgItem):
    """ A simple overloaded QGraphicsSvgItem that also stores the card position """
    def __init__(self, renderer, id):
        super().__init__()
        self.setSharedRenderer(renderer)
        self.position = id


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
        self.ActivePlayerLabel = QLabel()

        self.betButton = QPushButton("Bet")
        self.betAmmount = QLineEdit()
        self.betButton.clicked.connect(self.bet_ammount)

        self.foldButton = QPushButton("Fold")
        self.foldButton.clicked.connect(game.fold)

        self.callButton = QPushButton("Call")
        self.callButton.clicked.connect(game.call)

        self.checkButton = QPushButton("Check")
        self.checkButton.clicked.connect(game.check)

        self.potLabel = QLabel()

        # arrange widgets vertically
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        # add widgets
        vbox.addWidget(self.ActivePlayerLabel)
        vbox.addWidget(self.potLabel)
        vbox.addWidget(self.betAmmount)
        vbox.addWidget(self.betButton)
        vbox.addWidget(self.callButton)
        vbox.addWidget(self.foldButton)
        vbox.addWidget(self.checkButton)

        # Arrange horizontally
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addLayout(vbox)

        self.setLayout(hbox)

        game.data_changed.connect(self.update)
        self.update()

    def update(self):
        # update pot label
        self.potLabel.setText("Pot: ${}".format(self.game.pot))
        # update active player label
        self.ActivePlayerLabel.setText("Active Player: {}".format(self.game.active_player().name))

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
        player.data_changed.connect(self.update_credits)
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

