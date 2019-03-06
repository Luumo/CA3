from PyQt5.QtGui import *
from PyQt5.QtSvg import *
from PyQt5.QtWidgets import *
import cardlib


class MainWindow(QGroupBox):
    def __init__(self, game):
        super().__init__("Main window")

        # creates widgets
        cv = ControlView(game)
        pvs = [PlayerView(player) for player in game.players]
        tv = TableView(game)

        # add horizontal widgets
        hbox = QHBoxLayout()
        for pv in pvs: hbox.addWidget(pv)
        hbox.addWidget(cv)
        # add vertical widgets
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(tv)
        vbox.addLayout(hbox)

        self.setLayout(vbox)

        self.setGeometry(500, 500, 1200, 800)
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

        game.new_pot.connect(self.update_pot)
        self.update_pot()
        game.next_player.connect(self.update_active_player)
        self.update_active_player()

    def update_pot(self):
        # update pot label
        self.potLabel.setText("Pot: ${}".format(self.game.pot))

    def update_active_player(self):
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
        self.cardView = CardView(player.hand)

        # arrange vertically
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.creditLabel)
        vbox.addWidget(self.cardView)

        # arrange horizontally
        hbox = QHBoxLayout()
        # hbox.addStretch(1)
        hbox.addLayout(vbox)

        self.setLayout(hbox)

        # Model
        player.new_credits.connect(self.update_credits)
        self.update_credits()

    def update_credits(self):
        self.creditLabel.setText("Credits: ${}".format(self.player.credits))


class TableView(QGroupBox):
    def __init__(self, game):
        super().__init__("Table View")
        # widgets
        self.tableView = CardView(game.table)

        # arrange horizontally
        hbox = QHBoxLayout()
        # hbox.addStretch(1)
        hbox.addWidget(self.tableView)

        # arrange vertically
        vbox = QVBoxLayout()
        #vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)


class CardSvgItem(QGraphicsSvgItem):
    """ A simple overloaded QGraphicsSvgItem that also stores the card position """
    def __init__(self, renderer, id):
        super().__init__()
        self.setSharedRenderer(renderer)
        self.position = id


class TableScene(QGraphicsScene):
    """ A scene with a table cloth background """
    def __init__(self):
        super().__init__()
        self.tile = QPixmap('cards/table.png')
        self.setBackgroundBrush(QBrush(self.tile))


class CardItem(QGraphicsSvgItem):
    """ A simple overloaded QGraphicsSvgItem that also stores the card position """
    def __init__(self, renderer, position):
        super().__init__()
        self.setSharedRenderer(renderer)
        self.position = position


class CardView(QGraphicsView):
    """ A View widget that represents the table area displaying a players cards. """

    # Underscores indicate a private function/method!
    def __read_cards(): # Ignore the PyCharm warning on this line. It's correct.
        """
        Reads all the 52 cards from files.
        :return: Dictionary of SVG renderers
        """
        all_cards = dict() # Dictionaries let us have convenient mappings between cards and their images
        for suit_file, suit in zip('SHDC', cardlib.Suit): # Check the order of the suits here!!!
            for value_file, value in zip(['2', '3', '4', '5', '6',
                                          '7', '8', '9', '10', 'J', 'Q', 'K', 'A'], range(2, 15)):
                file = value_file + suit_file
                key = (value, suit)  # I'm choosing this tuple to be the key for this dictionary
                all_cards[key] = QSvgRenderer('cards/' + file + '.svg')
        return all_cards

    # We read all the card graphics as static class variables
    back_card = QSvgRenderer('cards/Red_Back_2.svg')
    all_cards = __read_cards()

    def __init__(self, cards_model, card_spacing=250, padding=10):
        """
        Initializes the view to display the content of the given model
        :param cards_model: A model that represents a set of cards.
        The model should have: data_changed, cards, clicked_position, flipped,
        :param card_spacing: Spacing between the visualized cards.
        :param padding: Padding of table area around the visualized cards.
        """
        self.scene = TableScene()
        super().__init__(self.scene)

        self.model = cards_model
        self.card_spacing = card_spacing
        self.padding = padding

        # Whenever the this window should update, it should call the "change_cards" method.
        # This can, for example, be done by connecting it to a signal.
        # The view can listen to changes:
        cards_model.new_cards.connect(self.change_cards)
        # It is completely optional if you want to do it this way, or have some overreaching Player/GameState
        # call the "change_cards" method instead. z

        # Add the cards the first time around to represent the initial state.
        self.change_cards()

    def change_cards(self):
        # Add the cards from scratch
        self.scene.clear()
        for i, card in enumerate(self.model):
            # The ID of the card in the dictionary of images is a tuple with (value, suit), both integers
            graphics_key = (card.get_value(), card.suit)
            renderer = self.back_card if self.model.flipped(i) else self.all_cards[graphics_key]
            c = CardItem(renderer, i)

            # Shadow effects are cool!
            shadow = QGraphicsDropShadowEffect(c)
            shadow.setBlurRadius(10.)
            shadow.setOffset(5, 5)
            shadow.setColor(QColor(0, 0, 0, 180)) # Semi-transparent black!
            c.setGraphicsEffect(shadow)

            # Place the cards on the default positions
            c.setPos(c.position * self.card_spacing, 0)
            self.scene.addItem(c)

        self.update_view()

    def update_view(self):
        scale = (self.viewport().height()-2*self.padding)/313
        self.resetTransform()
        self.scale(scale, scale)
        # Put the scene bounding box
        self.setSceneRect(-self.padding//scale, -self.padding//scale,
                          self.viewport().width()//scale, self.viewport().height()//scale)

    def resizeEvent(self, painter):
        # This method is called when the window is resized.
        # If the widget is resize, we gotta adjust the card sizes.
        # QGraphicsView automatically re-paints everything when we modify the scene.
        self.update_view()
        super().resizeEvent(painter)

    # You can remove these events if you don't need them.
    def mouseDoubleClickEvent(self, event):
        self.model.flip() # Another possible event. Lets add it to the flip functionality for fun!
