import sys, os
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from matplotlib.lines import Line2D

from MyOperationDialogUI import *
from TreeList import *
# from UI_OperationDialog import *



class OperationDialog(QDialog):
	"""Employee dialog."""
	def __init__(self, parent=None, myApp = None):
		super().__init__(parent)
		self.myApp = myApp
		self.initUI()
		# self.ui = Ui_Dialog(Dialog = self, window=self.window,  treeDict=treeDict)

	def _createTree(self):
		tree = self.myApp.myTree.getCheckedItemsTree()
		tree.setColumnCount(2)
		tree.setColumnWidth(0, 400)
		tree.setHeaderLabels(['Label','Note'])

		return tree

	def _createList(self):
		List = QListWidget()
		List.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

		[self._getActiveCurves(t, List) for t in self.myApp.myTree.trees]
		return List

	def _getActiveCurves(self, tree, List):
		index = 0
		for f in range(tree.topLevelItemCount()):
			fileroot = tree.topLevelItem(f)
			for t in range(fileroot.childCount()):
				testroot = fileroot.child(t)
				if (testroot.checkState(0) == Qt.Unchecked): continue
				test_item = QListWidgetItem()
				test_item.setText(fileroot.text(0)+' - '+testroot.text(0))
				test_item.setFlags(Qt.NoItemFlags)

				# test_item.setForeground(Qt.yellow)
				test_item.setBackground(Qt.lightGray)
				
				List.addItem(test_item)
				for c in range(testroot.childCount()):
					curve = testroot.child(c)
					if (curve.checkState(0) == Qt.Checked):
						curveData = curve.data(0, QtCore.Qt.UserRole)
						new_item = QListWidgetItem()
						new_item.setData(QtCore.Qt.UserRole, curveData)
						new_item.setText(curveData.label)
						List.addItem(new_item)
	


	def initUI(self):
		self.setWindowTitle("Operation Window")
		self.resize(800, 600)
		
		self.listWidget = self._createList()
		self.listWidget.itemSelectionChanged.connect(self.handleSelect)

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
		vboxlayout_main.addWidget(self.listWidget)
		vboxlayout_main.addWidget(label)
		vboxlayout_main.addWidget(self.lineEdit)
		vboxlayout_main.addWidget(pushButton)
		vboxlayout_main.addWidget(buttonBox)
		self.setLayout(vboxlayout_main)

	def handleSelect(self):
		# print("MyDialog handleSelect")
		for c in self.myApp.canvasPool:
			if (c.active):
				c._resetLineWidth()
		for item in self.listWidget.selectedItems():
			if not item.data(QtCore.Qt.UserRole): pass
			else:
				curve = item.data(QtCore.Qt.UserRole)
				curve.line.set_linewidth(LINEWIDTH_HIGHLIGHT)
		self.myApp.canvasReplot()

	def curveShift(self):
		try:
			offset = float(self.lineEdit.text())
		except ValueError:
			print('ERROR: can not turn ' + self.lineEdit.text())
			return
		
		for item in self.listWidget.selectedItems():
			curveData = item.data(Qt.UserRole)
			line = curveData.line
			xdata, ydata = line.get_data()
			new_ydata = [d+(offset-curveData.shifted) for d in ydata]
			line.set_data(xdata, new_ydata)
			curveData.shifted += (offset-curveData.shifted)

		self.myApp.canvasReplot()


