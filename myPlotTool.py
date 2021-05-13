from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import matplotlib, random
matplotlib.use('Qt5Agg')
from matplotlib.lines import Line2D
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib.backend_bases import MouseButton

# Self-defined module
from Canvas import *
from TreeList import *
from LoadFile import *
from OperationDialog import *

PLOTAREA_GRID_ROW = 4
PLOTAREA_GRID_COL = 10

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
		self.PlotAreaWidget = QWidget()
		self.canvasPool = []
		self.canvasPool.append(MplCanvas(self, [CurveType.FreqRes, CurveType.THD]))
		self.canvasPool.append(MplCanvas(self, [CurveType.IMP, CurveType.Phase]))
		self.canvasPool.append(MplCanvas(self, [CurveType.EX, CurveType.NoType]))
		self.canvasPool.append(MplCanvas(self, [CurveType.NoType, CurveType.NoType]))
		
		self.toolbar = MyToolBar(self.canvasPool[0], self)


		self._createButton()
		self.myTree = MyTree(self)
		#----
		vboxLayout = QVBoxLayout()
		grid_layout = QGridLayout()
		grid_layout = self._createCanvasLayout_Main(grid_layout)
		# grid_layout = self._createCanvasLayout_MainwithScrollArea(grid_layout)
		# grid_layout = self._createCanvasLayout_MainwithThreeSmallWindows(grid_layout)
		# grid_layout = self._createCanvasLayout_UpAndDown(grid_layout)
		# grid_layout = self._createCanvasLayout_Quater(grid_layout)
		vboxLayout.addWidget(self.toolbar)
		vboxLayout.addLayout(grid_layout)
		self.PlotAreaWidget.setLayout(vboxLayout)
		#===========
		hboxLayout_btn = QHBoxLayout()
		hboxLayout_btn.addWidget(self.btn_clearData)
		hboxLayout_btn.addWidget(self.btn_Layout_Main)
		hboxLayout_btn.addWidget(self.btn_Layout_UpAndDown)
		hboxLayout_btn.addWidget(self.btn_Layout_Quater)
		hboxLayout_btn.addWidget(self.btn_Layout_MainwithScrollArea)
		hboxLayout_btn.addWidget(self.btn_Layout_MainwithThreeSmallWindows)
		hboxLayout_btn.addWidget(self.btn_operationDialog)
		
		#===========
		self.splitter = QSplitter(self)		
		self.splitter.addWidget(self.PlotAreaWidget)
		self.splitter.addWidget(self.myTree)
		MainLayout.addWidget(self.splitter)
		layout = QVBoxLayout()
		layout.setContentsMargins(0, 0, 0, 0)
		handle = self.splitter.handle(1)
		self.splitter.setHandleWidth(40)
		button = QToolButton(handle)
		button.setArrowType(QtCore.Qt.RightArrow)
		button.clicked.connect(
			lambda: self.handleSplitterButton(False))
		layout.addWidget(button)
		
		MainLayout.addLayout(hboxLayout_btn)
		MainWidget.setLayout(MainLayout)
		self.setCentralWidget(MainWidget)
	
# Arrange PlotArea Layout
	def _createCanvasLayout_Main(self, layout):	
		for c in self.canvasPool:
			c.setStatus(False)
		self.canvasPool[0].setStatus(True)
		layout.addWidget(self.canvasPool[0], 0, 0, -1, 1)
		layout.setColumnStretch(0, 6)
		layout.setColumnStretch(1, 0)
		layout.setColumnStretch(2, 0)
		layout.setRowStretch(0, PLOTAREA_GRID_ROW)
		layout.setContentsMargins(10,10,10,10)
		return layout
	def _createCanvasLayout_Quater(self, layout):
		for c in self.canvasPool:
			c.setStatus(True)
		layout.addWidget(self.canvasPool[0], 0, 0, 1, 1)
		layout.addWidget(self.canvasPool[1], 1, 0, 1, 1)
		layout.addWidget(self.canvasPool[2], 0, 1, 1, 1)
		layout.addWidget(self.canvasPool[3], 1, 1, 1, 1)
		layout.setColumnStretch(0, 3)
		layout.setColumnStretch(1, 3)
		layout.setColumnStretch(2, 0)
		layout.setRowStretch(0, PLOTAREA_GRID_ROW/2)
		layout.setRowStretch(1, PLOTAREA_GRID_ROW/2)
		layout.setContentsMargins(10,10,10,10)
		return layout
	def _createCanvasLayout_UpAndDown(self, layout):
		for c in self.canvasPool:
			c.setStatus(False)
		self.canvasPool[0].setStatus(True)
		self.canvasPool[1].setStatus(True)
		layout.addWidget(self.canvasPool[0], 0, 0, 1, 1)
		layout.addWidget(self.canvasPool[1], 1, 0, 1, 1)
		layout.setColumnStretch(0, 6)
		layout.setColumnStretch(1, 0)
		layout.setColumnStretch(2, 0)
		layout.setRowStretch(0, PLOTAREA_GRID_ROW/2)
		layout.setRowStretch(1, PLOTAREA_GRID_ROW/2)
		layout.setContentsMargins(10,10,10,10)
		return layout
	def _createCanvasLayout_MainwithScrollArea(self, layout):
		for c in self.canvasPool:
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
		self.canvasPool[0].setStatus(True)
		layout.addWidget(self.canvasPool[0], 0, 0, 1, 1)
		layout.addWidget(scroll, 1, 0, 1, 1)
		layout.setColumnStretch(0, 6)
		layout.setColumnStretch(1, 0)
		layout.setColumnStretch(2, 0)
		layout.setRowStretch(0, (PLOTAREA_GRID_ROW)*3/4)
		layout.setRowStretch(1, (PLOTAREA_GRID_ROW)*1/4)
		layout.setContentsMargins(10,10,10,10)
		return layout
	def _createCanvasLayout_MainwithThreeSmallWindows(self, layout):
		for c in self.canvasPool:
			c.setStatus(True)
		layout.addWidget(self.canvasPool[0], 0, 0, 1, 3)
		layout.addWidget(self.canvasPool[1], 1, 0, 1, 1)
		layout.addWidget(self.canvasPool[2], 1, 1, 1, 1)
		layout.addWidget(self.canvasPool[3], 1, 2, 1, 1)
		layout.setColumnStretch(0, 2)
		layout.setColumnStretch(1, 2)
		layout.setColumnStretch(2, 2)
		layout.setRowStretch(0, 5)
		layout.setRowStretch(1, 1)
		layout.setContentsMargins(10,10,10,10)
		return layout

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

		self.btn_Layout_Main = QPushButton('Main')
		self.btn_Layout_MainwithScrollArea = QPushButton('Main + Scroll')
		self.btn_Layout_MainwithThreeSmallWindows = QPushButton('Main + 3')
		self.btn_Layout_UpAndDown = QPushButton('Up and Down')
		self.btn_Layout_Quater = QPushButton('Quater')
		self.btn_Layout_Main.clicked.connect(self.switchToMainLayout)
		self.btn_Layout_UpAndDown.clicked.connect(self.switchToUpAndDownLayout)
		self.btn_Layout_Quater.clicked.connect(self.switchToQuaterLayout)
		self.btn_Layout_MainwithThreeSmallWindows.clicked.connect(self.switchToMainwithThreeSmallWindowsLayout)
		self.btn_Layout_MainwithScrollArea.clicked.connect(self.switchToMainwithScrollAreaLayout)

		self.btn_operationDialog = QPushButton('Operation')
		self.btn_operationDialog.clicked.connect(self.operationDialog)
# Switch Layout	
	def clearLayout(self, layout):
		for i in reversed(range(layout.count())):
			widget = layout.itemAt(i).widget()
			# print(i, widget)
			layout.removeWidget(widget)
			widget.setParent(None)

	def switchToMainLayout(self):
		layout = self.PlotAreaWidget.layout()
		self.clearLayout(layout)
		layout = self._createCanvasLayout_Main(layout)
		self.PlotAreaWidget.setLayout(layout)	
	def switchToUpAndDownLayout(self):
		layout = self.PlotAreaWidget.layout()
		self.clearLayout(layout)
		layout = self._createCanvasLayout_UpAndDown(layout)
		self.PlotAreaWidget.setLayout(layout)
	def switchToQuaterLayout(self):
		layout = self.PlotAreaWidget.layout()
		self.clearLayout(layout)
		layout = self._createCanvasLayout_Quater(layout)
		self.PlotAreaWidget.setLayout(layout)
	def switchToMainwithThreeSmallWindowsLayout(self):
		layout = self.PlotAreaWidget.layout()
		self.clearLayout(layout)
		layout = self._createCanvasLayout_MainwithThreeSmallWindows(layout)
		self.PlotAreaWidget.setLayout(layout)
	def switchToMainwithScrollAreaLayout(self):
		layout = self.PlotAreaWidget.layout()
		self.clearLayout(layout)
		layout = self._createCanvasLayout_MainwithScrollArea(layout)
		self.PlotAreaWidget.setLayout(layout)

# Close Tree Widget
	def handleSplitterButton(self, left=True):
		if not all(self.splitter.sizes()):
			self.splitter.setSizes([(self.size().width())*2/3, (self.size().width())/3])
		elif left:
			self.splitter.setSizes([0, 1])
		else:
			self.splitter.setSizes([1, 0])

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
			for title, curveDatas in dataSequence.items():
				rdm = random.randint(1, 100)
				for i in range(len(curveDatas)):
					it = curveDatas[i]
					# line = Line2D(it.xdata, it.ydata, label=it.legend, color=COLORS[i%8])
					# it.line = line
					it.set_line(it.xdata, it.ydata, it.legend, COLORS_CMP[(int(i/10))%2])
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
	def operationDialog(self):
		dlg = OperationDialog(myApp = self)
		dlg.exec()
		# self.canvasReplot()

# Canves Pool Func
	def canvasReplot(self):
		for c in self.canvasPool:
			if (c.active): c.replot()

	def getRightAx(self, _type):
		ax = None
		if (_type != CurveType.NoType):
			for c in self.canvasPool:
				ax_match = c.getAxbyType(_type)
				if (ax_match): ax = ax_match
		return ax

def main():
	app = QApplication(sys.argv)
	main = MyApp()

	main.show()
	sys.exit(app.exec_())
if __name__ == '__main__':
		main()

