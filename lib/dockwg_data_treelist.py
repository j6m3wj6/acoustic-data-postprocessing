
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from .dlg_import_files import *
from .dlg_load_files import *
from .wg_treelist import *


class DockWidget_Data(QDockWidget):
    def __init__(self, mainwindow, Position):
        super().__init__("Data", mainwindow)
        self.setMinimumWidth(400)

        self.initUI(mainwindow, Position)
        self._load_project(mainwindow.project)

    def initUI(self, mainwindow, Position):
      # Create Component
        btn_importDlg = QPushButton("Import")

        self.tree = MyTree(mainwindow)
        self.tree_layout = QVBoxLayout()
        self.tree_layout.addWidget(self.tree)

        self.tab_data = QTabWidget(self)
        page_ALL = QWidget()
        self.tabs = ["ALL", CurveType.FreqRes,
                     CurveType.THD, CurveType.IMP, CurveType.Phase, CurveType.EX]
        self.tab_data.addTab(page_ALL, "ALL")
        self.tab_data.addTab(QWidget(), "SPL")
        self.tab_data.addTab(QWidget(), "THD")
        self.tab_data.addTab(QWidget(), "IMP")
        self.tab_data.addTab(QWidget(), "PHS")
        self.tab_data.addTab(QWidget(), "EXC")
      # Layout
        page_ALL.setLayout(self.tree_layout)
        self.dockWidgetContents_data = QWidget()
        self.setWidget(self.dockWidgetContents_data)
        vBoxLayout = QVBoxLayout(self.dockWidgetContents_data)
        vBoxLayout.addWidget(btn_importDlg)
        vBoxLayout.addWidget(self.tab_data)
        mainwindow.addDockWidget(Qt.DockWidgetArea(Position), self)
      # Style and Setting
        vBoxLayout.setContentsMargins(0, 0, 0, 0)
      # Connect Functions
        btn_importDlg.clicked.connect(self.btn_importDlg_handleClicked)
        self.tab_data.currentChanged.connect(self.handleChange)

    def append_file(self, file):
        self.tree.appendChildren(file)

    def _load_project(self, project):
        for _f in project.files:
            self.tree.appendChildren(_f)

    def handleChange(self, event):
        self.tree.filterChildren([self.tabs[event]])
        self.tab_data.currentWidget().setLayout(self.tree_layout)

    def btn_importDlg_handleClicked(self):
        dlg = ImportDialog(mainwindow=self.parent())
        dlg.exec()
