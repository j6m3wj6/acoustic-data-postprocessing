from PyQt5 import QtCore
from PyQt5.QtWidgets import *
import sys, os, numpy as np, pandas as pd
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class MplCanvas(FigureCanvasQTAgg):
  def __init__(self, parent=None):
    # Canvas init
    self.fig = Figure() # figsize=(6,6)
    # fig.canvas.mpl_connect('button_press_event', self.onclick)
    self.ax = self.fig.add_subplot(111)
    # self._setStyle()
    super(MplCanvas, self).__init__(self.fig)

#   def _setStyle(self):
    # axes' style
    # self.ax.set_xscale('log')
    # self.ax.set_xlim([20,20000])
    # self.ax.set_ylim(auto=True)
    # self.ax.grid()
    # self.ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
    # self.fig.tight_layout()
    # self.fig.subplots_adjust(right=0.75)

class MyApp(QWidget):
    """Widget for visualize data"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()
        self.ydata = pd.DataFrame()

        with open('bose.txt', 'r', encoding='UTF-8') as file:
            headers = file.readlines()[:3]
            self.filename = 'bose'
            self.title = headers[0]
            curves = headers[1].split('\t\t')
            curves = [c.replace('"', '').strip() for c in curves]
            
            data = pd.read_table('bose.txt',  skiprows=2)
            freq = data.iloc[:, 0]
            self.xdata_freq = [float(f.replace(',', '').strip()) for f in freq]
            self.ydata = data.iloc[:, [i%2==1 for i in range(len(data.columns))]]
            self.ydata.columns = curves
            
            file.close()

# User Interface
    def initUI(self):
        self.canvas = MplCanvas(self)
        self.btn_importData = QPushButton('Import data')
        self.btn_importData.clicked.connect(self.plotData)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.btn_importData)

        self.setLayout(layout)


    def plotData(self):
        for col in self.ydata.columns:
            self.canvas.ax.plot(self.xdata_freq, self.ydata[col], label=col)

        self.canvas.ax.legend(bbox_to_anchor=(1.04,1), loc="upper left")
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MyApp()
    main.show()
    sys.exit(app.exec_())

