# -*- coding:utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class InputDialog(QDialog):
    def __init__(self, parent=None, myApp=None):
        super().__init__(parent)
        self.myApp = myApp
        self.initUI()

    def initUI(self):
        self.fgb_parameters = self._createParametersForm()
        buttonBox = QDialogButtonBox()
        buttonBox.setOrientation(Qt.Horizontal)
        buttonBox.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok | QDialogButtonBox.Apply)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

    # def _createParametersForm(self):
    #     ly =
