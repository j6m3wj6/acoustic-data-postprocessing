from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import numpy as np, pandas as pd
import sys, os
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
from enum import Enum
from textwrap import fill
from matplotlib.lines import Line2D

_defaultLineWidth = 1.5
_highlightLineWidth = 4
COLORS = ['sienna', 'r', 'darkorange', 'gold', 'g', 'b', 'purple', 'gray']

class CurveType(Enum):
	NoType = 'None'
	FreqRes = 'Frequency Response'
	IMP = 'Impedance'
	Phase = 'Phase'

class CurveData:
	def __init__(self, label=None, note=None, xdata=None, ydata=None, _type=None, units=[]):
		self.label = label
		self.legend = fill(label, 11)
		self.note = note
		self.xdata = xdata
		self.ydata = ydata
		self.type = _type
		self.units = units
		self.line = None

class MplCanvas(FigureCanvasQTAgg):
	def __init__(self, parent=None):
		# Canvas init
		self.fig, _ = plt.subplots()
		# constrained_layout=True
		# self.fig.figsize = (12,4)
		super(MplCanvas, self).__init__(self.fig)
		self.fig.tight_layout()
		# self.fig.subplots_adjust(left=0.1, right=0.8, top=0.85, bottom=0.15)
		self.fig.subplots_adjust(left=0.05, right=0.8, top=0.9)

		self.ax_SPL = self.fig.axes[0]
		self.ax_SPL.set_title("SPL")
		self.ax_IMP = self.fig.axes[0].twinx()
		self.ax_IMP.set_title("IMP")
		self.ax_IMP.set_visible(False)
		self.setAxesStyle()

	def setAxStyle(self, ax):
		# axes' style
		ax.set_xscale('log')
		ax.set_xlim([20,20000])
		ax.set_ylim(auto=True)
		ax.patch.set_alpha(0.0)
		ax.grid()
		ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
	def setAxesStyle(self):
		for ax in self.fig.axes:
			ax.set_xscale('log')
			ax.set_xlim([20,20000])
			ax.set_ylim(auto=True)
			ax.grid()
			ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
			# ax.patch.set_alpha(0.0)
	
	def replot(self):
		self.ax_SPL.plot()
		self.ax_IMP.plot()
		self.ax_SPL.legend(bbox_to_anchor=(1.04,1), loc="upper left")
		self.ax_IMP.legend(bbox_to_anchor=(1.04,0), loc="lower left")
		self.draw()

	def _getAxbyType(self, curveType):
		if (curveType == CurveType.FreqRes):
			return self.ax_SPL
		elif (curveType == CurveType.IMP):
			return self.ax_IMP
		else: return None
	
	def _resetLineWidth(self):
		for ax in self.fig.axes:
			for line in ax.lines:
				line.set_linewidth(_defaultLineWidth)

class MyToolBar(NavigationToolbar2QT):
	def __init__(self,canvas_,parent_):
	#   self.toolitems = (
	#       ('Home', 'Lorem ipsum dolor sit amet', 'home', 'home'),
	#       ('Back', 'consectetuer adipiscing elit', 'back', 'back'),
	#       ('Forward', 'sed diam nonummy nibh euismod', 'forward', 'forward'),
	#       (None, None, None, None),
	#       ('Pan', 'tincidunt ut laoreet', 'move', 'pan'),
	#       ('Zoom', 'dolore magna aliquam', 'zoom_to_rect', 'zoom'),
	#       (None, None, None, None),
	#       ('Subplots', 'putamus parum claram', 'subplots', 'configure_subplots'),
	#       ('Save', 'sollemnes in futurum', 'filesave', 'save_figure'),
	#       ("Customize", "Edit axis, curve and image parameters",
	#      "qt4_editor_options", "edit_parameters"),
	#       ('Port', 'Select', "select", 'select_tool'),
	#       )
	  NavigationToolbar2QT.__init__(self,canvas_,parent_)
	def select_tool(self):
	  print("You clicked the selection tool")

class PlotGraph(QWidget):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.initUI()
		self.fileDict = {}

# User Interface

	def _createCanvasLayout_Quater(self):
		grid_layout = QGridLayout()
		self.tree.setColumnWidth(0,300)
		grid_layout.addWidget(self.canvas, 0, 0, 1, 1)
		grid_layout.addWidget(self.canvas2, 1, 0, 1, 1)
		grid_layout.addWidget(self.canvas3, 0, 1, 1, 1)
		grid_layout.addWidget(self.canvas4, 1, 1, 1, 1)
		grid_layout.addWidget(self.tree, 0, 2, -1, 1)
		grid_layout.setColumnStretch(0, 2)
		grid_layout.setColumnStretch(1, 2)
		grid_layout.setColumnStretch(2, 1)
		grid_layout.setContentsMargins(10,10,10,10)
		return grid_layout
	def _createCanvasLayout_UpAndDown(self):
		grid_layout = QGridLayout()
		self.tree.setColumnWidth(0,300)
		grid_layout.addWidget(self.canvas, 0, 0, 1, 1)
		grid_layout.addWidget(self.canvas2, 1, 0, 1, 1)
		grid_layout.addWidget(self.tree, 0, 1, -1, 1)
		grid_layout.setColumnStretch(0, 2)
		grid_layout.setColumnStretch(1, 1)
		grid_layout.setContentsMargins(10,10,10,10)
		return grid_layout
	def _createCanvasLayout_Main(self):
		grid_layout = QGridLayout()
		self.tree.setColumnWidth(0,300)
		grid_layout.addWidget(self.canvas, 0, 0, 1, 1)
		grid_layout.addWidget(self.tree, 0, 1, 1, 1)
		grid_layout.setColumnStretch(0, 2)
		grid_layout.setColumnStretch(1, 1)
		grid_layout.setContentsMargins(10,10,10,10)
		return grid_layout
	def _createCanvasLayout_MainwithScrollArea(self):
		grid_layout = QGridLayout()
		# self.tree.setColumnWidth(0,300)

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

		grid_layout.addWidget(self.canvas, 0, 0, 1, 1)
		grid_layout.addWidget(scroll, 1, 0, 1, 1)
		grid_layout.addWidget(self.tree, 0, 1, -1, 1)
		grid_layout.setColumnStretch(0, 2)
		grid_layout.setColumnStretch(1, 1)
		grid_layout.setRowStretch(0, 3)
		grid_layout.setRowStretch(1, 1)
		grid_layout.setContentsMargins(10,10,10,10)
		return grid_layout
	def _createCanvasLayout_MainwithThreeSmallWindows(self):
		grid_layout = QGridLayout()
		self.tree.setColumnWidth(0,300)
		grid_layout.addWidget(self.canvas, 0, 0, 1, 3)
		grid_layout.addWidget(self.canvas2, 1, 0, 1, 1)
		grid_layout.addWidget(self.canvas3, 1, 1, 1, 1)
		grid_layout.addWidget(self.canvas4, 1, 2, 1, 1)
		grid_layout.addWidget(self.tree, 0, 3, -1, 1)
		grid_layout.setColumnStretch(0, 2)
		grid_layout.setColumnStretch(1, 2)
		grid_layout.setColumnStretch(2, 2)
		grid_layout.setColumnStretch(3, 3)
		grid_layout.setRowStretch(0, 5)
		grid_layout.setRowStretch(1, 1)
		grid_layout.setContentsMargins(10,10,10,10)
		return grid_layout

	def initUI(self):
		# create components
		
		self._createButton()
		self._createShiftGridGroupBox()

		self.canvas = MplCanvas(self)
		self.canvas2 = MplCanvas(self)
		self.canvas3 = MplCanvas(self)
		self.canvas4 = MplCanvas(self)

		# self._createTreeList()
		self._createScrollTreeLists()
		self.toolbar = MyToolBar(self.canvas, self)
		
		# manage layout
		mainLayout = QVBoxLayout()
		# 2
		# grid_layout = self._createCanvasLayout_Main()
		grid_layout = self._createCanvasLayout_MainwithScrollArea()
		# grid_layout = self._createCanvasLayout_MainwithThreeSmallWindows()
		# grid_layout = self._createCanvasLayout_UpAndDown()
		# grid_layout = self._createCanvasLayout_Quater()
		
		# 3
		hboxLayout_btn = QHBoxLayout()
		vboxlayout_data = QVBoxLayout()
		vboxlayout_data.addWidget(self.btn_importAPData)
		vboxlayout_data.addWidget(self.btn_importLEAPData)
		vboxlayout_data.addWidget(self.btn_importNFSData)
		vboxlayout_data.addWidget(self.btn_clearData)
		hboxLayout_btn.addLayout(vboxlayout_data)
		# 4
		hboxLayout_btn.addWidget(self.shiftGridGroupBox)
		hboxLayout_btn.addWidget(QGroupBox())

		mainLayout.addWidget(self.toolbar)
		mainLayout.addLayout(grid_layout)
		mainLayout.addLayout(hboxLayout_btn)

		self.setLayout(mainLayout)

	def _createButton(self):
		self.btn_importAPData = QPushButton('Import AP data')
		self.btn_importLEAPData = QPushButton('Import LEAP data')
		self.btn_importNFSData = QPushButton('Import NFS data')
		self.btn_clearData = QPushButton('Clear data')
	def _createTreeList(self):
		self.tree=QTreeWidget()
		self.tree.setColumnCount(2)
		self.tree.setHeaderLabels(['Label','Note'])
		self.tree.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

	def _createScrollTreeLists(self):
		self.tree = QScrollArea()
		widget = QWidget()
		vboxLayout = QVBoxLayout()
		widget.setLayout(vboxLayout)
		self.tree.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
		# scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
		self.tree.setWidget(widget)
		self.tree.setWidgetResizable(True)

		for i in range(3):
			tree = QTreeWidget()
			tree.setColumnCount(2)
			tree.setHeaderLabels(['Label','Note'])
			tree.setFixedHeight(500)
			vboxLayout.addWidget(tree)
		

	def _createShiftGridGroupBox(self):
		self.shiftGridGroupBox = QGroupBox()
		layout = QVBoxLayout()
		btn_shift = QPushButton('Shift')
		self.cbox_shift = QComboBox()
		self.le_offsetInput = QLineEdit()

		layout.addWidget(btn_shift)
		layout.addWidget(self.cbox_shift)
		layout.addWidget(self.le_offsetInput) 
		self.shiftGridGroupBox.setLayout(layout)

		
class MyApp(QMainWindow):
	"""App's Main Window."""
	def __init__(self, parent=None):
		"""Initializer."""
		super().__init__(parent)
		self.initUI()

	def initUI(self):  
		self.setWindowTitle("Python Menus & Toolbars")
		self.resize(1600, 800)

		mainLayout = QVBoxLayout()
		self.canvas = MplCanvas(self)

		self.setCentralWidget(PlotGraph())



def main():
	app = QApplication(sys.argv)
	main = MyApp()
	main.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
		main()

