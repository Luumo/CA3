from PyQt5.QtCore import *
from cardlib import *
from gameview import *

class TexasHoldEm(QObject):
    new_pot = pyqtSignal()
    winner = pyqtSignal(str,)

    def __init__(self):
        super().__init__()
        # init players, should be represented by player class ?
        self.players = [Player("Janne"), Player("Fia")]
        self.pot = 0

    def active_player(self):
        return self.players[0]

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
        # call previous players decision
        pass

    def bet(self, amount: int):
        self.active_player().bet(amount)
        self.pot += amount
        self.new_pot.emit()


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
