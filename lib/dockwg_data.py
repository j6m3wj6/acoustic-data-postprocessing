
from lib.dlg_load_files import AP_DATA
from PyQt5.QtWidgets import QWidget, QPushButton, QTabWidget, QDockWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from .dlg_import_files import ImportDialog
from .obj_data import FileData, CurveData, CurveType, Measurement, Channel
from .tmp import FilePool


class DockWidget_Data(QDockWidget):

    def __init__(self, mainwindow, position: Qt.DockWidgetArea):
        super().__init__("Data", mainwindow)
        self.mainwindow = mainwindow
        self.initUI(mainwindow, position)

    def initUI(self, mainwindow, position: Qt.DockWidgetArea):
        """
        Initial User Interface.

        :param mainwindow: The mainwindow that this object placed on.
        :param position: The position where this object placed on the mainwindow.
        """
      # Create Component
        btn_importDlg = QPushButton("Import")
        btn_save = QPushButton("Save")

        # vbly = QVBoxLayout()

        self.filepool = FilePool(self.mainwindow)
        self.append_file(AP_DATA)

        wg = QWidget()
        wg.setObjectName("wg_main")
        self.setWidget(wg)
        vbly = QVBoxLayout(wg)
        vbly.addWidget(btn_importDlg)
        vbly.addWidget(self.filepool)
        vbly.addWidget(btn_save)
        mainwindow.addDockWidget(Qt.DockWidgetArea(position), self)
      # Style and Setting
        vbly.setContentsMargins(10, 0, 10, 10)
        self.setMinimumWidth(400)
      # Connect Functions
        btn_importDlg.clicked.connect(self.btn_importDlg_handleClicked)
        btn_save.clicked.connect(self.mainwindow.save_file)

    def append_file(self, file: FileData):
        """
        Listing each curve data from a new imported file on the component ``tree``.

        :param file: A FileData object generated from the imported file.
        """
        self.filepool.append_file(file)

    def delete_files(self, files):
        """
        Removing each curve data of a specific file on the component ``tree``.

        :param file: A FileData object user intends to delete.
        """
        self.filepool.delete_files(files)

    def _load_project(self, project):
        """
        Listing each curve data existing in the project on the component ``tree``.

        :param Project project: A Project object.
        """
        for _f in project.files:
            self.filepool.append_file(_f)

    def btn_importDlg_handleClicked(self):
        """
        This function connect with QPushButton component ``btn_importDlg``
        When the button is clicked, execute ``ImportDialog`` and pop up a dialog window.
        """
        dlg = ImportDialog(mainwindow=self.parent())
        dlg.exec()
