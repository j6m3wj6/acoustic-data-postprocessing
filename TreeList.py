from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from Canvas import *

class MyTree(QSplitter):
	def __init__(self, myApp):
		super(QSplitter, self).__init__()
		self.myApp = myApp
		self.initUI()

	def initUI(self):
		# self.splitter = QSplitter(Qt.Vertical)
		
		self.LEAPtree = TreeItem(self.myApp)
		self.APtree = TreeItem(self.myApp)
		self.Klippeltree = TreeItem(self.myApp)
		self.trees = [self.LEAPtree, self.APtree, self.Klippeltree]

		self.setOrientation(Qt.Vertical)
		self.addWidget(self._createTreeItem('LEAP File', self.LEAPtree, self.myApp.btn_importLEAPData))
		self.addWidget(self._createTreeItem('AP File', self.APtree, self.myApp.btn_importAPData))
		self.addWidget(self._createTreeItem('Kilppel File', self.Klippeltree, self.myApp.btn_importNFSData))

		
		for t in self.trees:
			t.setColumnCount(2)
			t.setHeaderLabels(['File & Label','Note'])
			t.setColumnWidth(0, 300) 
			t.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

	def _createTreeItem(self, label, tree, btn):
		widget = QWidget()
		grid_layout = QGridLayout()
		widget.setLayout(grid_layout)

		grid_layout.addWidget(QLabel(label), 0, 0, 1, 1)
		grid_layout.addWidget(btn, 0, 1, 1, 1)
		grid_layout.addWidget(tree, 1, 0, 1, -1)
		grid_layout.setContentsMargins(0,0,0,0)
		return widget

	def appendChildren(self, category, path, dataSequence):
		if (category == 'LEAP'):
			self.LEAPtree.appendChildren(path, dataSequence)
		elif (category == 'AP'):
			self.APtree.appendChildren(path, dataSequence)
		else:
			self.Klippeltree.appendChildren(path, dataSequence)
	
	def getCheckedItemsTree(self):
		root = TreeItem()

		for tree in self.trees:
			for f in range(tree.topLevelItemCount()):
				fileroot = tree.topLevelItem(f)
				# checkedItemsDict[fileroot.text(0)] = {}
				fileroot_copy = fileroot.clone()
				for t in range(fileroot.childCount()):
					test = fileroot.child(t)
					if (test.checkState(0) != Qt.Checked):
						# test_copy = test.clone()
						fileroot_copy.takeChild(t)

						# if (fileroot.text(0) not in checkedItemsDict.keys()): 
						# 	checkedItemsDict[fileroot.text(0)] = {}
						# checkedItemsDict[fileroot.text(0)][test.text(0)] = test
				# if (not checkedItemsDict[fileroot.text(0)]): del checkedItemsDict[_file.text(0)]
				root.addTopLevelItem(fileroot_copy)
		return root

	def clear(self):
		for tree in self.trees:
			tree.clear()

class TreeItem(QTreeWidget):
	def __init__(self, myApp=None):
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
				curve = item.child(index).data(0, QtCore.Qt.UserRole)
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
		print("MyTree handleSelect")
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
		fileroot.setData(0, QtCore.Qt.UserRole, dataSequence)

		for title, lines in dataSequence.items():
			testroot = QTreeWidgetItem()
			testroot.setText(0, title)
			testroot.setFlags(testroot.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
			for line in lines:
				child = QTreeWidgetItem(testroot)
				child.setText(0, line.label)
				child.setText(1, line.note)
				child.setData(0, QtCore.Qt.UserRole, line)
				child.setCheckState(0, Qt.Unchecked)
				# testroot.addChild(child)
			fileroot.addChild(testroot)
		self.addTopLevelItem(fileroot)
		self.expandAll()
		firstTest = fileroot.child(0)
		firstTest.setCheckState(0, Qt.Checked)

	def appendChildrenByTreeDict(self, treeDict):
		# for f in treeDict.keys():
		# 	_file = treeDict[f]
		# 	fileroot = QTreeWidgetItem(self)
		# 	fileroot.setText(0, f)

			# for testRoot in _file.values():
			# 	copyItem = testRoot.clone()
			# 	copyItem.setData(0, QtCore.Qt.CheckStateRole, None)
			# 	fileroot.addChild(copyItem)		
		for f in range(treeDict.topLevelItemCount()):
			fileroot = treeDict.topLevelItem(f)
			print(f, fileroot)
			for t in range(fileroot.childCount()):
				print(t, fileroot.child(t))
				testRoot = fileroot.child(t)
				copyItem = testRoot.clone()
				copyItem.setData(0, QtCore.Qt.CheckStateRole, None)
				fileroot.addChild(copyItem)	

			self.addTopLevelItem(fileroot)
		self.expandAll()

	def editText(self, event):
		# print("double click", event, event.column(), event.row(), event.data())
		item = self.itemFromIndex(event)
		item.setFlags(item.flags() | Qt.ItemIsEditable)
		self.edit(event)
