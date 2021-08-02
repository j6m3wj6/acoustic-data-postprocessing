from PyQt5.QtWidgets import QLineEdit, QPushButton, QLabel, QDialog, \
    QVBoxLayout, QHBoxLayout, QFormLayout
from PyQt5.QtCore import Qt
from .functions import verify_license, verify_due_day
import datetime as dt
import json
import base64


class Dlg_License(QDialog):
    def __init__(self, dlg_info="", license_used=[]):
        super().__init__()
        self.license_used = license_used
        self.initUI(dlg_info)

    def initUI(self, dlg_info):
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
        vbly.addWidget(QLabel(dlg_info))
        vbly.addLayout(fmly)
        vbly.addWidget(self.warning_massage)
        vbly.addLayout(hbly)
        self.setLayout(vbly)
        self.setWindowTitle("License Comfirmation")
        self.resize(300, 50)

    def btn_ok_handleClicked(self):
        key_input = self.le_license.text()
        self.warning_massage.setVisible(False)
        warning_massage = ""
        if "##" in key_input:
            key = key_input.split("##")
            license = key[0]
            due_day = base64.b64decode(key[1]).decode("utf-8")
            license_isvalid = verify_license(license)
            due_day_isvalid = verify_due_day(due_day)
            license_isused = (license_isvalid and license in self.license_used)
            if license_isvalid and due_day_isvalid and not license_isused:
                self.update_license_info({"license": license,
                                          "license_due_day": due_day,
                                          "license_used": self.license_used})
                self.accept()

            if license_isused:
                warning_massage += "This license had been executed before. It is not valid anymore."
            elif not license_isvalid:
                warning_massage += "This license is not valid."
            elif not due_day_isvalid:
                warning_massage += "This license was dued at %s." % due_day
        else:
            warning_massage += "Unable to identify this license. "

        self.warning_massage.setText(warning_massage)
        self.warning_massage.setVisible(True)

    def update_license_info(self, conf_to_update):
        print("update_license_info", conf_to_update)

        with open('./conf.txt') as f:
            code = f.readlines()[0]
            decode = base64.b64decode(code).decode("utf-8")
            conf = json.loads(decode)
            print("conf in file", conf)
            conf.update(conf_to_update)
            print("conf to file", conf)

        conf_str = json.dumps(conf)
        encode = base64.b64encode(conf_str.encode("utf-8"))
        with open("./conf.txt", "wb+") as file:
            file.write(encode)
