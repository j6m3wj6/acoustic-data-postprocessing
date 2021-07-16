from lib.dlg_load_files import determineTypeByTestName
import sys
from PyQt5.QtWidgets import QLabel, QWidget, QCheckBox, \
    QGridLayout, QStyle, QStyleOption
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter

from textwrap import fill


class Wg_Curve(QWidget):
    def __init__(self, wg_file=None, m_idx=None, ch_idx=0, testname=None):
        super(QWidget, self).__init__()
        self.wg_file = wg_file
        self.selector = wg_file.selector
        self.m_idx = m_idx
        self.ch_idx = ch_idx
        self.curveData = self.get_curveData(testname)
        self.checked = False
        self.setObjectName("Wg_Curve")
        self.initUI()

    def get_measurement(self):
        return self.wg_file.fileData.measurements[self.m_idx]

    def get_curveData(self, testname=None):
        if testname == None:
            testname = self.wg_file.get_testname()
        measurement = self.get_measurement()
        # print("wg_curve.get_curveData", testname, measurement.print(False))

        return measurement.channel[self.ch_idx].sequence[testname]

    def get_curveDatas(self):
        curveDatas = []
        measurement = self.wg_file.fileData.measurements[self.m_idx]
        for testname in self.wg_file.fileData.valid_testnames:
            curveDatas.append(
                measurement.channel[self.ch_idx].sequence[testname])
        return curveDatas

    def get_curveOrder(self, include_test=False):
        ch_count = len(self.wg_file.fileData.measurements[self.m_idx].channel)
        order_in_test = (int(self.m_idx))*ch_count+(int(self.ch_idx)+1)
        curveOrder = order_in_test
        if include_test:
            measurement_count = len(list(self.measurements.keys()))
            testname_idx = self.wg_file.fileData.testnames.index(
                self.wg_file.get_testname())
            curveOrder = testname_idx * \
                (measurement_count*ch_count)+order_in_test

        return curveOrder

    def initUI(self):
        self.checkbox = QCheckBox()
        self.lb_label = QLabel(self.curveData.get_label())
        self.lb_note = QLabel(self.curveData.note)
        self.lb_curve_id = QLabel(str(self.get_curveOrder()))
        self.lb_measurement_id = QLabel("")
        if self.wg_file.fileData.info["Source"] == "AP":
            self.lb_measurement_id = QLabel(str(int(self.m_idx)+1))

        gdly = QGridLayout()
        gdly.addWidget(self.checkbox, 0, 0, Qt.AlignCenter)
        gdly.addWidget(self.lb_curve_id, 1, 0, Qt.AlignCenter)
        gdly.addWidget(self.lb_label, 0, 1)
        gdly.addWidget(self.lb_note, 1, 1)
        gdly.addWidget(self.lb_measurement_id, 1, 2, alignment=Qt.AlignRight)

        gdly.setColumnStretch(1, 6)

        self.setLayout(gdly)

        for item in [self.checkbox, self.lb_label, self.lb_note, self.lb_curve_id, self.lb_measurement_id]:
            item.mousePressEvent = lambda event, item=item: self.handle_clicked(
                event, self.checkbox.checkState())

        # self.checkbox.stateChanged.connect(self.handle_checked)
        self.setStyleSheet("""
            QWidget#Wg_Curve {
                max-height: 80px;
                border-bottom: 1px solid #808080;
                background-color: white;
            }
            QWidget#Wg_Curve::hover {
                border: 1px solid #ff0000;
                border-radius: 5px;
            }
        """)

    def update_info(self, testname=None):
        if not testname:
            testname = self.wg_file.get_testname()
        curveData = self.get_curveData(testname)
        self.lb_label.setText(curveData.label)
        self.lb_note.setText(curveData.note)
        if curveData.line_props["visible"]:
            self.checkbox.setCheckState(Qt.Checked)
        else:
            self.checkbox.setCheckState(Qt.Unchecked)

    def paintEvent(self, pe):
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, o, p, self)

    def set_and_handle_checkState(self, checkState, link=None, testname=None):
        self.checkbox.setCheckState(checkState)
        self.checked = bool(checkState)
        self.handle_checked(checkState, link, testname)

    def handle_clicked(self, event, item):
        # print("wg_curve.handle_clicked", event, self.sender())
        if self.checkbox.checkState() == Qt.Unchecked:
            self.checkbox.setCheckState(Qt.Checked)
            self.checked = True

        elif self.checkbox.checkState() == Qt.Checked:
            self.checkbox.setCheckState(Qt.Unchecked)
            self.checked = False
        self.handle_checked()

    def handle_checked(self, checkState=None, link=None, testname=None):
        if checkState == None:
            checkState = self.checkbox.checkState()
        # print("wg_curve.handle_checked, self.checkbox.checkState() %s, checkState %s"
        #       % (self.checkbox.checkState(), checkState))

        self.wg_file.handle_checked(
            checkState, self.m_idx, self.ch_idx, self.get_curveOrder(), link, testname)

    def copy_params_from_canvas(self):
        for testname in self.wg_file.fileData.valid_testnames:
            curveData = self.get_curveData(testname)
            curveData.sync_with_line()
            self.wg_file.fileData.measurements[self.m_idx].channel[
                self.ch_idx].sequence[testname] = curveData
        self.update_info()


# class BasicContainer(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         wg = QWidget()
#         hbly = QHBoxLayout()
#         textwg = QTextEdit()
#         textwg.setText(AP_DATA.print())

#         vbly = QVBoxLayout()
#         wg_file = Wg_File(fileData=AP_DATA)
#         vbly.addWidget(wg_file)

#         hbly.addWidget(textwg)
#         hbly.addLayout(vbly)
#         wg.setLayout(hbly)
#         self.setCentralWidget(wg)
#         self.resize(600, 300)
#         vbly.setAlignment(Qt.AlignTop)

#         print(wg_file.findChildren(QWidget, "Wg_Curve"))


# if __name__ == '__main__':
#     app = QApplication(sys.argv)

#     main = BasicContainer()
#     main.show()
#     sys.exit(app.exec_())
