
from PyQt5.QtWidgets import QWidget, QPushButton, QTabWidget, QDockWidget, QVBoxLayout
from PyQt5.QtCore import Qt
from .dlg_import_files import ImportDialog
from .wg_treelist import MyTree
from .obj_data import CurveType, FileData, Project


class DockWidget_Data(QDockWidget):
    """
    :ivar QTabWidget tab_data: 
            Contains several tabs named by ``CurveType``, 
            each of which would filter current data with corresponding type.

    :ivar MyTree tree: 
            A self-defined QTreeWidget component that stores data from different file sources and
            contains several functions to interact with canvases.

    :ivar QVBoxLayout tree_layout: 
            This layout carries attribute ``tree``. When the tab is change in runtime, it would also 
            be re-placed on the current tab simultaneously.

    :ivar list(CurveType) tab_types:
            Store the CurveType supported by this application. 
            The order of each CurveType in this list is the same as the tab order relatively.

    :param mainwindow: The mainwindow that this object placed on.
    :param position: The position where this object placed on the mainwindow.
    """

    def __init__(self, mainwindow, position: Qt.DockWidgetArea):
        super().__init__("Data", mainwindow)
        self.mainwindow = mainwindow
        self.initUI(mainwindow, position)
        self._load_project(mainwindow.project)

    def initUI(self, mainwindow, position: Qt.DockWidgetArea):
        """
        Initial User Interface.

        :param mainwindow: The mainwindow that this object placed on.
        :param position: The position where this object placed on the mainwindow.
        """
      # Create Component
        btn_importDlg = QPushButton("Import")
        btn_save = QPushButton("Save")

        self.tree = MyTree(mainwindow)
        self.tree_layout = QVBoxLayout()
        self.tree_layout.addWidget(self.tree)

        self.tab_data = QTabWidget(self)
        page_ALL = QWidget()
        self.tab_types = [CurveType.ALL, CurveType.SPL,
                          CurveType.THD, CurveType.IMP, CurveType.PHS, CurveType.EXC]
        self.tab_data.addTab(page_ALL, "ALL")
        for _t in self.tab_types[1:]:
            self.tab_data.addTab(QWidget(), _t.name)
      # Layout
        page_ALL.setLayout(self.tree_layout)
        wg = QWidget()
        wg.setObjectName("wg_main")
        self.setWidget(wg)
        vbly = QVBoxLayout(wg)
        vbly.addWidget(btn_importDlg)
        vbly.addWidget(self.tab_data)
        vbly.addWidget(btn_save)
        mainwindow.addDockWidget(Qt.DockWidgetArea(position), self)
      # Style and Setting
        vbly.setContentsMargins(10, 0, 10, 10)
        self.setMinimumWidth(400)
      # Connect Functions
        btn_importDlg.clicked.connect(self.btn_importDlg_handleClicked)
        self.tab_data.currentChanged.connect(self.tab_data_handleChange)
        btn_save.clicked.connect(self.mainwindow.save_file)

    def append_file(self, file: FileData):
        """
        Listing each curve data from a new imported file on the component ``tree``.

        :param file: A FileData object generated from the imported file.
        """
        self.tree.appendChildren(file)

    def delete_files(self, files):
        """
        Removing each curve data of a specific file on the component ``tree``.

        :param file: A FileData object user intends to delete.
        """
        self.tree.removeChildren(files)

    def _load_project(self, project: Project):
        """
        Listing each curve data existing in the project on the component ``tree``.

        :param Project project: A Project object.
        """
        for _f in project.files:
            self.tree.appendChildren(_f)

    def tab_data_handleChange(self, event):
        """
        Triggered when the tab is changed.
        Filter the complete treelist to contain only the CurveType 
        identical to the current tab.

        :param int event: index of current tab.
        """
        self.tree.filterChildren([self.tab_types[event]])
        self.tab_data.currentWidget().setLayout(self.tree_layout)

    def btn_importDlg_handleClicked(self):
        """
        This function connect with QPushButton component ``btn_importDlg``
        When the button is clicked, execute ``ImportDialog`` and pop up a dialog window.
        """
        dlg = ImportDialog(mainwindow=self.parent())
        dlg.exec()
