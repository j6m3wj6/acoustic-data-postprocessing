import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from LoadFile import *
from TreeList import *


class DockWidget_Data(QDockWidget):
	def __init__(self, MainWindow, Position):
		super().__init__("Data", MainWindow)
		self.setMinimumWidth(400)

		self.initUI(MainWindow, Position)

	def initUI(self, MainWindow, Position):
		self.dockWidgetContents_data = QWidget()
		self.setWidget(self.dockWidgetContents_data)
		vBoxLayout = QVBoxLayout(self.dockWidgetContents_data)
		
		btn_importDialog = QPushButton("Import")
		btn_importDialog.clicked.connect(MainWindow.importDialog)

		self.tab_data = Data_Tab(MainWindow)

		vBoxLayout.setContentsMargins(0, 0, 0, 0)
		vBoxLayout.addWidget(btn_importDialog)
		vBoxLayout.addWidget(self.tab_data)

		MainWindow.addDockWidget(Qt.DockWidgetArea(Position), self)

	

class Data_Tab(QTabWidget):
	def __init__(self, MainWindow):
		super().__init__()
		self.initUI(MainWindow)
		self.currentChanged.connect(self.handleChange)

	def initUI(self, MainWindow):
		self.tree = TreeItem(MainWindow)
		self.tree_layout = QVBoxLayout()
		self.tab_ALL = QWidget()
		self.tab_ALL.setLayout(self.tree_layout)
		self.tree_layout.addWidget(self.tree)

		self.tab_SPL = QWidget()

		self.addTab(self.tab_ALL, "ALL")
		self.addTab(self.tab_SPL, "SPL")
		self.func = [self._switchToAllTab, self._switchToSPLTab]

	def handleChange(self, event):
		print(event)
		self.func[event]()
	
	def _switchToAllTab(self):
		self.tree.filterChildren("ALL")
		self.tab_ALL.setLayout(self.tree_layout)

	
	def _switchToSPLTab(self):
		self.tree.filterChildren(CurveType.FreqRes)
		self.tab_SPL.setLayout(self.tree_layout)
		# self.tab_SPL.appendChildrenByType(self.tab_ALL, CurveType.FreqRes)

	def appendData(self, DATA):
		self.tree.appendChildren(DATA)
		