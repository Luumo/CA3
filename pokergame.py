import sys
from pokerview import *


def main():
    app = QApplication(sys.argv)
    win = MainWindow(TexasHoldEm())
    win.show()
    app.exec_()


if __name__ == "__main__":
    main()
