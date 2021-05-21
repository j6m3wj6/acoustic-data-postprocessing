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
		# self.addWidget(self._createTreeItem('LEAP File', self.LEAPtree, self.myApp.btn_importLEAPData))
		# self.addWidget(self._createTreeItem('AP File', self.APtree, self.myApp.btn_importAPData))
		# self.addWidget(self._createTreeItem('Kilppel File', self.Klippeltree, self.myApp.btn_importNFSData))


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
		elif (category == 'Comsol'):
			self.LEAPtree.appendChildren(path, dataSequence)
		else:
			self.Klippeltree.appendChildren(path, dataSequence)
	
	def getCheckedItemsTree(self):
		root = TreeItem()
		for tree in self.trees:
			for f in range(tree.topLevelItemCount()):
				fileroot = tree.topLevelItem(f)
				fileroot_copy = fileroot.clone()
				fileroot_copy.setData(0, QtCore.Qt.CheckStateRole, None)
				for t in range(fileroot.childCount()):
					test = fileroot.child(t)
					if (test.checkState(0) == Qt.Unchecked):
						fileroot_copy.takeChild(t)
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
		self.setColumnWidth(0, 300) 
		self.setColumnWidth(1, 300) 

		self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
		self.itemChanged.connect(self.handleCheck)
		self.itemSelectionChanged.connect(self.handleSelect)
		self.doubleClicked.connect(self.editText)
	

	def handleCheck(self, item):
		if not item.parent(): # file root
			return
		elif(type(item.data(1, QtCore.Qt.UserRole)) == CurveType): # test root
			dataType = item.child(0).data(0, QtCore.Qt.UserRole).type
			for index in range(item.childCount()):
				curve = item.child(index).data(0, QtCore.Qt.UserRole)
				if (item.checkState(0) == Qt.Unchecked): 
					curve.line.set_label('_nolegend_')
					ax = self.myApp.getRightAx(curve.type)
					if (ax and curve.line in ax.lines): ax.lines.remove(curve.line)
				elif (item.child(index).checkState(0) == Qt.Checked): 
					curve.line.set_label(curve.get_legend())
					ax = self.myApp.getRightAx(curve.type)
					if (ax and curve.line not in ax.lines): ax.add_line(curve.line)
		else: # measurement leaves
			curve = item.data(0, QtCore.Qt.UserRole)
			curve.label = item.text(0)
			curve.note = item.text(1)
			if (item.checkState(0) == Qt.Unchecked): 
				curve.line.set_label('_nolegend_')
				ax = self.myApp.getRightAx(curve.type)
				if (ax and curve.line in ax.lines): ax.lines.remove(curve.line)
			else: 
				curve.line.set_label(curve.get_legend())
				ax = self.myApp.getRightAx(curve.type)
				if (ax and curve.line not in ax.lines): ax.add_line(curve.line)
		
		for c in self.myApp.wg_canvas.canvasPool:
			if (c.active):
				c.fig.axes[1].set_visible(bool(c.fig.axes[1].lines))
		self.myApp.canvasReplot()

	def handleSelect(self):
		# print("MyTree handleSelect")

		if not self.currentItem(): return
		for c in self.myApp.wg_canvas.canvasPool:
			if (c.active):
				c._resetLineWidth()
		for it in self.selectedItems():
			if not it.data(0, QtCore.Qt.UserRole): continue # not measurement leaves
			else:
				curve = it.data(0, QtCore.Qt.UserRole)
				curve.line.set_linewidth(LINEWIDTH_HIGHLIGHT)
		self.myApp.canvasReplot()

	def appendChildren(self, DATA):
		fileroot = QTreeWidgetItem(self)
		fileroot.setText(0, DATA.name)
		fileroot.setText(1, DATA.source)
		fileroot.setExpanded(True)
		fileroot.setBackground(0, QColor(237, 237, 237))
		fileroot.setBackground(1, QColor(237, 237, 237))

		for test_name, curveDatas in DATA.sequence.items():
			testroot = QTreeWidgetItem()
			testroot.setText(0, test_name)
			testroot.setText(1, curveDatas[0].type.value)
			testroot.setData(1, QtCore.Qt.UserRole, curveDatas[0].type)
			testroot.setFlags(testroot.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
			for line in curveDatas:
				child = QTreeWidgetItem(testroot)
				child.setText(0, line.label)
				child.setText(1, line.note)
				child.setData(0, QtCore.Qt.UserRole, line)
				child.setCheckState(0, Qt.Unchecked)
			fileroot.addChild(testroot)
		self.addTopLevelItem(fileroot)
		# self.expandAll()
		# fileroot.child(0).setCheckState(0, Qt.Checked)
	
	def filterChildren(self, _type):
		self.unHideChildren()
		if (_type == "ALL"): return
		for i_f in range(self.topLevelItemCount()):
			fileroot = self.topLevelItem(i_f)
			for i_t in range(fileroot.childCount()):
				test = fileroot.child(i_t)
				test_type = test.data(1, QtCore.Qt.UserRole)
				if (test_type != _type):
					test.setHidden(True)
					
			# root.addTopLevelItem(fileroot_copy)

	def unHideChildren(self):
		for i_f in range(self.topLevelItemCount()):
			fileroot = self.topLevelItem(i_f)
			for i_t in range(fileroot.childCount()):
				test = fileroot.child(i_t)
				test.setHidden(False)



	def editText(self, event):
		# print("double click", event, event.column(), event.row(), event.data())
		item = self.itemFromIndex(event)
		item.setFlags(item.flags() | Qt.ItemIsEditable)
		self.edit(event)
 