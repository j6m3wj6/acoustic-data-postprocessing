from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QLabel, QAction, QSizePolicy, QSpacerItem, QWidget, QToolButton
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from .dlg_graph_properties import Dlg_GraphProperties
from .ui_conf import ICON_DIR


class MyToolBar(NavigationToolbar2QT):
    def __init__(self, canvas, parent=None):
        self.mainwindow = parent
        self.focusing_canvas = canvas
        self.toolitems = []  # clear NavigationToolbar2QT object default setting
        self.actions = {}
        NavigationToolbar2QT.__init__(self, canvas, parent)

        toolitems = [       # toolitem = (name, icon_name, hover_text, callback)
            ('Home', 'home', 'Default-view', 'home'),
            ('Back', 'back-arrow', 'Previous view', 'back'),
            ('Forward', 'forward-arrow', 'Next view', 'forward'),
            ('Pan', 'move', 'move', 'pan'),
            ('Zoom', 'zoom-in', 'Zoom in', 'zoom'),
            ('Save', 'filesave', 'Save figure', 'save_figure'),
            ('Setting', 'setting', 'Canvas setting', 'edit_parameter'),
            # ('Lines', 'cross-line', 'Draggable vertical line', 'show_draggable_lines'),
            ('Y-scale', 'y-scale', 'Autoscale y axis', 'autoscale_yaxis'),
        ]

        self.initUI(toolitems)

    def _create_action(self, name, icon_name, hover_text, callback):
        icon_dir = ICON_DIR + f"%s.png" % (icon_name)
        button_action = QAction(QIcon(icon_dir), hover_text, self)
        button_action.triggered.connect(getattr(self, callback))
        if callback in ['zoom', 'pan', 'show_draggable_lines']:
            button_action.setCheckable(True)
        return button_action

    def _create_toolbtn(self, icon_name, hover_text):
        toolbtn = QToolButton()
        toolbtn.setToolTip(hover_text)
        toolbtn.setIcon(QIcon(ICON_DIR+f"{icon_name}.png"))
        toolbtn.setCheckable(True)
        toolbtn.setStyleSheet("""
            QToolButton {
                border: transparent;
                padding: 2px;
            }
            QToolButton::checked {
                background-color: #b4b4b4;
                opacity:1;
            }
            QToolButton::hover {
                background-color: #9accff;
                opacity: 0.2;
            }
        """)
        return toolbtn

    def _create_axis_toolbtnset(self, toolbtns):
        wg = QWidget()
        hbly = QHBoxLayout()
        for _btn_ in toolbtns:
            hbly.addWidget(_btn_)
        wg.setLayout(hbly)
        hbly.setContentsMargins(0, 0, 0, 0)

        return wg

    def initUI(self, toolitems):
      # Create and append actions to toolbar by the list ``toolitems``.
        self.lb_canvas = QLabel()
        self.addWidget(self.lb_canvas)
        for t in toolitems:
            (name, icon_name, hover_text, callback) = t
            button_action = self._create_action(
                name, icon_name, hover_text, callback)
            self.actions[name] = button_action
            self.addAction(button_action)

        wg = QWidget()
        hbly = QHBoxLayout()
        wg.setLayout(hbly)
        hbly.addItem(QSpacerItem(400, 20, QSizePolicy.Expanding,
                                 QSizePolicy.Minimum))
        hbly.setContentsMargins(0, 0, 0, 0)
        self.addWidget(wg)

        self.addWidget(QLabel("Right Axis  "))
        self.ax_main_toolbtns = {}
        self.ax_main_toolbtns['grid'] = self._create_toolbtn(
            'grid', "Toggle grid")
        self.ax_main_toolbtns['crosslines'] = self._create_toolbtn(
            'cross-line', "Toggle draggable cross lines")
        wg = self._create_axis_toolbtnset(self.ax_main_toolbtns.values())
        self.addWidget(wg)

        self.addWidget(QLabel("   Left Axis  "))
        self.ax_sub_toolbtns = {}
        self.ax_sub_toolbtns = {}
        self.ax_sub_toolbtns['grid'] = self._create_toolbtn(
            'grid', "Toggle grid")
        self.ax_sub_toolbtns['crosslines'] = self._create_toolbtn(
            'cross-line', "Toggle draggable cross lines")
        wg = self._create_axis_toolbtnset(self.ax_sub_toolbtns.values())
        self.addWidget(wg)

      # Style and Setting
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.setIconSize(QSize(24, 24))
        self.lb_canvas.setStyleSheet("""
            min-width: 110px;
            border: 1.5px solid #0D3B66;
            border-radius: 4px;
        """)
        self.lb_canvas.setAlignment(Qt.AlignCenter)

      # Connect Functions
        self.ax_sub_toolbtns
        self.ax_main_toolbtns['grid'].clicked.connect(self.toggle_grid)
        self.ax_sub_toolbtns['grid'].clicked.connect(self.toggle_grid)
        self.ax_main_toolbtns['crosslines'].clicked.connect(
            lambda event: self.toggle_crosslines(event, 0))
        self.ax_sub_toolbtns['crosslines'].clicked.connect(
            lambda event: self.toggle_crosslines(event, 1))

    def toggle_grid(self, toggle):
        # print("toggle_grid", toggle)
        status = [self.ax_main_toolbtns['grid'].isChecked(
        ), self.ax_sub_toolbtns['grid'].isChecked()]
        self.focusing_canvas.set_grid_status(status)

    def toggle_crosslines(self, toggle, ax_id):
        # print("toggle_crosslines", ax_id, toggle)
        self.focusing_canvas.draggable_lines[ax_id].set_visible(toggle)
        self.focusing_canvas.replot()
        # coords = self.focusing_canvas.draggable_lines.get_coords()

    def edit_parameter(self):
        dlg = Dlg_GraphProperties(mainwindow=self.mainwindow)
        dlg.exec()
        self.mainwindow.dwg_data.filepool.sync_curveData()

    def autoscale_yaxis(self):
        # self.focusing_canvas.autoscale(0)
        # self.focusing_canvas.autoscale(1)
        self.focusing_canvas.parameter["Axis"]["Y-Axis"]['auto-scale'] = True
        self.focusing_canvas.parameter["Axis"]["Sub_Y-Axis"]['auto-scale'] = True
        self.focusing_canvas.replot()

    def update_focus_canvas(self, canvas):
        self.lb_canvas.setText(canvas.get_name())
        for key, _a in self.actions.items():
            _a.setChecked(False)

        self.focusing_canvas = canvas
        NavigationToolbar2QT.__init__(self, canvas, self.mainwindow.wg_canvas)

        grid_main, grid_sub = self.focusing_canvas.set_grid_status()
        self.ax_main_toolbtns["grid"].setChecked(grid_main)
        self.ax_sub_toolbtns["grid"].setChecked(grid_sub)

        self.ax_main_toolbtns["crosslines"].setChecked(
            self.focusing_canvas.draggable_lines[0].vline.get_visible())
        self.ax_sub_toolbtns["crosslines"].setChecked(
            self.focusing_canvas.draggable_lines[1].vline.get_visible())
