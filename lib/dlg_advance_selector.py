from PyQt5.QtWidgets import QCheckBox, QGridLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QWidget, QDialog, QDialogButtonBox, \
    QVBoxLayout, QFormLayout, QGroupBox
from PyQt5.QtCore import Qt
from .toolbtn_link import Toolbtn_Link


class AdvanceSelector_Dialog(QDialog):
    def __init__(self, wg_file=None):
        super().__init__()
        self.wg_file = wg_file

        self.initUI()

    def initUI(self):
        """Initial User Interface."""

      # Create
        gb_testnames = QGroupBox("Tests")
        gbly = QGridLayout()
        for idx, testname in enumerate(self.wg_file.fileData.testnames):
            cbox = QCheckBox(testname)
            cbox.setObjectName("cbox_test")
            if testname in self.wg_file.fileData.valid_testnames:
                cbox.setCheckState(Qt.Checked)
            cbox.stateChanged.connect(self.toggle_valid_test)
            gbly.addWidget(cbox, int(idx/3), int(idx % 3))
        gb_testnames.setLayout(gbly)

        gb_selector = QGroupBox("Advance Selector")
        vbly = QVBoxLayout()
        fmly = QFormLayout()
        self.le_startat = QLineEdit()
        self.le_endat = QLineEdit()
        self.le_step = QLineEdit()
        fmly.addRow(f"Start at: ", self.le_startat)
        fmly.addRow(f"End at: ", self.le_endat)
        fmly.addRow(f"Step: ", self.le_step)
        btn_check = QPushButton("Check")
        btn_uncheck = QPushButton("Uncheck")
        btn_check.clicked.connect(lambda: self.apply_select(Qt.Checked))
        btn_uncheck.clicked.connect(lambda: self.apply_select(Qt.Unchecked))
        self.toolbtn_link = Toolbtn_Link(link=self.wg_file.link)
        self.toolbtn_link.clicked.connect(self.toggle_link)

        hbly = QHBoxLayout()
        [hbly.addWidget(btn)
         for btn in [self.toolbtn_link, btn_check, btn_uncheck]]
        [vbly.addLayout(ly) for ly in [fmly, hbly]]
        gb_selector.setLayout(vbly)
        # ----------------
        btn_short = QPushButton("Short")
        btn_median = QPushButton("Median")
        btn_expand = QPushButton("Expand")
        btn_short.clicked.connect(lambda: self.set_height(200))
        btn_median.clicked.connect(lambda: self.set_height(400))
        btn_expand.clicked.connect(lambda: self.set_height(750))
        hbly = QHBoxLayout()
        hbly.addWidget(QLabel("Height: "))
        [hbly.addWidget(btn) for btn in [btn_short, btn_median, btn_expand]]
        gb_widgetHeight = QGroupBox("Size")
        gb_widgetHeight.setLayout(hbly)
        # ----------------

      # Layout
        vbly_main = QVBoxLayout()
        vbly_main.addWidget(gb_testnames)
        vbly_main.addWidget(gb_selector)
        vbly_main.addWidget(gb_widgetHeight)
        self.warning_massage = QLabel("Error: ")
        self.warning_massage.setObjectName("warning_massage")
        vbly_main.addWidget(self.warning_massage)
        self.warning_massage.setVisible(False)
        self.setLayout(vbly_main)
      # Style and Setting
        self.setWindowTitle("Advance Selector")
        # self.resize(300, 300)

    def toggle_valid_test(self, checkState):
        cbox_tests = self.findChildren(QCheckBox, "cbox_test")
        self.wg_file.fileData.valid_testnames = []
        for cbox in cbox_tests:
            if cbox.isChecked():
                self.wg_file.fileData.valid_testnames.append(cbox.text())

        toggle_testname = self.sender().text()
        btn_tests = self.wg_file.findChildren(
            QPushButton, "btn_test")
        if checkState == Qt.Unchecked:
            print("toggle_testname", toggle_testname)
            self.wg_file.toggle_all(
                checkState=checkState, link=False, testname=toggle_testname)

        for btn_test in btn_tests:
            self.wg_file.vbly_tests.removeWidget(btn_test)
            self.wg_file.btngp_tests.removeButton(btn_test)
            btn_test.setParent(None)

        for idx, testname in enumerate(self.wg_file.fileData.valid_testnames):
            btn_test = QPushButton(testname)
            btn_test.setObjectName("btn_test")
            btn_test.setToolTip(testname)
            btn_test.clicked.connect(self.wg_file.changetab_test)
            btn_test.setCheckable(True)
            self.wg_file.vbly_tests.addWidget(btn_test)
            self.wg_file.btngp_tests.addButton(btn_test)
            if (idx == 0):
                btn_test.setChecked(True)
            self.wg_file.changetab_test()

    def apply_select(self, checkstate):
        try:
            startat = int(self.le_startat.text())
            endat = int(self.le_endat.text())
            step = int(self.le_step.text())
            if startat == "" or endat == "" or step == "":
                raise ValueError("invalid literal")

            if startat <= 0 or endat <= 0 or step <= 0:
                raise ValueError("Please input number bigger than zero.")
            if endat <= startat:
                raise ValueError(
                    "Start number should be smaller than End number.")
            print("### apply_select: %s:%s:%s" %
                  (startat-1, endat-1, step), checkstate)
            wg_curves = self.wg_file.findChildren(QWidget, "Wg_Curve")
            for wg_curve in wg_curves[(startat-1):(endat-1):step]:
                wg_curve.set_and_handle_checkState(checkstate)

        except ValueError as error_msg:
            if 'invalid literal' in str(error_msg):
                error_msg = "Please input valid numbers."
            self.warning_massage.setText(f"ERROR:\n {error_msg}")
            self.warning_massage.setVisible(True)
        else:
            self.warning_massage.setVisible(False)

    def set_height(self, height):
        try:
            wg_files = self.wg_file.filepool.findChildren(QWidget, "Wg_File")
            for wg_file in wg_files:
                self.wg_file.filepool.vbly.removeWidget(wg_file)
                wg_file.setParent(None)

            self.wg_file.fixedHeight = height
            for wg_file in wg_files:
                self.wg_file.filepool.vbly.addWidget(wg_file)
                if wg_file.fixedHeight:
                    wg_file.setFixedHeight(wg_file.fixedHeight)

        except ValueError:
            print('ERROR: can not turn ' + self.le_height.text())
            self.warning_massage.setText(
                f"ERROR:\n Height ({self.le_height.text()}) is not a number,\n please input a valid number.")
            self.warning_massage.setVisible(True)
        else:
            self.warning_massage.setVisible(False)

    def toggle_link(self):
        # print("before", self.wg_file.link)
        self.toolbtn_link.toggle_style(self.toolbtn_link.isChecked())
        self.wg_file.toolbtn_link.setChecked(self.toolbtn_link.isChecked())
        # print("after", self.wg_file.link)
