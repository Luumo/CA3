from PyQt5.QtCore import *
from cardlib import *
from gameview import *

class TexasHoldEm(QObject):
    data_changed = pyqtSignal()
    winner = pyqtSignal(str,)

    def __init__(self):
        super().__init__()
        # init players
        self.players = [Player("Janne"), Player("Fia")]
        # Data which will be changed while game is running
        self.pot = 0
        self.recent_bet = 0
        self.player_turn = 0
        self.players[self.player_turn].set_inplay(True)

    def active_player(self):
        # returns the active player
        return self.players[self.player_turn]

    def change_active_player(self):
        # Changes active player
        self.players[self.player_turn].set_inplay(False)
        self.player_turn = (self.player_turn + 1) % len(self.players)
        self.players[self.player_turn].set_inplay(True)
        self.data_changed.emit()

    def cards_on_table(self):
        # Which cards are on the table?
        pass

    def fold(self):
        # if active player folds, other player wins.
        if self.active_player() == self.players[0]:
            self.winner.emit(self.players[1].name + " won!")
        elif self.active_player() == self.players[1]:
            self.winner.emit(self.players[0].name + " won!")

    def call(self):
        # pay same ammount of credits as recent player, and keep playing
        self.bet(self.recent_bet)
        pass

    def bet(self, amount: int):
        self.active_player().bet(amount)
        self.pot += amount
        self.recent_bet = amount
        self.data_changed.emit()
        self.change_active_player()


class Player(QObject):
    new_credits = pyqtSignal()
    data_changed = pyqtSignal()

    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.credits = 1000
        self.hand = Hand()
        self.inplay = False

    def set_inplay(self, inplay):
        self.inplay = inplay
        self.data_changed.emit()

    def active(self):
        return self.credits > 0

    def bet(self, amount: int):
        self.credits -= amount
        self.new_credits.emit()


app = QApplication(sys.argv)
win = MainWindow(TexasHoldEm())
win.show()
app.exec_()
