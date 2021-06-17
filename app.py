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
        fileMenu.addAction(self.act_new)
        fileMenu.addAction(self.act_open)
        fileMenu.addAction(self.act_save)
        fileMenu.addAction(self.act_exit)

    def _createActions(self):
      # Creating Components
        self.act_new = QAction("&New", self)
        self.act_open = QAction("&Open", self)
        self.act_save = QAction("&Save", self)
        self.act_exit = QAction("&Exit", self)
        self.act_copy = QAction("&Copy", self)
        self.act_paste = QAction("&Paste", self)
        self.act_cut = QAction("&Cut", self)
        self.act_helpContent = QAction("&Help Content", self)
        self.act_about = QAction("&About", self)
      # Connect Functions
        # Connect File actions
        self.act_new.triggered.connect(self.new_file)
        self.act_open.triggered.connect(self.open_file)
        self.act_save.triggered.connect(self.save_file)

    def new_file(self):
        self.parent().app.open_project()

    def open_file(self):
        # Logic for opening an existing file goes here...
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFile)
        # dialog.setOption(QFileDialog.DontUseNativeDialog)
        dialog.setNameFilter("PKL files (*.pkl)")

        if dialog.exec_():
            path = dialog.selectedFiles()[0]
            self.parent().app.open_project(path)
        else:
            pass

    def save_file(self):
        self.parent().save_file()


class MainWindow(QMainWindow):
    def __init__(self, parent=None, app=None, project=None):
        super().__init__(parent)
        self.app = app
        self.project = Project.load_project(project)
        self.MainLayout = QVBoxLayout()
        self.initUI()

    def initUI(self):
      # Create Component
        self.menutopbar = MyMenuBar(self)
        self.setMenuBar(self.menutopbar)

        self.btn_clearData = QPushButton('Clear data')
        self.btn_processingDlg = QPushButton('Operation')
        self.wg_canvas = MyCanvas(
            self, ui_conf=self.project.ui_conf["MyCanvas"])
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
        self.setWindowTitle(self.project.info["Name"])
        self.resize(1600, 800)
        self.setContentsMargins(0, 0, 0, 0)
        self.MainLayout.setContentsMargins(0, 0, 0, 0)

      # Connect Functions
        self.btn_clearData.clicked.connect(self.btn_clearData_handleClicked)
        self.btn_processingDlg.clicked.connect(
            self.btn_processingDlg_handleClicked)

  # Handle Functions
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

    def save_file(self):
        if (self.project.info["Name"] == "Untitled"):
            print("Untitle")
            file_path, file_type = QFileDialog.getSaveFileName(
                self, 'Save File', 'Untitle', "Pickle Files (*.pkl)")
            self.project.info['File Location'] = file_path[0:file_path.rfind(
                '/')]
            self.project.info['Name'] = file_path[file_path.rfind(
                '/')+1:file_path.rfind('.')]

        self.project.dump(location=self.project.get_path())


class MyApp(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.windows = []
        self.open_project()

    def open_project(self, filename=None):
        new_windows = MainWindow(app=self, project=filename)
        self.windows.append(new_windows)
        new_windows.show()


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
