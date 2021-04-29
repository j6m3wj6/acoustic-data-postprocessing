from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Canvas import *

class MyTree(QTreeWidget):
	def __init__(self, canvas):
		super(QTreeWidget, self).__init__()
		self.canvas = canvas
		self.setColumnCount(2)
		self.setHeaderLabels(['Label','Note'])
		self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
		self.itemChanged.connect(self.handleCheck)
		self.itemSelectionChanged.connect(self.handleSelect)

	def handleCheck(self, item):
		print("MyTree handleCheck")
		if not item.parent(): # file root
			pass
		elif(not item.data(0, QtCore.Qt.UserRole)):
			pass
			for index in range(item.childCount()):
				child = item.child(index)
				child.setCheckState(0, item.checkState(0))
				curve = child.data(0, QtCore.Qt.UserRole)

				if (item.checkState(0) == 0): 
					curve.line.set_label('_nolegend_')
					ax = self.canvas._getAxbyType(curve.type)
					if (ax and curve.line in ax.lines): ax.lines.remove(curve.line)
					else: pass		
				else: 
					curve.line.set_label(curve.legend)
					ax = self.canvas._getAxbyType(curve.type)
					if (ax and curve.line not in ax.lines): ax.add_line(curve.line)
					else: pass		
		else:
			curve = item.data(0, QtCore.Qt.UserRole)

			if (item.checkState(0) == 0): 
				curve.line.set_label('_nolegend_')
				ax = self.canvas._getAxbyType(curve.type)
				if (ax and curve.line in ax.lines): ax.lines.remove(curve.line)
				else: pass			
			else: 
				curve.line.set_label(curve.legend)
				ax = self.canvas._getAxbyType(curve.type)
				if (ax and curve.line not in ax.lines): ax.add_line(curve.line)
				else: pass

		self.canvas.ax_IMP.set_visible(bool(self.canvas.ax_IMP.lines))
		self.canvas.replot()

	def handleSelect(self):
		print("MyTree handleSelect")
		if not self.currentItem(): return
		self.canvas._resetLineWidth()
		for item in self.selectedItems():
			if not item.data(0, QtCore.Qt.UserRole): pass
			else:
				curve = item.data(0, QtCore.Qt.UserRole)
				curve.line.set_linewidth(LINEWIDTH_HIGHLIGHT)
		self.canvas.replot()

	def appendChildren(self, path, dataSequence):
		filename = path[path.rfind('/')+1:path.rfind('.')]
		fileroot = QTreeWidgetItem(self)
		fileroot.setText(0, filename)
		fileroot.setText(1, path)
		for title, lines in dataSequence.items():

			testroot = QTreeWidgetItem()
			testroot.setText(0, title)
			testroot.setCheckState(0, 0)
			for line in lines:
				child = QTreeWidgetItem()
				child.setText(0, line.label)
				child.setText(1, line.note)
				child.setData(0, QtCore.Qt.UserRole, line)
				child.setCheckState(0, 0)
				testroot.addChild(child)
			fileroot.addChild(testroot)
		self.addTopLevelItem(fileroot)
		self.expandAll()
		firstTest = fileroot.child(0)
		firstTest.setCheckState(0, 2)
		self.handleCheck(firstTest)
