# -*- coding:utf-8 -*-
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QFileDialog, QMainWindow, QVBoxLayout
from PyQt5.QtCore import Qt
from typing import List
from .wg_menubar import MyMenuBar
from .dockwg_data import DockWg_Data
from .dlg_operation import Dlg_Operation
from .dlg_axis_setting import Dlg_AxisSetting
from .wg_canvas import MyCanvas
from .dockwg_canvas import DockWg_Canvas
from .obj_data import Project, FileData
from .functions import KLIPPEL_DATA, AP_DATA, LEAP_DATA
from .ui_conf import ICON_DIR


class MainWindow(QMainWindow):
    """
    :ivar MyApp app: Object MyApp.
    :vartype app: MyApp

    :ivar Project project: 
            A Mainwindow object contains only one Project object. \n
            It is the data base.

    :ivar MyMenuBar menutopbar: 

    :ivar MyCanvas wg_canvas: 
            A self-defined QWidget component placed on the center of the mainwindow.\n
            It contains most of the ploting functions.

    :ivar DockWidget_Data dwg_data: 
            A self-defined QDockWidget placed on the left area by default.\n
            It contains a list of imported files and several functions interacting with the canvases in ``wg_canvas``.

    :ivar DockWidget_CanvasLayout dwg_canvasLayout: 
            A self-defined QDockWidget placed on the left area by default.\n
            It contains functions of switching canvas layout mode, customizing canvas setting and post-processing.
    """

    def __init__(self, app, project_path: str = None) -> None:
        super().__init__()
        self.app = app
        self.project = Project.load_project(project_path)
        self.initUI()

    def initUI(self) -> None:
        """ Initial mainwindow's user interface base on data in attribute ``project``. """
      # Create Component

        self.wg_canvas = MyCanvas(self)

        self.dwg_data = DockWg_Data(self, Qt.RightDockWidgetArea)
        self.dwg_canvasLayout = DockWg_Canvas(
            self, Qt.LeftDockWidgetArea)

        self.dwg_canvasLayout._setCanvasLayout_Main()
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
        vbly_main.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.setWindowTitle(self.project.info["Name"])
        self.setWindowIcon(QIcon(ICON_DIR+"audiowave.png"))
        self.resize(1600, 900)
        self.dwg_canvasLayout.set_canvas_mode(self.wg_canvas.mode)

  # Handle Functions

    def btn_processingDlg_handleClicked(self) -> None:
        """
        This function connect with QPushButton component in ``dockwg_canvas``.\n
        When the button is clicked, execute ``Dlg_Operation`` and pop up a dialog window.
        """
        dlg = Dlg_Operation(mainwindow=self)
        dlg.exec()

    def btn_axis_setting_handleClicked(self) -> None:
        """
        This function connect with QPushButton component ``btn_axis_setting``.\n
        When the button is clicked, execute ``Dlg_AxisSetting`` and pop up a dialog window.

        It is used for customizing which curve types ``CurveType`` would be drawn on a canvas.
        Each canvas has main axis and sub axis.\n
        After dialog window closed, update related component with new setting.
        """
        dlg = Dlg_AxisSetting(mainwindow=self)
        if dlg.exec_():
            for _label_ in self.dwg_canvasLayout.lb_canvas:
                _label_.set_text(
                    self.wg_canvas.canvasPool[_label_.idx].get_name())

            for _canvas_ in self.wg_canvas.canvasPool:
                _canvas_.ax_main.set_title(_canvas_.update_title())
                _canvas_.replot()

            self.wg_canvas.toolbar.update_focus_canvas(
                self.wg_canvas.focusing_canvas)
        else:
            pass

  # Canves Pool Func
    def append_file(self, file: FileData) -> None:
        """
        Append a new imported file to attributes ``project``, 
        and also to the list in DockWidget component ``dwg_data``.

        :param FileData file: A FileData object generated from the imported file.
        """
        self.project.append_file(file)
        self.dwg_data.append_file(file)

    def delete_files(self, filenames_to_del: List[FileData]) -> None:
        """
        Delete files from attributes ``project``, 
        and also the data on the list in DockWidget component ``dwg_data``.

        :param FileData file: A FileData object user intends to delete.
        """
        files_to_del = []
        for _fileData_ in self.project.files:
            if _fileData_.info["Name"] in filenames_to_del and _fileData_ not in files_to_del:
                files_to_del.append(_fileData_)
        self.project.delete_files(files_to_del)
        self.dwg_data.delete_files(filenames_to_del)

    def clear_files(self):
        """
        Delete all the files in attributes ``project``, 
        and also clear curves data on the treelist in DockWidget component ``dwg_data``.
        """
        filenames_to_del = [_f.info["Name"] for _f in self.project.files]
        self.project.clear_files()
        self.dwg_data.delete_files(filenames_to_del)

    def _update_ui_conf(self):
        self.project.ui_conf["MyCanvas"]["mode"] = self.wg_canvas.mode
        for mode, canvas_set in self.wg_canvas.status.items():
            self.project.ui_conf["MyCanvas"]["status"][mode] = [
                _c.id for _c in canvas_set]
        for _c in self.wg_canvas.canvasPool:
            self.project.ui_conf["MyCanvas"]["canvasPool"][str(_c.id)]["types"] = [
                _t.value for _t in _c.ax_types]
            self.project.ui_conf["MyCanvas"]["canvasPool"][str(
                _c.id)]["parameter"] = _c.parameter

    def _update_files(self):
        wg_files = self.dwg_data.filepool.findChildren(QWidget, "Wg_File")
        self.project.files = [wg.fileData for wg in wg_files]

    def save_file(self) -> None:
        """
        Save project to file.\n
        If this project is "Untitled", which is the default name for a new project, 
        it would execute ``QFileDialog`` with a dialog window popping up. 
        User can determain a new name and where to save. \n
        Otherwise, it would be updated to the origin project file.
        """
        if (self.project.info["Name"] == "Untitled"):
            self.save_file_as()
        else:
            self._update_ui_conf()
            self._update_files()
            self.project.dump(location=self.project.get_path())

    def save_file_as(self) -> None:
        """
        Execute ``QFileDialog`` and pop up a dialog window letting user to determain a new name and where to save. 
        """

        file_path, file_type = QFileDialog.getSaveFileName(
            self, 'Save File', self.project.info['Name'], "Pickle Files (*.pkl)")

        if file_path:
            self.project.info['File Location'] = \
                file_path[0:file_path.rfind('/')]
            self.project.info['Name'] = \
                file_path[file_path.rfind('/')+1:file_path.rfind('.')]
            self.setWindowTitle(self.project.info["Name"])
            self._update_ui_conf()
            self._update_files()
            self.project.dump(location=self.project.get_path())
        else:
            pass
