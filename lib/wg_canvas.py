from enum import Enum
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from textwrap import fill
from matplotlib.lines import Line2D
from .wg_toolbar import *


LINEWIDTH_DEFAULT = 1.5
LINEWIDTH_HIGHLIGHT = 4
COLORS = ['sienna', 'r', 'darkorange', 'gold', 'g', 'b', 'purple', 'gray']
COLORS_CMP = ['r', 'b', 'g']
LEGEND_WRAP = 25


class CurveType(Enum):
    NoType = 'None'
    FreqRes = 'Frequency Response'
    IMP = 'Impedance'
    Phase = 'Phase'
    THD = 'THD'
    EX = 'Excursion'


class CurveData:
    def __init__(self, label=None, note=None, xdata=None, ydata=None, type_=None, units=[]):
        self.label = label
        self.note = note
        self.xdata = xdata
        self.ydata = ydata
        self.type = type_
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


class MyCanvasItem(FigureCanvasQTAgg):
    def __init__(self, parent=None, id=None, types_=[], status=False):
        # Canvas init
        self.fig, _ = plt.subplots(constrained_layout=True)
        super(MyCanvasItem, self).__init__(self.fig)
        self.name = f"%s | %s" % (types_[0].value, types_[1].value)
        self.id = id
        self.wg_canvas = parent

        self.ax_main = self.fig.axes[0]
        self.ax_main.set_title(types_[0].value)

        self.ax_sub = self.fig.axes[0].twinx()
        self.ax_sub.set_visible(False)
        self.setAxesStyle()

        self.ax_types = types_
        self.active = status

        self.fig.canvas.mpl_connect('pick_event', self.handle_pick)
        self.fig.canvas.mpl_connect('button_press_event', self.handle_click)

        # self.ax_main.text(1.07, 0.98, "Label"+" "*40,
        #                   transform=self.ax_main.transAxes)

        self.setAcceptDrops(True)

    def set_active(self, active):
        self.active = active

    def setAxStyle(self, ax):
        ax.set_xscale('log')
        ax.set_xlim([20, 20000])
        ax.set_ylim(auto=True)
        ax.patch.set_alpha(0.0)
        ax.grid()
        ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')

    def setAxesStyle(self):
        for ax in self.fig.axes:
            ax.set_xscale('log')
            ax.set_xlim([20, 20000])
            ax.set_ylim(auto=True)
            ax.grid()
            ax.grid(which='minor', linestyle=':',
                    linewidth='0.5', color='black')

    def replot(self):
        self.ax_main.plot()
        self.ax_main.legend(bbox_to_anchor=(1.07, .5, .18, .4),
                            loc="upper left", borderaxespad=0)

        if self.ax_sub.get_visible():
            self.ax_sub.plot()
            self.ax_sub.legend(bbox_to_anchor=(1.07, 0, .18, .4),
                               loc="lower left", borderaxespad=0)
        self.draw()

    def getAxbyType(self, curveType):
        if self.ax_types[0] == curveType:
            return self.ax_main
        elif self.ax_types[1] == curveType:
            return self.ax_sub
        else:
            return None

    def get_name(self): return f"%s | %s" % (
        self.ax_types[0].value, self.ax_types[1].value)

    def _resetLineWidth(self):
        for ax in self.fig.axes:
            for line in ax.lines:
                line.set_linewidth(LINEWIDTH_DEFAULT)

    def handle_pick(self, event):
        print('pick event')
        print(event)

    def handle_click(self, event):
        self.wg_canvas.handle_canvas_clicked(event.canvas)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('text/plain'):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        id = int(event.mimeData().text())
        if id != self.id:
            self.wg_canvas.switch_canvas(self.id, id)


class MyCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.myApp = parent
        self.canvasPool = []
        self.canvasPool.append(MyCanvasItem(parent=self, id=0, types_=[
                               CurveType.FreqRes, CurveType.THD]))
        self.canvasPool.append(MyCanvasItem(parent=self, id=1, types_=[
                               CurveType.IMP, CurveType.Phase]))
        self.canvasPool.append(MyCanvasItem(parent=self, id=2, types_=[
                               CurveType.EX, CurveType.NoType]))
        self.canvasPool.append(MyCanvasItem(parent=self, id=3, types_=[
                               CurveType.NoType, CurveType.NoType]))
        # Status = Main, UpAndDown, Quater, MainwithThreeSmall, MainwithScrollArea
        self.status = {"Main": [self.canvasPool[0]],
                       "UpAndDown": [self.canvasPool[0],  self.canvasPool[1]],
                       "Quater": [self.canvasPool[0],  self.canvasPool[1], self.canvasPool[2],  self.canvasPool[3]],
                       "MainwithThreeSmall": [self.canvasPool[0],  self.canvasPool[1], self.canvasPool[2],  self.canvasPool[3]]
                       }
        self.mode = "Main"

        self.gdly_canvasPool = QGridLayout()
        self.toolbar = MyToolBar(self.canvasPool[0], self)
        self.canvasPool[0].fig.axes[0].format_coord = lambda x, y: ""

        self.vbly = QVBoxLayout()
        self.vbly.addWidget(self.toolbar)
        self.vbly.addLayout(self.gdly_canvasPool)
        # self.setContentsMargins(0,0,0,0)
        # self.vbly.setContentsMargins(0,0,0,0)
        # self.gdly_canvasPool.setContentsMargins(0,0,0,0)
        self.setLayout(self.vbly)

    def _add_canvas(self, types_):
        id = self.canvasPool.count()
        new_canvas = MyCanvasItem(parent=self, id=id, types=types_)
        self.canvasPool.append(new_canvas)
        return id

    def set_status(self, status):
        for c in self.canvasPool:
            if (c.active):
                self.status[status].append(c)

    def set_mode(self, mode): self.mode = mode

    def get_active_canvas(self):
        active_canvas_names = []
        for act_c in self.status[self.mode]:
            active_canvas_names.append(act_c.get_name())
        print(active_canvas_names)
        return active_canvas_names

    def onMyToolBarButtonClick(self):
        print("btn clicked")

    def replot(self):
        for c in self.canvasPool:
            if (c.active):
                c.replot()

    def handle_canvas_clicked(self, canvas):
        for c in self.canvasPool:

            if (c is not canvas):
                c.ax_main.set_facecolor("#efefef")
                c.fig.set_facecolor("#efefef")
            else:
                c.ax_main.set_facecolor("white")
                c.fig.set_facecolor("white")
        self.replot()

    def switch_canvas(self, old_id, new_id):
        old_canvas = self.canvasPool[old_id]
        new_canvas = self.canvasPool[new_id]

        if new_canvas in self.status[self.mode]:
            tmp_wg = QWidget()
            self.gdly_canvasPool.replaceWidget(new_canvas, tmp_wg)
            new_canvas.setParent(None)

            self.gdly_canvasPool.replaceWidget(old_canvas, new_canvas)
            old_canvas.setParent(None)

            self.gdly_canvasPool.replaceWidget(tmp_wg, old_canvas)
            tmp_wg.setParent(None)

        else:
            self.gdly_canvasPool.replaceWidget(old_canvas, new_canvas)
            old_canvas.setParent(None)
