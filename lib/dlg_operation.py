from PyQt5.QtWidgets import QLabel, QLineEdit, QRadioButton, QPushButton, QComboBox,\
    QHBoxLayout, QVBoxLayout, QSpacerItem, QGroupBox, QSizePolicy,\
    QDialog, QDialogButtonBox, QColorDialog
from PyQt5.QtCore import Qt
from .obj_data import *
from .wg_treelist import *


class OperationDialog(QDialog):

    def __init__(self, parent=None, mainwindow=None):
        super().__init__(parent)
        self.mainwindow = mainwindow
        self.canvas = mainwindow.wg_canvas.focusing_canvas
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Post-Processing Operation")
        self.resize(800, 600)

        self.listWidget = self.mainwindow.dwg_data.filepool.transfer_to_list()
        # self.listWidget.itemSelectionChanged.connect(self.handleSelect)
        vbly_list = QVBoxLayout()
        vbly_list.addWidget(QLabel("Curves"))
        vbly_list.addWidget(self.listWidget)

        buttonBox = QDialogButtonBox()
        buttonBox.setOrientation(Qt.Horizontal)
        buttonBox.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok | QDialogButtonBox.Apply)
        buttonBox.accepted.connect(self.btn_ok_handleClicked)
        buttonBox.rejected.connect(self.reject)
        buttonBox.button(QDialogButtonBox.Apply).clicked.connect(
            self._apply_operation)

        hbly_offset = QHBoxLayout()
        rb_offset = QRadioButton()
        rb_offset.setObjectName("rb_offset")
        hbly_offset.addWidget(rb_offset)
        lb_offset = QLabel("Magnitude Offset")
        lb_offset.mousePressEvent = lambda event: rb_offset.setChecked(True)
        hbly_offset.addWidget(lb_offset)
        self.le_offset = QLineEdit()
        hbly_offset.addWidget(self.le_offset)
        # cb_offset_unit = QComboBox()
        # cb_offset_unit.addItems(["dB", "%"])
        # hbly_offset.addWidget(cb_offset_unit)
        hbly_offset.addWidget(QLabel("dB"))

        hbly_align = QHBoxLayout()
        rb_align = QRadioButton()
        rb_align.setObjectName("rb_align")
        hbly_align.addWidget(rb_align)
        lb_align = QLabel("Align at ")
        lb_align.mousePressEvent = lambda event: rb_align.setChecked(True)
        hbly_align.addWidget(lb_align)
        hbly_align.addWidget(QLabel("X-Axis"))
        self.le_align_x = QLineEdit()
        hbly_align.addWidget(self.le_align_x)
        hbly_align.addWidget(QLabel("Hz"))
        hbly_align.addWidget(QLabel("Y-Axis"))
        self.le_align_y = QLineEdit()
        hbly_align.addWidget(self.le_align_y)
        hbly_align.addWidget(QLabel("dB"))

        btn_reset = QPushButton("Reset")
        btn_reset.clicked.connect(self.curve_reset)

        gb_vbly = QVBoxLayout()
        gb_vbly.setAlignment(Qt.AlignTop)
        gb_vbly.addLayout(hbly_offset)
        gb_vbly.addLayout(hbly_align)
        gb_vbly.addWidget(btn_reset, alignment=Qt.AlignLeft)
        gb_vbly.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum,
                                    QSizePolicy.Expanding))
        self.warning_massage = QLabel("Error: ")
        self.warning_massage.setStyleSheet("""
            background-color: "#e80000";
            padding: 4px;
            color: "white";
        """)
        gb_vbly.addWidget(self.warning_massage)
        self.warning_massage.setVisible(False)

        self.gb_opperation = QGroupBox("Unary Operation")
        self.gb_opperation.setLayout(gb_vbly)

        btn_color = QPushButton("Color")
        btn_color.clicked.connect(self.colorDialog)

        self.cbox_lineWidth = QComboBox()
        self.cbox_lineWidth.addItems(['1', '2', '3', '4'])
        btn_lineWidth = QPushButton("Align")
        btn_lineWidth.clicked.connect(self.curveLineWidth)

        hbly = QHBoxLayout()
        hbly.addLayout(vbly_list, 3)
        hbly.addWidget(self.gb_opperation, 2)

        vbly = QVBoxLayout()
        vbly.addLayout(hbly)
        vbly.addWidget(buttonBox)
        self.setLayout(vbly)

    def btn_ok_handleClicked(self):
        self._apply_operation()
        self.accept()

    def _apply_operation(self):
        rbuttons = self.gb_opperation.findChildren(QRadioButton)
        callback = {
            "rb_offset": "curve_offset",
            "rb_align": "curve_align",
        }
        for _rb in rbuttons:
            if (_rb.isChecked()):
                getattr(self, callback[_rb.objectName()])()

    def curveLineWidth(self):
        # print(self.cbox_lineWidth.currentText())
        for item in self.listWidget.selectedItems():
            curveData = item.data(Qt.UserRole)
            curveData.line.set_linewidth(
                float(self.cbox_lineWidth.currentText()))
        self.wg_canvas.replot()

    def colorDialog(self):
        col = QColorDialog.getColor()
        print(col, col.name(QColor.HexRgb))
        # if col.isValid():
        # 	self.frm.setStyleSheet('QWidget { background-color: %s }'
        # 						   % col.name())
        for item in self.listWidget.selectedItems():
            curveData = item.data(Qt.UserRole)
            curveData.line.set_color(col.name(QColor.HexRgb))
        self.wg_canvas.replot()

    def handleSelect(self):
        # print("MyDialog handleSelect")
        for c in self.wg_canvas.get_active_canvas():
            c.reset_linewidth()
        for item in self.listWidget.selectedItems():
            if not item.data(Qt.UserRole):
                pass
            else:
                curve = item.data(Qt.UserRole)
                curve.line.set_linewidth(LINEWIDTH_HIGHLIGHT)
        self.wg_canvas.replot()

    def curve_offset(self):
        try:
            selectedItems = self.listWidget.selectedItems()
            selectedItems[0]
            offset = float(self.le_offset.text())
        except IndexError:
            self.warning_massage.setText(
                f"ERROR:\n Please select at least one curve.")
            self.warning_massage.setVisible(True)
        except ValueError:
            print('ERROR: can not turn ' + self.le_offset.text())
            self.warning_massage.setText(
                f"ERROR:\n Maginatude ({self.le_offset.text()}) is not a number,\n please input a valid number.")
            self.warning_massage.setVisible(True)
        else:
            self.warning_massage.setVisible(False)
            for item in selectedItems:
                curveData = item.data(Qt.UserRole)
                curveData.shift(offset)

            self.canvas.replot()

    def curve_align(self):
        try:
            selectedItems = self.listWidget.selectedItems()
            selectedItems[0]
            align_y = float(self.le_align_y.text())
            align_x = float(self.le_align_x.text())
        except IndexError:
            self.warning_massage.setText(
                f"ERROR:\n Please select at least one curve.")
            self.warning_massage.setVisible(True)
        except ValueError:
            print('ERROR: can not turn ' + self.le_align_y.text() +
                  ' and ' + self.le_align_x.text())
            self.warning_massage.setText(
                f"ERROR:\n X-Axis ({self.le_align_x.text()}) or Y-Axis ({self.le_align_y.text()}) is not a number,\n please input a valid number.")
            self.warning_massage.setVisible(True)
        else:
            self.warning_massage.setVisible(False)

            for item in selectedItems:
                curveData = item.data(Qt.UserRole)
                curveData.align(align_y, align_x)

            self.canvas.replot()

    def curve_reset(self):
        try:
            selectedItems = self.listWidget.selectedItems()
            selectedItems[0]
        except IndexError:
            self.warning_massage.setText(
                f"ERROR:\n Please select at least one curve.")
            self.warning_massage.setVisible(True)
        else:
            self.warning_massage.setVisible(False)
            for item in selectedItems:
                curveData = item.data(Qt.UserRole)
                curveData.shift(0)
            self.canvas.replot()
