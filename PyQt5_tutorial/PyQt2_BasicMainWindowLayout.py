import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import pyqtgraph as pg
import pyqtgraph.exporters
import numpy as np

class BasicMainWindowLayout(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.pyqtGraph()


    def initUI(self):
        self.resize(1400, 900)
        # self.centralWidget = QWidget()
        # self.centralWidget().setParent(None)。
        # self.setCentralWidget(self.centralWidget)
        # self.gridLayout_3 = QtWidgets.QGridLayout(self.centralWidget)
        # self.mdiArea = QtWidgets.QMdiArea(self.centralWidget)
        # self.gridLayout_3.addWidget(self.mdiArea, 0, 0, 1, 1)

        # self.menubar = QtWidgets.QMenuBar(self)
        # self.menuFile = QtWidgets.QMenu(self.menubar)
        # self.setMenuBar(self.menubar)

        # self.statusbar = QtWidgets.QStatusBar(self)
        # self.setStatusBar(self.statusbar)

        # self.toolBar = QtWidgets.QToolBar(self)
        # self.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        # self.setWindowTitle("MainWindow Title")
        # self.menuFile.setTitle("File")
        # self.toolBar.setWindowTitle("toolBar")
        cen = self.takeCentralWidget()
        print(cen)
        self.dockWidget1 = QtWidgets.QDockWidget("Dock 1", self)
        self.dockWidget2 = QtWidgets.QDockWidget("Dock 2", self)
        # self.dockWidget3 = QtWidgets.QDockWidget("Dock 3", self)
        # self.dockWidget4 = QtWidgets.QDockWidget("Dock 4", self)
        # self.dockWidget5 = QtWidgets.QDockWidget("Dock 5", self)
        # self.dockWidget6 = QtWidgets.QDockWidget("Dock 6", self)
        self.dockWidgetContents = QtWidgets.QWidget()
        self.btn = QPushButton('Button')
        # self.gridLayout = QtWidgets.QGridLayout(self.dockWidget1)
        # self.gridLayout.addWidget(self.btn, 0, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout(self.dockWidgetContents)
        # self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.addWidget(self.btn, 0, 0, 1, 1)

        self.dockWidget1.setWidget(self.dockWidgetContents)
        # self.dockWidget1.setLayout(self.gridLayout)
        self.addDockWidget(Qt.DockWidgetArea(Qt.LeftDockWidgetArea), self.dockWidget1)
        self.addDockWidget(Qt.DockWidgetArea(Qt.RightDockWidgetArea), self.dockWidget2)
        # self.addDockWidget(Qt.DockWidgetArea(Qt.TopDockWidgetArea), self.dockWidget3)
        # self.addDockWidget(Qt.DockWidgetArea(Qt.BottomDockWidgetArea), self.dockWidget4)
        # self.addDockWidget(Qt.DockWidgetArea(Qt.LeftDockWidgetArea), self.dockWidget5)
        # self.addDockWidget(Qt.DockWidgetArea(Qt.LeftDockWidgetArea), self.dockWidget6)

    def pyqtGraph(self):
        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        hour = [1,2,3,4,5,6,7,8,9,10]
        temperature = [30,32,34,32,33,31,29,32,35,45]

        #Add Background colour to white
        self.graphWidget.setBackground('w')
        # Add Title
        self.graphWidget.setTitle("Your Title Here", color="b", size="30pt")
        # Add Axis Labels
        styles = {"color": "#f00", "font-size": "20px"}
        self.graphWidget.setLabel("left", "Temperature (°C)", **styles)
        self.graphWidget.setLabel("bottom", "Hour (H)", **styles)
        #Add legend
        self.graphWidget.addLegend()
        #Add grid
        self.graphWidget.showGrid(x=True, y=True)
        #Set Range
        self.graphWidget.setXRange(0, 10, padding=0)
        self.graphWidget.setYRange(20, 55, padding=0)

        pen = pg.mkPen(color=(255, 0, 0))
        self.graphWidget.plot(hour, temperature, name="Sensor 1",  pen=pen, symbol='+', symbolSize=30, symbolBrush=('b'))

       

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = BasicMainWindowLayout()
    main.show()
    sys.exit(app.exec_())