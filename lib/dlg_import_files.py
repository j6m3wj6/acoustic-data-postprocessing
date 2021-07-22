from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QPushButton,\
    QHBoxLayout, QVBoxLayout, \
    QDialog, QDialogButtonBox,\
    QAbstractItemView, QHeaderView
from PyQt5.QtCore import Qt
from .dlg_load_files import load_file


class ImportDialog(QDialog):
    def __init__(self, parent=None, mainwindow=None):
        super().__init__(parent)
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

    def delete_files(self):
        filenames_to_del = [
            _f.text() for _f in self.tb_files.selectedItems()[0::3]]

        for _f in self.tb_files.selectedItems()[0::3]:
            row = _f.row()
            self.tb_files.removeRow(row)
        self.mainwindow.delete_files(filenames_to_del)

    def clear_files(self):
        self.mainwindow.clear_files()
        for row in range(self.tb_files.rowCount()):
            self.tb_files.removeRow(0)

    def _btn_import_handleClicked(self):
        self.import_file(self.sender().text())

    def import_file(self, source):
        file = load_file(source)
        if file:
            file_existed = False
            for _f in self.mainwindow.project.files:
                if (_f.info["Name"] == file.info["Name"]):
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
        else:
            print("Not support this file!")

    def _tb_files_reload_status(self, files):
        for _f in files:
            row = self.tb_files.rowCount()
            self.tb_files.setRowCount(row + 1)
            self.tb_files.setItem(
                row, 0, QTableWidgetItem(_f.info["Source"]))
            self.tb_files.setItem(
                row, 1, QTableWidgetItem(_f.info["Name"]))
            self.tb_files.setItem(
                row, 2, QTableWidgetItem(_f.get_import_time()))
