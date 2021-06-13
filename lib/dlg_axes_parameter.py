# -*- coding:utf-8 -*-
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Curve_Style_Page(QWidget):
    def __init__(self, tree=None):
        super().__init__()
        self.lt_curves = tree.get_focusing_curves_lists()

        self.initUI()

    def initUI(self):
        vbly_curves = QVBoxLayout()
        vbly_curves.addWidget(QLabel("Curves"))
        vbly_curves.addWidget(self.lt_curves)

        hbly = QHBoxLayout()
        hbly.addLayout(vbly_curves)
        self.setLayout(hbly)


class Parameter_Dialog(QDialog):
    def __init__(self, myApp=None):
        super().__init__()
        self.wg_treelist = myApp.dwg_data.tree
        self.wg_canvas = myApp.wg_canvas

        self.parameter = {
            "General": {
                "Title": QLineEdit(),
                "Margin": {
                    "left": QLineEdit(),
                    "right": QLineEdit(),
                    "top": QLineEdit(),
                    "bottom": QLineEdit(),
                },
                "Legend": {
                    "visible": QCheckBox(),
                    "wrap": QLineEdit()
                }
            },
            "Axis": {
                "X-Axis": {
                    "auto-scale": QCheckBox(),
                    "min": QLineEdit(),
                    "max": QLineEdit(),
                    "label": QLineEdit(),
                    "unit": QLineEdit(),
                    "scale": self._create_cbox_scale()
                },
                "Y-Axis": {
                    "auto-scale": QCheckBox(),
                    "min": QLineEdit(),
                    "max": QLineEdit(),
                    "label": QLineEdit(),
                    "unit": QLineEdit(),
                    "scale": self._create_cbox_scale()
                },
                "Sub_Y-Axis": {
                    "auto-scale": QCheckBox(),
                    "min": QLineEdit(),
                    "max": QLineEdit(),
                    "label": QLineEdit(),
                    "unit": QLineEdit(),
                    "scale": self._create_cbox_scale()
                }
            }
        }
        self.parameter["Axis"]["Y-Axis"]["auto-scale"].stateChanged.connect(
            lambda: self._toggle_auto_scale("Y-Axis"))
        self.parameter["Axis"]["Sub_Y-Axis"]["auto-scale"].stateChanged.connect(
            lambda: self._toggle_auto_scale("Sub_Y-Axis"))

        self._load_parameters(
            self.parameter, self.wg_canvas.focusing_canvas.parameter)
        self.parameter["General"]["Legend"]["visible"].setCheckState(
            Qt.Checked)
        self.page_curves = Curve_Style_Page(tree=self.wg_treelist)
        self.initUI()

    def _toggle_auto_scale(self, axis_name):
        scale = self.parameter["Axis"][axis_name]
        if (scale["auto-scale"].checkState() == Qt.PartiallyChecked):
            scale["auto-scale"].setCheckState(Qt.Checked)
            return
        isChecked = scale["auto-scale"].checkState() == Qt.Checked
        self._toggle_readonly(scale["min"], isChecked)
        self._toggle_readonly(scale["max"], isChecked)

    def _toggle_readonly(self, lineEdit, readonly):
        lineEdit.setReadOnly(readonly)
        if (readonly):
            lineEdit.setStyleSheet("background: #efefef;")
        else:
            lineEdit.setStyleSheet("background: white;")

    def _change_editing_canvas(self):
        editing_canvas_name = self.cbox_canvas.currentText()
        for act_c in self.wg_canvas.status[self.wg_canvas.mode]:
            if act_c.get_name() == editing_canvas_name:
                self.wg_canvas.change_focusing_canvas(act_c)
        self._load_parameters(
            self.parameter, self.wg_canvas.focusing_canvas.parameter)

    def _load_parameters(self, params, info):
        for (param_k, param_v), (info_k, info_v) in zip(params.items(), info.items()):
            if isinstance(param_v, dict):
                self._load_parameters(param_v, info_v)
            else:
                if isinstance(param_v, QLineEdit):
                    param_v.setText(str(info_v))
                elif isinstance(param_v, QCheckBox):
                    if info_v:
                        param_v.setCheckState(Qt.Checked)
                    else:
                        param_v.setCheckState(Qt.Unchecked)
                else:
                    pass

    def _update_parameters(self, params, info):
        for (param_k, param_v), (info_k, info_v) in zip(params.items(), info.items()):
            if isinstance(param_v, dict):
                self._update_parameters(param_v, info_v)
            else:
                if isinstance(param_v, QLineEdit):
                    info[info_k] = param_v.text()
                elif isinstance(param_v, QCheckBox):
                    info[info_k] = bool(param_v.checkState())
                else:
                    pass

    def _apply_parameters(self):
        # print("Before update", self.wg_canvas.focusing_canvas.parameter)

        self._update_parameters(
            self.parameter, self.wg_canvas.focusing_canvas.parameter)

        # print("After update", self.wg_canvas.focusing_canvas.parameter)
        self.wg_canvas.focusing_canvas.set_style()

    def _create_form(self, form_dict, layout, level):
        for key, value in form_dict.items():
            if isinstance(value, dict):
                layout.addRow(QLabel(key))
                self._create_form(value, layout, level+2)
            else:
                layout.addRow(QLabel("    "*level + key), value)
                layout.setHorizontalSpacing(25)

    def _create_page(self, form_dict):
        page = QWidget()
        layout = QFormLayout()
        self._create_form(form_dict, layout, 0)
        page.setLayout(layout)
        return page

    def _create_cbox_scale(self):
        cbox_scale = QComboBox()
        cbox_scale.addItems(["log", "linear"])
        return cbox_scale

    def initUI(self):
        self.cbox_canvas = QComboBox(self)
        for act_c in self.wg_canvas.status[self.wg_canvas.mode]:
            self.cbox_canvas.addItem(act_c.get_name())

        self.cbox_canvas.setCurrentIndex(self.cbox_canvas.findText(
            self.wg_canvas.focusing_canvas.get_name()))

        self.cbox_canvas.currentIndexChanged.connect(
            self._change_editing_canvas)

        self.tab = QTabWidget()
        for page_name, form_dict in self.parameter.items():
            page = self._create_page(form_dict)
            self.tab.addTab(page, page_name)

        self.tab.addTab(self.page_curves, "Curves")

        buttonBox = QDialogButtonBox()
        buttonBox.setOrientation(Qt.Horizontal)
        buttonBox.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok | QDialogButtonBox.Apply)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        buttonBox.button(QDialogButtonBox.Apply).clicked.connect(
            self._apply_parameters)

        self.vbly = QVBoxLayout()
        self.vbly.addWidget(self.cbox_canvas)
        self.vbly.addWidget(self.tab)
        self.vbly.addWidget(buttonBox)

        self.setLayout(self.vbly)
