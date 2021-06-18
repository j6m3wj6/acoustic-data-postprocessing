from pickle import LIST
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from .wg_toolbar import *
from .data_objects import *
from .ui_conf import FIGURE_CONF


class Draggable_lines:
    def __init__(self, ax=None, xcoord=1000, ycoord=60):
        self.vline = ax.axvline(x=xcoord, picker=5)  # , label="_nolegend_"
        self.hline = ax.axhline(y=ycoord, picker=5)
        self.xcoord = xcoord
        self.ycoord = xcoord
        self.text = ax.text(1, 1.01, 'x = {:6.2f}, y = {:6.2f}'.format(
            xcoord, ycoord), transform=ax.transAxes, ha='right', color='#0000cd')
        self.canvas = ax.get_figure().canvas
        self.canvas.mpl_connect('pick_event', self.clickonline)

    def clickonline(self, event):
        if event.artist in [self.hline, self.vline]:
            # print("line selected ", event.artist)
            self.follower = self.canvas.mpl_connect(
                "motion_notify_event", self.followmouse)
            self.releaser = self.canvas.mpl_connect(
                "button_press_event", self.releaseonclick)

    def followmouse(self, event):
        self.vline.set_xdata([event.xdata, event.xdata])
        self.hline.set_ydata([event.ydata, event.ydata])
        self.text.set_text('x = {:6.2f}, y = {:6.2f}'.format(
            event.xdata, event.ydata))
        # self.text.set_position((event.xdata*1.1, event.ydata*1.002))
        self.canvas.replot()

    def releaseonclick(self, event):
        self.xcoord = self.vline.get_xdata()[0]
        self.ycoord = self.hline.get_ydata()[0]
        self.canvas.mpl_disconnect(self.releaser)
        self.canvas.mpl_disconnect(self.follower)

    def set_visible(self, visible):
        self.vline.set_visible(visible)
        self.hline.set_visible(visible)
        self.text.set_visible(visible)
        self.canvas.replot()

    def get_coords(self):
        return [self.xcoord, self.ycoord]


class MyCanvasItem(FigureCanvasQTAgg):
    def __init__(self, parent=None, id=None, types_=[], params=FIGURE_CONF):
        # Canvas init
        self.fig, _ = plt.subplots(constrained_layout=True)
        super(MyCanvasItem, self).__init__(self.fig)
        self.name = f"%s | %s" % (types_[0].value, types_[1].value)
        self.id = id
        self.parameter = params
        self.wg_canvas = parent

        self.ax_main = self.fig.axes[0]
        self.ax_sub = self.fig.axes[0].twinx()
        self.ax_sub.set_visible(False)
        self.ylim = [100, 0]

        self.ax_types = types_
        self.draggable_lines = Draggable_lines(self.ax_main, 1000, 0)
        self.draggable_lines.set_visible(False)
        self.ax_main.format_coord = lambda x, y: ""

        self.fig.canvas.mpl_connect('pick_event', self.handle_pick)
        self.fig.canvas.mpl_connect('button_press_event', self.handle_click)
        # self.ax_main.text(1.07, 0.98, "Label"+" "*40,
        #                   transform=self.ax_main.transAxes)

        self.setAcceptDrops(True)
        for ax in self.fig.axes:
            ax.grid()
            ax.grid(which='minor', linestyle=':',
                    linewidth='0.5', color='black')
            ax.set_ymargin(0.1)

        self.set_style()
        self.fig.set_constrained_layout_pads(w_pad=10/72., h_pad=10/72.,
                                             hspace=0.5, wspace=0.5)

    def set_focus(self, focus):
        if focus:
            self.fig.set_edgecolor("#0D3B66")
            self.fig.patch.set_linewidth(3)
        else:
            self.fig.set_edgecolor("#efefef")
            self.fig.patch.set_linewidth(0.5)

    def set_style(self):

        param_gen = self.parameter["General"]
        print(self.parameter)
        self.ax_main.set_title(param_gen["Title"])
        for idx, _type in enumerate(self.ax_types):
            if _type == CurveType.THD:
                self.fig.axes[idx].yaxis.set_major_formatter(
                    matplotlib.ticker.PercentFormatter())

        w_pad = param_gen["Margin"]["left-right"]
        h_pad = param_gen["Margin"]["top-bottom"]
        self.fig.set_constrained_layout_pads(w_pad=w_pad/72., h_pad=h_pad/72.,
                                             hspace=0.5, wspace=0.5)

        param_axis = self.parameter["Axis"]
        if (param_axis["Y-Axis"]['auto-scale']):
            self.ax_main.set_ylim(auto=True)
        else:
            self.ax_main.set_ylim(
                [int(param_axis["Y-Axis"]['min']), int(param_axis["Y-Axis"]['max'])])

        if (param_axis["Sub_Y-Axis"]['auto-scale']):
            self.ax_sub.set_ylim(auto=True)
        else:
            self.ax_sub.set_ylim(
                [int(param_axis["Sub_Y-Axis"]['min']), int(param_axis["Sub_Y-Axis"]['max'])])

        for ax in self.fig.axes:
            ax.set_xscale(param_axis["X-Axis"]['scale'])
            if (param_axis["X-Axis"]['auto-scale']):
                ax.set_xlim(auto=True)
            else:
                ax.set_xlim([int(param_axis["X-Axis"]['min']),
                            int(param_axis["X-Axis"]['max'])])

        self.replot()

    def replot(self):
        # for _l in self.ax_main.lines:
        #     line_ymax = max(_l.get_ydata())
        #     line_ymin = min(_l.get_ydata())
        #     if line_ymax > self.ylim[1]:
        #         self.ylim[1] = line_ymax
        #     if line_ymin < self.ylim[0]:
        #         self.ylim[0] = line_ymin

        legend_visible = self.parameter["General"]["Legend"]["visible"]
        handles, labels = self.ax_sub.get_legend_handles_labels()
        pad_h = .03
        if self.ax_sub.get_visible():
            self.ax_sub.plot()
            pad_h = .07
            if legend_visible:
                if labels:
                    self.ax_sub.legend(bbox_to_anchor=(1+pad_h, 0, 1, .5),
                                       loc="lower left", borderaxespad=0)
                else:
                    leg = self.ax_main.legend([])
                    leg.remove()

        handles, labels = self.ax_main.get_legend_handles_labels()
        self.ax_main.plot()
        if legend_visible:
            if labels:
                self.ax_main.legend(bbox_to_anchor=(1+pad_h, .5, 1, .5),
                                    loc="upper left", borderaxespad=0)
            else:
                leg = self.ax_main.legend([])
                leg.remove()
        self.draw()

    def set_ax_type(self, ax, _type):
        type_transfer = CurveType.NoType
        if isinstance(ax, int):
            ax_id = ax
            if _type == self.ax_types[ax_id]:
                pass
            elif _type == self.ax_types[not ax_id]:
                self.fig.axes[ax_id].lines = []
                self.fig.axes[not ax_id].lines = []
                types = self.ax_types
                self.ax_types = [types[1], types[0]]
            else:
                type_transfer = self.ax_types[ax_id]
                lines_transfer = self.fig.axes[ax_id].lines
                origin_canvas, origin_ax_id, origin_ax = self.wg_canvas.get_canvas(
                    _type)
                self.ax_types[ax_id] = _type
                self.fig.axes[ax_id].lines = []

                if origin_canvas:
                    # self.fig.axes[ax_id].lines = origin_ax.lines
                    # origin_ax.lines = lines_transfer
                    origin_ax.lines = []
                    origin_canvas.ax_types[origin_ax_id] = type_transfer
            self.replot()
            return type_transfer

        elif isinstance(ax, matplotlib.axes.Axes):
            if (ax == self.ax_main):
                self.ax_types[0] = _type
            else:
                self.ax_types[1] = _type

    def get_ax(self, curveType):
        if self.ax_types[0] == curveType:
            return 0, self.ax_main
        elif self.ax_types[1] == curveType:
            return 1, self.ax_sub
        else:
            return -1, None

    def get_name(self): return f"%s | %s" % (
        self.ax_types[0].value, self.ax_types[1].value)

    def get_title(self):
        if (self.ax_sub.get_visible()):
            return self.get_name()
        else:
            return self.ax_types[0].value

    def _resetLineWidth(self):
        for ax in self.fig.axes:
            for line in ax.lines:
                line.set_linewidth(LINEWIDTH_DEFAULT)

    def handle_pick(self, event):
        print('pick event')
        print(event)

    def handle_click(self, event):
        if event.dblclick:
            self.wg_canvas.change_focusing_canvas(event.canvas)

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
    def __init__(self, parent=None, ui_conf=None):
        super().__init__()
        self.mainwindow = parent
        self.ui_conf = ui_conf
        self.canvasPool = []
        self.status = {}
        for _k, _v in self.ui_conf["canvasPool"].items():
            id, types, parameter = _v.values()
            self.canvasPool.append(MyCanvasItem(parent=self, id=id, types_=[
                CurveType(types[0]), CurveType(types[1])], params=parameter))
        for mode, canvas_idx in self.ui_conf["status"].items():
            canvas_set = []
            for _i in canvas_idx:
                canvas_set.append(self.canvasPool[_i])
            self.status.update({mode: canvas_set})

        self.mode = self.ui_conf["mode"]
        self.focusing_canvas = self.canvasPool[0]

        self.initUI()

    def initUI(self):
        # Create Component
        self.toolbar = MyToolBar(
            canvas=self.canvasPool[0], parent=self.mainwindow)
        self.gdly_canvasPool = QGridLayout()

        # Layout
        self.vbly = QVBoxLayout()
        self.vbly.addWidget(self.toolbar)
        self.vbly.addLayout(self.gdly_canvasPool)
        self.setLayout(self.vbly)

        # Layout Styling
        self.vbly.setSpacing(0)

    def _add_canvas(self, types_):
        id = self.canvasPool.count()
        new_canvas = MyCanvasItem(parent=self, id=id, types=types_)
        self.canvasPool.append(new_canvas)
        return id

    def replot(self):
        for _c in self.get_active_canvas():
            _c.replot()

    def change_focusing_canvas(self, focusing_canvas):
        self.focusing_canvas = focusing_canvas

        for _c in self.get_active_canvas():
            _c.set_focus(_c == focusing_canvas)

        self.toolbar.update_focus_canvas(focusing_canvas)
        self.replot()

    def switch_canvas(self, old_id, new_id):
        old_canvas = self.canvasPool[old_id]
        new_canvas = self.canvasPool[new_id]

        if new_canvas in self.get_active_canvas():
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
            self.status[self.mode] = [new_canvas if _c ==
                                      old_canvas else _c for _c in self.status[self.mode]]
        self.change_focusing_canvas(new_canvas)

    def set_mode(self, mode):
        self.mode = mode
        self.change_focusing_canvas(self.get_active_canvas()[0])

    def get_canvas(self, _type):
        for _c in self.canvasPool:
            ax_id, ax_match = _c.get_ax(_type)
            if (ax_match):
                return _c, ax_id, ax_match

    def get_active_canvas_names(self):
        active_canvas_names = []
        for act_c in self.get_active_canvas():
            active_canvas_names.append(act_c.get_name())
        return active_canvas_names

    def get_active_canvas(self): return self.status[self.mode]
