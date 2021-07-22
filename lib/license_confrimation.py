from PyQt5.QtWidgets import QCheckBox, QGridLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, QWidget, QDialog, QDialogButtonBox, \
    QVBoxLayout, QFormLayout, QGroupBox
from PyQt5.QtCore import Qt
import datetime as dt

import calendar
import json
import base64


def add_months(sourcedate, months):
    month = sourcedate.month - 1 + months
    year = sourcedate.year + month // 12
    month = month % 12 + 1
    day = min(sourcedate.day, calendar.monthrange(year, month)[1])
    return dt.date(year, month, day)


def verify_due_day(due_day_str):
    print("verify_due_day: ", due_day_str)
    try:
        due_day = dt.datetime.strptime(due_day_str, "%Y/%m/%d %H:%M:%S")
        if due_day < dt.datetime.now():
            print("::: license is due at %s" % due_day)
            return False
        else:
            print("::: license is not dued until ", due_day)
            return True
    except:
        return False


def verify_license(license):
    print("verify_license: ", license)
    try:
        license = license.lower()
        score = 0
        check_digit = license[0]
        check_digit_count = 0
        chunks = license.split('-')
        for chunk in chunks:
            if len(chunk) != 4:
                return False
            for char in chunk:
                if char == check_digit:
                    check_digit_count += 1
                score += ord(char)
        if score == 1772 and check_digit_count == 5:
            print("::: license (%s) is Valid" % license)
            return True
        return False
    except:
        return False


class License_Confimation(QDialog):
    def __init__(self, conf_path):
        super().__init__()
        self.initUI()

    def initUI(self):
        """Initial User Interface."""
      # Create
        btn_ok = QPushButton("Ok")
        btn_cancel = QPushButton("Cancel")
        hbly = QHBoxLayout()
        hbly.addWidget(btn_ok)
        hbly.addWidget(btn_cancel)
        hbly.setAlignment(Qt.AlignRight)
        btn_ok.clicked.connect(self.btn_ok_handleClicked)
        btn_cancel.clicked.connect(self.reject)
        self.le_license = QLineEdit()
        self.warning_massage = QLabel()
        self.warning_massage.setObjectName("warning_massage")
        self.warning_massage.setVisible(False)

        vbly = QVBoxLayout()
        fmly = QFormLayout()
        fmly.addRow("License", self.le_license)
        vbly.addLayout(fmly)
        vbly.addWidget(self.warning_massage)
        vbly.addLayout(hbly)
        self.setLayout(vbly)
        self.setWindowTitle("License Comfirmation")
        self.resize(300, 50)

    def btn_ok_handleClicked(self):
        license_input = self.le_license.text()
        self.warning_massage.setVisible(False)
        if verify_license(license_input):
            due_day = add_months(dt.datetime.today(), 6)
            self.update_license_info({"license": license_input,
                                     "license_due_day": due_day.strftime("%Y/%m/%d %H:%M:%S")})
            self.accept()
        else:
            self.warning_massage.setText("This license is not valid.")
            self.warning_massage.setVisible(True)

    def update_license_info(self, conf):
        # print("update_license_info", conf)
        conf_str = json.dumps(conf)
        encode = base64.b64encode(conf_str.encode("utf-8"))
        with open("./conf.txt", "wb+") as file:
            file.write(encode)
