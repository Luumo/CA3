from PyQt5.QtCore import *
from cardlib import *
from pokerview import *
import sys


class TexasHoldEm(QObject):
    new_pot = pyqtSignal()
    next_player = pyqtSignal()
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
        self.next_player.emit()

    def fold(self):
        # if active player folds, other player wins.
        if self.active_player() == self.players[0]:
            self.winner.emit(self.players[1].name + " won!")
        elif self.active_player() == self.players[1]:
            self.winner.emit(self.players[0].name + " won!")

    def check(self):
        # TODO: only allow check when noone have betted. else warn to do something else
        self.change_active_player()
        self.next_player.emit()

    def call(self):
        # pay same ammount of credits as recent player, and keep playing
        self.bet(self.recent_bet)

    def bet(self, amount: int):
        self.active_player().bet(amount)
        self.pot += amount
        self.recent_bet = amount
        self.new_pot.emit()
        self.change_active_player()

    def next_round(self):
        #  wipe cards, deck, pot
        # self.deck = StandardDeck()
        # self.pot = 0
        # activate player
        # self.new_active_player.emit()
        pass

    def cards_on_table(self):
        # Which cards are on the table?
        pass


class Player(QObject):
    new_credits = pyqtSignal()

    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.credits = 1000
        self.hand = Hand()
        self.inplay = False

    def set_inplay(self, inplay):
        self.inplay = inplay
        self.new_credits.emit()

    def active(self):
        return self.credits > 0

    def bet(self, amount: int):
        self.credits -= amount
        self.new_credits.emit()

class HandModel(Hand, QObject):
    data_changed = pyqtSignal()

    def __init__(self):
        Hand.__init__(self)
        QObject.__init__(self)

        # Additional state needed by the UI, keeping track of the selected cards:
        self.marked_cards = [False]*len(self.cards)
        self.flipped_cards = True

    def flip(self):
        # Flips over the cards (to hide them)
        self.flipped_cards = not self.flipped_cards
        self.data_changed.emit()

    def marked(self, i):
        return self.marked_cards[i]

    def flipped(self, i):
        # This model only flips all or no cards, so we don't care about the index.
        # Might be different for other games though!
        return self.flipped_cards

    def clicked_position(self, i):
        # Mark the card as position "i" to be thrown away
        self.marked_cards[i] = not self.marked_cards[i]
        self.data_changed.emit()

    def add_card(self, card):
        super().add_card(card)
        self.data_changed.emit()


# pokergame.py
app = QApplication(sys.argv)
win = MainWindow(TexasHoldEm())
win.show()
app.exec_()
