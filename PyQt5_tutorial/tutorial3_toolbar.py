#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication, QPushButton, QTableView, QToolBar
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def jump_A(self):
        print("Hello A.")
   

    def initUI(self):               

        table = QTableView()
        self.setCentralWidget(table)

        exitAct = QAction(QIcon('system-shutdown.png'), 'Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(self.close)

        AAct = QAction('A', self)
        AAct.setShortcut('A')
        AAct.setStatusTip('Jump to first entry with "A"')
        AAct.triggered.connect(self.jump_A)


        # self.statusBar()

        # menubar = self.menuBar()
        # fileMenu = menubar.addMenu('&File')
        # fileMenu.addAction(exitAct)

        toolbar_main = self.addToolBar('Exit')
        toolbar_main.addAction(exitAct)

        toolbar_speed_dial = self.addToolBar('SpeedDial')
        self.addToolBar(Qt.RightToolBarArea, toolbar_speed_dial)

        # toolbar_speed_dial.setOrientation(Qt.Vertical)

        toolbar_speed_dial.addAction(AAct)
        toolbar_speed_dial.addAction(BAct)
        toolbar_speed_dial.addAction(CAct)

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Main window')    
        self.show()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())