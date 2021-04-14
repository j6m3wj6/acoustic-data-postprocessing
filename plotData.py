from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
import numpy as np, pandas as pd
import sys, os
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
import mplcursors

_defaultLineWidth = 2

class MplCanvas(FigureCanvasQTAgg):
  def __init__(self, parent=None):
    # Canvas init
    self.fig = Figure()
    # fig.canvas.mpl_connect('button_press_event', self.onclick)
    self.ax = self.fig.add_subplot(111)
    self._setStyle()
    super(MplCanvas, self).__init__(self.fig)

  def _setStyle(self):
    # axes' style
    self.ax.set_xscale('log')
    self.ax.set_xlim([20,20000])
    self.ax.set_ylim(auto=True)
    self.ax.grid()
    self.ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')

class PlotGraph(QWidget):
  """Widget for visualize data"""
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.initUI()
    self.data = pd.DataFrame()
# User Interface
  def initUI(self):
    self._createButton()
    self._createCanvas()
    self.canvas.fig.canvas.mpl_connect('button_press_event', self.canvas_handleClick)
    self._createTreeList()
    self._createComboBox()
    self._createInput()

    layout = QVBoxLayout()
    layout.addWidget(self.toolbar)

    hboxLayout_canvas = QHBoxLayout()
    # hboxLayout.addStretch()
    hboxLayout_canvas.addWidget(self.canvas)
    hboxLayout_canvas.addWidget(self.tree)
    layout.addLayout(hboxLayout_canvas)

    hboxLayout_btn = QHBoxLayout()
    # hboxLayout.addStretch()
    hboxLayout_btn.addWidget(self.btn_importData)
    hboxLayout_btn.addWidget(self.btn_shift)
    hboxLayout_btn.addWidget(self.cbox_shift)
    hboxLayout_btn.addWidget(self.le_input)
    layout.addLayout(hboxLayout_btn)

    self.setLayout(layout)
  
  def _createButton(self):
    self.btn_importData = QPushButton('Upload data')
    self.btn_importData.clicked.connect(self.plotData)
    self.btn_shift = QPushButton('Shift')
    self.btn_shift.clicked.connect(self.curveShift)

  def _createCanvas(self):
    self.canvas = MplCanvas(self)
    self.toolbar = NavigationToolbar(self.canvas, self)

  def _createTreeList(self):
    self.tree=QTreeWidget()
    self.tree.setColumnCount(2)
    self.tree.setHeaderLabels(['Key','Value'])
    self.tree.setColumnWidth(0,300)
    self.tree.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
    self.tree.itemClicked.connect(self.tree_handleClick)
    self.tree.itemChanged.connect(self.tree_handleChange)

  def _createComboBox(self):
    self.cbox_shift = QComboBox()
    self.cbox_shift.currentIndexChanged.connect(self.cbox_handleChange)
    # self.display()
  
  def _createInput(self):
    self.le_input = QLineEdit()
    

# Reset Functions
  def _resetLineWidth(self):
    for line in self.canvas.ax.lines:
      line.set_linewidth(_defaultLineWidth)

# Handle Functions
  def tree_handleChange(self, item): 
    print("Change")
    # index = self.tree.currentIndex().row()
    if not item.parent(): return
    index = item.parent().indexOfChild(item)
    print(item.text(0), index, item.checkState(0))
    if (item.checkState(0) == 0):
      self.canvas.ax.lines[index].set_visible(False)
    else: self.canvas.ax.lines[index].set_visible(True)
    self.canvas.draw()
    # if not item.parent():
    #   print("Change ", item.text(0), "　and it is a root")
    # else:
    #   print("Change ", item.text(0), "　and its root is " , item.parent().text(0))
    
  def tree_handleClick(self):
    print("Click")
    items = self.tree.selectedItems()
    x = []
    for i in range(len(items)):
      if not items[i].parent():
        x.append(items[i].text(0))
      else:
        x.append(str(items[i].parent().text(0) + ' - ' + items[i].text(0)))
    index = self.tree.currentIndex().row()
    self._resetLineWidth()
    if (index != -1):
      self.canvas.ax.lines[index].set_linewidth(4)
      self.canvas.draw()

  def canvas_handleClick(self, event):
    # print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
    #     ('double' if event.dblclick else 'single', event.button,
    #     event.x, event.y, event.xdata, event.ydata))
    if self.data.empty or not event.inaxes: return

    line_i = self._findSelectedLine(event.xdata, event.ydata)
    if (line_i == -1):
      self._resetLineWidth()
    else:
      self.canvas.ax.lines[line_i].set_linewidth(4)
      self.canvas.draw()

  def _findSelectedLine(self, cursor_x, cursor_y):
    min_i = 0
    max_i = len(self.data["Frequency"])    
    while (max_i - min_i > 1):
      middle_i = int((max_i - min_i)/2) + min_i
      if (cursor_x > float(self.data['Frequency'][middle_i])):
        min_i = middle_i
      else:
        max_i = middle_i
    if (cursor_x - self.data['Frequency'][min_i] > self.data['Frequency'][max_i] - cursor_x):
      freq_i = max_i
    else:
      freq_i = min_i
    
    error = float('inf')
    for i in range(len(self.data.iloc[freq_i])):
      # print(abs(cursor_y - float(self.data.iloc[freq_i][i])), error)
      if (abs(cursor_y - float(self.data.iloc[freq_i][i])) < error):
        error = abs(cursor_y - float(self.data.iloc[freq_i][i]))
        line_i = i
    # print(line_i)
    if (error > 1): return -1
    return line_i

  def cbox_handleChange(self):
    print(self.cbox_shift.currentText())
    

# Import data
  def appendChildonTree(self):
    root=QTreeWidgetItem(self.tree)
    root.setText(0,'Curve')
    root.setCheckState(0, 2)
    for i in range(len(self.data.columns[:-1])):
      child = QTreeWidgetItem()
      child.setText(0,self.data.columns[i])
      child.setCheckState(0, 2)
      root.addChild(child)
    self.tree.addTopLevelItem(root)
    self.tree.expandAll()

    self.cbox_shift.addItems(self.data.columns)

  def get_text_file(self):
    dialog = QFileDialog()
    dialog.setFileMode(QFileDialog.AnyFile)
    dialog.setFilter(QtCore.QDir.Files)

    if dialog.exec_():
      file_name = dialog.selectedFiles()

      if file_name[0].endswith('.txt'):
        with open(file_name[0], 'r', encoding='UTF-8') as file:
          
          headers = file.readlines()[:3]
          print(headers[0])
          title = headers[0]
          curves = headers[1].split('\t\t')
          curves = [c.replace('"', '').strip() for c in curves]
          
          dtbl = pd.read_table(file_name[0],  skiprows=2)
          freq = dtbl.iloc[:, 0]
          freq = [float(f.replace(',', '').strip()) for f in freq]
          dtbl = dtbl.iloc[:, [i%2==1 for i in range(len(dtbl.columns))]]
          dtbl.columns = curves
          
          dtbl['Frequency'] = freq
          file.close()
          return dtbl
      else:
        pass
  
  def get_bose(self):
    with open('bose.txt', 'r', encoding='UTF-8') as file:
      headers = file.readlines()[:3]
      print(headers[0])
      title = headers[0]
      curves = headers[1].split('\t\t')
      curves = [c.replace('"', '').strip() for c in curves]
      
      dtbl = pd.read_table('bose.txt',  skiprows=2)
      freq = dtbl.iloc[:, 0]
      freq = [float(f.replace(',', '').strip()) for f in freq]
      dtbl = dtbl.iloc[:, [i%2==1 for i in range(len(dtbl.columns))]]
      dtbl.columns = curves
      
      dtbl['Frequency'] = freq
      file.close()
    return dtbl
  def plotData(self):
    # self.data = self.get_text_file()
    self.data = self.get_bose()
    print(self.data)

    for col in self.data.columns[:-1]:
      line, = self.canvas.ax.plot(self.data["Frequency"], self.data[col], label=col)
      # self.canvas.lines.append(line)
    # mplcursors.cursor(self.canvas.ax.lines, highlight=True, highlight_kwargs=dict(linewidth=5))
    self.canvas.ax.legend(loc='lower left')
    # self.data.plot("Frequency", ax = self.canvas.ax)
    self.canvas.draw()
    self.appendChildonTree()

# Operations
  def curveShift(self):
    print("Shift", self.cbox_shift.currentText(), self.le_input.text())
    try:
      offset = float(self.le_input.text())
    except ValueError:
      print('ERROR: can not turn ' + self.le_input.text())
      return
    new_data = [d+offset for d in self.data[self.cbox_shift.currentText()]]
    # also change origin data
    # self.data[self.cbox_shift.currentText()] = new_data
    
    self.canvas.ax.lines[self.cbox_shift.currentIndex()].set_data(self.data["Frequency"], new_data)
    self.canvas.draw()
    
class MyApp(QMainWindow):
  """App's Main Window."""
  def __init__(self, parent=None):
    """Initializer."""
    super().__init__(parent)
    self.initUI()

  def initUI(self):  
    self.setWindowTitle("Python Menus & Toolbars")
    self.resize(1400, 600)
    self.setCentralWidget(PlotGraph())
    self._createMenuBar()

  def _createMenuBar(self):
    menuBar = QMenuBar(self)
    # Creating menus using a QMenu object
    fileMenu = QMenu("&File", self)
    menuBar.addMenu(fileMenu)
    # Creating menus using a title
    editMenu = menuBar.addMenu("&Edit")
    helpMenu = menuBar.addMenu("&Help")
    self.setMenuBar(menuBar)

def main():
  app = QApplication(sys.argv)
  main = MyApp()
  main.show()
  sys.exit(app.exec_())

if __name__ == '__main__':
    main()

