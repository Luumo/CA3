import sys
from pokermodel import TexasHoldEm
from pokerview import *


def main():
    app = QApplication(sys.argv)
    win = MainWindow(TexasHoldEm())
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
