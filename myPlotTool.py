from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.lines import Line2D
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib.backend_bases import MouseButton

# Self-defined module
from Canvas import *
from TreeList import *
from LoadFile import *
from OperationDialog import *


class MyApp(QMainWindow):
	"""App's Main Window."""
	def __init__(self, parent=None):
		"""Initializer."""
		super().__init__(parent)
		self.initUI()
		self.fileDict = {}

	def initUI(self):  
		self.setWindowTitle("Python Menus & Toolbars")
		self.resize(1600, 800)
		MainWidget = QWidget()
		MainLayout = QVBoxLayout()
		#===========
		PlotAreaWidget = QWidget()
		self.canvasPool = []
		self.canvasPool.append(MplCanvas(self, [CurveType.FreqRes, CurveType.IMP]))
		self.canvasPool.append(MplCanvas(self, [CurveType.THD, CurveType.NoType]))
		self.canvasPool.append(MplCanvas(self, [CurveType.NoType, CurveType.NoType]))
		self.canvasPool.append(MplCanvas(self, [CurveType.NoType, CurveType.NoType]))
		self._createButton()
		self._createShiftGridGroupBox()
		self.myTree = MyTree(self)
		#----
		grid_layout = self._createCanvasLayout_Main()
		# grid_layout = self._createCanvasLayout_MainwithScrollArea()
		# grid_layout = self._createCanvasLayout_MainwithThreeSmallWindows()
		# grid_layout = self._createCanvasLayout_UpAndDown()
		# grid_layout = self._createCanvasLayout_Quater()
		PlotAreaWidget.setLayout(grid_layout)
		#===========
		hboxLayout_btn = QHBoxLayout()
		hboxLayout_btn.addWidget(self.btn_clearData)
		hboxLayout_btn.addWidget(self.shiftGridGroupBox)
		#===========
		MainLayout.addWidget(PlotAreaWidget)
		MainLayout.addLayout(hboxLayout_btn)
		MainWidget.setLayout(MainLayout)
		self.setCentralWidget(MainWidget)
	
# Arrange PlotArea Layout
	def _createCanvasLayout_Quater(self):
		grid_layout = QGridLayout()
		for c in self.canvasPool:
			c.setStatus(True)
		grid_layout.addWidget(self.canvasPool[0], 0, 0, 1, 1)
		grid_layout.addWidget(self.canvasPool[1], 1, 0, 1, 1)
		grid_layout.addWidget(self.canvasPool[2], 0, 1, 1, 1)
		grid_layout.addWidget(self.canvasPool[3], 1, 1, 1, 1)
		grid_layout.addWidget(self.myTree, 0, 2, -1, 1)
		grid_layout.setColumnStretch(0, 2)
		grid_layout.setColumnStretch(1, 2)
		grid_layout.setColumnStretch(2, 1)
		grid_layout.setContentsMargins(10,10,10,10)
		return grid_layout
	def _createCanvasLayout_UpAndDown(self):
		grid_layout = QGridLayout()
		self.canvasPool[0].setStatus(True)
		self.canvasPool[1].setStatus(True)
		grid_layout.addWidget(self.canvasPool[0], 0, 0, 1, 1)
		grid_layout.addWidget(self.canvasPool[1], 1, 0, 1, 1)
		grid_layout.addWidget(self.myTree, 0, 1, -1, 1)
		grid_layout.setColumnStretch(0, 2)
		grid_layout.setColumnStretch(1, 1)
		grid_layout.setContentsMargins(10,10,10,10)
		return grid_layout
	def _createCanvasLayout_Main(self):
		grid_layout = QGridLayout()
		self.canvasPool[0].setStatus(True)
		grid_layout.addWidget(self.canvasPool[0], 0, 0, 1, 1)
		grid_layout.addWidget(self.myTree, 0, 1, 1, 1)
		grid_layout.setColumnStretch(0, 2)
		grid_layout.setColumnStretch(1, 1)
		grid_layout.setContentsMargins(10,10,10,10)
		return grid_layout
	def _createCanvasLayout_MainwithScrollArea(self):
		grid_layout = QGridLayout()

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
		self.canvasPool[0].setStatus(True)
		grid_layout.addWidget(self.canvasPool[0], 0, 0, 1, 1)
		grid_layout.addWidget(scroll, 1, 0, 1, 1)
		grid_layout.addWidget(self.myTree, 0, 1, -1, 1)
		grid_layout.setColumnStretch(0, 2)
		grid_layout.setColumnStretch(1, 1)
		grid_layout.setRowStretch(0, 3)
		grid_layout.setRowStretch(1, 1)
		grid_layout.setContentsMargins(10,10,10,10)
		return grid_layout
	def _createCanvasLayout_MainwithThreeSmallWindows(self):
		grid_layout = QGridLayout()
		for c in self.canvasPool:
			c.setStatus(True)
		grid_layout.addWidget(self.canvasPool[0], 0, 0, 1, 3)
		grid_layout.addWidget(self.canvasPool[1], 1, 0, 1, 1)
		grid_layout.addWidget(self.canvasPool[2], 1, 1, 1, 1)
		grid_layout.addWidget(self.canvasPool[3], 1, 2, 1, 1)
		grid_layout.addWidget(self.myTree, 0, 3, -1, 1)
		grid_layout.setColumnStretch(0, 2)
		grid_layout.setColumnStretch(1, 2)
		grid_layout.setColumnStretch(2, 2)
		grid_layout.setColumnStretch(3, 3)
		grid_layout.setRowStretch(0, 5)
		grid_layout.setRowStretch(1, 1)
		grid_layout.setContentsMargins(10,10,10,10)
		return grid_layout

# Create Components
	def _createButton(self):
		self.btn_importAPData = QPushButton('Import AP data')
		self.btn_importLEAPData = QPushButton('Import LEAP data')
		self.btn_importNFSData = QPushButton('Import NFS data')
		self.btn_importAPData.clicked.connect(self.plotAPData)
		self.btn_importLEAPData.clicked.connect(self.plotLEAPData)
		self.btn_importNFSData.clicked.connect(self.plotKlippelData)
		self.btn_clearData = QPushButton('Clear data')
		self.btn_clearData.clicked.connect(self.clearData)

	def _createShiftGridGroupBox(self):
		self.shiftGridGroupBox = QGroupBox()
		layout = QVBoxLayout()
		btn_shift = QPushButton('Shift')
		# btn_shift.clicked.connect(self.dialog_shift)
		btn_shift.clicked.connect(self.curveShift)
		self.cbox_shift_group = QComboBox()
		self.cbox_shift_curve = QComboBox()
		# self.cbox_shift.currentIndexChanged.connect(self.cbox_handleChange)
		self.le_offsetInput = QLineEdit()

		layout.addWidget(btn_shift)
		layout.addWidget(self.cbox_shift_group)
		layout.addWidget(self.cbox_shift_curve)
		layout.addWidget(self.le_offsetInput) 
		self.shiftGridGroupBox.setLayout(layout)

# Btn Func - Plot Data
	def plotAPData(self):
		path, dataSequence = load_AP_file()
		self.plotData('AP', path, dataSequence)
	def plotLEAPData(self):
		path, dataSequence = load_LEAP_file()
		self.plotData('LEAP', path, dataSequence)
	def plotKlippelData(self):
		path, dataSequence = load_Klippel_file()
		self.plotData('Klippel', path, dataSequence)
	def plotData(self, category, path, dataSequence):
		if (dataSequence): 
			for title, cruvesArr in dataSequence.items():
				for i in range(len(cruvesArr)):
					it = cruvesArr[i]
					line = Line2D(it.xdata, it.ydata, label=it.legend, color=COLORS[i%8])
					it.line = line
			self.fileDict[path] = dataSequence
			self.canvasReplot()
			self.myTree.appendChildren(category, path, dataSequence)
		else:
			print("Not support this file!")

# Btn Func - Clear data
	def clearData(self):
		for c in self.canvasPool:
			for ax in c.fig.axes:
	  			ax.lines = []
			c.replot()
		self.myTree.clear()

# Btn Func - Shift Data
	def curveShift(self):
		# treeDict = self.myTree.getCheckedItems()
		# treeDict = self.myTree.getCheckedItemsTree()
		# print(treeDict)
		dlg = OperationDialog(myApp = self)
		dlg.exec()
		# self.canvasReplot()

	def canvasReplot(self):
		for c in self.canvasPool:
			if (c.active): c.replot()

def main():
	app = QApplication(sys.argv)
	main = MyApp()

	main.show()
	sys.exit(app.exec_())
if __name__ == '__main__':
		main()

