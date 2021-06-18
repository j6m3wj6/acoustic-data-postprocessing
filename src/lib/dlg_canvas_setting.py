from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from .wg_canvas import *


class CanvasSetting_Dialog(QDialog):
    def __init__(self, parent=None, mainwindow=None):
        super().__init__(parent)
        self.mainwindow = mainwindow
        self.wg_canvas = mainwindow.wg_canvas
        self.form_parameter = {}
        self.initUI()
        # self.form_parameter = self._load_form_parameter()

    def _load_form_parameter(self):
        for idx, _c in enumerate(self.wg_canvas.canvasPool):
            cbox_ax0 = self.form_parameter["Canvas"][idx]["ax0"]
            cbox_ax0.setCurrentIndex(CurveType.index(_c.ax_types[0]))

            cbox_ax1 = self.form_parameter["Canvas"][idx]["ax1"]
            cbox_ax1.setCurrentIndex(CurveType.index(_c.ax_types[1]))

    def initUI(self):
        self.setWindowTitle("Operation Window")
        self.resize(300, 300)
        self.update = {}

        dlg_btnBox = QDialogButtonBox()
        dlg_btnBox.setOrientation(Qt.Horizontal)
        dlg_btnBox.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        dlg_btnBox.accepted.connect(self.accept)
        dlg_btnBox.rejected.connect(self.reject)
        QMetaObject.connectSlotsByName(self)

        self.form = self._create_form()
        self.form.setObjectName("form")
        vbly_main = QVBoxLayout()
        vbly_main.addWidget(self.form)

        vbly_main.addWidget(dlg_btnBox)
        self.setLayout(vbly_main)

    def _link_func(self, idx, cb_axis):
        cb_axis.currentTextChanged.connect(
            lambda event: self.handle_change(event, self.wg_canvas.canvasPool[idx], cb_axis))

    def _create_form(self):
        self.form_parameter = {"Canvas": {}}
        widget = QWidget()
        layout = QFormLayout()

        for idx, _c in enumerate(self.wg_canvas.canvasPool):
            cbox_ax0 = QComboBox()
            cbox_ax0.addItems(CurveType.list())
            cbox_ax0.setCurrentIndex(CurveType.index(_c.ax_types[0]))
            cbox_ax0.setObjectName("ax0")
            cbox_ax1 = QComboBox()
            cbox_ax1.addItems(CurveType.list())
            cbox_ax1.setCurrentIndex(CurveType.index(_c.ax_types[1]))
            cbox_ax1.setObjectName("ax1")

            self._link_func(idx, cbox_ax0)
            self._link_func(idx, cbox_ax1)
            hbly = QHBoxLayout()
            hbly.addWidget(cbox_ax0)
            hbly.addWidget(cbox_ax1)
            layout.addRow(f"Canvas {idx}", hbly)

            extra = {
                idx: {
                    "name": f"Canvas {idx}",
                    "ax0": cbox_ax0,
                    "ax1": cbox_ax1
                }
            }
            self.form_parameter["Canvas"].update(extra)

        widget.setLayout(layout)
        return widget

    def handle_change(self, event, canvas, axis):
        ax_id = int(bool(axis.objectName() == "ax1"))
        _type = CurveType(event)
        type_transfer = canvas.set_ax_type(ax_id, _type)
        self.mainwindow.dwg_data.tree.set_children_checkstate(
            _type, Qt.Unchecked)
        self.mainwindow.dwg_data.tree.set_children_checkstate(
            type_transfer, Qt.Unchecked)
        self.wg_canvas.replot()
        # change canvas name/title

        self._load_form_parameter()
