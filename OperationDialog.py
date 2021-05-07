import sys, os
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from MyOperationDialogUI import *
from TreeList import *
# from UI_OperationDialog import *



class OperationDialog(QDialog):
	"""Employee dialog."""
	def __init__(self, parent=None, treeDict = None, myApp = None):
		super().__init__(parent)
		self.myApp = myApp
		self.initUI(treeDict)
		# self.ui = Ui_Dialog(Dialog = self, window=self.window,  treeDict=treeDict)

	def _createTree(self, treeDict):
		tree = TreeItem(self.myApp)
		tree.appendChildrenByTreeDict(treeDict)
		tree.setColumnCount(2)
		tree.setColumnWidth(0, 400)
		tree.setHeaderLabels(['Label','Note'])

		return tree


	def initUI(self, treeDict = None):
		self.setWindowTitle("Operation Window")
		self.resize(800, 600)
		
		
		self.treeWidget = self._createTree(treeDict)
		self.treeWidget.itemSelectionChanged.connect(self.treeWidget.handleSelect)

		label = QLabel("Offset")
		self.lineEdit = QLineEdit()
		pushButton = QPushButton("Shift")
		pushButton.clicked.connect(self.curveShift)
		buttonBox = QDialogButtonBox()
		buttonBox.setOrientation(QtCore.Qt.Horizontal)
		buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok|QDialogButtonBox.Apply)
		buttonBox.accepted.connect(self.accept)
		buttonBox.rejected.connect(self.reject)
		QtCore.QMetaObject.connectSlotsByName(self)

		vboxlayout_main = QVBoxLayout()
		vboxlayout_main.addWidget(self.treeWidget)
		vboxlayout_main.addWidget(label)
		vboxlayout_main.addWidget(self.lineEdit)
		vboxlayout_main.addWidget(pushButton)
		vboxlayout_main.addWidget(buttonBox)
		self.setLayout(vboxlayout_main)

	def handleSelect(self):
		print("MyTree handleSelect2")

	def curveShift(self):
		try:
			offset = float(self.lineEdit.text())
		except ValueError:
			print('ERROR: can not turn ' + self.lineEdit.text())
			return
		curves = []
		iterator = QTreeWidgetItemIterator(self.treeWidget)
		while (iterator.value()):
			item = iterator.value()
			if (item.data(0, QtCore.Qt.UserRole) and item.checkState(0) == 2):
				curves.append(item.data(0, QtCore.Qt.UserRole).line)
			iterator += 1
		
		for c in curves:
			xdata, ydata = c.get_data()
			new_data = [d+offset for d in ydata]
			c.set_data(xdata, new_data)

		self.myApp.canvasReplot()