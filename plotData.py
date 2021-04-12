from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import (QApplication, QWidget, QFileDialog, QTextEdit, QPushButton, QLabel, QVBoxLayout, QTreeWidget, QTreeWidgetItem)
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os
import numpy as np
import pandas as pd

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        # fig.canvas.mpl_connect('button_press_event', onclick)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class PlotGraph(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.resize(800, 600)
        self.button1 = QPushButton('Upload data')
        self.button1.clicked.connect(self.plotData)
        self.sc = MplCanvas(self, width=5, height=4, dpi=100)
        toolbar = NavigationToolbar(self.sc, self)

        self.tree=QTreeWidget()
        #设置列数
        self.tree.setColumnCount(2)
        #设置树形控件头部的标题
        self.tree.setHeaderLabels(['Key','Value'])
        #设置树形控件的列的宽度
        self.tree.setColumnWidth(0,150)
        #加载根节点的所有属性与子控件
        self.tree.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        
        self.tree.itemClicked.connect(self.printItemText)

        #节点全部展开
        self.tree.expandAll()

        layout = QVBoxLayout()
        layout.addWidget(self.button1)
        layout.addWidget(toolbar)
        layout.addWidget(self.sc)
        layout.addWidget(self.tree)

        self.setLayout(layout)

    def printItemText(self):
      items = self.tree.selectedItems()
      x = []
      for i in range(len(items)):
          x.append(str(self.tree.selectedItems()[i].parent().text(0) + self.tree.selectedItems()[i].text(0)))
      print (x)
      self.refreshData([1,2,3])

    def appendChildonTree(self):
      root=QTreeWidgetItem(self.tree)
      root.setText(0,'Curve')
      for i in range(len(self.data.columns)):
        child=QTreeWidgetItem()
        child.setText(0,self.data.columns[i])
        root.addChild(child)
      self.tree.addTopLevelItem(root)

    def plot(self, x, y, plotname, color):
      pen = pg.mkPen(color=color)
      self.graphWidget.plot(x, y, name=plotname, pen=pen, symbol='+', symbolSize=30, symbolBrush=(color))

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

    def plotData(self):
      self.data = self.get_text_file()
      print(self.data)
      self.data.plot("Frequency", ax = self.sc.axes)
      self.sc.draw()
      self.appendChildonTree()

    def refreshData(self, selectedData):
      self.data.plot("Frequency", ax = self.sc.axes, y=selectedData)
      print(selectedData)

      self.sc.draw()

def onclick(event):
    print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          ('double' if event.dblclick else 'single', event.button,
           event.x, event.y, event.xdata, event.ydata))
    
def main():
    app = QApplication(sys.argv)
    main = PlotGraph()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

