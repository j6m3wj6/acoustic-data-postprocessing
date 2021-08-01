from lib.dlg_advance_selector import Dlg_AdvancedSelector
from operator import indexOf
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton,\
    QGroupBox, QScrollArea, QButtonGroup, QHBoxLayout, \
    QToolButton, QVBoxLayout, QStyle, QStyleOption, QSpacerItem, QSizePolicy
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QIcon
from .ui_conf import ICON_DIR
from .wg_curve import Wg_Curve
from .wg_selfdefined import Toolbtn_Link
import textwrap


class Wg_File(QWidget):
    def __init__(self, filepool=None, fileData=None):
        super(QWidget, self).__init__()
        self.filepool = filepool
        self.wg_canvas = filepool.mainwindow.wg_canvas
        self.fileData = fileData
        self.fixedHeight = None
        self.link = True
        self.setObjectName("Wg_File")
        self.initUI()
        self.reload_checkstate()

    def initUI(self):
        """Initial User Interface."""
      # Create Components
        self.lb_filename = QLabel(self.fileData.info["Name"])
        self.lb_filename.setObjectName("lb_filename")

        self.btngp_tests = QButtonGroup()
        wg_btns = QWidget()
        wg_btns.setObjectName("wg_btns")
        self.vbly_tests = QVBoxLayout(wg_btns)
        for idx, testname in enumerate(self.fileData.valid_testnames):
            display_test = "\n".join(textwrap.wrap(
                testname, 10, drop_whitespace=False))
            btn_test = QPushButton(display_test)
            btn_test.setObjectName("btn_test")
            btn_test.setToolTip(testname)
            btn_test.clicked.connect(self.changetab_test)
            btn_test.setCheckable(True)
            self.vbly_tests.addWidget(btn_test)
            self.btngp_tests.addButton(btn_test)
            if (idx == 0):
                btn_test.setChecked(True)

        vbly_data = QVBoxLayout()
        self.toolbtn_checkall = QToolButton()
        # self.toolbtn_checkall.setText("Check All")
        self.toolbtn_checkall.setToolTip("Check All")
        self.toolbtn_checkall.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toolbtn_checkall.setIcon(QIcon(ICON_DIR+"checkall.png"))

        self.toolbtn_uncheckall = QToolButton()
        # self.toolbtn_uncheckall.setText("Uncheck All")
        self.toolbtn_uncheckall.setToolTip("Uncheck All")
        self.toolbtn_uncheckall.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toolbtn_uncheckall.setIcon(QIcon(ICON_DIR+"uncheckall.png"))

        self.toolbtn_advanced = QToolButton()
        # self.toolbtn_advanced.setText("Selector")
        self.toolbtn_advanced.setToolTip("Selector")
        self.toolbtn_advanced.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toolbtn_advanced.setIcon(QIcon(ICON_DIR+"selector.png"))
        self.toolbtn_advanced.clicked.connect(self.advance_selector)

        self.toolbtn_link = Toolbtn_Link(link=self.link)

        self.selector = QGroupBox()
        hbly_checked = QHBoxLayout()
        hbly_checked.addWidget(self.toolbtn_checkall)
        hbly_checked.addWidget(self.toolbtn_uncheckall)
        hbly_checked.addWidget(self.toolbtn_advanced)
        hbly_checked.addItem(QSpacerItem(20, 20, QSizePolicy.Expanding,
                                         QSizePolicy.Minimum))
        hbly_checked.setAlignment(Qt.AlignLeft)
        hbly_checked.addWidget(self.toolbtn_link)
        hbly_checked.setSpacing(2)
        self.selector.setLayout(hbly_checked)

        scroll = QScrollArea()
        wg_curves = QWidget()
        wg_curves.setObjectName("wg_curves")
        vbly_curves = QVBoxLayout(wg_curves)
        for m_idx, measurement in self.fileData.measurements.items():
            for ch_idx in range(len(measurement.channel)):
                wg_curve = Wg_Curve(
                    self, m_idx, ch_idx, self.get_testname())
                vbly_curves.addWidget(wg_curve)
        scroll.setWidgetResizable(True)
        scroll.setWidget(wg_curves)

      # Layout
        vbly_data.addWidget(self.selector)
        vbly_data.addWidget(scroll)

        hbly = QHBoxLayout()
        hbly.addWidget(wg_btns)
        hbly.addLayout(vbly_data)

        vbly = QVBoxLayout()
        vbly.addWidget(self.lb_filename)
        vbly.addLayout(hbly)
        self.setLayout(vbly)
      # Style and Setting
        self.vbly_tests.setAlignment(Qt.AlignTop)
        self.vbly_tests.setContentsMargins(0, 0, 0, 0)
        self.vbly_tests.setSpacing(0)
        vbly_curves.setAlignment(Qt.AlignTop)
        vbly_curves.setSpacing(0)

        vbly_curves.setContentsMargins(2, 0, 0, 0)
        hbly_checked.setContentsMargins(2, 0, 0, 0)
        # hbly_checked.setAlignment(Qt.AlignLeft)

        hbly.setAlignment(Qt.AlignLeft)
        hbly.setContentsMargins(0, 0, 0, 0)
        hbly.setSpacing(0)

        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        # scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

        self.setStyleSheet("""
            QWidget#Wg_File {
                min-height: 300px;
                max-height: 800px;
                border: 2px solid #808080
            }
            QLabel#lb_filename {
                font-size: 14px;
                font-weight: bold;
            }
            QLabel#lb_label {
                font-size: 12px;
            }
            QLabel#lb_note {
                color: #808080
            }
            QWidget#wg_btns {
                max-width: 100px;
            }
            QPushButton {
                Text-align: left;
                padding: 6px 6px;
                width: 80px;
            }
            QPushButton::checked {
                background-color: white;
            }
            
            QToolButton {
                border: transparent
            }
            
        """)
      # Connect Functions
        self.toolbtn_checkall.clicked.connect(
            lambda event, checkState=Qt.Checked: self.toggle_all(event, checkState))
        self.toolbtn_uncheckall.clicked.connect(
            lambda event, checkState=Qt.Unchecked: self.toggle_all(event, checkState))
        self.toolbtn_link.toggled.connect(self.toggle_link)

    def paintEvent(self, pe):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, o, p, self)

    def toggle_link(self):
        # print("!!! wg_file.toggle_link !!!", self.toolbtn_link.isChecked())
        self.link = self.toolbtn_link.isChecked()
        self.toolbtn_link.toggle_style(self.link)

    # def is_valid(self, testname):
    #     btn_tests = self.wg_file.findChildren(QPushButton, "btn_test")
    #     for btn in btn_tests:
    #         if btn.isEnable() and btn.text() == testname:
    #             return True
    #     return False

    def reload_checkstate(self):
        wg_curves = self.findChildren(QWidget, "Wg_Curve")
        for idx, testname in enumerate(self.fileData.valid_testnames):
            for wg_curve in wg_curves:
                curveData = wg_curve.get_curveData(testname)
                if curveData.line_props["visible"]:
                    self.update_canvas(curveData, Qt.Checked,
                                       (idx+1)*wg_curve.get_curveOrder())
        self.changetab_test()

    def changetab_test(self):
        wg_curves = self.findChildren(QWidget, "Wg_Curve")
        for wg in wg_curves:
            wg.update_info()

    def get_visible_curveData(self):
        visible_curveData = {}
        wg_curves = self.findChildren(QWidget, "Wg_Curve")
        for testname in self.fileData.valid_testnames:
            visible_curveData[testname] = []
            for wg_curve in wg_curves:
                curveData = wg_curve.get_curveData(testname)
                if curveData.line_props["visible"]:
                    visible_curveData[testname].append(curveData)

        return visible_curveData

    def get_checkedItems(self, testname=None, mergeAll=False):
        if mergeAll:
            checked_items = []
            wg_curves = self.findChildren(QWidget, "Wg_Curve")
            for wg_curve in wg_curves:
                for testname in self.fileData.valid_testnames:
                    curveData = wg_curve.get_curveData(testname)
                    if curveData.line_props["visible"] and wg_curve not in checked_items:
                        checked_items.append(wg_curve)
        elif not testname:
            testname = self.get_testname()
            checked_items = []
            wg_curves = self.findChildren(QWidget, "Wg_Curve")
            for wg_curve in wg_curves:
                curveData = wg_curve.get_curveData(testname)
                if curveData.line_props["visible"]:
                    checked_items.append(wg_curve)
        return checked_items

    def get_testname(self):
        return self.btngp_tests.checkedButton().text().replace('\n', '')

    def toggle_all(self, event=None, checkState=None, link=None, testname=None, set_and_handle=True):
        print("\n\nwg_file.toggle_all", checkState, testname)
        wg_curves = self.findChildren(QWidget, "Wg_Curve")
        for wg in wg_curves:
            if wg.checkbox.checkState() is not checkState:
                if set_and_handle:
                    wg.set_and_handle_checkState(checkState, link, testname)
                else:
                    wg.handle_checked(checkState, link, testname)

    def handle_checked(self, checkState, m_idx, ch_idx, curveOrder, link=None, testname=None):
        measurement = self.fileData.measurements[m_idx]
        if link == None:
            link = self.link
        if not testname:
            testname = self.get_testname()
        # print("wg_file.handle_checked, checkState %s, self.link %s, link %s, current tab %s, testname %s"
        #       % (checkState, self.link, link, self.btngp_tests.checkedButton().text(), testname))
        # measurement.print()
        if link:
            for _t in self.fileData.valid_testnames:
                # print(_t)
                curveData = measurement.channel[ch_idx].sequence[_t]
                idx = self.fileData.testnames.index(_t)
                self.update_canvas(
                    curveData, checkState, (idx+1)*curveOrder)
        else:
            curveData = measurement.channel[ch_idx].sequence[testname]
            idx = self.fileData.testnames.index(testname)
            self.update_canvas(
                curveData, checkState, (idx+1)*curveOrder)

    def update_canvas(self, curveData, checkState, curveOrder):
        canvas, ax_id, ax = self.wg_canvas.get_canvas(curveData.type)
        if curveData.line and checkState == Qt.Unchecked:
            curveData.line.set_label('_nolegend_')
            curveData.line_props["visible"] = False
            if (ax and curveData.line in ax.lines):
                ax.lines.remove(curveData.line)
        elif checkState == Qt.Checked:
            if curveData.line not in ax.lines:
                legend_wrap = int(
                    canvas.parameter["General"]['Legend']['text-wrap'])
                line = curveData.create_line2D(
                    canvas, ax_id, curveOrder, legend_wrap)
                curveData.line_props["visible"] = True
        canvas.fig.axes[1].set_visible(bool(canvas.fig.axes[1].lines))
        canvas.replot()
        # print("  :::%s, order=%s" %
        #       (curveData.print(console=False), curveOrder), bool(checkState))
        return curveData

    def advance_selector(self):
        dlg = Dlg_AdvancedSelector(wg_file=self)
        if dlg.exec():
            print("advance_selector")
        else:
            pass
