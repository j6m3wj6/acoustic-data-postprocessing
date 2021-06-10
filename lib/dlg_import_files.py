from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from .wg_treelist import *
from .dlg_load_files import *


class ImportFile_Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def initUI(self):
        # Layout
        self.hbly_main = QHBoxLayout(self)
        self.vbly_left = QVBoxLayout()
        self.vbly_mid = QVBoxLayout()
        self.vbly_right = QVBoxLayout()
        self.hbly_main.addLayout(self.vbly_left)
        self.hbly_main.addLayout(self.vbly_mid)
        self.hbly_main.addLayout(self.vbly_right)

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
            ['Source', 'FileName', 'DateTime'])

        header = self.tb_files.horizontalHeader()
        header.setStretchLastSection(True)
        self.tb_files.resizeColumnsToContents()
        self.tb_files.setSelectionBehavior(QAbstractItemView.SelectRows)

        # Add into Layout
        self.vbly_left.addWidget(self.btn_importAP)
        self.vbly_left.addWidget(self.btn_importKLIPPEL)
        self.vbly_left.addWidget(self.btn_importLEAP)
        self.vbly_left.addWidget(self.btn_importCOMSOL)

        self.vbly_mid.addWidget(self.tb_files)

        self.vbly_right.addWidget(self.btn_deleteFile)
        self.vbly_right.addWidget(self.btn_clearFile)
        self.vbly_right.addWidget(self.btn_exportFile)


class ImportDialog(QDialog):
    """Employee dialog."""

    def __init__(self, parent=None, myApp=None):
        super().__init__(parent)
        self.myApp = myApp
        self.initUI()
        self._load_file()

    def initUI(self):
        self.setWindowTitle("Operation Window")
        self.resize(800, 600)

        dlg_btnBox = QDialogButtonBox()
        dlg_btnBox.setOrientation(Qt.Horizontal)
        dlg_btnBox.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        dlg_btnBox.accepted.connect(self.accept)
        dlg_btnBox.rejected.connect(self.reject)
        QMetaObject.connectSlotsByName(self)

        self.wg_importFile = ImportFile_Widget()
        self.wg_importFile.initUI()
        self.wg_importFile.btn_importAP.clicked.connect(
            lambda: self.import_file("AP"))
        self.wg_importFile.btn_importLEAP.clicked.connect(
            lambda: self.import_file("LEAP"))
        self.wg_importFile.btn_importKLIPPEL.clicked.connect(
            lambda: self.import_file("KLIPPEL"))
        self.wg_importFile.btn_clearFile.clicked.connect(self.myApp.clearData)

        vbly_main = QVBoxLayout()
        vbly_main.addWidget(self.wg_importFile)

        vbly_main.addWidget(dlg_btnBox)
        self.setLayout(vbly_main)

    def _load_file(self):
        for _f in self.myApp.project.files:
            row = self.wg_importFile.tb_files.rowCount()
            self.wg_importFile.tb_files.setRowCount(row + 1)
            self.wg_importFile.tb_files.setItem(
                row, 0, QTableWidgetItem(_f.info["Source"]))
            self.wg_importFile.tb_files.setItem(
                row, 1, QTableWidgetItem(_f.info["Name"]))
            self.wg_importFile.tb_files.setItem(
                row, 2, QTableWidgetItem(_f.get_import_time()))

    def import_file(self, source):
        file = load_file(source)
        if (file and file.sequence):
            file_existed = False
            for _f in self.myApp.project.files:
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
                self.myApp.update_file(file)
        else:
            print("Not support this file!")
