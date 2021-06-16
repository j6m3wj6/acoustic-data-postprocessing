# -*- coding:utf-8 -*-
from lib.extended_enum import COLORS
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

LINEWIDTHS = [1, 1.5, 2.5, 4]


class Curve_Style_Page(QWidget):
    def __init__(self, tree=None):
        super().__init__()
        self.tree = tree
        self.canvas = tree.wg_canvas.focusing_canvas

        self.initUI()

    def initUI(self):
      # Create Components
        self.cbox_color = QComboBox()
        self.cbox_color.setPlaceholderText("-- Select --")
        self.cbox_color.setIconSize(QSize(65, 20))
        for _col in COLORS:
            pixmap = QPixmap(65, 20)
            pixmap.fill(QColor(_col))
            redIcon = QIcon(pixmap)
            self.cbox_color.addItem(redIcon, "")

        self.cbox_linewidth = QComboBox()
        for _idx, _icon in enumerate(LINEWIDTHS):
            icon_dir = f"./lib/icons/linewidth_%s.png" % (_idx)
            self.cbox_linewidth.addItem(QIcon(icon_dir), "")
        self.cbox_linewidth.setPlaceholderText("-- Select --")
        self.cbox_linewidth.setIconSize(QSize(65, 20))

        self.tb_curves = self._create_table()
        self.le_legend = QLineEdit("")
      # Layout
        vbly_curves = QVBoxLayout()
        vbly_curves.addWidget(QLabel("Curves ————————"))
        vbly_curves.addWidget(self.tb_curves)

        hbly_legend = QHBoxLayout()
        hbly_legend.addWidget(QLabel("Legend"))
        hbly_legend.addWidget(self.le_legend)

        hbly_color = QHBoxLayout()
        hbly_color.addWidget(QLabel("Color"))
        hbly_color.addWidget(self.cbox_color)

        hbly_linewidth = QHBoxLayout()
        hbly_linewidth.addWidget(QLabel("Line Style"))
        hbly_linewidth.addWidget(self.cbox_linewidth)

        vbly_parameters = QVBoxLayout()
        vbly_parameters.addWidget(QLabel("Edit Style ————————"))
        vbly_parameters.addLayout(hbly_legend)
        vbly_parameters.addLayout(hbly_color)
        vbly_parameters.addLayout(hbly_linewidth)
        vbly_parameters.setAlignment(Qt.AlignTop)

        hbly = QHBoxLayout()
        hbly.addLayout(vbly_curves, 3)
        hbly.addLayout(vbly_parameters, 2)
        self.setLayout(hbly)
      # Style and Setting
        self.setStyleSheet("""
            QLabel {
                min-width: 80px;
            }
            QComboBox {
                min-width: 100px;
            }
        """)
        # self.tb_curves.setStyleSheet("QTableWidget::item { padding: 10px }")
        self.tb_curves.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tb_curves.verticalHeader().setDefaultSectionSize(20)
        self.tb_curves.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tb_curves.setIconSize(QSize(65, 20))
      # Connect Functions
        self.le_legend.textEdited.connect(self.le_legend_handleEdited)
        self.cbox_color.currentIndexChanged.connect(
            self.cbox_color_handleChange)
        self.cbox_linewidth.currentIndexChanged.connect(
            self.cbox_linewidth_handleChange)
        self.tb_curves.itemSelectionChanged.connect(
            self.tb_curves_handleSelect)

    def _create_table(self):
        tb_curves = QTableWidget()
        tb_curves.setColumnCount(3)
        tb_curves.setHorizontalHeaderLabels(
            ['Label', 'Color', 'LineWidth'])

        for f in range(self.tree.topLevelItemCount()):
            fileroot = self.tree.topLevelItem(f)
            for t in range(fileroot.childCount()):
                testroot = fileroot.child(t)
                testType = testroot.data(1, QtCore.Qt.UserRole)
                if (testroot.checkState(0) == Qt.Unchecked or testType not in self.canvas.ax_types):
                    continue
                row = tb_curves.rowCount()
                tb_curves.setRowCount(row + 1)

                test_item = QTableWidgetItem(
                    fileroot.text(0)+' - '+testroot.text(0))
                test_item.setBackground(Qt.lightGray)
                test_item.setFlags(Qt.NoItemFlags)
                tb_curves.setItem(row, 0, test_item)
                tb_curves.setSpan(row, 0, 1, 3)

                for c in range(testroot.childCount()):
                    curve = testroot.child(c)
                    if (curve.checkState(0) == Qt.Checked):
                        row = tb_curves.rowCount()
                        tb_curves.setRowCount(row + 1)

                        curveData = curve.data(0, QtCore.Qt.UserRole)
                        new_item = QTableWidgetItem(curveData.label)
                        new_item.setData(QtCore.Qt.UserRole, curveData)
                        tb_curves.setItem(row, 0, new_item)
                        tb_curves.item(row, 0).setFlags(
                            tb_curves.item(row, 0).flags() ^ Qt.ItemIsEditable)

                        pixmap = QPixmap(65, 20)
                        pixmap.fill(QColor(curveData.line.get_color()))
                        color_item = QTableWidgetItem()
                        color_item.setIcon(QIcon(pixmap))
                        tb_curves.setItem(row, 1, color_item)

                        linewidth_index = LINEWIDTHS.index(
                            curveData.line.get_linewidth())
                        icon_dir = f"./lib/icons/linewidth_%s.png" % (
                            linewidth_index)
                        linewidth_item = QTableWidgetItem()
                        linewidth_item.setIcon(QIcon(icon_dir))
                        tb_curves.setItem(row, 2, linewidth_item)
        return tb_curves

  # Handle Functions
    def tb_curves_handleSelect(self):
        seleced_items = self.tb_curves.selectedItems()[0::3]
        if len(seleced_items) > 1:
            self.le_legend.setText("( Multiple selected )")
            self.cbox_linewidth.setCurrentIndex(-1)
            self.cbox_color.setCurrentIndex(-1)

        elif len(seleced_items) == 1:
            curve = seleced_items[0].data(QtCore.Qt.UserRole)
            color_index = COLORS.index(curve.line.get_color())
            self.cbox_color.setCurrentIndex(color_index)
            linewidth_index = LINEWIDTHS.index(curve.line.get_linewidth())
            self.cbox_linewidth.setCurrentIndex(linewidth_index)
            self.le_legend.setText(curve.label)

    def le_legend_handleEdited(self, event):
        for item in self.tb_curves.selectedItems()[0::3]:
            curveData = item.data(QtCore.Qt.UserRole)
            curveData.line.set_label(event)
            row, col = item.row(), item.column()
            self.tb_curves.item(row, col).setText(event)

        self.canvas.replot()

    def cbox_linewidth_handleChange(self, event):
        if event == -1:
            return
        for item in self.tb_curves.selectedItems()[0::3]:
            curveData = item.data(QtCore.Qt.UserRole)
            curveData.line.set_linewidth(LINEWIDTHS[event])
            row, col = item.row(), item.column()

            icon_dir = f"./lib/icons/linewidth_%s.png" % (event)
            self.tb_curves.item(row, col+2).setIcon(QIcon(icon_dir))
        self.canvas.replot()

    def cbox_color_handleChange(self, event):
        if event == -1:
            return
        for item in self.tb_curves.selectedItems()[0::3]:
            curveData = item.data(QtCore.Qt.UserRole)
            curveData.line.set_color(COLORS[event])
            row, col = item.row(), item.column()
            pixmap = QPixmap(65, 20)
            pixmap.fill(QColor(COLORS[event]))
            self.tb_curves.item(row, col+1).setIcon(QIcon(pixmap))
        self.canvas.replot()


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
            },
        }

        self._load_parameters(
            self.parameter, self.wg_canvas.focusing_canvas.parameter)
        self.parameter["General"]["Legend"]["visible"].setCheckState(
            Qt.Checked)
        self.parameter["Axis"]["Y-Axis"]["auto-scale"].stateChanged.connect(
            lambda: self._toggle_auto_scale("Y-Axis"))
        self.parameter["Axis"]["Sub_Y-Axis"]["auto-scale"].stateChanged.connect(
            lambda: self._toggle_auto_scale("Sub_Y-Axis"))

        self.initUI()

    def _create_form(self, form_dict, hbly, fmly, level):
        for key, value in form_dict.items():
            if isinstance(value, dict):
                fmly = QFormLayout()
                fmly.addRow(QLabel(key))
                self._create_form(value, hbly, fmly, level+2)
                hbly.addLayout(fmly)

            else:
                fmly.addRow(QLabel("    "*level + key), value)
                fmly.setHorizontalSpacing(25)

    def _create_page(self, form_dict):
        page = QWidget()
        hbly = QHBoxLayout()
        fmly = QFormLayout()
        self._create_form(form_dict, hbly, fmly, 0)
        page.setLayout(hbly)
        return page

    def _create_cbox_scale(self):
        cbox_scale = QComboBox()
        cbox_scale.addItems(["log", "linear"])
        return cbox_scale

    def initUI(self):
      # Create Components
        self.cbox_canvas = QComboBox(self)
        for act_c in self.wg_canvas.status[self.wg_canvas.mode]:
            self.cbox_canvas.addItem(act_c.get_name())
        self.cbox_canvas.setCurrentIndex(self.cbox_canvas.findText(
            self.wg_canvas.focusing_canvas.get_name()))

        self.tab = QTabWidget()
        for page_name, form_dict in self.parameter.items():
            page = self._create_page(form_dict)
            self.tab.addTab(page, page_name)
        self.page_curves = Curve_Style_Page(tree=self.wg_treelist)
        self.tab.addTab(self.page_curves, "Curves")

        buttonBox = QDialogButtonBox()
        buttonBox.setOrientation(Qt.Horizontal)
        buttonBox.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok | QDialogButtonBox.Apply)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        buttonBox.button(QDialogButtonBox.Apply).clicked.connect(
            self._apply_parameters)
      # Layout
        self.vbly = QVBoxLayout()
        self.vbly.addWidget(self.cbox_canvas)
        self.vbly.addWidget(self.tab)
        self.vbly.addWidget(buttonBox)
        self.setLayout(self.vbly)
      # Style and Setting
        self.resize(400, 600)
        self.setStyleSheet("""
            QLineEdit {
                max-width: 100px;
            }
            QComboBOx {
                max-width: 100px;
            }
        """)
      # Connect Functions
        self.cbox_canvas.currentIndexChanged.connect(
            self.cbox_canvas_handleChange)

  # Handle Funtions
    def cbox_canvas_handleChange(self):
        editing_canvas_name = self.cbox_canvas.currentText()
        for act_c in self.wg_canvas.status[self.wg_canvas.mode]:
            if act_c.get_name() == editing_canvas_name:
                self.wg_canvas.change_focusing_canvas(act_c)
        self._load_parameters(
            self.parameter, self.wg_canvas.focusing_canvas.parameter)

  # Setting Functions
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
