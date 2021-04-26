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

_defaultLineWidth = 1.5
_highlightLineWidth = 4


class MplCanvas(FigureCanvasQTAgg):
  def __init__(self, parent=None):
    # Canvas init
    self.fig, _ = plt.subplots()
    self.fig.figsize=(12,4)
    super(MplCanvas, self).__init__(self.fig)
    self.fig.tight_layout()
    self.fig.subplots_adjust(right=0.8)
    self.myPlotDict = {'main': self.fig.axes[0]}
    self.setStyle(self.myPlotDict['main'])

    self.h_line = self.myPlotDict['main'].axhline(y=70, color='k', lw=0.8, ls='--', picker=5, visible=False)
    self.v_line = self.myPlotDict['main'].axvline(x=1000, color='k', lw=0.8, ls='--', picker=5, visible=False)
    self.text = self.myPlotDict['main'].text(0.72, 0.9, '', transform=self.myPlotDict['main'].transAxes)
    self.mpl_connect('pick_event', self.clickonline)
  
  def setStyle(self, ax):
    # axes' style
    ax.set_xscale('log')
    ax.set_xlim([20,20000])
    ax.set_ylim(auto=True)
    ax.patch.set_alpha(0.0)
    ax.grid()
    ax.grid(which='minor', linestyle=':', linewidth='0.5', color='black')
  
  def updata_ylim(self, ylim):
    ylim = list(ylim)
    main_ylim = list(self.myPlotDict['main'].get_ylim())
    if (main_ylim[0] > ylim[0]): main_ylim[0] = ylim[0]
    if (main_ylim[1] < ylim[1]): main_ylim[1] = ylim[1]
    for title, ax in self.myPlotDict.items():
      ax.set_ylim(main_ylim)
    # self.myPlotDict['main'].set_ylim(main_ylim)
    return main_ylim

  def set_cross_hair_visible(self, visible):
    need_redraw = self.h_line.get_visible() != visible
    self.h_line.set_visible(visible)
    self.v_line.set_visible(visible)
    self.text.set_visible(visible)

    return need_redraw

  def clickonline(self, event):
    print('clickonline', event, event.artist)
    if event.artist == self.h_line or event.artist == self.v_line:
      print("line selected ", event.artist)
      self.follower = self.mpl_connect("motion_notify_event", lambda event: self.followmouse(event, 'h'))
      self.releaser = self.mpl_connect("button_press_event", lambda event: self.releaseonclick(event, 'h'))
  
  def followmouse(self, event, artist):
    # print('followmouse', artist)
    if artist == 'h':
      self.h_line.set_ydata([event.ydata, event.ydata])
    else:
      self.v_line.set_xdata([event.xdata, event.xdata])
    self.draw_idle()

  def releaseonclick(self, event, artist):
    print('releaseonclick', artist)
    # if artist == 'h':
    #   self.XorY = self.h_line.get_ydata()[0]
    # else:
    #   self.XorY = self.v_line.get_xdata()[0]
    # print (self.XorY)
    self.mpl_disconnect(lambda event: self.followmouse(event, 'h'))
    self.mpl_disconnect(self.releaser)


class MyToolBar(NavigationToolbar2QT):
  def __init__(self, canvas_, parent_):
    NavigationToolbar2QT.__init__(self, canvas_, parent_)

    self.toolitems.append(('Cursor', 'Select', "select", 'cursor'))
    # print(self.toolitems)

    a = self.addAction(self._icon('Select' + '.png'),
                'Cursor', getattr(self, 'cursor'))
    if ('cursor' in self._actions.keys()): pass
    else:
      self._actions['cursor'] = a
      a.setCheckable(True)
      a.setToolTip('Select')
    self.cursor = a

  def cursor(self):
    
    self.canvas.set_cross_hair_visible(self.cursor.isChecked())
    self.canvas.draw()

    # x = []
    # for title, ax in self.canvas.myPlotDict.items():
    #   for line in ax.lines:
    #     if (line.get_linewidth() == _highlightLineWidth):
    #       x.append(line.get_label())
    # print(x)


class PlotGraph(QWidget):
  """Widget for visualize data"""
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.initUI()
    self.dataDict = {}
    self.data = pd.DataFrame()

# User Interface
  def initUI(self):
    # create components
    self._createCanvas()
    # self.canvas.fig.canvas.mpl_connect('motion_notify_event', self.on_mouse_move)

    self._createTreeList()
    self._createButton()

    # manage layout
    mainLayout = QVBoxLayout()
    # 1
    mainLayout.addWidget(self.toolbar)
    # 2
    hboxLayout_canvas = QHBoxLayout()
    hboxLayout_canvas.addWidget(self.canvas)
    
    hboxLayout_canvas.addWidget(self.tree)
    mainLayout.addLayout(hboxLayout_canvas)
    # 3
    hboxLayout_btn = QHBoxLayout()
    vboxlayout_data = QVBoxLayout()
    vboxlayout_data.addWidget(self.btn_importAPData)
    vboxlayout_data.addWidget(self.btn_importLEAPData)
    vboxlayout_data.addWidget(self.btn_clearData)
    hboxLayout_btn.addLayout(vboxlayout_data)
    # 4
    mainLayout.addLayout(hboxLayout_btn)

    self.setLayout(mainLayout)

  def _createCanvas(self):
    self.canvas = MplCanvas(self)
    self.toolbar = MyToolBar(self.canvas, self)
    self.canvas.mpl_connect('button_press_event', self.canvas_handleClick)

  def _createButton(self):
    self.btn_importAPData = QPushButton('Import AP data')
    self.btn_importLEAPData = QPushButton('Import LEAP data')
    self.btn_importAPData.clicked.connect(self.plotAPData)
    self.btn_importLEAPData.clicked.connect(self.plotLEAPData)
    self.btn_clearData = QPushButton('Clear data')
    self.btn_clearData.clicked.connect(self.clearData)

  def _createTreeList(self):
    self.tree=QTreeWidget()
    self.tree.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)

    self.tree.setColumnCount(2)
    self.tree.setHeaderLabels(['Key','Value'])
    self.tree.setColumnWidth(0,300)
    self.tree.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
    self.tree.itemClicked.connect(self.tree_handleSelect)
    # self.tree.itemSelectionChanged.connect(self.tree_handleSelect)
    self.tree.itemChanged.connect(self.tree_handleCheck)

# Reset Functions
  def _resetLineWidth(self):
    for title, ax in self.canvas.myPlotDict.items():
      for line in ax.lines:
        line.set_linewidth(_defaultLineWidth)
    self.canvas.draw()   

# Tree Functions
  def _switchCheckStatusWithFigure(self, title, index, originStatus, legendName):
    if (originStatus == 0):
      self.canvas.myPlotDict[title].lines[index].set_visible(False)
      self.canvas.myPlotDict[title].lines[index].set_label('_nolegend_')
    else: 
      self.canvas.myPlotDict[title].lines[index].set_visible(True)
      self.canvas.myPlotDict[title].lines[index].set_label(legendName)

  def tree_handleCheck(self, item): 
    if not item.parent(): 
      pass
      title = item.text(0)
      for index in range(item.childCount()):
        child = item.child(index)
        if (item.checkState(0) == 0): child.setCheckState(0, QtCore.Qt.Unchecked)
        else: child.setCheckState(0, QtCore.Qt.Checked)
        self._switchCheckStatusWithFigure(title, index, child.checkState(0), child.text(0))
    else:
      title = item.parent().text(0)
      index = item.parent().indexOfChild(item)
      self._switchCheckStatusWithFigure(title, index, item.checkState(0), item.text(0))

    self._replot()

  def tree_handleSelect(self):
    if not self.tree.currentItem(): return

    self._resetLineWidth()
    for item in self.tree.selectedItems():
      if not item.parent():
        pass
      else:
        title = item.parent().text(0)
        index = item.parent().indexOfChild(item)
        print(title, index)
        self.canvas.myPlotDict[title].lines[index].set_linewidth(_highlightLineWidth)
    self.canvas.draw()

# Canvas Functions
  def canvas_handleClick(self, event):
    print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
        ('double' if event.dblclick else 'single', event.button,
        event.x, event.y, event.xdata, event.ydata))
    if not self.dataDict or not event.inaxes or self.toolbar.cursor.isChecked(): return
    title, line_i = self._pickLine(event.xdata, event.ydata)
    if (line_i == -1):
      self._resetLineWidth()
    elif (event.button == MouseButton.RIGHT and\
          self.canvas.myPlotDict[title].lines[line_i].get_linewidth() == 4):
      self.canvas.myPlotDict[title].lines[line_i].set_linewidth(_defaultLineWidth)
    else:
      self.canvas.myPlotDict[title].lines[line_i].set_linewidth(_highlightLineWidth)
    self.canvas.draw()

  def _pickLine(self, cursor_x, cursor_y):
    error = float('inf')
    title = ''
    for _t, data in self.dataDict.items():
      min_i = 0
      max_i = len(data['Frequency'])    
      while (max_i - min_i > 1):
        middle_i = int((max_i - min_i)/2) + min_i
        if (cursor_x > float(data['Frequency'][middle_i])):
          min_i = middle_i
        else:
          max_i = middle_i
      if (cursor_x - data['Frequency'][min_i] > data['Frequency'][max_i] - cursor_x):
        freq_i = max_i
      else:
        freq_i = min_i

      for i in range(1, len(data.iloc[freq_i])):
        # print(float(data.iloc[freq_i][i]), error)
        if (abs(cursor_y - float(data.iloc[freq_i][i])) < error):
          error = abs(cursor_y - float(data.iloc[freq_i][i]))
          line_i = i
          title = _t
      # print(line_i)
    if (error > 1): return '', -1
    return title, (line_i-1)
  
  # def _trackYdata(self, cursor_x, cursor_y, line_index):
    # left_x = 0
    # right_x = len(self.data['Frequency'])
    # while (right_x - left_x > 1):
    #   middle_freq = int((right_x - left_x)/2) + left_x
    #   if (cursor_x > float(self.data['Frequency'][middle_freq])):
    #     left_x = middle_freq
    #   else:
    #     right_x = middle_freq
    # left_freq = self.data['Frequency'][left_x]
    # right_freq = self.data['Frequency'][right_x]
    # left_ydata = self.data.iloc[left_x][line_index]
    # right_ydata = self.data.iloc[right_x][line_index]

    # estimate_ydata = left_ydata + ((cursor_x - left_freq) / (right_freq - left_freq))*(right_ydata - left_ydata)
    # return estimate_ydata

  def on_mouse_move(self, event):
    if not event.inaxes: return
    else:
      visible = self.toolbar.cursor.isChecked()
      self.canvas.set_cross_hair_visible(visible)
      x = event.xdata
      # y = self._trackYdata(event.xdata, event.ydata, 0)
      y = event.ydata

      self.canvas.h_line.set_ydata(y)
      self.canvas.v_line.set_xdata(x)
      self.canvas.text.set_text('x=%1.2f, y=%1.2f' % (x, y))
      self.canvas.draw()

# Import data - data preprocessing
  def _get_LEAP_text_file(self):
    dialog = QFileDialog()
    dialog.setFileMode(QFileDialog.AnyFile)
    dialog.setFilter(QtCore.QDir.Files)

    if dialog.exec_():
      file_name = dialog.selectedFiles()
      file_dir = file_name[0]
      if file_dir.endswith('.txt'):
        with open(file_dir, 'r', encoding='UTF-8', errors='ignore') as file:
          headers = file.readlines()[:11]
          title = file_dir[file_dir.rfind('/')+1:file_dir.rfind('.')]
          curve = headers[4]
          curve = curve[curve.find('=')+1:curve.find(':')]

          cols = headers[-1]
          cols = cols.strip().split(" ")
          cols = [x for x in cols if x][2:-1]
          
          cols[0] = 'Frequency'
          cols[1] = curve

          data = pd.read_csv(file_dir,  skiprows=11)
          data = data.iloc[:, :-1]

          data.columns = cols

          file.close()
          return title, data
      else:
        pass
  def _get_AP_text_file(self):
    dialog = QFileDialog()
    dialog.setFileMode(QFileDialog.AnyFile)
    dialog.setFilter(QtCore.QDir.Files)

    if dialog.exec_():
      file_name = dialog.selectedFiles()
      with open(file_name[0], 'r', encoding='UTF-8', errors='ignore') as file:
        file_dir = file_name[0]
        self.filename = file_name[0][file_dir.rfind('/')+1:file_dir.rfind('.')]         
        
        print(file_dir)
        headers = file.readlines()[:4]
        self.title = headers[0]

        cols = headers[1]
        cols = cols.strip().split(",")
        cols = [x for x in cols if x]

        cols.insert(0, 'Frequency')
        data = pd.read_csv(file_name[0],  skiprows=4)
        data = data.dropna()
        data = data.iloc[:, [i%2==1 or i==0 for i in range(len(data.columns))]]
        data = data.transform(pd.to_numeric, errors='coerce')
        data.columns = cols
        for col in data.columns:
          data[col] = data[col].transform(pd.to_numeric, errors='coerce').round(decimals=2)
        title = headers[0]
        title = title[:title.find(',')].strip('""')
        
        file.close()
        return title, data
# Import data - plot initialize
  def appendChildrenTree(self, title):
    root=QTreeWidgetItem(self.tree)
    root.setText(0, title)
    root.setCheckState(0, 2)
    for col in self.dataDict[title].columns[1:]:
      child = QTreeWidgetItem()
      child.setText(0, col)
      child.setCheckState(0, 2)
      root.addChild(child)
    self.tree.addTopLevelItem(root)
    self.tree.expandAll()

  def _checkAxExist(self, title):
    if title in self.canvas.myPlotDict.keys(): return
    else:
      self.canvas.fig.add_subplot(111)
      self.canvas.myPlotDict[title] = self.canvas.fig.axes[len(self.canvas.fig.axes)-1]
      self.canvas.setStyle(self.canvas.myPlotDict[title])
      return

  def plotAPData(self):
    title, data = self._get_AP_text_file()
    self.dataDict[title] = data
    self._checkAxExist(title)

    for col in data.columns[1:]:
      self.canvas.myPlotDict[title].plot(data['Frequency'], data[col], label=col) # marker='o'

    self.canvas.updata_ylim(self.canvas.myPlotDict[title].get_ylim())
    self._replot()    
    self.appendChildrenTree(title)

  def plotLEAPData(self):
    title, data = self._get_LEAP_text_file()
    self.dataDict[title] = data

    self._checkAxExist(title)

    for col in data.columns[1:]:
      self.canvas.myPlotDict[title].plot(data['Frequency'], data[col], label=col) # marker='o'
    
    self.canvas.updata_ylim(self.canvas.myPlotDict[title].get_ylim())
    self._replot()
    self.appendChildrenTree(title)


  def _replot(self):
    lines = []
    labels = []
    for key in self.canvas.myPlotDict.keys():
        ax = self.canvas.myPlotDict[key]
        axLine, axLabel = ax.get_legend_handles_labels()
        lines.extend(axLine)
        labels.extend(axLabel)
    # print(lines, labels)
    self.canvas.fig.legends = []
    self.canvas.fig.legend(lines, labels, bbox_to_anchor=(0.95,0.95), loc="upper right")
    self.canvas.draw()


# Clear data
  def clearData(self):
    for ax in self.canvas.myPlotDict:
      ax.lines = []

    self._replot()
    self.tree.clear()

    
class MyApp(QMainWindow):
  """App's Main Window."""
  def __init__(self, parent=None):
    """Initializer."""
    super().__init__(parent)
    self.initUI()

  def initUI(self):  
    self.setWindowTitle("Python Menus & Toolbars")
    self.resize(1600, 800)
    self.setCentralWidget(PlotGraph())

def main():
  app = QApplication(sys.argv)
  main = MyApp()
  main.show()
  sys.exit(app.exec_())

if __name__ == '__main__':
    main()

