import sys, os
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from matplotlib.lines import Line2D

from MyOperationDialogUI import *
from TreeList import *


class OperationDialog(QDialog):
	"""Employee dialog."""
	def __init__(self, parent=None, myApp = None):
		super().__init__(parent)
		self.myApp = myApp
		self.initUI()
		# self.ui = Ui_Dialog(Dialog = self, window=self.window,  treeDict=treeDict)

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

		buttonBox = QDialogButtonBox()
		buttonBox.setOrientation(QtCore.Qt.Horizontal)
		buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok|QDialogButtonBox.Apply)
		buttonBox.accepted.connect(self.accept)
		buttonBox.rejected.connect(self.reject)
		QtCore.QMetaObject.connectSlotsByName(self)

		self.le_shift = QLineEdit()
		btn_shift = QPushButton("Shift")
		btn_shift.clicked.connect(self.curveShift)

		self.le_alignDB = QLineEdit()
		self.le_alignFreq = QLineEdit()
		btn_align = QPushButton("Align")
		btn_align.clicked.connect(self.curveAlign)

		vboxlayout_main = QVBoxLayout()
		vboxlayout_main.addWidget(self.listWidget)
		vboxlayout_main.addWidget(QLabel("Offset"))
		vboxlayout_main.addWidget(self.le_shift)
		vboxlayout_main.addWidget(btn_shift)
		vboxlayout_main.addWidget(QLabel("Align"))
		vboxlayout_main.addWidget(self.le_alignDB)
		vboxlayout_main.addWidget(self.le_alignFreq)
		vboxlayout_main.addWidget(btn_align)
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
			offset = float(self.le_shift.text())
		except ValueError:
			print('ERROR: can not turn ' + self.le_shift.text())
			return
		
		for item in self.listWidget.selectedItems():
			curveData = item.data(Qt.UserRole)
			curveData.shift(offset)

		self.myApp.canvasReplot()

	def curveAlign(self):
		try:
			alignDB = float(self.le_alignDB.text())
			alignFreq = float(self.le_alignFreq.text())
		except ValueError:
			print('ERROR: can not turn ' + self.le_alignDB.text() + ' and ' + self.le_alignFreq.text())
			return

		for item in self.listWidget.selectedItems():
			curveData = item.data(Qt.UserRole)
			curveData.align(alignDB, alignFreq)

		self.myApp.canvasReplot()
