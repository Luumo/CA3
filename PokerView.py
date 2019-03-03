from PyQt5.QtCore import *
from cardlib import *

class TexasHoldEm(QObject):
    new_pot = pyqtSignal()
    winner = pyqtSignal(str,)

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

    def fold(self):
        # if active player folds, other player wins.
        if self.active_player() == self.players[0]:
            self.winner.emit(self.players[1].name + " won!")
        elif self.active_player() == self.players[1]:
            self.winner.emit(self.players[0].name + " won!")

    def call(self):
        # call previous players decision
        pass

    def bet(self, amount):
        self.active_player().bet(amount)
        self.pot += amount
        self.new_pot.emit()


class Player(QObject):
    new_credits = pyqtSignal()

    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.credits = 1000
        self.hand = Hand()

    def active(self):
        return self.credits > 0

    def bet(self, amount):
        self.credits -= amount
        self.new_credits.emit()

