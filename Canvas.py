from enum import Enum
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from textwrap import fill
from matplotlib.lines import Line2D

LINEWIDTH_DEFAULT = 1.5
LINEWIDTH_HIGHLIGHT = 4
COLORS = ['sienna', 'r', 'darkorange', 'gold', 'g', 'b', 'purple', 'gray']
COLORS_CMP = ['r', 'b', 'g']
LEGEND_WRAP = 11

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
		self.legend = fill(self.label, 11)
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


class MplCanvas(FigureCanvasQTAgg):
	def __init__(self, parent=None, types=[], status=False):
		# Canvas init
		self.fig, _ = plt.subplots()
		super(MplCanvas, self).__init__(self.fig)
		self.fig.tight_layout()
		self.fig.subplots_adjust(right=0.8)

		self.ax_main = self.fig.axes[0]
		self.ax_sub = self.fig.axes[0].twinx()
		self.ax_sub.set_visible(False)
		self.setAxesStyle()

		self.ax_types = types
		self.active = status

		self.fig.canvas.mpl_connect('pick_event', self.on_pick)

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
			# ax.patch.set_alpha(0.0)
	
	def replot(self):
		self.ax_main.plot()
		self.ax_main.legend(bbox_to_anchor=(1.04,1), loc="upper left")
		
		if (self.ax_sub.get_visible()):
			self.ax_sub.plot()
			self.ax_sub.legend(bbox_to_anchor=(1.04,0), loc="lower left")
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
    def __init__(self,canvas_,parent_):
      self.toolitems = (
          ('Home', 'Lorem ipsum dolor sit amet', 'home', 'home'),
          ('Back', 'consectetuer adipiscing elit', 'back', 'back'),
          ('Forward', 'sed diam nonummy nibh euismod', 'forward', 'forward'),
          (None, None, None, None),
          ('Pan', 'tincidunt ut laoreet', 'move', 'pan'),
          ('Zoom', 'dolore magna aliquam', 'zoom_to_rect', 'zoom'),
          (None, None, None, None),
          ('Subplots', 'putamus parum claram', 'subplots', 'configure_subplots'),
          ('Save', 'sollemnes in futurum', 'filesave', 'save_figure'),
          ("Customize", "Edit axis, curve and image parameters",
         "qt4_editor_options", "edit_parameters"),
          ('Port', 'Select', "select", 'select_tool'),
          )
      NavigationToolbar2QT.__init__(self,canvas_,parent_)
    def select_tool(self):
      print("You clicked the selection tool")