from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
import numpy as np, pandas as pd
import sys, os
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
from enum import Enum

_defaultLineWidth = 1.5
_highlightLineWidth = 4

class CurveType(Enum):
	NoType = 'None'
	FreqRes = 'Frequency Response'
	IMP = 'Impedance'
	Phase = 'Phase'

class CurveData:
	def __init__(self, label=None, note=None, xdata=None, ydata=None, _type=None, units=[]):
		self.label = label
		self.note = note
		self.xdata = xdata
		self.ydata = ydata
		self.type = _type
		self.units = units
		self.line = None



class MplCanvas(FigureCanvasQTAgg):
	def __init__(self, parent=None):
		# Canvas init
		self.fig, _ = plt.subplots()
		# self.fig.figsize = (12,4)
		super(MplCanvas, self).__init__(self.fig)
		self.fig.tight_layout()
		self.fig.subplots_adjust(right=0.8)

		self.axType = [CurveType.NoType, CurveType.NoType]
		self.fig.axes[0].twinx()
		self.fig.axes[1].set_visible(False)
		# self.myPlotDict = {'main': self.fig.axes[0]}
		# self.setStyle(self.ax)

	def setAxStyle(self, ax):
		# axes' style
		ax.set_xscale('log')
		ax.set_xlim([20,20000])
		ax.set_ylim(auto=True)
		ax.patch.set_alpha(0.0)
		ax.grid()
		ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
		
	def setAxesStyle(self):
		# axes' style
		for ax in self.fig.axes:
			ax.set_xscale('log')
			ax.set_xlim([20,20000])
			ax.set_ylim(auto=True)
			ax.grid()
			ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
			ax.patch.set_alpha(0.0)

	
	def set_AxType(self, axIndex, _type):
		self.axType[axIndex] = _type
	
	def get_AxType(self, axIndex):
		return self.axType[axIndex]
	
	def _replot(self):
		self.fig.axes[0].legend(bbox_to_anchor=(1.04,1), loc="upper left")
		self.draw()

class PlotGraph(QWidget):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.initUI()
		self.fileDict = {}

# User Interface
	def initUI(self):
		# create components
		self.canvas = MplCanvas(self)

		self._createTreeList()
		self._createButton()

		# manage layout
		mainLayout = QVBoxLayout()

		# 2
		grid_layout = QGridLayout()

		self.tree.setMinimumWidth(600)
		self.tree.setColumnWidth(0,300)
		self.canvas.setMinimumWidth(1000)

		grid_layout.addWidget(self.canvas, 0, 0, 1, 1)
		grid_layout.addWidget(self.tree, 0, 1, 1, 1)
		# grid_layout.addWidget(button, 1, 1, 1, 1)
		# grid_layout.addWidget(button2, 2, 1, 1, 1)
		grid_layout.setContentsMargins(10,10,10,10)
		# grid_layout.setColumnStretch(1, 10)

		mainLayout.addLayout(grid_layout)
		# 3
		hboxLayout_btn = QHBoxLayout()
		vboxlayout_data = QVBoxLayout()
		vboxlayout_data.addWidget(self.btn_importAPData)
		vboxlayout_data.addWidget(self.btn_importLEAPData)
		vboxlayout_data.addWidget(self.btn_importNFSData)
		vboxlayout_data.addWidget(self.btn_clearData)
		hboxLayout_btn.addLayout(vboxlayout_data)
		# 4
		mainLayout.addLayout(hboxLayout_btn)

		self.setLayout(mainLayout)

	def _createButton(self):
		self.btn_importAPData = QPushButton('Import AP data')
		self.btn_importLEAPData = QPushButton('Import LEAP data')
		self.btn_importNFSData = QPushButton('Import NFS data')
		self.btn_importAPData.clicked.connect(self.plotAPData)
		self.btn_importLEAPData.clicked.connect(self.plotLEAPData)
		self.btn_importNFSData.clicked.connect(self.plotKlippelData)
		self.btn_clearData = QPushButton('Clear data')
		self.btn_clearData.clicked.connect(self.clearData)

	def _createTreeList(self):
		self.tree=QTreeWidget()
		self.tree.setColumnCount(2)
		self.tree.setHeaderLabels(['Label','Note'])
		self.tree.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
		self.tree.itemChanged.connect(self.tree_handleCheck)

# Import data - data preprocessing
	def _load_LEAP_file(self):
		dialog = QFileDialog()
		dialog.setFileMode(QFileDialog.AnyFile)
		dialog.setFilter(QtCore.QDir.Files)

		if dialog.exec_():
			file_name = dialog.selectedFiles()
			path = file_name[0]
			if path.endswith('.txt'):
				with open(path, 'r', encoding='UTF-8', errors='ignore') as file:
					dataSequence = {}
					headers = file.readlines()[:11]
					title = path[path.rfind('/')+1:path.rfind('.')].strip() # LEAP_Impedance
					
					if title in dataSequence: pass
					else: dataSequence[title] = []
							
					label = headers[4][headers[4].find('=')+1:].strip()   # Impedance_PR: T201100003660

					units = headers[-1]
					units = units.strip().split(" ")
					units = [x for x in units if x][2:]     # ['Hz', 'Ohm', 'Deg']

					data = pd.read_csv(path,  skiprows=11)
					freq = pd.Series(data.iloc[:,0], name='x', dtype=float)
					val = pd.Series(data.iloc[:,1], name='y', dtype=float)
					phase = pd.Series(data.iloc[:,2], name='y', dtype=float)
					
					curveDatas = []
					note = ""

					_type = CurveType.NoType
					if ("Impedance" in title): _type = CurveType.IMP
					elif ("SPL" in title): _type = CurveType.FreqRes

					curveDatas.append(CurveData(label=label, xdata=freq, ydata=val, _type = _type))
					curveDatas.append(CurveData(label=label, xdata=freq, ydata=phase, _type = CurveType.Phase))

					dataSequence[title].extend(curveDatas)
					file.close()
					return path, dataSequence
			else:
				pass

	def _load_AP_file(self):
		dialog = QFileDialog()
		dialog.setFileMode(QFileDialog.AnyFile)
		dialog.setFilter(QtCore.QDir.Files)

		if dialog.exec_():
			file_name = dialog.selectedFiles()
			path = file_name[0]
			if path.endswith('.xlsx'):
				dataSequence = {}
				data = pd.read_excel(path, engine="openpyxl", sheet_name=None)
				# del data['Summary']
				for key, value in data.items():
					title = data[key].columns[0].strip()
					

					_type = CurveType.NoType
					if ("Phase" in title): _type = CurveType.Phase 
					elif ("Impedance" in title): _type = CurveType.IMP
					elif ("RMS" in title): _type = CurveType.FreqRes

					note = data[key].columns[1].strip()
					curveDatas = []
					isline = True
					for curveIndex in range(int(len(data[key].columns)/2)):
						label = data[key].iloc[0, curveIndex*2].strip()
						curve_x = pd.Series(data[key].iloc[3:, curveIndex*2], name='x', dtype=float)
						curve_y = pd.Series(data[key].iloc[3:, curveIndex*2+1], name='y', dtype=float)
						
						if (curve_x.dtype != float or curve_y.dtype != float): 
							isline = False
							continue
						curveDatas.append(CurveData(label=label, note=note, xdata=curve_x, ydata=curve_y, _type = _type))
					
					if (not isline): continue
					if title in dataSequence: dataSequence[title].extend(curveDatas)
					else: dataSequence[title] = curveDatas

				return path, dataSequence
			else:
				pass

	def _load_Klippel_file(self):
		dialog = QFileDialog()
		dialog.setFileMode(QFileDialog.AnyFile)
		dialog.setFilter(QtCore.QDir.Files)

		if dialog.exec_():
			file_name = dialog.selectedFiles()
			path = file_name[0]
			if path.endswith('.txt'):
				with open(path, 'r', encoding='UTF-8') as file:
					file_dir = path
					filename = path[file_dir.rfind('/')+1:file_dir.rfind('.')]         

					headers = file.readlines()[:3]
					title = headers[0].strip().strip('"')
					labels = headers[1].split('\t\t')
					labels = [c.replace('"', '').strip() for c in labels]
					dataSequence = {}	
					data = pd.read_table(path,  skiprows=2)
					data = data.dropna() 
					curveDatas = []
					note = ""
					
					freq = data.iloc[:, 0]
					freq = [float(f.replace(',', '').strip()) for f in freq]
					freq = pd.Series(freq, name='y', dtype=float)
					
					if ("Phase" in title): _type = CurveType.Phase 
					elif ("Impedance" in title): _type = CurveType.IMP
					elif ("SPL" in title or "CEA" in title): _type = CurveType.FreqRes


					for i in range(int(len(data.columns)/2)):
						spl = pd.Series(data.iloc[:, i*2+1], name='y', dtype=float)
						curveDatas.append(CurveData(label=labels[i], note=note, xdata=freq, ydata=spl, _type = _type))

					if title in dataSequence: pass
					else: dataSequence[title] = []
					dataSequence[title].extend(curveDatas)

				return path, dataSequence
			else:
				pass

	def plotAPData(self):
		filename, dataSequence = self._load_AP_file()
		self.plotData(filename, dataSequence)		
	def plotLEAPData(self):
		filename, dataSequence = self._load_LEAP_file()
		self.plotData(filename, dataSequence)
	def plotKlippelData(self):
		filename, dataSequence = self._load_Klippel_file()
		self.plotData(filename, dataSequence)
	
	def _check_and_set_AxType(self, axIndex, _type):
		if (self.canvas.get_AxType(axIndex) is CurveType.NoType or self.canvas.get_AxType(axIndex) is _type):
			self.canvas.set_AxType(axIndex, _type)
			return True
		else: return False

	def plotData(self, filename, dataSequence):
		for title, cruvesArr in dataSequence.items():
			for it in cruvesArr:
				print(it.type, self.canvas.get_AxType(0), self.canvas.get_AxType(1))
				current_ax = self.canvas.fig.axes[0]
				if (self._check_and_set_AxType(0, it.type)): pass
				else:	
					if (self._check_and_set_AxType(1, it.type)):
						current_ax = self.canvas.fig.axes[1]
						self.canvas.fig.axes[1].set_visible(True)
					else: 
						print("no ax can plot")
						continue
				line, = current_ax.plot(it.xdata, it.ydata, label=it.label)
				it.line = line

		self.fileDict[filename] = dataSequence
		self.canvas.setAxesStyle()
		self.canvas._replot()
		self.appendChildrenTree(filename, dataSequence)
		

	def get_ax(line):
		print(line.type)
	
	def appendChildrenTree(self, filename, dataSequence):
		fileroot = QTreeWidgetItem(self.tree)
		fileroot.setText(0, filename)
		for title, lines in dataSequence.items():
			root = QTreeWidgetItem()
			root.setText(0, title)
			root.setCheckState(0, 2)
			for line in lines:
				child = QTreeWidgetItem()
				child.setText(0, line.label)
				child.setText(1, line.note)
				child.setData(0, QtCore.Qt.UserRole, line)
				child.setCheckState(0, 2)
				root.addChild(child)
			fileroot.addChild(root)
		self.tree.addTopLevelItem(fileroot)
		self.tree.expandAll()

# Handle Function
	def tree_handleCheck(self, item): 
		if not item.parent(): # file root
			pass
			# title = item.text(0)
		elif(not item.data(0, QtCore.Qt.UserRole)):
			print("test root")
			for index in range(item.childCount()):
				child = item.child(index)
				child.setCheckState(0, item.checkState(0))
				curve = child.data(0, QtCore.Qt.UserRole)
				if (curve.line):
					if (item.checkState(0) == 0): 
						curve.line.set_visible(False)
						curve.line.set_label('_nolegend_')
					else: 
						curve.line.set_visible(True)
						curve.line.set_label(curve.label)
		else:
			title = item.parent().text(0)
			index = item.parent().indexOfChild(item)
			curve = item.data(0, QtCore.Qt.UserRole)
			if (curve.line):
				if (item.checkState(0) == 0): 
					curve.line.set_visible(False)
					curve.line.set_label('_nolegend_')
				else: 
					curve.line.set_visible(True)
					curve.line.set_label(curve.label)
		self.canvas._replot()

	

# Clear data
	def clearData(self):
		print('clearData')

		
class MyApp(QMainWindow):
	"""App's Main Window."""
	def __init__(self, parent=None):
		"""Initializer."""
		super().__init__(parent)
		self.initUI()

	def initUI(self):  
		self.setWindowTitle("Python Menus & Toolbars")
		# self.resize(1600, 800)
		self.setCentralWidget(PlotGraph())

def main():
	app = QApplication(sys.argv)
	main = MyApp()
	main.show()
	sys.exit(app.exec_())

if __name__ == '__main__':
		main()

