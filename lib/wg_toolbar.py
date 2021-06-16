from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from .dlg_axes_parameter import Parameter_Dialog
from .icons import *


class MyToolBar(NavigationToolbar2QT):
    def __init__(self, canvas, parent=None):
        # toolitem = (name, icon_name, hover_text, callback)
        # self.toolitems = [('Subplots', 'putamus parum claram', 'subplots', 'configure_subplots')]
        self.mainwindow = parent
        self.focusing_canvas = canvas

        self.toolitems = []
        toolitems = [
            ('Home', 'home', 'Default-view', 'home'),
            ('Back', 'back-arrow', 'Previous view', 'back'),
            ('Forward', 'forward-arrow', 'Next view', 'forward'),
            ('Pan', 'move', 'move', 'pan'),
            ('Zoom', 'zoom-in', 'Zoom in', 'zoom'),
            ('Save', 'filesave', 'Save figure', 'save_figure'),
            ('Setting', 'setting', 'Canvas setting', 'edit_parameter'),
            ('Lines', 'cross-line', 'Draggable vertical line', 'show_draggable_lines'),
            ('Y-scale', 'y-scale', 'Autoscale y axis', 'autoscale_yaxis'),
        ]
        self.actions = {}
        NavigationToolbar2QT.__init__(self, canvas, parent)
        self.setIconSize(QtCore.QSize(24, 24))
        self.setStyleSheet("""
            spacing: 3px;
        """)

        # self.addWidget(self.cbox_canvas)
        self.lb_canvas = QLabel()
        self.lb_canvas.setStyleSheet("""
            border: 1.5px solid red;
            border-radius: 4px;
            padding: 4px;
        """)
        self.addWidget(self.lb_canvas)

        for t in toolitems:
            (name, icon_name, hover_text, callback) = t
            button_action = self._create_btn_action(
                name, icon_name, hover_text, self, callback)
            self.actions[name] = button_action
            self.addAction(button_action)
        # self.setFixedHeight(36)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    def edit_parameter(self):
        dlg = Parameter_Dialog(mainwindow=self.mainwindow)
        if dlg.exec():
            print("edit_parameter")

            self.mainwindow.dwg_data.tree.sync_with_canvas()
        else:
            pass

    def autoscale_yaxis(self):
        self.focusing_canvas.ax_main.set_ylim(auto=True)
        self.focusing_canvas.ax_sub.set_ylim(auto=True)
        self.focusing_canvas.replot()

    def show_draggable_lines(self, toggle):
        self.focusing_canvas.draggable_lines.set_visible(toggle)
        coords = self.focusing_canvas.draggable_lines.get_coords()

    def update_focus_canvas(self, canvas):
        self.lb_canvas.setText(canvas.get_name())
        for key, _a in self.actions.items():
            _a.setChecked(False)
        self.focusing_canvas = canvas
        if (self.focusing_canvas.draggable_lines.vline.get_visible()):
            self.show_draggable_lines(True)
        NavigationToolbar2QT.__init__(self, canvas, self.mainwindow.wg_canvas)

    def _create_btn_action(self, name, icon_name, hover_text, parent, callback):
        icon_dir = f"./lib/icons/%s.png" % (icon_name)
        # icon_dir = f":/icons/{icon_name}.png"
        button_action = QAction(QIcon(icon_dir), hover_text, parent)

        button_action.triggered.connect(getattr(self, callback))

        if callback in ['zoom', 'pan', 'show_draggable_lines']:
            button_action.setCheckable(True)

        return button_action
