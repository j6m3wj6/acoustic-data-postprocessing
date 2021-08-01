from PyQt5.QtWidgets import QLineEdit, QPushButton, QLabel, QDialog, \
    QVBoxLayout, QHBoxLayout, QFormLayout
from PyQt5.QtCore import Qt
from .functions import verify_license, add_months
import datetime as dt
import json
import base64


class Dlg_License(QDialog):
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
