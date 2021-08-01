from os import stat
from PyQt5.QtWidgets import QWidget, QGridLayout, QVBoxLayout
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib import ticker
from .wg_toolbar import MyToolBar
from .obj_data import CurveType
from .wg_selfdefined import Draggable_lines
from .functions import swapPositions
from .ui_conf import FIGURE_CONF, LINEWIDTH_DEFAULT
from typing import Dict, List, Tuple, Optional
from textwrap import fill
from quantiphy import Quantity
import math


class MyCanvasItem(FigureCanvasQTAgg):
    '''
    Self-defined Matplot Figure object.

    :ivar str title: Canvas titel, use axis CurveType by default
    :ivar int id: Canvas id
    :ivar dict parameter: Canvas setting parameter
    :ivar MyCanvas wg_canvas: Its parent, a QWidget that contains canvas layout and toolbar.

    :ivar matplotlib.pyplot.figure fig:
    :ivar matplotlib.pyplot.Axes ax_main: main y-axis on fig
    :ivar matplotlib.pyplot.Axes ax_sub: sub y-axis on fig, share the same x-axis with main ax_main

    :ivar Draggable_lines draggable_lines:
            A set of horizontal and vertical lines that can be drag by mouse movement.
            Use for highlighting a specific coordinate.

    :ivar List[CurveType] ax_types: A list that contains 2 element, both main and sub axis' data type.
    '''

    def __init__(self, parent=None, id: int = None, types: List[CurveType] = [], params: Dict = FIGURE_CONF) -> None:
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
        self.grid_status = [True, False]

        self.apply_style()

        self.draggable_lines = [Draggable_lines(
            self, self.ax_main), Draggable_lines(self, self.ax_sub)]
        self.draggable_lines[0].set_visible(False)
        self.draggable_lines[1].set_visible(False)

      # Interation functions with canvas
        self.setAcceptDrops(True)
        # self.fig.canvas.mpl_connect('pick_event', self.handle_pick)
        self.fig.canvas.mpl_connect(
            'button_press_event', self.handleDoubleClicked)
        self.fig.canvas.mpl_connect('button_press_event', self.handle_click)

      # Default Setting
        self.ax_main.format_coord = lambda x, y: ""
        self.ax_main.set_ylim(auto=False)
        self.ax_main.grid(linewidth='0.75', linestyle='-', color='black')
        self.ax_main.grid(which='minor',
                          linewidth='0.5', linestyle=':', color='#808080')
        self.ax_main.yaxis.set_minor_locator(ticker.AutoMinorLocator(5))

        self.ax_sub.set_visible(False)
        self.ax_sub.set_ylim(auto=False)
        self.ax_sub.grid(linewidth='0.75', color='#1f77b4',
                         linestyle='dashed', dashes=(20, 10))
        self.ax_sub.grid(which='minor',
                         linewidth='0.5', color='#8fbbd9', linestyle='--', dashes=(10, 5))
        self.ax_sub.yaxis.set_minor_locator(ticker.AutoMinorLocator(5))

        self.set_grid_status()

        self.fig.set_constrained_layout_pads(w_pad=10/72., h_pad=10/72.,
                                             hspace=0.5, wspace=0.5)

    def clear_lines(self, ax_id: int) -> None:
        """
        Clear all the line on the given y-axis, while avoid deleting the draggable lines,
        which is the frist two line in ``ax_main`` (axis' id = 0).

        :param int ax_idx: Either 0 or 1. It is used as the index for accessing specific axis on the figure.
        """
        if ax_id == 0:
            self.ax_main.lines = self.ax_main.lines[:2]
        elif ax_id == 1:
            self.ax_sub.lines = self.ax_main.lines[:2]

    def apply_style(self) -> None:
        '''Apply ``parameters`` to this MyCanvasItem instance.'''
        param_gen = self.parameter["General"]
        self.ax_main.set_title(param_gen["Title"])
        for _idx_, _type_ in enumerate(self.ax_types):
            if _type_ == CurveType.THD:
                self.fig.axes[_idx_].yaxis.set_major_formatter(
                    matplotlib.ticker.PercentFormatter())
            else:
                # self.fig.axes[_idx_].yaxis.set_major_formatter(
                #     matplotlib.ticker.ScalarFormatter())
                self.fig.axes[_idx_].yaxis.set_major_formatter(
                    matplotlib.ticker.EngFormatter())

        w_pad = int(param_gen["Margin"]["left-right"])
        h_pad = int(param_gen["Margin"]["top-bottom"])
        self.fig.set_constrained_layout_pads(w_pad=w_pad/72., h_pad=h_pad/72.,
                                             hspace=0.5, wspace=0.5)

        handles, labels = self.ax_main.get_legend_handles_labels()
        for _hd_, _lb_ in zip(handles, labels):
            _lb_ = _lb_.replace('\n', '')
            _hd_.set_label(fill(_lb_,
                                int(param_gen['Legend']['text-wrap'])))

        handles, labels = self.ax_sub.get_legend_handles_labels()
        for _hd_, _lb_ in zip(handles, labels):
            _lb_ = _lb_.replace('\n', '')
            _hd_.set_label(fill(_lb_,
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

        for _ax_ in self.fig.axes:
            _ax_.set_xscale(param_axis["X-Axis"]['scale'])
            if (param_axis["X-Axis"]['auto-scale']):
                _ax_.set_xlim(auto=True)
            else:
                _ax_.set_xlim([int(param_axis["X-Axis"]['min']),
                               int(param_axis["X-Axis"]['max'])])

        self.replot()

  # Get and Set
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
        '''Return a string contains its axis types.'''
        return f"%s | %s" % (self.ax_types[0].value, self.ax_types[1].value)

    def set_grid_status(self, status=None):
        if status:
            self.grid_status = status
        self.ax_main.grid(self.grid_status[0], axis='y', which='both')
        self.ax_sub.grid(self.grid_status[1], axis='y', which='both')
        self.replot()
        return self.grid_status

    def toggle_ax_grid(self, ax_id, status):
        self.fig.axes[ax_id].grid(status, axis='y', which='both')

  # Replot
    def replot(self) -> None:
        '''Replot the canvas.'''
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

    def update_title(self) -> str:
        '''Update canvas's title.'''
        if (self.ax_sub.get_visible()):
            self.ax_main.set_title(self.get_name())
            return self.get_name()
        else:
            self.ax_main.set_title(self.ax_types[0].value)
            return self.ax_types[0].value

    def autoscale(self, ax_idx: int) -> None:
        '''
        Autoscale given y-axis.

        :param int ax_idx: Either 0 or 1. It is used as the index for accessing specific axis on the figure.
        '''
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
        for _line_ in lines:
            line_ymax = max(_line_.get_ydata())
            line_ymin = min(_line_.get_ydata())
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

    def _sort_legend(self, ax: matplotlib.axes.Axes):
        """Sort legend of a given axis base on lines' zorder."""
        handles, labels = ax.get_legend_handles_labels()
        zipped_list = list(zip(handles, labels))
        # print("Before:",  zipped_list)
        zipped_list.sort(key=lambda x: x[0].get_zorder())
        # print("After: ", zipped_list)
        unzipped = [[i for i, j in zipped_list], [j for i, j in zipped_list]]
        return unzipped[0], unzipped[1]

    def _toggle_legend(self, ax: matplotlib.axes.Axes,  pad_h: float) -> None:
        '''
        Update legends according to those curves on the canvas.
        Clear and remove all legend instance if no curves on the canvas.
        Set legend to invisible but still keeping all legend instances existed
        if user choose to hide legend in the axes parameter dialog.
        Those customized setting are stored in ``parameter``.
        '''
        handles, labels = self._sort_legend(ax)
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

  # Change focusing status
    def handleDoubleClicked(self, event) -> None:
        '''
        If User double clicked on this canvas, change this canvas to be the focusing canvas.
        '''
        if event.dblclick:
            self.wg_canvas.change_focusing_canvas(event.canvas)

    def toggle_focus_style(self, focus: bool) -> None:
        '''
        Only one focusing canvas instance in an application.
        Focusing canvas instance  have a highlight border.

        :param bool focus: given focus status to toggle and modify this MyCanvasItem instance's displaying style.
        '''
        if focus:
            self.fig.set_edgecolor("#0D3B66")
            self.fig.patch.set_linewidth(3)
        else:
            self.fig.set_edgecolor("#efefef")
            self.fig.patch.set_linewidth(0.5)

    def handle_click(self, event):
        x, main_y = self.ax_main.transData.inverted().transform((event.x, event.y))
        x, sub_y = self.ax_sub.transData.inverted().transform((event.x, event.y))
        xycoord = self.draggable_lines[0].get_coords()
        sub_xycoord = self.draggable_lines[1].get_coords()
        yrange = self.ax_main.get_ylim()[1] - self.ax_main.get_ylim()[0]
        sub_yrange = self.ax_sub.get_ylim()[1] - self.ax_sub.get_ylim()[0]
        picker = 0.005

        if math.log(abs(x - xycoord[0])) < 3 or abs(main_y - xycoord[1]) < yrange*picker:
            self.draggable_lines[0].follower = self.mpl_connect(
                "motion_notify_event", self.draggable_lines[0].followmouse)
            self.draggable_lines[0].releaser = self.mpl_connect(
                "button_press_event", self.draggable_lines[0].releaseonclick)

        elif math.log(abs(x - sub_xycoord[0])) < 3 or abs(sub_y - sub_xycoord[1]) < sub_yrange*picker:
            self.draggable_lines[1].follower = self.mpl_connect(
                "motion_notify_event", self.draggable_lines[1].sub_followmouse)
            self.draggable_lines[1].releaser = self.mpl_connect(
                "button_press_event", self.draggable_lines[1].sub_releaseonclick)

  # Drag and Drop

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
            self.wg_canvas._switch_canvas(self.id, id)

  # Others
    def reset_linewidth(self) -> None:
        '''
        Set linewidth of all curves on the canvas to default value.
        '''
        for _ax_ in self.fig.axes:
            for line in _ax_.lines:
                line.set_linewidth(LINEWIDTH_DEFAULT)

    # def handle_pick(self, event):
    #     print('wg_canvas.py pick event')
        # print(event)


class MyCanvas(QWidget):
    """
    Self-defined QWidget containing a toolbar and multiple ``MyCanvasItem``.
    The layout inside it can adjust by user at the run time.

    :ivar MainWindow mainwindow: The MainWindow instance that this MyCanvas instance belongs to.
    :ivar List[MyCanvasItem] canvasPool: A list of ``MyCanvasItem``.

    :ivar str mode: current canvas layout mode. \n
            Support mode *main*, *up and down* for ver_0.2.0.
    :ivar Dict status:
            Store the mode and its canvas arrangement as a dictionary.
    :ivar MyToolBar toolbar: A MyToolBar instance.
    """

    def __init__(self, mainwindow=None):
        super().__init__()
        self.mainwindow = mainwindow
        ui_conf = mainwindow.project.ui_conf["MyCanvas"]
        self.canvasPool = []
        self.status = {}
        for _key_, _value_ in ui_conf["canvasPool"].items():
            id, types, parameter = _value_.values()
            self.canvasPool.append(MyCanvasItem(parent=self, id=id, types=[
                CurveType(types[0]), CurveType(types[1])], params=parameter))
        for mode, canvas_idx in ui_conf["status"].items():
            canvas_set = []
            for _i in canvas_idx:
                canvas_set.append(self.canvasPool[_i])
            self.status.update({mode: canvas_set})

        self.initUI()
        self.mode = ui_conf["mode"]
        self.focusing_canvas = self.canvasPool[0]
        self.focusing_canvas.apply_style()

    def initUI(self) -> None:
        """Initial User Interface."""
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

    def _add_canvas(self, types_: List[CurveType]) -> int:
        id = self.canvasPool.count()
        new_canvas = MyCanvasItem(parent=self, id=id, types=types_)
        self.canvasPool.append(new_canvas)
        return id

    def replot(self) -> None:
        '''
        Replot all the canvas instances in the list ``canvasPool``.
        '''
        for _canvas_ in self._get_active_canvas():
            _canvas_.replot()

    def change_focusing_canvas(self, focusing_canvas: MyCanvasItem) -> None:
        """
        Change current focusing canvas, only one at a time.
        Modify the displaying style and also change ``toolbar``'s target canvas.
        """
        self.focusing_canvas = focusing_canvas

        for _canvas_ in self._get_active_canvas():
            _canvas_.toggle_focus_style(_canvas_ == focusing_canvas)

        self.toolbar.update_focus_canvas(focusing_canvas)
        self.replot()

    def _switch_canvas(self, old_id: int, new_id: int) -> None:
        """
        Switch two MyCanvasItem instances' positions in the layout.
        """
        old_canvas = self.canvasPool[old_id]
        new_canvas = self.canvasPool[new_id]

        if new_canvas in self._get_active_canvas():
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
        for _mode_, _canvas_arr_ in self.status.items():
            canvas_set = [_canvas_.id for _canvas_ in _canvas_arr_]
            self.mainwindow.project.ui_conf["MyCanvas"]["status"].update({
                                                                         _mode_: canvas_set})

    def set_mode(self, mode: str) -> None:
        """
        Set canvas layout mode.
        """
        self.mode = mode
        self.change_focusing_canvas(self._get_active_canvas()[0])

    def get_canvas(self, _type: CurveType = None, id: int = None):
        """
        Return a MyCanvasItem with given id or given axis' CurveType.
        """
        if _type is not None:
            for _canvas_ in self.canvasPool:
                ax_id, ax_match = _canvas_.get_ax(_type)
                if ax_match:
                    return _canvas_, ax_id, ax_match

        elif id is not None:
            for _canvas_ in self.canvasPool:
                if id == _canvas_.id:
                    return _canvas_
        return None, None, None

    def _get_active_canvas(self): return self.status[self.mode]
