import datetime
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.lines import Line2D
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib.backend_bases import MouseButton

import datetime as dt

# Self-defined module
from Canvas import *
from TreeList import *
from LoadFile import *
from OperationDialog import *
from DockWidget_Data import *

# widget_tmp = MyWidget_UI()
# widget_tmp.setupUI_importFile()
# MainLayout.addWidget(widget_tmp)
import json
with open('test.json', newline='') as jsonfile:
    data = json.load(jsonfile)
    # 或者這樣
    # data = json.loads(jsonfile.read())
    print(data["Project"], data["Files"])

class MyWidget_UI(QWidget):
	def __init__(self, parent = None):
		super().__init__(parent)
		today_time = dt.datetime.today()
		self.mockData_files = [('LEAP', 'On-Axis.txt', today_time.strftime("%Y/%m/%d %H:%M:%S")),
			('AP', 'Acoustic Response.txt', (today_time + dt.timedelta(hours=3)).strftime("%Y/%m/%d %H:%M:%S")),
			('LEAP', 'On-Axis.txt', (today_time + dt.timedelta(hours=1)).strftime("%Y/%m/%d %H:%M:%S")),
			('KLIPPEL', 'On-Axis.txt', (today_time + dt.timedelta(hours=2)).strftime("%Y/%m/%d %H:%M:%S"))
		]

	def setupUI_importFile(self):
		# Layout
		self.hBoxLayout_main = QHBoxLayout(self)
		self.vBoxLayout_left = QVBoxLayout()
		self.vBoxLayout_mid = QVBoxLayout()
		self.vBoxLayout_right = QVBoxLayout()
		self.hBoxLayout_main.addLayout(self.vBoxLayout_left)
		self.hBoxLayout_main.addLayout(self.vBoxLayout_mid)
		self.hBoxLayout_main.addLayout(self.vBoxLayout_right)
		
		# Button
		self.btn_importAP = QPushButton('AP')
		self.btn_importKLIPPEL = QPushButton('KLIPPEL')
		self.btn_importLEAP = QPushButton('LEAP')
		self.btn_importCOMSOL = QPushButton('COMSOL')
		
		self.btn_deleteFile = QPushButton('Delete')
		self.btn_clearFile = QPushButton('Clear')
		self.btn_exportFile = QPushButton('Export')

		# List
		self.table_files = QTableWidget()
		self.table_files.setColumnCount(3)
		self.table_files.setHorizontalHeaderLabels(['Source', 'FileName', 'DateTime'])
		for m_data in self.mockData_files:
			source, fileName, dateTime = m_data
			row = self.table_files.rowCount()
			self.table_files.setRowCount(row + 1)
			self.table_files.setItem(row, 0, QTableWidgetItem(source))
			self.table_files.setItem(row, 1, QTableWidgetItem(fileName))
			self.table_files.setItem(row, 2, QTableWidgetItem(dateTime))

			print(row, source, fileName, dateTime)
		header = self.table_files.horizontalHeader()
		header.setStretchLastSection(True)
		self.table_files.resizeColumnsToContents()
		self.table_files.setSelectionBehavior(QAbstractItemView.SelectRows)

		# Add into Layout
		self.vBoxLayout_left.addWidget(self.btn_importAP)
		self.vBoxLayout_left.addWidget(self.btn_importKLIPPEL)
		self.vBoxLayout_left.addWidget(self.btn_importLEAP)
		self.vBoxLayout_left.addWidget(self.btn_importCOMSOL)

		self.vBoxLayout_mid.addWidget(self.table_files)

		self.vBoxLayout_right.addWidget(self.btn_deleteFile)
		self.vBoxLayout_right.addWidget(self.btn_clearFile)
		self.vBoxLayout_right.addWidget(self.btn_exportFile)







PLOTAREA_GRID_ROW = 4
PLOTAREA_GRID_COL = 10

class MyApp(QMainWindow):
	"""App's Main Window."""
	def __init__(self, parent=None):
		"""Initializer."""
		super().__init__(parent)
		self.initUI()
		
		self.fileDict = {}
	
	def _create_dockWidget_data(self):
		self.dockWidget_data = QDockWidget("Data", self)
		self.dockWidgetContents_data = QWidget()
		self.dockWidget_data.setWidget(self.dockWidgetContents_data)
		vBoxLayout = QVBoxLayout(self.dockWidgetContents_data)
		vBoxLayout.setContentsMargins(0, 0, 0, 0)


		vBoxLayout.addWidget(self.myTree)


		self.addDockWidget(Qt.DockWidgetArea(Qt.RightDockWidgetArea), self.dockWidget_data)
	

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
		
		self._createButton()
		self.myTree = MyTree(self)
		#----
		grid_layout = QGridLayout()
		grid_layout = self._createCanvasLayout_Main(grid_layout)
		# grid_layout = self._createCanvasLayout_MainwithScrollArea(grid_layout)
		# grid_layout = self._createCanvasLayout_MainwithThreeSmallWindows(grid_layout)
		# grid_layout = self._createCanvasLayout_UpAndDown(grid_layout)
		# grid_layout = self._createCanvasLayout_Quater(grid_layout)
		self.PlotAreaWidget.setLayout(grid_layout)
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
		# self.splitter = QSplitter(self)		
		# self.splitter.addWidget(self.PlotAreaWidget)
		# self.splitter.addWidget(self.myTree)
		# self.splitter.setSizes([(self.size().width())*2/3, (self.size().width())/3])

		# MainLayout.addWidget(self.splitter)



		MainLayout.addWidget(self.PlotAreaWidget)
		MainLayout.addLayout(hboxLayout_btn)


		widget_tmp = MyWidget_UI()
		widget_tmp.setupUI_importFile()
		MainLayout.addWidget(widget_tmp)

		MainWidget.setLayout(MainLayout)
		self.setCentralWidget(MainWidget)
		# self.setCentralWidget(self.PlotAreaWidget)
		# self._create_dockWidget_data()
		self.dockWidget_data = DockWidget_Data(self, Qt.RightDockWidgetArea)
		
	def handleSplitterButton(self, left=True):
		if not all(self.splitter.sizes()):
			self.splitter.setSizes([(self.size().width())*2/3, (self.size().width())/3])
		elif left:
			self.splitter.setSizes([0, 1])
		else:
			self.splitter.setSizes([1, 0])
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
		self.btn_clearData = QPushButton('Clear data')

		self.btn_Layout_Main = QPushButton('Main')
		self.btn_Layout_MainwithScrollArea = QPushButton('Main + Scroll')
		self.btn_Layout_MainwithThreeSmallWindows = QPushButton('Main + 3')
		self.btn_Layout_UpAndDown = QPushButton('Up and Down')
		self.btn_Layout_Quater = QPushButton('Quater')
		# self.btn_Layout_Main.clicked.connect(self.switchToMainLayout)
		# self.btn_Layout_UpAndDown.clicked.connect(self.switchToUpAndDownLayout)
		# self.btn_Layout_Quater.clicked.connect(self.switchToQuaterLayout)
		# self.btn_Layout_MainwithThreeSmallWindows.clicked.connect(self.switchToMainwithThreeSmallWindowsLayout)
		# self.btn_Layout_MainwithScrollArea.clicked.connect(self.switchToMainwithScrollAreaLayout)

		self.btn_operationDialog = QPushButton('Operation')
# Switch Layout	
	# def clearLayout(self, layout):
	# 	for i in reversed(range(layout.count())):
	# 		widget = layout.itemAt(i).widget()
	# 		print(i, widget)
	# 		layout.removeWidget(widget)
	# 		widget.setParent(None)

	# def switchToMainLayout(self):
	# 	layout = self.PlotAreaWidget.layout()
	# 	self.clearLayout(layout)
	# 	layout = self._createCanvasLayout_Main(layout)
	# 	self.PlotAreaWidget.setLayout(layout)	
	# def switchToUpAndDownLayout(self):
	# 	layout = self.PlotAreaWidget.layout()
	# 	self.clearLayout(layout)
	# 	layout = self._createCanvasLayout_UpAndDown(layout)
	# 	self.PlotAreaWidget.setLayout(layout)
	# def switchToQuaterLayout(self):
	# 	layout = self.PlotAreaWidget.layout()
	# 	self.clearLayout(layout)
	# 	layout = self._createCanvasLayout_Quater(layout)
	# 	self.PlotAreaWidget.setLayout(layout)
	# def switchToMainwithThreeSmallWindowsLayout(self):
	# 	layout = self.PlotAreaWidget.layout()
	# 	self.clearLayout(layout)
	# 	layout = self._createCanvasLayout_MainwithThreeSmallWindows(layout)
	# 	self.PlotAreaWidget.setLayout(layout)
	# def switchToMainwithScrollAreaLayout(self):
	# 	layout = self.PlotAreaWidget.layout()
	# 	self.clearLayout(layout)
	# 	layout = self._createCanvasLayout_MainwithScrollArea(layout)
	# 	self.PlotAreaWidget.setLayout(layout)

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

