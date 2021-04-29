from enum import Enum
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from textwrap import fill

LINEWIDTH_DEFAULT = 1.5
LINEWIDTH_HIGHLIGHT = 4
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
		# self.fig.figsize = (12,4)
		super(MplCanvas, self).__init__(self.fig)
		self.fig.tight_layout()
		self.fig.subplots_adjust(right=0.8)

		self.ax_SPL = self.fig.axes[0]
		self.ax_IMP = self.fig.axes[0].twinx()
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
				line.set_linewidth(LINEWIDTH_DEFAULT)
	