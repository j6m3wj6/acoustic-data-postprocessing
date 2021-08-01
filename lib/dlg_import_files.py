from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QPushButton, QLabel,\
    QHBoxLayout, QVBoxLayout, \
    QDialog, QDialogButtonBox,\
    QAbstractItemView, QHeaderView
from PyQt5.QtCore import Qt
from .functions import load_file


class Dlg_ImportFiles(QDialog):
    """
    A dialog for user to import or delete files.
    There are four file sources

    :ivar MainWindow mainwindow: The MainWindow instance this dialog belongs to.
    """

    def __init__(self, mainwindow):
        super().__init__()
        self.mainwindow = mainwindow
        self.initUI()
        self._tb_files_reload_status(mainwindow.project.files)

    def initUI(self):
        """Initail User Interface."""
      # Create Component
        file_sources = ['AP', 'KLIPPEL', 'LEAP', 'COMSOL']
        btns_import = []
        for _source_ in file_sources:
            btn = QPushButton(_source_)
            btns_import.append(btn)
            btn.clicked.connect(self._btn_import_handleClicked)

        btn_deleteFile = QPushButton('Delete')
        btn_clearFile = QPushButton('Clear')
        btn_exportFile = QPushButton('Export')
        # Table
        self.tb_files = QTableWidget()
        self.tb_files.setColumnCount(3)
        self.tb_files.setHorizontalHeaderLabels(
            ['    Source    ', '    FileName    ', '    DateTime    '])

        self.warning_massage = QLabel("")
        self.warning_massage.setObjectName("warning_massage")

        dlg_btnBox = QDialogButtonBox()
        dlg_btnBox.setOrientation(Qt.Horizontal)
        dlg_btnBox.setStandardButtons(QDialogButtonBox.Ok)
        dlg_btnBox.accepted.connect(self.accept)
      # Layout
        vbly_left = QVBoxLayout()
        for _btn_ in btns_import:
            vbly_left.addWidget(_btn_)
        vbly_right = QVBoxLayout()
        vbly_right.addWidget(btn_deleteFile)
        vbly_right.addWidget(btn_clearFile)

        hbly_main = QHBoxLayout()
        hbly_main.addLayout(vbly_left)
        hbly_main.addWidget(self.tb_files)
        hbly_main.addLayout(vbly_right)

        vbly_main = QVBoxLayout()
        vbly_main.addLayout(hbly_main)
        vbly_main.addWidget(self.warning_massage)
        vbly_main.addWidget(dlg_btnBox)
        self.setLayout(vbly_main)
      # Connect Functions
        btn_deleteFile.clicked.connect(self.delete_files)
        btn_clearFile.clicked.connect(self.clear_files)
      # Style and Setting
        headerview = self.tb_files.horizontalHeader()
        headerview.setSectionResizeMode(1, QHeaderView.Stretch)
        self.tb_files.resizeColumnsToContents()
        self.tb_files.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tb_files.setStyleSheet("""
            QTableView::item {
                padding-left: 50px;
                padding-right: 50px;
            }
        """)
        self.setWindowTitle("Import Files")
        self.setFixedSize(800, 400)
        self.warning_massage.setVisible(False)

    def delete_files(self):
        """
        Delete files that user select from the table.
        """
        filenames_to_del = [
            _f.text() for _f in self.tb_files.selectedItems()[1::3]]

        for _f in self.tb_files.selectedItems()[1::3]:
            row = _f.row()
            self.tb_files.removeRow(row)
        self.mainwindow.delete_files(filenames_to_del)

    def clear_files(self):
        """
        Delete all files of the project and clear the table simultanenously.
        """
        self.mainwindow.clear_files()
        for i in range(self.tb_files.rowCount()):
            self.tb_files.removeRow(0)

    def _btn_import_handleClicked(self):
        self.import_file(self.sender().text())

    def import_file(self, source):
        """
        Import file from given source.

        :param str source: Indicate what application is the file exported from.
        """
        file = load_file(source)
        if file:
            file_existed = False
            for _file_ in self.mainwindow.project.files:
                if (_file_.info["Name"] == file.info["Name"]):
                    print("File already exists")
                    file_existed = True
                    break
            if not file_existed:
                row = self.tb_files.rowCount()
                self.tb_files.setRowCount(row + 1)
                self.tb_files.setItem(
                    row, 0, QTableWidgetItem(source))
                self.tb_files.setItem(
                    row, 1, QTableWidgetItem(file.info["Name"]))
                self.tb_files.setItem(
                    row, 2, QTableWidgetItem(file.get_import_time()))
                self.mainwindow.append_file(file)
            self.warning_massage.setVisible(False)

        else:
            print("Not support this file!")
            self.warning_massage.setText(
                f"ERROR: Not support this file! \n Only accept files from AP, KLIPPEL, LEAP and COMSOL. \n And Please use the import button respectively. ")
            self.warning_massage.setVisible(True)

    def _tb_files_reload_status(self, files):
        for _file_ in files:
            row = self.tb_files.rowCount()
            self.tb_files.setRowCount(row + 1)
            self.tb_files.setItem(
                row, 0, QTableWidgetItem(_file_.info["Source"]))
            self.tb_files.setItem(
                row, 1, QTableWidgetItem(_file_.info["Name"]))
            self.tb_files.setItem(
                row, 2, QTableWidgetItem(_file_.get_import_time()))
