from traceback import print_tb
from PyQt5.QtWidgets import QWidget, QTabWidget,\
    QComboBox, QLineEdit, QCheckBox, QLabel, \
    QDialog, QDialogButtonBox, QStyledItemDelegate,\
    QHBoxLayout, QVBoxLayout, QFormLayout, QAbstractItemView, QHeaderView
from PyQt5.QtCore import QSize, Qt, QEvent
from PyQt5.QtGui import QPixmap, QColor, QIcon
from .ui_conf import ICON_DIR, LINEWIDTHS, COLORS
from .wg_filepool import TB_CURVES_HEADER
from textwrap import fill
from .wg_selfdefined import Cbox_Color, Cbox_Linewidth


class Delegate(QStyledItemDelegate):
    def __init__(self, tb):
        super().__init__()
        print(self, tb)
        self.tb_curves = tb

    def eventFilter(self, source, event):
        if event.type() == QEvent.KeyPress:
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
        """Initial User Interface."""

      # Create Components
        self.cbox_color = Cbox_Color()
        self.cbox_linewidth = Cbox_Linewidth()

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

        tb_cboxes_color = self.tb_curves.findChildren(
            QComboBox, "cbox_color")
        tb_cboxes_linewidth = self.tb_curves.findChildren(
            QComboBox, "cbox_linewidth")

        for (_color_, _linewidth_) in zip(tb_cboxes_color, tb_cboxes_linewidth):
            _color_.currentIndexChanged.connect(self._tbcbox_handle_changed)
            _linewidth_.currentIndexChanged.connect(
                self._tbcbox_handle_changed)

        self.delegate = Delegate(self.tb_curves)
        self.tb_curves.installEventFilter(self.delegate)
        self.tb_curves.setItemDelegate(self.delegate)
        self.tb_curves.setTabKeyNavigation(False)
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

    def _tbcbox_handle_changed(self, event):
        row = self.tb_curves.currentIndex().row()
        col = self.tb_curves.currentIndex().column()
        # print("_tbcbox_handle_changed", row, col, event)
        if col == TB_CURVES_HEADER.index("Color"):
            self.cbox_color.setCurrentIndex(event)
        elif col == TB_CURVES_HEADER.index("LineWidth"):
            self.cbox_linewidth.setCurrentIndex(event)

    def handle_cellChanged(self, row, col):
        # print("handle_cellChanged")
        if TB_CURVES_HEADER[col] in ["Data testname", "Color", "LineWidth"]:
            return

        item = self.tb_curves.item(row, col)
        item_text = item.text()
        wg_curve, testnames = self.tb_curves.item(row, 0).data(Qt.UserRole)
        for _testname_ in testnames:
            curveData = wg_curve.get_curveData(_testname_)
            if col == 0:

                if item_text is "":
                    item_text = "Curve"
                    item.setText("Curve")
                curveData.label = item_text
                if not curveData.line_props["visible"]:
                    continue
                curveData.line.set_label(
                    fill(item_text, int(
                        self.canvas.parameter["General"]['Legend']['text-wrap'])))
            elif col == 1:
                curveData.note = item_text
            wg_curve.set_curveData(curveData, _testname_)

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
                _testname_) for _testname_ in testnames]
            curveData = list(
                filter(lambda x: x.line_props["visible"] == True, curveDatas))[0]
            color_index = COLORS.index(curveData.line.get_color())
            self.cbox_color.setCurrentIndex(color_index)
            linewidth_index = LINEWIDTHS.index(curveData.line.get_linewidth())
            self.cbox_linewidth.setCurrentIndex(linewidth_index)
            self.le_legend.setText(curveData.label)
            self.le_note.setText(curveData.note)

    def le_legend_handleEdited(self, event):
        for _item_ in self.tb_curves.selectedItems()[0::len(TB_CURVES_HEADER)]:
            wg_curve, testnames = _item_.data(Qt.UserRole)
            for _testname_ in testnames:
                curveData = wg_curve.get_curveData(_testname_)
                if not curveData.line_props["visible"]:
                    continue
                curveData.label = event
                curveData.line.set_label(
                    fill(event, int(
                        self.canvas.parameter["General"]['Legend']['text-wrap'])))
                wg_curve.set_curveData(curveData, _testname_)
            self.tb_curves.item(
                _item_.row(), TB_CURVES_HEADER.index('Label')).setText(event)

        self.canvas.replot()

    def le_note_handleEdited(self, event):
        for _item_ in self.tb_curves.selectedItems()[0::len(TB_CURVES_HEADER)]:
            wg_curve, testnames = _item_.data(Qt.UserRole)
            for _testname_ in testnames:
                curveData = wg_curve.get_curveData(_testname_)
                if not curveData.line_props["visible"]:
                    continue
                curveData.note = event
                wg_curve.set_curveData(curveData, _testname_)
            self.tb_curves.item(
                _item_.row(), TB_CURVES_HEADER.index('Note')).setText(event)

        # self.canvas.replot()

    def cbox_color_handleChange(self, event):
        if event == -1:
            return
        for _item_ in self.tb_curves.selectedItems()[0::len(TB_CURVES_HEADER)]:
            wg_curve, testnames = _item_.data(Qt.UserRole)
            for _testname_ in testnames:
                curveData = wg_curve.get_curveData(_testname_)
                curveData.line_props["color"] = COLORS[event]
                if not curveData.line_props["visible"]:
                    continue
                curveData.line.set_color(COLORS[event])
                wg_curve.set_curveData(curveData, _testname_)

            self.tb_curves.cellWidget(_item_.row(), TB_CURVES_HEADER.index(
                'Color')).set_color(COLORS[event])

        self.canvas.replot()

    def cbox_linewidth_handleChange(self, event):
        # print("cbox_linewidth_handleChange", event)
        if event == -1:
            return
        for _item_ in self.tb_curves.selectedItems()[0::len(TB_CURVES_HEADER)]:
            wg_curve, testnames = _item_.data(Qt.UserRole)
            for _testname_ in testnames:
                curveData = wg_curve.get_curveData(_testname_)
                curveData.line_props["linewidth"] = LINEWIDTHS[event]
                if not curveData.line_props["visible"]:
                    continue
                curveData.line.set_linewidth(LINEWIDTHS[event])
                wg_curve.set_curveData(curveData, _testname_)

            self.tb_curves.cellWidget(_item_.row(), TB_CURVES_HEADER.index(
                'LineWidth')).set_linewidth(LINEWIDTHS[event])
        self.canvas.replot()

    def _apply_parameters(self):
        self.le_legend_handleEdited(self.le_legend.text())
        self.cbox_linewidth_handleChange(self.cbox_linewidth.currentIndex())
        self.cbox_color_handleChange(self.cbox_color.currentIndex())


class GraphProperties_Dialog(QDialog):
    """
    A dialog for user to customize setting for current focusing canvas. 

    :ivar QWidget filepool: A widget component contains a list of Wg_File instances with all imported data.
    :ivar QWidget canvas: The main canvas area of the window.
    :ivar Dict parameter: 
            A dictionary with the same key structure with general configuration ``FIGURE_CONF``, 
            but stores PyQt components as values instead.
    """

    def __init__(self, mainwindow):
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
        """
        Recursively making the form.

        :param Dict form_dict: A dictionary used to transfer to the form layout on dialog.
        """
        for _key_, _value_ in form_dict.items():
            if isinstance(_value_, dict):
                fmly = QFormLayout()
                fmly.addRow(QLabel(_key_))
                self._create_form(_value_, hbly, fmly, level+2)
                hbly.addLayout(fmly)

            else:
                fmly.addRow(QLabel("  "*level + _key_), _value_)
                fmly.setHorizontalSpacing(25)

    def _create_cbox_scale(self):
        cbox_scale = QComboBox()
        cbox_scale.addItems(["log", "linear"])
        return cbox_scale

    def initUI(self):
        """Initial User Interface."""

      # Create Components
        self.cbox_canvas = QComboBox(self)
        for _act_canvas_ in self.wg_canvas.status[self.wg_canvas.mode]:
            self.cbox_canvas.addItem(_act_canvas_.get_name())
        self.cbox_canvas.setCurrentIndex(self.cbox_canvas.findText(
            self.wg_canvas.focusing_canvas.get_name()))

        self.tab = QTabWidget()
        for _pagename_, _formdict_ in self.parameter.items():
            page = QWidget()
            hbly = QHBoxLayout()
            fmly = QFormLayout()
            self._create_form(_formdict_, hbly, fmly, 0)
            page.setLayout(hbly)
            self.tab.addTab(page, _pagename_)
        self.page_curves = Curve_Style_Page(filepool=self.filepool)
        self.tab.addTab(self.page_curves, "Curves")

        buttonBox = QDialogButtonBox()
        buttonBox.setOrientation(Qt.Horizontal)
        buttonBox.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok | QDialogButtonBox.Apply)
        buttonBox.accepted.connect(self._btn_ok_handleClicked)
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
        """
        Change current focusing canvas that this dialog target on.
        """
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
        """
        Retrieve figure configuration of current focusing canvas.
        """
        for (_param_k_, _param_v_), (_info_k_, _info_v_) in zip(params.items(), info.items()):
            if isinstance(_param_v_, dict):
                self._load_parameters(_param_v_, _info_v_)
            else:
                if isinstance(_param_v_, QLineEdit):
                    _param_v_.setText(str(_info_v_))
                elif isinstance(_param_v_, QCheckBox):
                    if _info_v_:
                        _param_v_.setCheckState(Qt.Checked)

                    else:
                        _param_v_.setCheckState(Qt.Unchecked)
                else:
                    pass

    def _update_parameters(self, params, info):
        """
        Store the parameters of dialog that modified by user to current focusing canvas's figure configuration.
        """
        for (_param_k_, _param_v_), (_info_k_, _info_v_) in zip(params.items(), info.items()):
            if isinstance(_param_v_, dict):
                self._update_parameters(_param_v_, _info_v_)
            else:
                if isinstance(_param_v_, QLineEdit):
                    info[_info_k_] = _param_v_.text()
                elif isinstance(_param_v_, QCheckBox):
                    info[_info_k_] = bool(_param_v_.checkState())
                elif isinstance(_param_v_, QComboBox):
                    info[_info_k_] = _param_v_.currentText()
                else:
                    pass

    def _apply_parameters(self):
        """
        Apply the parameters of dialog that modified by user to current focusing canvas.
        """
        # print("_apply_parameters")
        # print("Before update", self.wg_canvas.focusing_canvas.parameter)
        self._update_parameters(
            self.parameter, self.wg_canvas.focusing_canvas.parameter)
        # print("After update", self.wg_canvas.focusing_canvas.parameter)
        self.page_curves._apply_parameters()
        self.wg_canvas.focusing_canvas.apply_style()
        self._load_parameters(
            self.parameter, self.wg_canvas.focusing_canvas.parameter)

    def _btn_ok_handleClicked(self):
        # print("_btn_ok_handleClicked")
        self._apply_parameters()
        self.accept()
