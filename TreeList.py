from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGugi import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Canvas import *

class MyTree(QTreeWidget):
	def __init__(self, myApp):
		super(QTreeWidget, self).__init__()
		self.myApp = myApp
		self.setColumnCount(2)
		self.setHeaderLabels(['Label','Note'])
		self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
		self.itemChanged.connect(self.handleCheck)
		self.itemSelectionChanged.connect(self.handleSelect)
		self.doubleClicked.connect(self.editText)

	def _getRightAx(self, _type):
		ax = None
		if (_type != CurveType.NoType):
			for c in self.myApp.canvasPool:
				ax_match = c._getAxbyType(_type)
				if (ax_match): ax = ax_match
		return ax

	def handleCheck(self, item):
		# print("MyTree handleCheck")
		if not item.parent(): # file root
			return
		elif(not item.data(0, QtCore.Qt.UserRole)): # test root
			dataType = item.child(0).data(0, QtCore.Qt.UserRole).type
			for index in range(item.childCount()):
				child = item.child(index)
				child.setCheckState(0, item.checkState(0))
				curve = child.data(0, QtCore.Qt.UserRole)
				if (item.checkState(0) == 0): 
					curve.line.set_label('_nolegend_')
					ax = self._getRightAx(curve.type)
					if (ax and curve.line in ax.lines): ax.lines.remove(curve.line)
				else: 
					curve.line.set_label(fill(curve.label, LEGEND_WRAP))
					ax = self._getRightAx(curve.type)
					if (ax and curve.line not in ax.lines): ax.add_line(curve.line)
		else:
			curve = item.data(0, QtCore.Qt.UserRole)
			curve.label = item.text(0)
			curve.note = item.text(1)
			if (item.checkState(0) == 0): 
				curve.line.set_label('_nolegend_')
				ax = self._getRightAx(curve.type)
				if (ax and curve.line in ax.lines): ax.lines.remove(curve.line)
			else: 
				curve.line.set_label(fill(curve.label, LEGEND_WRAP))
				ax = self._getRightAx(curve.type)
				if (ax and curve.line not in ax.lines): ax.add_line(curve.line)
		
		for c in self.myApp.canvasPool:
			if (c.active):
				c.fig.axes[1].set_visible(bool(c.fig.axes[1].lines))
		self.myApp.canvasReplot()

	def handleSelect(self):
		# print("MyTree handleSelect")
		if not self.currentItem(): return
		for c in self.myApp.canvasPool:
			if (c.active):
				c._resetLineWidth()
		for item in self.selectedItems():
			if not item.data(0, QtCore.Qt.UserRole): pass
			else:
				curve = item.data(0, QtCore.Qt.UserRole)
				curve.line.set_linewidth(LINEWIDTH_HIGHLIGHT)
		self.myApp.canvasReplot()


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

	def getCheckedItems(self):
		checkedItemsDict = {}
		for f in range(self.topLevelItemCount()):
			_file = self.topLevelItem(f)
			checkedItemsDict[_file.text(0)] = {}
			for t in range(_file.childCount()):
				test = _file.child(t)
				if (test.checkState(0)):
					checkedItemsDict[_file.text(0)][test.text(0)] = test
		return checkedItemsDict

	def editText(self, event):
		# print("double click", event, event.column(), event.row(), event.data())
		item = self.itemFromIndex(event)
		item.setFlags(item.flags() | Qt.ItemIsEditable)
		self.edit(event)
