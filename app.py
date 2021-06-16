from lib.dockwg_data_treelist import *
from lib.dlg_operation import *
from lib.dlg_canvas_setting import *
from lib.dlg_load_files import *
from lib.wg_treelist import *
from lib.wg_canvas import *
from lib.data_objects import *
from lib.dockwg_canvas_layout import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import matplotlib
import sys
import json
matplotlib.use('Qt5Agg')


class MyMenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._createActions()
        fileMenu = QMenu("&File", self)
        self.addMenu(fileMenu)
        self.addMenu('&Help')
        fileMenu.addAction(self.newAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.exitAction)

    def _createActions(self):
      # Creating Components
        self.newAction = QAction("&Act", self)
        self.openAction = QAction("&Open", self)
        self.saveAction = QAction("&Save", self)
        self.exitAction = QAction("&Exit", self)
        self.copyAction = QAction("&Copy", self)
        self.pasteAction = QAction("&Paste", self)
        self.cutAction = QAction("&Cut", self)
        self.helpContentAction = QAction("&Help Content", self)
        self.aboutAction = QAction("&About", self)
      # Connect Functions
        # Connect File actions
        self.newAction.triggered.connect(self.newFile)
        self.openAction.triggered.connect(self.openFile)
        self.saveAction.triggered.connect(self.saveFile)
        # self.exitAction.triggered.connect(self.close)
        # # Connect Edit actions
        # self.copyAction.triggered.connect(self.copyContent)
        # self.pasteAction.triggered.connect(self.pasteContent)
        # self.cutAction.triggered.connect(self.cutContent)
        # # Connect Help actions
        # self.helpContentAction.triggered.connect(self.helpContent)
        # self.aboutAction.triggered.connect(self.about)

    def newFile(self):
        print("newFile")

    def openFile(self):
        # Logic for opening an existing file goes here...
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFile)
        # dialog.setOption(QFileDialog.DontUseNativeDialog)
        dialog.setNameFilter("PKL files (*.pkl)")

        if dialog.exec_():
            path = dialog.selectedFiles()[0]
            filename = path[path.rfind('/')+1:path.rfind('.')]
            self.parent().app.open_project(filename)
        else:
            pass

    def saveFile(self):
        print("saveFile")


class MyApp(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.windows = []
        self.open_project()

    def open_project(self, filename=None):
        new_windows = MainWindow(app=self, project=filename)
        self.windows.append(new_windows)
        new_windows.show()


class MainWindow(QMainWindow):
    def __init__(self, parent=None, app=None, project=None):
        super().__init__(parent)
        self.app = app
        self.project = Project.load_project(project)
        self.ui_conf = self._load_ui_conf()
        self.MainLayout = QVBoxLayout()
        self.initUI()

    def clearLayout(self, layout):
        for i in reversed(range(layout.count())):
            print(type(layout.itemAt(i)))
            # print(i, layout.itemAt(i))
            if (type(layout.itemAt(i)) == QWidgetItem):
                widget = layout.itemAt(i).widget()
                layout.removeWidget(widget)
                widget.setParent(None)
            elif (type(layout.itemAt(i)) == QLayout):
                self.clearLayout(layout.itemAt(i))

    def initUI(self):
      # Create Component
        self.menutopbar = MyMenuBar(self)
        self.setMenuBar(self.menutopbar)

        self.btn_clearData = QPushButton('Clear data')
        self.btn_processingDlg = QPushButton('Operation')
        self.wg_canvas = MyCanvas(self, ui_conf=self.ui_conf["MyCanvas"])
        self.dwg_data = DockWidget_Data(self, Qt.RightDockWidgetArea)
        self.dwg_canvasLayout = DockWidget_CanvasLayout(
            self, Qt.LeftDockWidgetArea)
        self.dwg_canvasLayout._setCanvasLayout_Main(self.wg_canvas)

      # Layout
        MainWidget = QWidget()
        self.MainLayout.addWidget(self.wg_canvas)
        MainWidget.setLayout(self.MainLayout)
        self.setCentralWidget(MainWidget)

      # Style and Setting
        self.setWindowTitle("Python Menus & Toolbars")
        self.resize(1600, 800)
        self.setContentsMargins(0, 0, 0, 0)
        self.MainLayout.setContentsMargins(0, 0, 0, 0)

      # Connect Functions
        self.btn_clearData.clicked.connect(self.btn_clearData_handleClicked)
        self.btn_processingDlg.clicked.connect(
            self.btn_processingDlg_handleClicked)

   # Btn Func - Clear data

    def btn_clearData_handleClicked(self):
        for _c in self.wg_canvas.canvasPool:
            for ax in _c.fig.axes:
                ax.lines = []
            _c.replot()
        self.dwg_data.tab_data.tree.clear()
        self.project.files = []

    def btn_processingDlg_handleClicked(self):
        dlg = OperationDialog(mainwindow=self)
        dlg.exec()

    def btn_axis_setting_handleClicked(self):
        dlg = CanvasSetting_Dialog(mainwindow=self)
        if dlg.exec_():
            print("axisSettingDialog.exec")  # %%%%%%
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
        print("update_ui_conf", self.ui_conf)


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QWidget {
            font-family: Arial;
        }
    """)
    MyApp()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
