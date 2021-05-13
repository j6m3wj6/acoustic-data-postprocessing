import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class BasicContainer(QMainWindow):

    def __init__(self):
        super().__init__()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = BasicContainer()
    main.show()
    sys.exit(app.exec_())