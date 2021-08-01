from PyQt5.QtWidgets import QLabel, QLineEdit, QRadioButton, QPushButton,\
    QHBoxLayout, QVBoxLayout, QSpacerItem, QGroupBox, QSizePolicy,\
    QDialog, QDialogButtonBox
from PyQt5.QtCore import Qt
from .obj_data import *


class Dlg_Operation(QDialog):
    """
    A dialog for user to apply post-processing operation to curves.
    Support uniary operation: Shift and Align.

    :ivar MainWindow mainwindow: The MainWindow instance this dialog belongs to.
    :ivar MyCanvasItem canvas: Current focusing canvas of the ``mainwindow``.
    """

    def __init__(self, mainwindow=None) -> None:
        super().__init__()
        self.mainwindow = mainwindow
        self.canvas = mainwindow.wg_canvas.focusing_canvas
        self.initUI()

    def initUI(self):
        """Initial User Interface."""
        self.listWidget = self.mainwindow.dwg_data.filepool.transfer_to_list()

        rb_offset = QRadioButton()
        rb_offset.setObjectName("rb_offset")
        lb_offset = QLabel("Magnitude Offset")
        self.le_offset = QLineEdit()
        rb_align = QRadioButton()
        rb_align.setObjectName("rb_align")
        lb_align = QLabel("Normalize to")
        self.le_align_x = QLineEdit()
        self.le_align_y = QLineEdit()
        btn_reset = QPushButton("Reset")

        self.warning_massage = QLabel()
        self.warning_massage.setObjectName("warning_massage")

        buttonBox = QDialogButtonBox()
        buttonBox.setOrientation(Qt.Horizontal)
        buttonBox.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok | QDialogButtonBox.Apply)
      # Layout
        vbly_list = QVBoxLayout()
        vbly_list.addWidget(QLabel("Curves"))
        vbly_list.addWidget(self.listWidget)
        hbly_offset = QHBoxLayout()
        for _wg_ in [rb_offset, lb_offset, self.le_offset, QLabel("units")]:
            hbly_offset.addWidget(_wg_)
        hbly_align = QHBoxLayout()
        for _wg_ in [rb_align, lb_align, QLabel("X-Axis"), self.le_align_x, QLabel("Hz"),
                     QLabel("Y-Axis"), self.le_align_y, QLabel("units")]:
            hbly_align.addWidget(_wg_)

        gb_vbly = QVBoxLayout()
        gb_vbly.setAlignment(Qt.AlignTop)
        gb_vbly.addLayout(hbly_offset)
        gb_vbly.addLayout(hbly_align)
        gb_vbly.addWidget(btn_reset, alignment=Qt.AlignLeft)
        gb_vbly.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum,
                                    QSizePolicy.Expanding))
        gb_vbly.addWidget(self.warning_massage)

        self.gb_opperation = QGroupBox("Unary Operation")
        self.gb_opperation.setLayout(gb_vbly)

        hbly = QHBoxLayout()
        hbly.addLayout(vbly_list, 3)
        hbly.addWidget(self.gb_opperation, 2)
        vbly = QVBoxLayout()
        vbly.addLayout(hbly)
        vbly.addWidget(buttonBox)
        self.setLayout(vbly)
      # Function Connecting
        buttonBox.accepted.connect(self._btn_ok_handleClicked)
        buttonBox.rejected.connect(self.reject)
        buttonBox.button(QDialogButtonBox.Apply).clicked.connect(
            self._apply_operation)
        lb_offset.mousePressEvent = lambda event: rb_offset.setChecked(True)
        lb_align.mousePressEvent = lambda event: rb_align.setChecked(True)
        btn_reset.clicked.connect(self.curve_reset)
      # Style and Setting
        self.warning_massage.setVisible(False)
        self.setWindowTitle("Post-Processing Operation")
        self.resize(800, 600)

    def _btn_ok_handleClicked(self) -> None:
        self._apply_operation()
        self.accept()

    def _get_operation(self) -> str:
        operation = None
        rbuttons = self.gb_opperation.findChildren(QRadioButton)
        for _rb_ in rbuttons:
            if _rb_.isChecked():
                operation = _rb_.objectName()
        return operation

    def _apply_operation(self) -> None:
        """
        Route the operation radio button user chooses to the corresponding operation function.
        If user doesn't choose an operation radio button, show the error message.
        """
        callback = {
            "rb_offset": "curve_offset",
            "rb_align": "curve_align",
        }
        operation = self._get_operation()
        if operation:
            getattr(self, callback[operation])()
        else:
            self.warning_massage.setText(
                f"ERROR:\n Please select one operation.")
            self.warning_massage.setVisible(True)

    def curve_offset(self) -> None:
        """
        Shift those urves user select by given magnitude (y-axis).
        """
        try:
            selectedItems = self.listWidget.selectedItems()
            selectedItems[0]
            offset = float(self.le_offset.text())
        except IndexError:
            self.warning_massage.setText(
                f"ERROR:\n Please select at least one curve.")
            self.warning_massage.setVisible(True)
        except ValueError:
            self.warning_massage.setText(
                f"ERROR:\n Maginatude ({self.le_offset.text()}) is not a number,\n please input a valid number.")
            self.warning_massage.setVisible(True)
        else:
            self.warning_massage.setVisible(False)
            for item in selectedItems:
                curveData = item.data(Qt.UserRole)
                curveData.shift(offset)

            self.canvas.replot()

    def curve_align(self) -> None:
        """
        Align those urves user select to a given maginitude (y-axis) at given frequency (x-axis).
        """
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
            self.warning_massage.setText(
                f"ERROR:\n X-Axis ({self.le_align_x.text()}) or Y-Axis ({self.le_align_y.text()}) is not a number,\n please input a valid number.")
            self.warning_massage.setVisible(True)
        else:
            self.warning_massage.setVisible(False)

            for item in selectedItems:
                curveData = item.data(Qt.UserRole)
                curveData.align(align_y, align_x)

            self.canvas.replot()

    def curve_reset(self) -> None:
        """
        Remove all curves' offset and reset to their original data.
        """
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
