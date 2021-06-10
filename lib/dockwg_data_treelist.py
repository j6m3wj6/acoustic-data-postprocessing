
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from .dlg_load_files import *
from .wg_treelist import *


class DockWidget_Data(QDockWidget):
    def __init__(self, myApp, Position):
        super().__init__("Data", myApp)
        self.setMinimumWidth(400)

        self.initUI(myApp, Position)
        self._load_project(myApp.project)

    def initUI(self, myApp, Position):
        self.dockWidgetContents_data = QWidget()
        self.setWidget(self.dockWidgetContents_data)
        vBoxLayout = QVBoxLayout(self.dockWidgetContents_data)

        btn_importDialog = QPushButton("Import")
        btn_importDialog.clicked.connect(myApp.importDialog)

        self.tab_data = QTabWidget(self)

        page_ALL = QWidget()
        page_SPL = QWidget()
        page_THD = QWidget()
        page_IMP = QWidget()
        page_PHS = QWidget()
        page_EXC = QWidget()

        self.tab_data.addTab(page_ALL, "ALL")
        self.tab_data.addTab(page_SPL, "SPL")
        self.tab_data.addTab(page_THD, "THD")
        self.tab_data.addTab(page_IMP, "IMP")
        self.tab_data.addTab(page_PHS, "PHS")
        self.tab_data.addTab(page_EXC, "EXC")

        self.tree = MyTree(myApp)
        self.tree_layout = QVBoxLayout()
        self.tree_layout.addWidget(self.tree)
        page_ALL.setLayout(self.tree_layout)
        self.tab_data.currentChanged.connect(self.handleChange)

        self.tabs = ["ALL", CurveType.FreqRes,
                     CurveType.THD, CurveType.IMP, CurveType.Phase, CurveType.EX]
        vBoxLayout.setContentsMargins(0, 0, 0, 0)
        vBoxLayout.addWidget(btn_importDialog)
        vBoxLayout.addWidget(self.tab_data)

        myApp.addDockWidget(Qt.DockWidgetArea(Position), self)

    def append_file(self, file):
        self.tree.appendChildren(file)

    def _load_project(self, project):
        for _f in project.files:
            self.tree.appendChildren(_f)

    def handleChange(self, event):
        self.tree.filterChildren([self.tabs[event]])
        self.tab_data.currentWidget().setLayout(self.tree_layout)
