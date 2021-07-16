from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib import ticker
from .wg_toolbar import MyToolBar
from .obj_data import CurveType
from .ui_conf import FIGURE_CONF, LINEWIDTH_DEFAULT
from typing import Tuple, Optional
from textwrap import fill
from quantiphy import Quantity


class MyCanvasItem(FigureCanvasQTAgg):
    '''
    :ivar str title: Canvas titel, use axis CurveType by default
    :ivar int id: Canvas id
    :ivar dict parameter: Canvas setting parameter
    :ivar MyCanvas wg_canvas: Its parent, a QWidget that contains canvas layout and toolbar.

    :ivar matplotlib.pyplot.figure fig:
    :ivar matplotlib.pyplot.Axis ax_main: main y-axis on fig
    :ivar matplotlib.pyplot.Axis ax_sub: sub y-axis on fig, share the same x-axis with main ax_main

    :ivar Draggable_lines draggable_lines:
            A set of horizontal and vertical lines that can be drag by mouse movement.
            Use for highlighting a specific coordinate.
    '''

    def __init__(self, parent=None, id=None, types=[], params=FIGURE_CONF):
      # Canvas Attributes
        self.fig, _ = plt.subplots(constrained_layout=True)
        super(MyCanvasItem, self).__init__(self.fig)
        self.id = id
        self.parameter = params
        self.parameter["Title"] = f"%s | %s" % (types[0].value, types[1].value)

        self.wg_canvas = parent

        self.ax_types = types
        self.ax_main = self.fig.axes[0]
        self.ax_sub = self.fig.axes[0].twinx()
        self.ax_sub.set_zorder(1)
        self.ax_main.set_zorder(2)
        self.ax_main.patch.set_visible(False)
        self.ylim = [0, 1]

        # self.ax_sub.yaxis.set_major_formatter(matplotlib.ticker.EngFormatter())

        self.draggable_lines = Draggable_lines(self.ax_main, 1000, 0)
        self.draggable_lines.set_visible(False)

      # Interation functions with canvas
        self.setAcceptDrops(True)
        self.fig.canvas.mpl_connect('pick_event', self.handle_pick)
        self.fig.canvas.mpl_connect(
            'button_press_event', self.handleDoubleClicked)
        # self.ax_main.text(1.07, 0.98, "Label"+" "*40,
        #                   transform=self.ax_main.transAxes)

      # Default Setting
        self.ax_sub.set_visible(False)
        self.ax_main.format_coord = lambda x, y: ""
        for ax in self.fig.axes:
            ax.set_ylim(auto=False)

            ax.grid()
            ax.grid(which='minor', linestyle=':',
                    linewidth='0.5', color='black')
            ax.yaxis.set_minor_locator(ticker.AutoMinorLocator(5))

        self.apply_style()
        self.fig.set_constrained_layout_pads(w_pad=10/72., h_pad=10/72.,
                                             hspace=0.5, wspace=0.5)

    def clear_lines(self, ax_id):
        if ax_id == 0:
            self.ax_main.lines = self.ax_main.lines[:2]
        elif ax_id == 1:
            self.ax_sub.lines = []

    def toggle_focus_style(self, focus):
        '''
        Only one focusing canvas instance in an application.
        Focusing canvas instance  have a highlight border.
        '''
        if focus:
            self.fig.set_edgecolor("#0D3B66")
            self.fig.patch.set_linewidth(3)
        else:
            self.fig.set_edgecolor("#efefef")
            self.fig.patch.set_linewidth(0.5)

    def apply_style(self):
        '''
        Apply ``parameters`` to this canvas instance.
        '''
        param_gen = self.parameter["General"]
        self.ax_main.set_title(param_gen["Title"])
        for idx, _type in enumerate(self.ax_types):
            if _type == CurveType.THD:
                self.fig.axes[idx].yaxis.set_major_formatter(
                    matplotlib.ticker.PercentFormatter())
            else:
                # self.fig.axes[idx].yaxis.set_major_formatter(
                #     matplotlib.ticker.ScalarFormatter())
                self.fig.axes[idx].yaxis.set_major_formatter(
                    matplotlib.ticker.EngFormatter())

        w_pad = int(param_gen["Margin"]["left-right"])
        h_pad = int(param_gen["Margin"]["top-bottom"])
        self.fig.set_constrained_layout_pads(w_pad=w_pad/72., h_pad=h_pad/72.,
                                             hspace=0.5, wspace=0.5)

        handles, labels = self.ax_main.get_legend_handles_labels()
        for _hd, _lb in zip(handles, labels):
            _lb = _lb.replace('\n', '')
            _hd.set_label(fill(_lb,
                               int(param_gen['Legend']['text-wrap'])))

        handles, labels = self.ax_sub.get_legend_handles_labels()
        for _hd, _lb in zip(handles, labels):
            _lb = _lb.replace('\n', '')
            _hd.set_label(fill(_lb,
                               int(param_gen['Legend']['text-wrap'])))

        param_axis = self.parameter["Axis"]
        self.ax_main.set_xlabel(param_axis["X-Axis"]['label'])
        self.ax_main.set_ylabel(param_axis["Y-Axis"]['label'])
        self.ax_sub.set_xlabel(param_axis["X-Axis"]['label'])
        # if (param_axis["Y-Axis"]['auto-scale']):
        #     self.ax_main.set_ylim(auto=True)
        # else:
        self.ax_main.set_ylim(
            [float(Quantity(param_axis["Y-Axis"]['min'])), float(Quantity(param_axis["Y-Axis"]['max']))])
        # self.ax_main.set_ymargin(1)

        # if (param_axis["Sub_Y-Axis"]['auto-scale']):
        #     self.ax_sub.set_ylim(auto=True)
        # else:
        self.ax_sub.set_ylim(
            [float(Quantity(param_axis["Sub_Y-Axis"]['min'])), float(Quantity(param_axis["Sub_Y-Axis"]['max']))])
        # self.ax_sub.set_ymargin(1)

        for ax in self.fig.axes:
            ax.set_xscale(param_axis["X-Axis"]['scale'])
            if (param_axis["X-Axis"]['auto-scale']):
                ax.set_xlim(auto=True)
            else:
                ax.set_xlim([int(param_axis["X-Axis"]['min']),
                            int(param_axis["X-Axis"]['max'])])

        self.replot()

    def autoscale(self, ax_idx):
        # print("autoscale____", ax_idx, len(self.fig.axes[ax_idx].lines))

        if ax_idx == 0 and len(self.fig.axes[ax_idx].lines) > 2:
            line_ymax = max(self.fig.axes[ax_idx].lines[2].get_ydata())
            line_ymin = min(self.fig.axes[ax_idx].lines[2].get_ydata())
            ylim = [line_ymin, line_ymax]
            param_axis = self.parameter["Axis"]["Y-Axis"]
            lines = self.fig.axes[ax_idx].lines[2:]

        elif ax_idx == 1 and len(self.fig.axes[ax_idx].lines) > 0:
            line_ymax = max(self.fig.axes[ax_idx].lines[0].get_ydata())
            line_ymin = min(self.fig.axes[ax_idx].lines[0].get_ydata())
            ylim = [line_ymin, line_ymax]
            param_axis = self.parameter["Axis"]["Sub_Y-Axis"]
            lines = self.fig.axes[ax_idx].lines
        else:
            return
        for _l in lines:
            line_ymax = max(_l.get_ydata())
            line_ymin = min(_l.get_ydata())
            if line_ymax > ylim[1]:
                ylim[1] = line_ymax
            if line_ymin < ylim[0]:
                ylim[0] = line_ymin
        # print("final", ylim)
        rg = ylim[1] - ylim[0]
        self.fig.axes[ax_idx].set_ylim(
            [ylim[0]-rg*0.1, ylim[1]+rg*0.1])

        # param_axis['min'] = "{0:.4g}".format(ylim[0]-rg*0.1)
        # param_axis['max'] = "{0:.4g}".format(ylim[1]+rg*0.1)
        param_axis['min'] = str(Quantity(ylim[0]-rg*0.1))
        param_axis['max'] = str(Quantity(ylim[1]+rg*0.1))

    def sort_legend(self, ax):
        handles, labels = ax.get_legend_handles_labels()
        zipped_list = list(zip(handles, labels))
        # print("Before:",  zipped_list)
        zipped_list.sort(key=lambda x: x[0].get_zorder())
        # print("After: ", zipped_list)
        unzipped = [[i for i, j in zipped_list], [j for i, j in zipped_list]]
        return unzipped[0], unzipped[1]

    def _toggle_legend(self, ax: matplotlib.axes.Axes,  pad_h: float):
        '''
        Update legends according to those curves on the canvas.
        Clear and remove all legend instance if no curves on the canvas.
        Set legend to invisible but still keeping all legend instances existed
        if user choose to hide legend in the axes parameter dialog.
        Those customized setting are stored in ``parameter``.
        '''
        handles, labels = self.sort_legend(ax)
        if ax == self.ax_main:
            loc = "upper left"
            leg_bottom = 0.5
        else:
            loc = "lower left"
            leg_bottom = 0

        if labels:
            ax.legend(handles, labels, bbox_to_anchor=(1+pad_h, leg_bottom, 1, .5),
                      loc=loc, borderaxespad=0)
            legend_visible = self.parameter["General"]["Legend"]["visible"]
            ax.get_legend().set_visible(legend_visible)
        else:
            leg = ax.legend([])
            leg.remove()

    def replot(self):
        '''
        Replot the canvas.
        '''
        pad_h = .03
        self.update_title()
        if self.ax_sub.get_visible():
            self.ax_sub.plot()
            if self.parameter["Axis"]["Sub_Y-Axis"]['auto-scale'] == True:
                self.autoscale(1)

            pad_h = .07
            self._toggle_legend(self.ax_sub, pad_h)

        self.ax_main.plot()
        self._toggle_legend(self.ax_main, pad_h)

        if self.parameter["Axis"]["Y-Axis"]['auto-scale'] == True:
            self.autoscale(0)
        self.draw()

    def get_ax(self, curveType: CurveType) -> Tuple[int, Optional[matplotlib.axes.Axes]]:
        '''
        If canvas has any axis's type in line with the input parameter ``curveType``,
        return axis id and axis instance. Otherwise, return (-1, None).

        :param CurveType curveType:
        '''
        if self.ax_types[0].name == curveType.name:
            return 0, self.ax_main
        elif self.ax_types[1].name == curveType.name:
            return 1, self.ax_sub
        else:
            return -1, None

    def get_name(self) -> str:
        '''
        Return a string contains its axis types.
        '''
        return f"%s | %s" % (self.ax_types[0].value, self.ax_types[1].value)

    def update_title(self) -> str:
        '''
        Update canvas's title.
        '''
        if (self.ax_sub.get_visible()):
            self.ax_main.set_title(self.get_name())
            return self.get_name()
        else:
            self.ax_main.set_title(self.ax_types[0].value)
            return self.ax_types[0].value

    def reset_linewidth(self) -> None:
        '''
        Set linewidth of all curves on the canvas to default value.
        '''
        for ax in self.fig.axes:
            for line in ax.lines:
                line.set_linewidth(LINEWIDTH_DEFAULT)

    def handle_pick(self, event):
        print('wg_canvas.py pick event')
        # print(event)

    def handleDoubleClicked(self, event) -> None:
        '''
        If User double clicked on this canvas, change this canvas to be the focusing canvas.
        '''
        if event.dblclick:
            self.wg_canvas.change_focusing_canvas(event.canvas)

    def dragEnterEvent(self, event) -> None:
        '''
        Triggered when User drag the canvas label in left dockwidget on this canvas instance.
        '''
        if event.mimeData().hasFormat('text/plain'):
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event) -> None:
        '''
        Triggered when User drop the canvas label in left dockwidget on this canvas instance.
        Modifying canvas layout according to user's options.
        '''
        id = int(event.mimeData().text())
        if id != self.id:
            self.wg_canvas.switch_canvas(self.id, id)


class MyCanvas(QWidget):
    def __init__(self, mainwindow=None):
        super().__init__()
        self.mainwindow = mainwindow
        ui_conf = mainwindow.project.ui_conf["MyCanvas"]
        self.canvasPool = []
        self.status = {}
        for _k, _v in ui_conf["canvasPool"].items():
            id, types, parameter = _v.values()

            self.canvasPool.append(MyCanvasItem(parent=self, id=id, types=[
                CurveType(types[0]), CurveType(types[1])], params=parameter))
        for mode, canvas_idx in ui_conf["status"].items():
            canvas_set = []
            for _i in canvas_idx:
                canvas_set.append(self.canvasPool[_i])
            self.status.update({mode: canvas_set})

        self.mode = ui_conf["mode"]
        self.focusing_canvas = self.canvasPool[0]

        self.initUI()

    def initUI(self) -> None:
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

    def _add_canvas(self, types_) -> int:
        id = self.canvasPool.count()
        new_canvas = MyCanvasItem(parent=self, id=id, types=types_)
        self.canvasPool.append(new_canvas)
        return id

    def replot(self) -> None:
        for _c in self.get_active_canvas():
            _c.replot()

    def change_focusing_canvas(self, focusing_canvas) -> None:
        self.focusing_canvas = focusing_canvas

        for _c in self.get_active_canvas():
            _c.toggle_focus_style(_c == focusing_canvas)

        self.toolbar.update_focus_canvas(focusing_canvas)
        self.replot()

    def switch_canvas(self, old_id, new_id) -> None:
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
            arr = self.status[self.mode]
            self.status[self.mode] = swapPositions(
                arr, arr.index(old_canvas), arr.index(new_canvas))

        else:
            self.gdly_canvasPool.replaceWidget(old_canvas, new_canvas)
            old_canvas.setParent(None)
            self.status[self.mode] = [new_canvas if _c ==
                                      old_canvas else _c for _c in self.status[self.mode]]
        self.change_focusing_canvas(new_canvas)
        for mode, canvas in self.status.items():
            canvas_set = [_c.id for _c in canvas]
            self.mainwindow.project.ui_conf["MyCanvas"]["status"].update({
                                                                         mode: canvas_set})

    def set_mode(self, mode: str) -> None:
        self.mode = mode
        self.mainwindow.project.ui_conf["MyCanvas"]["mode"] = self.mode
        self.change_focusing_canvas(self.get_active_canvas()[0])

    def get_canvas(self, _type: CurveType = None, id: int = None):
        if _type is not None:
            for _c in self.canvasPool:
                ax_id, ax_match = _c.get_ax(_type)
                if ax_match:
                    return _c, ax_id, ax_match

        elif id is not None:
            for _c in self.canvasPool:
                if id == _c.id:
                    return _c
        return None, None, None

    def get_active_canvas_names(self):
        active_canvas_names = []
        for act_c in self.get_active_canvas():
            active_canvas_names.append(act_c.get_name())
        return active_canvas_names

    def get_active_canvas(self): return self.status[self.mode]


class Draggable_lines:
    def __init__(self, ax=None, xcoord=1000, ycoord=60):
        self.vline = ax.axvline(x=xcoord, picker=5)  # , label="_nolegend_"
        self.hline = ax.axhline(y=ycoord, picker=5)
        self.vline.set_zorder(1000)
        self.hline.set_zorder(1000)
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


def swapPositions(list, pos1, pos2):
    list[pos1], list[pos2] = list[pos2], list[pos1]
    return list
