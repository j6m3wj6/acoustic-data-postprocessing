from lib.dockwg_data_treelist import *
from lib.dlg_operation import *
from lib.dlg_import_files import *
from lib.dlg_load_files import *
from lib.wg_treelist import *
from lib.wg_canvas import *
from lib.dockwg_canvas_layout import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import matplotlib
import datetime as dt
import sys
matplotlib.use('Qt5Agg')


class MyApp(QMainWindow):
    """App's Main Window."""

    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.initUI()
        self.project_info = {
            "Name": "myproject",
            "File Path": sys.path[0],
            'Import Time': dt.datetime.today().strftime("%Y/%m/%d %H:%M:%S"),
            'Last Modified Time': dt.datetime.today().strftime("%Y/%m/%d %H:%M:%S"),
            'Files': []
        }
        self.files = []

    def initUI(self):
        self.setWindowTitle("Python Menus & Toolbars")
        self.resize(1600, 800)

        MainWidget = QWidget()
        MainLayout = QVBoxLayout()
        # ===========

        self._createButton()

        self.wg_canvas = MyCanvas(self)
        self.dwg_data = DockWidget_Data(self, Qt.RightDockWidgetArea)
        self.dwg_canvasLayout = DockWidget_CanvasLayout(
            self, Qt.LeftDockWidgetArea)
        self.dwg_canvasLayout._setCanvasLayout_Main(self.wg_canvas)

        MainLayout.addWidget(self.wg_canvas)

        MainWidget.setLayout(MainLayout)
        self.setCentralWidget(MainWidget)
        # MainLayout.setContentsMargins(0, 0, 0, 0)
        # self.setContentsMargins(0, 0, 0, 0)


# Create Components


    def _createButton(self):
        self.btn_clearData = QPushButton('Clear data')
        self.btn_clearData.clicked.connect(self.clearData)

        self.btn_operationDialog = QPushButton('Operation')
        self.btn_operationDialog.clicked.connect(self.operationDialog)

# Btn Func - Clear data
    def clearData(self):
        for c in self.canvasPool:
            for ax in c.fig.axes:
                ax.lines = []
            c.replot()
        self.myTree.clear()

# Btn Func - Shift Data
    def operationDialog(self):
        dlg = OperationDialog(myApp=self)
        dlg.exec()
        # self.canvasReplot()

    def importDialog(self):
        dlg = ImportDialog(myApp=self)
        dlg.exec()


# Canves Pool Func

    def canvasReplot(self):
        for c in self.wg_canvas.canvasPool:
            if (c.active):
                c.replot()

    def getRightAx(self, _type):
        ax = None
        if (_type != CurveType.NoType):
            for c in self.wg_canvas.canvasPool:
                ax_match = c.getAxbyType(_type)
                if (ax_match):
                    ax = ax_match
        return ax

    def dumps(self, file_josn):
        self.project_info["Files"].append(file_josn)
        with open('project.json', 'w') as json_file:
            json.dump(self.project_info, json_file)


def main():
    app = QApplication(sys.argv)
    main = MyApp()

    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
