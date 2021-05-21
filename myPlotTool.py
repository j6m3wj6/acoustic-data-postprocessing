from DockWidget_CanvasLayout import DockWidget_CanvasLayout
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import matplotlib, random
matplotlib.use('Qt5Agg')
from matplotlib.lines import Line2D
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib.backend_bases import MouseButton

# Self-defined module
from Canvas import *
from TreeList import *
from LoadFile import *
from OperationDialog import *
from ImportDialog import *
from DockWidget_Data import *


class MyApp(QMainWindow):
	"""App's Main Window."""
	def __init__(self, parent=None):
		"""Initializer."""
		super().__init__(parent)
		self.initUI()

	def initUI(self):  
		self.setWindowTitle("Python Menus & Toolbars")
		self.resize(1600, 800)
		
		MainWidget = QWidget()
		MainLayout = QVBoxLayout()
		#===========

		self._createButton()
		self.myTree = MyTree(self)
	
		self.wg_canvas = Canvas_Widget(self)
		self.dwg_data = DockWidget_Data(self, Qt.RightDockWidgetArea)
		self.dwg_canvasLayout = DockWidget_CanvasLayout(self, Qt.LeftDockWidgetArea)
		self.dwg_canvasLayout._setCanvasLayout_Main(self.wg_canvas)
		

		MainLayout.addWidget(self.wg_canvas)

		MainWidget.setLayout(MainLayout)
		self.setCentralWidget(MainWidget)
		MainLayout.setContentsMargins(0,0,0,0)
		self.setContentsMargins(0,0,0,0)

	
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
		dlg = OperationDialog(myApp = self)
		dlg.exec()
		# self.canvasReplot()
	def importDialog(self):
		dlg = ImportDialog(myApp = self)
		dlg.exec()

# Canves Pool Func
	def canvasReplot(self):
		for c in self.wg_canvas.canvasPool:
			if (c.active): c.replot()

	def getRightAx(self, _type):
		ax = None
		if (_type != CurveType.NoType):
			for c in self.wg_canvas.canvasPool:
				ax_match = c.getAxbyType(_type)
				if (ax_match): ax = ax_match
		return ax

def main():
	app = QApplication(sys.argv)
	main = MyApp()

	main.show()
	sys.exit(app.exec_())
if __name__ == '__main__':
		main()

