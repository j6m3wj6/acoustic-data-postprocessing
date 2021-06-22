# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import QPushButton, QWidget,\
    QFileDialog, QVBoxLayout, QMainWindow
from PyQt5.QtCore import Qt
from lib.wg_menubar import MyMenuBar
from lib.dockwg_data_treelist import DockWidget_Data
from lib.dlg_operation import OperationDialog
from lib.dlg_canvas_setting import CanvasSetting_Dialog
from lib.wg_canvas import MyCanvas
from lib.dockwg_canvas_layout import DockWidget_CanvasLayout
from lib.obj_data import Project, FileData


class MainWindow(QMainWindow):
    """
    :ivar MyApp app: Object MyApp.
    :vartype app: MyApp

    :ivar Project project: 
            A Project object retrieved from existing project file(.pkl)
            or a empty Project object with default setting.

    :ivar MyMenuBar menutopbar: mainwindow's menubar.

    :ivar MyCanvas wg_canvas: 
            A self-defined QWidget component placed on the center of the mainwindow.

    :ivar DockWidget_Data dwg_data: 
            A self-defined QDockWidget placed on the left area by default 
            that contains imported data listing by a treelist 
            and several functions interacting with the canvases.

    :ivar DockWidget_CanvasLayout dwg_canvasLayout: 
            A self-defined QDockWidget placed on the left area by default that buttons
            in order to switch canvas layout mode and customize canvas setting.
    """

    def __init__(self, app, project_path: str = None) -> None:
        super().__init__()
        self.app = app
        self.project = Project.load_project(project_path)
        self.initUI()

    def initUI(self):
        """ Initial mainwindow's user interface. """
      # Create Component
        btn_clearData = QPushButton('Clear data')
        btn_processingDlg = QPushButton('Operation')
        self.wg_canvas = MyCanvas(
            self, ui_conf=self.project.ui_conf["MyCanvas"])
        self.dwg_data = DockWidget_Data(self, Qt.RightDockWidgetArea)
        self.dwg_canvasLayout = DockWidget_CanvasLayout(
            self, Qt.LeftDockWidgetArea)
        self.dwg_canvasLayout._setCanvasLayout_Main(self.wg_canvas)
        self.menutopbar = MyMenuBar(self)
      # Layout
        vbly_main = QVBoxLayout()
        wg_main = QWidget()
        wg_main.setObjectName("wg_central")
        vbly_main.addWidget(self.wg_canvas)
        wg_main.setLayout(vbly_main)
        self.setMenuBar(self.menutopbar)
        self.setCentralWidget(wg_main)

      # Style and Setting
        self.setWindowTitle(self.project.info["Name"])
        self.resize(1600, 900)
        self.setContentsMargins(0, 0, 0, 0)
        vbly_main.setContentsMargins(0, 0, 0, 0)

      # Connect Functions
        btn_clearData.clicked.connect(self.btn_clearData_handleClicked)
        btn_processingDlg.clicked.connect(
            self.btn_processingDlg_handleClicked)

  # Handle Functions
    def btn_clearData_handleClicked(self) -> None:
        """
        This function connect with QPushButton component ``btn_clearData``
        When the button is clicked, all imported datas and curves on canvases would be cleared.
        """
        for _c in self.wg_canvas.canvasPool:
            for ax in _c.fig.axes:
                ax.lines = []
            _c.replot()
        self.dwg_data.tab_data.tree.clear()
        self.project.files = []

    def btn_processingDlg_handleClicked(self) -> None:
        """
        This function connect with QPushButton component ``btn_processingDlg``
        When the button is clicked, execute ``OperationDialog`` and pop up a dialog window.
        """
        dlg = OperationDialog(mainwindow=self)
        dlg.exec()

    def btn_axis_setting_handleClicked(self) -> None:
        """
        This function connect with QPushButton component ``btn_axis_setting``
        When the button is clicked, execute ``CanvasSetting_Dialog`` and pop up a dialog window.

        It is used for customizing which curve types ``CurveType`` would be drawn on a canvas.
        Each canvas has main axis and sub axis.
        After dialog window closed, update related component with new setting.
        """
        dlg = CanvasSetting_Dialog(mainwindow=self)
        if dlg.exec_():
            for _lb in self.dwg_canvasLayout.lb_canvas:
                _lb.set_text(self.wg_canvas.canvasPool[_lb.idx].get_name())

            for _c in self.wg_canvas.canvasPool:
                _c.ax_main.set_title(_c.update_title())
                _c.replot()

            self.wg_canvas.toolbar.update_focus_canvas(
                self.wg_canvas.focusing_canvas)
        else:
            pass

  # Canves Pool Func
    def append_file(self, file: FileData) -> None:
        """
        Append a new imported file to attributes ``project``, 
        And also append to the treelist in DockWidget component ``dwg_data``.

        :param FileData file: A FileData object generated from the imported file.
        """
        self.project.append_file(file)
        self.dwg_data.append_file(file)

    def save_file(self) -> None:
        """
        Save project to file.
        If this project is "Untitled", which is the default name for a new project, 
        it would execute ``QFileDialog`` and pop up a dialog window letting user to determain a new name and where to save. 
        Otherwise, it would be updated to the origin project file.
        """
        if (self.project.info["Name"] == "Untitled"):
            file_path, file_type = QFileDialog.getSaveFileName(
                self, 'Save File', 'Untitle', "Pickle Files (*.pkl)")
            self.project.info['File Location'] = file_path[0:file_path.rfind(
                '/')]
            self.project.info['Name'] = file_path[file_path.rfind(
                '/')+1:file_path.rfind('.')]

        self.project.dump(location=self.project.get_path())
