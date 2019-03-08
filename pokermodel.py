# import sys
from PyQt5.QtCore import *
from cardlib import *
# from pokerview import *


class TexasHoldEm(QObject):
    new_pot = pyqtSignal()
    next_player = pyqtSignal()
    winner = pyqtSignal(str,)

    def __init__(self):
        super().__init__()
        # init players, deck, gameplay variables
        self.players = [Player("Janne"), Player("Fia")]
        self.pot = 0
        self.recent_bet = 0
        self.player_turn = 0
        self.table = TableModel()
        self.deck = None
        self.init_round()
        self.call_count = 0

    def _reset(self):
        self.pot = 0
        self.call_count = 0
        self.table.clear()
        self.deck = StandardDeck()
        self.deck.shuffle_deck()
        for player in self.players:
            self.new_pot.emit()
            player.hand.clear()

    def init_round(self):
        self._reset()
        # add cards to player hand
        for player in self.players:
            player.hand.clear()
            for _ in range(2):
                player.hand.add_card(self.deck.pop_card())
        self.players[self.player_turn].set_inplay(True)
        self.next_player.emit()

    def active_round(self):
        # print(self.call_count)
        if self.call_count == 2:
            self.call_count = 0
            if len(self.table.cards) == 0:
                for _ in range(3):
                    self.table.add_card(self.deck.pop_card())
            elif len(self.table.cards) < 5:
                self.table.add_card(self.deck.pop_card())
            else:
                self.announce_winner()

    def announce_winner(self):
        if len(self.table.cards) == 5:
            # Compare cards
            p1_poker_hand = self.players[0].hand.best_poker_hand(self.table.cards)
            p2_poker_hand = self.players[1].hand.best_poker_hand(self.table.cards)

            if p1_poker_hand > p2_poker_hand:
                self.winner.emit(self.players[0].name + " won with {}!".format(p1_poker_hand.pokertype.name))
                self.players[0].credits += self.pot
            else:
                self.winner.emit(self.players[1].name + " won with {}!".format(p2_poker_hand.pokertype.name))
                self.players[1].credits += self.pot

            for player in self.players:
                player.new_credits.emit()

            for player in self.players:
                if player.credits <= 0:
                    self.winner.emit("{} Lost this Game. Game will close if you press OK".format(player.name))
                    # TODO: ??
                    app.exit()
                else:
                    self.init_round()

    def active_player(self):
        return self.players[self.player_turn]

    def change_active_player(self):
        self.players[self.player_turn].set_inplay(False)
        self.player_turn = (self.player_turn + 1) % len(self.players)
        self.players[self.player_turn].set_inplay(True)
        self.next_player.emit()
        self.active_round()

    def fold(self):
        # if active player folds, other player wins.
        if self.active_player() == self.players[0]:
            self.winner.emit(self.players[1].name + " won!")
        elif self.active_player() == self.players[1]:
            self.winner.emit(self.players[0].name + " won!")
        self.init_round()

    def check(self):
        # disabled function
        # self.change_active_player()
        # self.next_player.emit()
        pass


    def call(self):
        self.call_count += 1
        # pay same amount of credits as recent player, and keep playing
        amount = self.recent_bet
        self.active_player().bet(amount)
        self.pot += amount
        self.recent_bet = amount
        self.new_pot.emit()
        self.change_active_player()

    def bet(self, amount: int):
        self.call_count = 0
        self.active_player().bet(amount)
        self.pot += amount
        self.recent_bet = amount
        self.new_pot.emit()
        self.change_active_player()


class Player(QObject):
    new_credits = pyqtSignal()

    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.credits = 1000
        self.hand = HandModel()
        self.inplay = False

    def set_inplay(self, inplay):
        self.inplay = inplay
        self.new_credits.emit()

    def active(self):
        return self.credits > 0

    def bet(self, amount: int):
        self.credits -= amount
        self.new_credits.emit()


class CardModel(QObject):
    new_cards = pyqtSignal()

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def flip(self):
        pass

    @abstractmethod
    def flipped(self, i):
        pass


class TableModel(CardModel):
    def __init__(self):
        CardModel.__init__(self)
        self.cards = []

    def __iter__(self):
        return iter(self.cards)

    def flip(self):
        pass

    def flipped(self, i):
        return False

    def add_card(self, card):
        self.cards.append(card)
        self.new_cards.emit()

    def clear(self):
        self.cards = []
        self.new_cards.emit()


class HandModel(Hand, CardModel):
    def __init__(self):
        Hand.__init__(self)
        CardModel.__init__(self)
        # Additional state needed by the UI, keeping track of the selected cards
        self.flipped_cards = True

    def __iter__(self):
        return iter(self.cards)

    def flip(self):
        # Flips over the cards (to hide them)
        self.flipped_cards = not self.flipped_cards
        self.new_cards.emit()

    def flipped(self, i):
        # This model only flips all or no cards, so we don't care about the index.
        return self.flipped_cards

    def add_card(self, card):
        super().add_card(card)
        self.new_cards.emit()

    def clear(self):
        self.cards = []
        self.new_cards.emit()

"""
app = QApplication(sys.argv)
win = MainWindow(TexasHoldEm())
win.show()
app.exec_()
"""