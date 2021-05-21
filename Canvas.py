from enum import Enum
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from textwrap import fill
from matplotlib.lines import Line2D

import matplotlib.image as mpimg

LINEWIDTH_DEFAULT = 1.5
LINEWIDTH_HIGHLIGHT = 4
COLORS = ['sienna', 'r', 'darkorange', 'gold', 'g', 'b', 'purple', 'gray']
COLORS_CMP = ['r', 'b', 'g']
LEGEND_WRAP = 30

class CurveType(Enum):
	NoType = 'None'
	FreqRes = 'Frequency Response'
	IMP = 'Impedance'
	Phase = 'Phase'
	THD = 'THD'
	EX = 'Excursion'


class CurveData:
	def __init__(self, label=None, note=None, xdata=None, ydata=None, _type=None, units=[]):
		self.label = label
		# self.legend = fill(self.label, LEGEND_WRAP)
		# self.legend = fill(self.label, 11)
		self.note = note
		self.xdata = xdata
		self.ydata = ydata
		self.type = _type
		self.shifted = 0
		self.units = units
		self.line = None

	def shift(self, offset):
		xdata, ydata = self.line.get_data()
		new_ydata = [d+(offset-self.shifted) for d in ydata]
		self.line.set_data(xdata, new_ydata)
		self.shifted += (offset-self.shifted)

	def align(self, targetDB, freq):
		xdata, ydata = self.line.get_data()
		(index, freq) = min(enumerate(xdata), key=lambda x: abs(x[1]-freq))
		offset = targetDB - ydata[index]
		self.shift(offset)
	
	def set_line(self, xdata, ydata, label, color):
		self.line = Line2D(xdata, ydata, label=label, color=color, picker=True)

	def get_legend(self):
		# if (len(self.label) < LEGEND_WRAP): return self.label.ljust(LEGEND_WRAP, ' ')
		# else: 
		return fill(self.label, LEGEND_WRAP)
	def get_dict(self):
		dictToJSON = {
			'Data Type': self.type.value,
			'xData': self.xdata.to_numpy().tolist(),
			'yData': self.ydata.to_numpy().tolist(),
			'Label': self.label,
			'Note': self.note,
		}
		return dictToJSON



		


class MplCanvas(FigureCanvasQTAgg):
	def __init__(self, parent=None, types=[], status=False):
		# Canvas init
		self.fig, _ = plt.subplots(constrained_layout = True)
		super(MplCanvas, self).__init__(self.fig)


		self.ax_main = self.fig.axes[0]

		self.ax_sub = self.fig.axes[0].twinx()
		self.ax_sub.set_visible(False)
		self.setAxesStyle()

		self.ax_types = types
		self.active = status

		self.fig.canvas.mpl_connect('pick_event', self.on_pick)

		self.ax_main.text(1.07, 0.98, "Label                         ", transform=self.ax_main.transAxes)


	def setStatus(self, status):
		self.active = status

	def setAxStyle(self, ax):
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
	
	def replot(self):
		self.ax_main.plot()
		self.ax_main.legend(bbox_to_anchor=(1.07, .5, .18, .5), loc="upper left", borderaxespad = 0)

		if (self.ax_sub.get_visible()):
			self.ax_sub.plot()
			self.ax_sub.legend(bbox_to_anchor=(1.07, 0, .18, .5), loc="lower left", borderaxespad = 0)
		self.draw()

	def getAxbyType(self, curveType):
		if (self.ax_types[0] == curveType): 
			return self.ax_main
		elif (self.ax_types[1] == curveType):
			return self.ax_sub
		else: return None

	def _resetLineWidth(self):
		for ax in self.fig.axes:
			for line in ax.lines:
				line.set_linewidth(LINEWIDTH_DEFAULT)
	
	def on_pick(self, event):
		print('pick event')
		print(event)


class MyToolBar(NavigationToolbar2QT):
	def __init__(self, canvas_, parent_ = None):

		# toolitem = (text, tooltip_text, image_file, callback)
		self.toolitems = (
			('Home', 'Lorem ipsum dolor sit amet', 'home', 'home'),
			('Back', 'consectetuer adipiscing elit', 'back', 'back'),
			('Forward', 'sed diam nonummy nibh euismod', 'forward', 'forward'),
			('Pan', 'tincidunt ut laoreet', 'move', 'pan'),
			('Zoom', 'dolore magna aliquam', 'zoom_to_rect', 'zoom'),
			('Subplots', 'putamus parum claram', 'subplots', 'configure_subplots'),
			('Save', 'sollemnes in futurum', 'filesave', 'save_figure'),
			("Customize", "Edit axis, curve and image parameters",
			"qt4_editor_options", "edit_parameters"),
			
		)
		NavigationToolbar2QT.__init__(self,canvas_,parent_)
		self.setIconSize(QtCore.QSize(24, 24))
		
		button_action = QAction(QIcon("../icons/layout-4.png"), "Your button", self)
		button_action.setStatusTip("This is your button")
		# button_action.triggered.connect(self.onMyToolBarButtonClick)
		button_action.setCheckable(True)
		self.addAction(button_action)
		self.setFixedHeight(36)
		self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

	def select_tool(self):
	  print("You clicked the selection tool")


class Canvas_Widget(QWidget):
	def __init__(self, MainWindow):
		super().__init__()
		self.canvasPool = []
		self.canvasPool.append(MplCanvas(self, [CurveType.FreqRes, CurveType.THD]))
		self.canvasPool.append(MplCanvas(self, [CurveType.IMP, CurveType.Phase]))
		self.canvasPool.append(MplCanvas(self, [CurveType.EX, CurveType.NoType]))
		self.canvasPool.append(MplCanvas(self, [CurveType.NoType, CurveType.NoType]))
		
		self.gdly_canvasPool = QGridLayout()
		self.toolbar = MyToolBar(self.canvasPool[0])
		self.canvasPool[0].fig.axes[0].format_coord = lambda x, y: ""

		self.vbly = QVBoxLayout()
		self.vbly.addWidget(self.toolbar)
		self.vbly.addLayout(self.gdly_canvasPool)
		self.setContentsMargins(0,0,0,0)
		self.vbly.setContentsMargins(0,0,0,0)
		self.gdly_canvasPool.setContentsMargins(0,0,0,0)

		self.setLayout(self.vbly)

		

		# Status = Main, UpAndDown, Quater, MainwithThreeSmall, MainwithScrollArea
		self.status = None  
	
	def setStatus(self, status):
		self.status = status
	
	def onMyToolBarButtonClick(self):
		print("btn clicked")
