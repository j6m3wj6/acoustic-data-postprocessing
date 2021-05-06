import sys, os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from UI_Dialog import *


class Main(QWidget):
    def __init__(self):       
        super(Main,self).__init__()
        self.initUi()

    def initUi(self):
        self.setWindowTitle("项目信息")
        self.setGeometry(400,400,300,260)

        label1=QLabel("项目名称:")


        self.nameLable = QLabel("PyQt5")

        nameButton=QPushButton("...")
        nameButton.clicked.connect(self.onDialogBtnClicked)
 

    # layout
        mainLayout=QGridLayout()
        mainLayout.addWidget(label1,0,0)
        mainLayout.addWidget(self.nameLable,0,1)
        mainLayout.addWidget(nameButton,0,2)

        self.setLayout(mainLayout)


    def selectName(self):
        name,ok = QInputDialog.getText(self,"项目名称","输入项目名称:",
                                       QLineEdit.Normal,self.nameLable.text())
        if ok and (len(name)!=0):
            self.nameLable.setText(name)

    def onDialogBtnClicked(self):
        """Launch the employee dialog."""
        
        dlg = OperationDialog(self)
        dlg.exec()
        print('dlg', dlg.ui.textEdit.toPlainText())


class OperationDialog(QDialog):
    """Employee dialog."""
    def __init__(self, parent=None):
        super().__init__(parent)
        # Create an instance of the GUI
        self.ui = Ui_Dialog()
        # Run the .setupUi() method to show the GUI
        self.ui.setupUi(self)

if __name__=="__main__":
    app = QApplication(sys.argv)
    myshow = Main()
    myshow.show()
    sys.exit(app.exec_())
