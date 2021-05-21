import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from LoadFile import *
from TreeList import *


class DockWidget_CanvasLayout(QDockWidget):
	def __init__(self, MainWindow, Position):
		super().__init__("Data", MainWindow)
		self.setMinimumWidth(100)
		self.MainWindow = MainWindow
		self.initUI(MainWindow, Position)

		self._setCanvasLayout_Main()


	def initUI(self, MainWindow, Position):
		self.dockWidgetContents_data = QWidget()
		self.setWidget(self.dockWidgetContents_data)
		vbly = QVBoxLayout(self.dockWidgetContents_data)
		vbly.setContentsMargins(0, 0, 0, 0)
		

		self.btn_Main = QPushButton('Main')
		self.btn_MainwithScrollArea = QPushButton('Main + Scroll')
		self.btn_MainwithThreeSmallWindows = QPushButton('Main + 3')
		self.btn_UpAndDown = QPushButton('Up and Down')
		self.btn_Quater = QPushButton('Quater')

		self.btn_Main.clicked.connect(lambda: self._setCanvasLayout_Main())
		self.btn_UpAndDown.clicked.connect(lambda: self._setCanvasLayout_UpAndDown())
		self.btn_Quater.clicked.connect(lambda: self._setCanvasLayout_Quater())
		self.btn_MainwithThreeSmallWindows.clicked.connect(lambda: self._setCanvasLayout_MainwithThreeSmall())
		self.btn_MainwithScrollArea.clicked.connect(lambda: self._setCanvasLayout_MainwithScrollArea())
		
		btnGroup = [self.btn_Main, self.btn_MainwithScrollArea, self.btn_MainwithThreeSmallWindows, self.btn_Quater, self.btn_UpAndDown]
		for btn in btnGroup:
			vbly.addWidget(btn)

		MainWindow.addDockWidget(Qt.DockWidgetArea(Position), self)

	
	def clearLayout(self, layout):
		for i in reversed(range(layout.count())):
			# print(i, layout.itemAt(i))
			if (type(layout.itemAt(i)) == QWidgetItem):
				widget = layout.itemAt(i).widget()
				layout.removeWidget(widget)
				widget.setParent(None)
			elif (type(layout.itemAt(i)) == QGridLayout):
				self.clearLayout(layout.itemAt(i))

	def _setCanvasLayout_Main(self):	
		self.clearLayout(self.MainWindow.canvasLayout)
		for c in self.MainWindow.canvasPool:
			c.setStatus(False)
		self.MainWindow.canvasPool[0].setStatus(True)
		layout = self.MainWindow.canvasLayout
		layout.addWidget(self.MainWindow.canvasPool[0], 0, 0, -1, 1)
		layout.setColumnStretch(0, 6)
		layout.setColumnStretch(1, 0)
		layout.setColumnStretch(2, 0)
		layout.setRowStretch(0, 4)
		layout.setContentsMargins(10,10,10,10)
	def _setCanvasLayout_Quater(self):
		self.clearLayout(self.MainWindow.canvasLayout)
		for c in self.MainWindow.canvasPool:
			c.setStatus(True)
		layout = self.MainWindow.canvasLayout
		layout.addWidget(self.MainWindow.canvasPool[0], 0, 0, 1, 1)
		layout.addWidget(self.MainWindow.canvasPool[1], 1, 0, 1, 1)
		layout.addWidget(self.MainWindow.canvasPool[2], 0, 1, 1, 1)
		layout.addWidget(self.MainWindow.canvasPool[3], 1, 1, 1, 1)
		layout.setColumnStretch(0, 3)
		layout.setColumnStretch(1, 3)
		layout.setColumnStretch(2, 0)
		layout.setRowStretch(0, 2)
		layout.setRowStretch(1, 2)
		layout.setContentsMargins(10,10,10,10)
	def _setCanvasLayout_UpAndDown(self):
		self.clearLayout(self.MainWindow.canvasLayout)

		for c in self.MainWindow.canvasPool:
			c.setStatus(False)
		self.MainWindow.canvasPool[0].setStatus(True)
		self.MainWindow.canvasPool[1].setStatus(True)
		layout = self.MainWindow.canvasLayout
		layout.addWidget(self.MainWindow.canvasPool[0], 0, 0, 1, 1)
		layout.addWidget(self.MainWindow.canvasPool[1], 1, 0, 1, 1)
		layout.setColumnStretch(0, 6)
		layout.setColumnStretch(1, 0)
		layout.setColumnStretch(2, 0)
		layout.setRowStretch(0, 2)
		layout.setRowStretch(1, 2)
		layout.setContentsMargins(10,10,10,10)
	def _setCanvasLayout_MainwithScrollArea(self):
		self.clearLayout(self.MainWindow.canvasLayout)
		for c in self.MainWindow.canvasPool:
			c.setStatus(False)
		scroll = QScrollArea()
		widget = QWidget()
		hboxLayout = QHBoxLayout()
		widget.setLayout(hboxLayout)
		scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
		scroll.setWidget(widget)
		scroll.setWidgetResizable(True)

		for i in range(10):
			Label = QLabel('BlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBla')
			Label.setFixedWidth(200)
			hboxLayout.addWidget(Label)
		self.MainWindow.canvasPool[0].setStatus(True)
		layout = self.MainWindow.canvasLayout
		layout.addWidget(self.MainWindow.canvasPool[0], 0, 0, 1, 1)
		layout.addWidget(scroll, 1, 0, 1, 1)
		layout.setColumnStretch(0, 6)
		layout.setColumnStretch(1, 0)
		layout.setColumnStretch(2, 0)
		layout.setRowStretch(0, 3)
		layout.setRowStretch(1, 1)
		layout.setContentsMargins(10,10,10,10)

	def _setCanvasLayout_MainwithThreeSmall(self):
		self.clearLayout(self.MainWindow.canvasLayout)
		for c in self.MainWindow.canvasPool:
			c.setStatus(True)
		layout = self.MainWindow.canvasLayout
		layout.addWidget(self.MainWindow.canvasPool[0], 0, 0, 1, 3)
		layout.addWidget(self.MainWindow.canvasPool[1], 1, 0, 1, 1)
		layout.addWidget(self.MainWindow.canvasPool[2], 1, 1, 1, 1)
		layout.addWidget(self.MainWindow.canvasPool[3], 1, 2, 1, 1)
		layout.setColumnStretch(0, 2)
		layout.setColumnStretch(1, 2)
		layout.setColumnStretch(2, 2)
		layout.setRowStretch(0, 5)
		layout.setRowStretch(1, 1)
		layout.setContentsMargins(10,10,10,10)
