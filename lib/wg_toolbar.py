from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT


class MyToolBar(NavigationToolbar2QT):

    def __init__(self, canvas, parent=None):

        # toolitem = (name, icon_name, hover_text, callback)
        # self.toolitems = [('Subplots', 'putamus parum claram', 'subplots', 'configure_subplots')]

        self.wg_canvas = parent

        self.toolitems = []
        toolitems = [
            ('Home', 'home', 'Default-view', 'home'),
            ('Back', 'back-arrow', 'Previous view', 'back'),
            ('Forward', 'forward-arrow', 'Next view', 'forward'),
            ('Pan', 'move', 'move', 'pan'),
            ('Zoom', 'zoom-in', 'Zoom in', 'zoom'),
            ('Save', 'filesave', 'Save figure', 'save_figure'),
            ('Setting', 'setting', 'Canvas setting', 'edit_parameter'),
        ]

        NavigationToolbar2QT.__init__(self, canvas, parent)
        self.setIconSize(QtCore.QSize(24, 24))

        self.cbox_canvas = QComboBox(self)
        self.cbox_canvas.addItems(self.wg_canvas.get_active_canvas())

        self.addWidget(self.cbox_canvas)

        for t in toolitems:
            (name, icon_name, hover_text, callback) = t
            button_action = self._create_btn_action(
                name, icon_name, hover_text, self, callback)
            self.addAction(button_action)
        # self.setFixedHeight(36)
        # self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    def edit_parameter(self):
        print("edit_parameter")

    def update_canvas(self):
        self.cbox_canvas.clear()
        self.cbox_canvas.addItems(self.wg_canvas.get_active_canvas())

    def _create_btn_action(self, name, icon_name, hover_text, parent, callback):
        icon_dir = f"./lib/image/%s.png" % (icon_name)
        button_action = QAction(QIcon(icon_dir), hover_text, parent)

        button_action.triggered.connect(getattr(self, callback))
        self._actions[name] = button_action

        if callback in ['zoom', 'pan']:
            button_action.setCheckable(True)

        return button_action
