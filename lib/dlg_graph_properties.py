from traceback import print_tb
from lib.wg_filepool import TB_CURVES_HEADER
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QTabWidget,\
    QComboBox, QLineEdit, QCheckBox, QLabel, \
    QDialog, QDialogButtonBox, QStyledItemDelegate,\
    QHBoxLayout, QVBoxLayout, QFormLayout, QAbstractItemView, QHeaderView, QAbstractScrollArea, QAbstractItemDelegate
from PyQt5.QtCore import QSize, Qt, QEvent
from PyQt5.QtGui import QPixmap, QColor, QIcon
from .ui_conf import ICON_DIR, LINEWIDTHS
from .obj_data import COLORS, CurveData
from textwrap import fill


class Delegate(QStyledItemDelegate):
    def __init__(self, tb):
        super().__init__()
        print(self, tb)
        self.tb_curves = tb

    def eventFilter(self, source, event):
        if event.type() == QEvent.KeyPress:
            # print("eventFilter", source)
            current_row = self.tb_curves.currentIndex().row()
            next_column = self.tb_curves.currentIndex().column()
            if event.key() == Qt.Key_Backtab:
                next_row = current_row-1
                item = self.tb_curves.item(next_row, 0)
                while not (item and item.flags()):
                    next_row -= 1
                    if next_row < 0:
                        next_row = self.tb_curves.rowCount()
                    item = self.tb_curves.item(next_row, 0)

                # print("Delegate-next_row, next_column",next_row, next_column)
                self.tb_curves.setCurrentCell(next_row, next_column)
                return True
            elif event.key() == Qt.Key_Tab:
                next_row = current_row+1
                item = self.tb_curves.item(next_row, 0)
                while not (item and item.flags()):
                    next_row += 1
                    if next_row > self.tb_curves.rowCount():
                        next_row = 0
                    item = self.tb_curves.item(next_row, 0)
                # print("Delegate-next_row, next_column",next_row, next_column)
                self.tb_curves.setCurrentCell(next_row, next_column)
                return True
        return super().eventFilter(source, event)


class Curve_Style_Page(QWidget):
    def __init__(self, filepool=None):
        super().__init__()
        self.filepool = filepool
        self.canvas = filepool.mainwindow.wg_canvas.focusing_canvas
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
            icon_dir = ICON_DIR + f"linewidth_%s.png" % (_idx)
            self.cbox_linewidth.addItem(QIcon(icon_dir), "")
        self.cbox_linewidth.setPlaceholderText("-- Select --")
        self.cbox_linewidth.setIconSize(QSize(65, 20))

        self.tb_curves = self.filepool.tranfer_to_table()
        self.le_legend = QLineEdit("")
        self.le_note = QLineEdit("")
      # Layout
        vbly_curves = QVBoxLayout()
        vbly_curves.addWidget(QLabel("Curves ————————"))
        vbly_curves.addWidget(self.tb_curves)

        hbly_legend = QHBoxLayout()
        hbly_legend.addWidget(QLabel("Legend"))
        hbly_legend.addWidget(self.le_legend)

        hbly_note = QHBoxLayout()
        hbly_note.addWidget(QLabel("Note"))
        hbly_note.addWidget(self.le_note)

        hbly_color = QHBoxLayout()
        hbly_color.addWidget(QLabel("Color"))
        hbly_color.addWidget(self.cbox_color)

        hbly_linewidth = QHBoxLayout()
        hbly_linewidth.addWidget(QLabel("Line Style"))
        hbly_linewidth.addWidget(self.cbox_linewidth)

        vbly_parameters = QVBoxLayout()
        vbly_parameters.addWidget(QLabel("Edit Style ————————"))
        vbly_parameters.addLayout(hbly_legend)
        vbly_parameters.addLayout(hbly_note)
        vbly_parameters.addLayout(hbly_color)
        vbly_parameters.addLayout(hbly_linewidth)
        vbly_parameters.setAlignment(Qt.AlignTop)

        hbly = QHBoxLayout()
        hbly.addLayout(vbly_curves, 4)
        hbly.addLayout(vbly_parameters, 3)
        self.setLayout(hbly)
      # Style and Setting
        self.setStyleSheet("""
            QLabel {
                min-width: 100px;
            }
            QComboBox {
                min-width: 120px;
            }
        """)
        # self.tb_curves.setStyleSheet("QTableWidget::item { padding: 10px }")
        self.tb_curves.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tb_curves.verticalHeader().setDefaultSectionSize(20)
        self.tb_curves.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tb_curves.setIconSize(QSize(65, 20))
      # Connect Functions
        self.le_legend.textEdited.connect(self.le_legend_handleEdited)
        self.le_note.textEdited.connect(self.le_note_handleEdited)
        self.cbox_color.currentIndexChanged.connect(
            self.cbox_color_handleChange)
        self.cbox_linewidth.currentIndexChanged.connect(
            self.cbox_linewidth_handleChange)
        self.tb_curves.itemSelectionChanged.connect(
            self.tb_curves_handleSelect)
        self.tb_curves.cellChanged.connect(self.handle_cellChanged)
        self.delegate = Delegate(self.tb_curves)
        self.tb_curves.installEventFilter(self.delegate)
        self.tb_curves.setItemDelegate(self.delegate)
        self.tb_curves.setTabKeyNavigation(False)
  # Handle Functions

    def handle_cellChanged(self, row, col):
        if col in [TB_CURVES_HEADER.index("Color"), TB_CURVES_HEADER.index("LineWidth")]:
            return
        # print("handle_cellChanged", row, col,
        #       self.tb_curves.currentIndex().row(), self.tb_curves.currentIndex().column())

        item = self.tb_curves.item(row, col)
        item_text = item.text()
        wg_curve, testnames = self.tb_curves.item(row, 0).data(Qt.UserRole)
        for testname in testnames:
            curveData = wg_curve.get_curveData(testname)
            # curveData.set_label(event)
            if col == 0:

                if item_text is "":
                    item_text = "Curve"
                    item.setText("Curve")
                curveData.set_label(item_text)
                if not curveData.line_props["visible"]:
                    continue
                curveData.line.set_label(
                    fill(item_text, int(
                        self.canvas.parameter["General"]['Legend']['text-wrap'])))
            elif col == 1:
                curveData.note = item_text
            wg_curve.set_curveData(curveData, testname)

        if col == 0:
            self.le_legend.setText(item_text)
            self.canvas.replot()
        elif col == 1:
            self.le_note.setText(item_text)

        # print("______")

    def tb_curves_handleSelect(self):
        seleced_items = self.tb_curves.selectedItems()[
            0::len(TB_CURVES_HEADER)]
        if len(seleced_items) > 1:
            self.le_legend.setText("")
            self.le_note.setText("")
            self.cbox_linewidth.setCurrentIndex(-1)
            self.cbox_color.setCurrentIndex(-1)

        elif len(seleced_items) == 1:
            wg_curve, testnames = seleced_items[0].data(Qt.UserRole)
            curveDatas = [wg_curve.get_curveData(
                testname) for testname in testnames]
            curveData = list(
                filter(lambda x: x.line_props["visible"] == True, curveDatas))[0]
            color_index = COLORS.index(curveData.line.get_color())
            self.cbox_color.setCurrentIndex(color_index)
            linewidth_index = LINEWIDTHS.index(curveData.line.get_linewidth())
            self.cbox_linewidth.setCurrentIndex(linewidth_index)
            self.le_legend.setText(curveData.label)
            self.le_note.setText(curveData.note)

    def le_legend_handleEdited(self, event):
        for item in self.tb_curves.selectedItems()[0::len(TB_CURVES_HEADER)]:
            wg_curve, testnames = item.data(Qt.UserRole)
            for testname in testnames:
                curveData = wg_curve.get_curveData(testname)
                # curveData.set_label(event)
                if not curveData.line_props["visible"]:
                    continue
                curveData.line.set_label(
                    fill(event, int(
                        self.canvas.parameter["General"]['Legend']['text-wrap'])))
                wg_curve.set_curveData(curveData, testname)
            row, col = item.row(), item.column()
            self.tb_curves.item(
                row, TB_CURVES_HEADER.index('Label')).setText(event)

        self.canvas.replot()

    def le_note_handleEdited(self, event):
        for item in self.tb_curves.selectedItems()[0::len(TB_CURVES_HEADER)]:
            wg_curve, testnames = item.data(Qt.UserRole)
            for testname in testnames:
                curveData = wg_curve.get_curveData(testname)
                # curveData.set_label(event)
                if not curveData.line_props["visible"]:
                    continue
                curveData.note = event
                wg_curve.set_curveData(curveData, testname)
            row, col = item.row(), item.column()
            self.tb_curves.item(
                row, TB_CURVES_HEADER.index('Note')).setText(event)

        # self.canvas.replot()

    def cbox_linewidth_handleChange(self, event):
        if event == -1:
            return
        for item in self.tb_curves.selectedItems()[0::len(TB_CURVES_HEADER)]:
            wg_curve, testnames = item.data(Qt.UserRole)
            for testname in testnames:
                curveData = wg_curve.get_curveData(testname)
                curveData.line_props["linewidth"] = LINEWIDTHS[event]
                if not curveData.line_props["visible"]:
                    continue
                curveData.line.set_linewidth(LINEWIDTHS[event])
                wg_curve.set_curveData(curveData, testname)
                row, col = item.row(), item.column()

                icon_dir = ICON_DIR + f"linewidth_%s.png" % (event)
            self.tb_curves.item(row, TB_CURVES_HEADER.index(
                'LineWidth')).setIcon(QIcon(icon_dir))
        self.canvas.replot()

    def cbox_color_handleChange(self, event):
        if event == -1:
            return
        for item in self.tb_curves.selectedItems()[0::len(TB_CURVES_HEADER)]:
            wg_curve, testnames = item.data(Qt.UserRole)
            for testname in testnames:
                curveData = wg_curve.get_curveData(testname)
                curveData.line_props["color"] = COLORS[event]
                if not curveData.line_props["visible"]:
                    continue
                curveData.line.set_color(COLORS[event])
                wg_curve.set_curveData(curveData, testname)
                row, col = item.row(), item.column()
                pixmap = QPixmap(65, 20)
                pixmap.fill(QColor(COLORS[event]))
            self.tb_curves.item(row, TB_CURVES_HEADER.index(
                'Color')).setIcon(QIcon(pixmap))
        self.canvas.replot()

    def _apply_parameters(self):
        self.le_legend_handleEdited(self.le_legend.text())
        self.cbox_linewidth_handleChange(self.cbox_linewidth.currentIndex())
        self.cbox_color_handleChange(self.cbox_color.currentIndex())


class GraphProperties_Dialog(QDialog):
    def __init__(self, mainwindow=None):
        super().__init__()
        self.filepool = mainwindow.dwg_data.filepool
        self.wg_canvas = mainwindow.wg_canvas

        self.parameter = {
            "General": {
                "Title": QLineEdit(),
                "Margin": {
                    "left-right": QLineEdit(),
                    "top-bottom": QLineEdit(),
                },
                "Legend": {
                    "visible": QCheckBox(),
                    "text-wrap": QLineEdit()
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
                    # "scale": self._create_cbox_scale()
                },
                "Sub_Y-Axis": {
                    "auto-scale": QCheckBox(),
                    "min": QLineEdit(),
                    "max": QLineEdit(),
                    "label": QLineEdit(),
                    "unit": QLineEdit(),
                    # "scale": self._create_cbox_scale()
                }
            },
        }

        self.parameter["Axis"]["X-Axis"]["auto-scale"].stateChanged.connect(
            lambda: self._toggle_autoscale("X-Axis"))
        self.parameter["Axis"]["Y-Axis"]["auto-scale"].stateChanged.connect(
            lambda: self._toggle_autoscale("Y-Axis"))
        self.parameter["Axis"]["Sub_Y-Axis"]["auto-scale"].stateChanged.connect(
            lambda: self._toggle_autoscale("Sub_Y-Axis"))

        self.parameter["General"]["Legend"]["visible"].setCheckState(
            Qt.Checked)
        self._load_parameters(
            self.parameter, self.wg_canvas.focusing_canvas.parameter)

        self.initUI()

    def _create_form(self, form_dict, hbly, fmly, level):
        for key, value in form_dict.items():
            if isinstance(value, dict):
                fmly = QFormLayout()
                fmly.addRow(QLabel(key))
                self._create_form(value, hbly, fmly, level+2)
                hbly.addLayout(fmly)

            else:
                fmly.addRow(QLabel("  "*level + key), value)
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
        self.page_curves = Curve_Style_Page(filepool=self.filepool)
        self.tab.addTab(self.page_curves, "Curves")

        buttonBox = QDialogButtonBox()
        buttonBox.setOrientation(Qt.Horizontal)
        buttonBox.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok | QDialogButtonBox.Apply)
        buttonBox.accepted.connect(self.btn_ok_handleClicked)
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
        self.resize(1000, 600)
        self.setWindowTitle("Graph Properties")
        self.setStyleSheet("""
            QLabel {
                min-width: 100px;
                max-width: 125px;
            }
            QLineEdit {
                min-width: 100px;
                max-width: 125px;
            }
            QComboBox {
                min-width: 100px;
                max-width: 125px;
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
    def _toggle_autoscale(self, axis_name):
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
                elif isinstance(param_v, QComboBox):
                    info[info_k] = param_v.currentText()
                else:
                    pass

    def _apply_parameters(self):
        # print("_apply_parameters")
        # print("Before update", self.wg_canvas.focusing_canvas.parameter)
        self._update_parameters(
            self.parameter, self.wg_canvas.focusing_canvas.parameter)
        # print("After update", self.wg_canvas.focusing_canvas.parameter)
        self.page_curves._apply_parameters()
        self.wg_canvas.focusing_canvas.apply_style()
        self._load_parameters(
            self.parameter, self.wg_canvas.focusing_canvas.parameter)

    def btn_ok_handleClicked(self):
        # print("btn_ok_handleClicked")
        self._apply_parameters()
        self.accept()
