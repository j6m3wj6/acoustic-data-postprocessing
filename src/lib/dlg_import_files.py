from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QPushButton,\
    QHBoxLayout, QVBoxLayout, \
    QDialog, QDialogButtonBox,\
    QAbstractItemView, QHeaderView
from PyQt5.QtCore import Qt
from .dlg_load_files import load_file


class Wg_ImportFile(QWidget):
    def __init__(self, parent=None, files=None):
        super().__init__(parent)
        self.initUI()
        self.tb_files_reload_status(files)

    def initUI(self):
      # Create Component
        # Button
        self.btn_importAP = QPushButton('AP')
        self.btn_importKLIPPEL = QPushButton('KLIPPEL')
        self.btn_importLEAP = QPushButton('LEAP')
        self.btn_importCOMSOL = QPushButton('COMSOL')

        self.btn_deleteFile = QPushButton('Delete')
        self.btn_clearFile = QPushButton('Clear')
        self.btn_exportFile = QPushButton('Export')
        # Table
        self.tb_files = QTableWidget()
        self.tb_files.setColumnCount(3)
        self.tb_files.setHorizontalHeaderLabels(
            ['    Source    ', '    FileName    ', '    DateTime    '])
      # Layout
        self.hbly_main = QHBoxLayout(self)
        self.vbly_left = QVBoxLayout()
        self.vbly_mid = QVBoxLayout()
        self.vbly_right = QVBoxLayout()
        self.hbly_main.addLayout(self.vbly_left)
        self.hbly_main.addLayout(self.vbly_mid)
        self.hbly_main.addLayout(self.vbly_right)

        self.vbly_left.addWidget(self.btn_importAP)
        self.vbly_left.addWidget(self.btn_importKLIPPEL)
        self.vbly_left.addWidget(self.btn_importLEAP)
        self.vbly_left.addWidget(self.btn_importCOMSOL)

        self.vbly_mid.addWidget(self.tb_files)

        self.vbly_right.addWidget(self.btn_deleteFile)
        self.vbly_right.addWidget(self.btn_clearFile)
        self.vbly_right.addWidget(self.btn_exportFile)
      # Style and Setting
        headerview = self.tb_files.horizontalHeader()
        # headerview.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        # headerview.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        headerview.setSectionResizeMode(1, QHeaderView.Stretch)
        # self.tb_files.horizontalHeader().setStretchLastSection(True)
        self.tb_files.resizeColumnsToContents()
        self.tb_files.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tb_files.setStyleSheet("""
            QTableView::item {
                padding-left: 50px;
                padding-right: 50px;
            }
        """)

    def tb_files_reload_status(self, files):
        for _f in files:
            row = self.tb_files.rowCount()
            self.tb_files.setRowCount(row + 1)
            self.tb_files.setItem(
                row, 0, QTableWidgetItem(_f.info["Source"]))
            self.tb_files.setItem(
                row, 1, QTableWidgetItem(_f.info["Name"]))
            self.tb_files.setItem(
                row, 2, QTableWidgetItem(_f.get_import_time()))


class ImportDialog(QDialog):
    def __init__(self, parent=None, mainwindow=None):
        super().__init__(parent)
        self.mainwindow = mainwindow
        self.initUI()

    def initUI(self):
      # Create Component
        self.wg_importFile = Wg_ImportFile(files=self.mainwindow.project.files)

        dlg_btnBox = QDialogButtonBox()
        dlg_btnBox.setOrientation(Qt.Horizontal)
        dlg_btnBox.setStandardButtons(QDialogButtonBox.Ok)
        dlg_btnBox.accepted.connect(self.accept)
      # Layout
        vbly_main = QVBoxLayout()
        vbly_main.addWidget(self.wg_importFile)
        vbly_main.addWidget(dlg_btnBox)
        self.setLayout(vbly_main)
      # Style and Setting
        self.setWindowTitle("Operation Window")
        self.setFixedSize(800, 400)
      # Connect Functions
        self.wg_importFile.btn_importAP.clicked.connect(
            lambda: self.import_file("AP"))
        self.wg_importFile.btn_importLEAP.clicked.connect(
            lambda: self.import_file("LEAP"))
        self.wg_importFile.btn_importKLIPPEL.clicked.connect(
            lambda: self.import_file("KLIPPEL"))

    def import_file(self, source):
        file = load_file(source)
        if (file and file.sequence):
            file_existed = False
            for _f in self.mainwindow.project.files:
                if (_f.info["Name"] == file.info["Name"]):
                    print("File already exists")
                    file_existed = True
                    break
            if not file_existed:
                row = self.wg_importFile.tb_files.rowCount()
                self.wg_importFile.tb_files.setRowCount(row + 1)
                self.wg_importFile.tb_files.setItem(
                    row, 0, QTableWidgetItem(source))
                self.wg_importFile.tb_files.setItem(
                    row, 1, QTableWidgetItem(file.info["Name"]))
                self.wg_importFile.tb_files.setItem(
                    row, 2, QTableWidgetItem(file.get_import_time()))
                self.mainwindow.append_file(file)
        else:
            print("Not support this file!")
