
from PyQt5.QtWidgets import QWidget, QPushButton, QTabWidget, QDockWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from .dlg_import_files import ImportDialog
from .wg_treelist import MyTree
from .obj_data import CurveType, FileData, Project
from .tmp import *


class DockWidget_Data_new(QDockWidget):

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
        self.data1 = Wg_File(AP_DATA)
        self.data2 = Wg_File(AP_DATA2)
        # vbly.addWidget(self.data1)
        # vbly.addWidget(self.data2)

        wg = QWidget()
        wg.setObjectName("wg_main")
        self.setWidget(wg)
        vbly = QVBoxLayout(wg)
        vbly.addWidget(btn_importDlg)
        vbly.addWidget(self.data1)
        vbly.addWidget(self.data2)
        vbly.addWidget(btn_save)
        mainwindow.addDockWidget(Qt.DockWidgetArea(position), self)
      # Style and Setting
        vbly.setContentsMargins(10, 0, 10, 10)
        self.setMinimumWidth(400)
      # Connect Functions
