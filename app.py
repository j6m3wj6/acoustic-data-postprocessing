import pickle
from lib.dockwg_data_treelist import *
from lib.dlg_operation import *
from lib.dlg_canvas_setting import *
from lib.dlg_import_files import *
from lib.dlg_load_files import *
from lib.wg_treelist import *
from lib.wg_canvas import *
from lib.extended_enum import *
from lib.dockwg_canvas_layout import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import matplotlib
import datetime as dt
import sys
import pickle
import dill
matplotlib.use('Qt5Agg')


class MyApp(QMainWindow):
    """App's Main Window."""

    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        # self.project = Project()
        self.project = Project._load_project("myproject")
        self.ui_conf = self._load_ui_conf()
        self.initUI()

    def initUI(self):
        # Create Component
        self._createButton()
        self.wg_canvas = MyCanvas(self, ui_conf=self.ui_conf["MyCanvas"])
        self.dwg_data = DockWidget_Data(self, Qt.RightDockWidgetArea)
        self.dwg_canvasLayout = DockWidget_CanvasLayout(
            self, Qt.LeftDockWidgetArea)
        self.dwg_canvasLayout._setCanvasLayout_Main(self.wg_canvas)

        # Layout
        MainWidget = QWidget()
        MainLayout = QVBoxLayout()
        MainLayout.addWidget(self.wg_canvas)
        MainWidget.setLayout(MainLayout)
        self.setCentralWidget(MainWidget)

        # Layout Style
        self.setWindowTitle("Python Menus & Toolbars")
        self.resize(1600, 800)
        self.setContentsMargins(0, 0, 0, 0)
        MainLayout.setContentsMargins(0, 0, 0, 0)

# Create Components

    def _createButton(self):
        self.btn_clearData = QPushButton('Clear data')
        self.btn_clearData.clicked.connect(self.clearData)

        self.btn_operationDialog = QPushButton('Operation')
        self.btn_operationDialog.clicked.connect(self.operationDialog)

# Btn Func - Clear data
    def clearData(self):
        for _c in self.wg_canvas.canvasPool:
            for ax in _c.fig.axes:
                ax.lines = []
            _c.replot()
        self.dwg_data.tab_data.tree.clear()
        self.project.files = []

# Btn Func - Shift Data
    def operationDialog(self):
        dlg = OperationDialog(myApp=self)
        dlg.exec()

    def importDialog(self):
        dlg = ImportDialog(myApp=self)
        dlg.exec()

    def axisSettingDialog(self):
        dlg = CanvasSetting_Dialog(myApp=self)
        if dlg.exec_():
            for _lb in self.dwg_canvasLayout.lb_canvas:
                _lb.set_text(self.wg_canvas.canvasPool[_lb.idx].get_name())
            for _c in self.wg_canvas.canvasPool:
                _c.ax_main.set_title(_c.get_title())
            self.wg_canvas.toolbar.update_focus_canvas(
                self.wg_canvas.focusing_canvas)
            self.wg_canvas.replot()
        else:
            pass

# Canves Pool Func

    def update_file(self, file):
        self.project.files.append(file)
        self.dwg_data.append_file(file)
        # self.dump()

    def dump(self):
        self.project.dump()
        self.update_ui_conf()

        # self.ui_conf["MyCanvas"]["mode"] = self.wg_canvas.mode
        # self.project.files[0].sequence['CEA2034'][0].dump()
    def _load_ui_conf(self):
        with open("ui_conf.json", "r") as fj:
            ui_conf = json.load(fj)
        # print(ui_conf)
        return ui_conf

    def update_ui_conf(self):
        self.ui_conf["MyCanvas"]["mode"] = self.wg_canvas.mode
        for mode, canvas_set in self.wg_canvas.status.items():
            self.ui_conf["MyCanvas"]["status"][mode] = [
                _c.id for _c in canvas_set]
        for _c in self.wg_canvas.canvasPool:
            self.ui_conf["MyCanvas"]["canvasPool"][str(_c.id)]["types"] = [
                _t.value for _t in _c.ax_types]
            self.ui_conf["MyCanvas"]["canvasPool"][str(
                _c.id)]["parameter"] = _c.parameter
        with open("ui_conf.json", "w") as fj:
            json.dump(self.ui_conf, fj)


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QWidget {
            font-family: Arial;
        }
    """)
    main = MyApp()

    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
