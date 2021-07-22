
from typing import List
from PyQt5.QtWidgets import QScrollArea, QWidget, QPushButton, QTabWidget, QDockWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from .dlg_import_files import ImportDialog
from .obj_data import FileData, Project
from .wg_filepool import FilePool


class DockWidget_Data(QDockWidget):
    """
    :ivar MainWindow mainwindow: The MainWindow object that this DockWidget_Data object belongs.

    :ivar FilePool filePool: 
          A QWidget component contains a list of imported file components.
          It contains functions of interaction between file components.
    """

    def __init__(self, mainwindow, position: Qt.DockWidgetArea) -> None:
        super().__init__("Data", mainwindow)
        self.mainwindow = mainwindow
        self.initUI()
        mainwindow.addDockWidget(Qt.DockWidgetArea(position), self)

        self.load_project(mainwindow.project)

    def initUI(self) -> None:
        """Initial User Interface."""
      # Create Component
        btn_importDlg = QPushButton("Import")
        btn_save = QPushButton("Save")
        self.filepool = FilePool(self.mainwindow)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.filepool)
      # Layout
        vbly = QVBoxLayout()
        vbly.addWidget(btn_importDlg)
        vbly.addWidget(scroll)
        vbly.addWidget(btn_save)
        wg_main = QWidget()
        wg_main.setLayout(vbly)
        self.setWidget(wg_main)
      # Connect Functions
        btn_importDlg.clicked.connect(self.btn_importDlg_handleClicked)
        btn_save.clicked.connect(self.mainwindow.save_file)
      # Style and Setting
        vbly.setContentsMargins(10, 0, 10, 10)
        self.setMinimumWidth(400)

    def append_file(self, fileData: FileData) -> None:
        """
        Append a new imported file to component ``filepool``.

        :param FileData fileData: A FileData object generated from the imported file.
        """
        self.filepool.append_file(fileData)

    def delete_files(self, filenames: List[str]) -> None:
        """
        Removing files from component ``filepool``.

        :param List[str] filenames: A list of filenames user intends to delete.
        """
        self.filepool.delete_files(filenames)

    def load_project(self, project: Project) -> None:
        """
        Retrieve files from a specific project and append them to component ``filepool``.

        :param Project project: A Project object.
        """
        for _fileData_ in project.files:
            self.filepool.append_file(_fileData_)

    def btn_importDlg_handleClicked(self) -> None:
        """
        This function connect with **Import** button.\n 
        When the button is clicked, execute ``ImportDialog`` and pop up a dialog window.
        """
        dlg = ImportDialog(mainwindow=self.parent())
        dlg.exec()
