from matplotlib.backend_bases import MouseButton
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
import numpy as np
import pandas as pd
import sys
import matplotlib
matplotlib.use('Qt5Agg')

_defaultLineWidth = 1.5
_highlightLineWidth = 4


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None):
        # Canvas init
        self.fig = Figure(figsize=(12, 4))  # figsize=(6,6)
        self.ax = self.fig.add_subplot(111)
        self._setStyle()
        super(MplCanvas, self).__init__(self.fig)

        self.horizontal_line = self.ax.axhline(color='k', lw=0.8, ls='--')
        self.vertical_line = self.ax.axvline(color='k', lw=0.8, ls='--')
        self.text = self.ax.text(0.72, 0.9, '', transform=self.ax.transAxes)

    def _setStyle(self):
        # axes' style
        self.ax.set_xscale('log')
        self.ax.set_xlim(auto=True)
        self.ax.set_ylim(auto=True)
        self.ax.grid()
        self.ax.grid(which='minor', linestyle=':',
                     linewidth='0.5', color='black')
        self.fig.tight_layout()
        self.fig.subplots_adjust(right=0.8)

    def set_cross_hair_visible(self, visible):
        need_redraw = self.horizontal_line.get_visible() != visible
        self.horizontal_line.set_visible(visible)
        self.vertical_line.set_visible(visible)
        self.text.set_visible(visible)
        return need_redraw


class MyToolBar(NavigationToolbar2QT):
    def __init__(self, canvas_, parent_):
        self.toolitems = (
            ('Home', 'Lorem ipsum dolor sit amet', 'home', 'home'),
            ('Back', 'consectetuer adipiscing elit', 'back', 'back'),
            ('Forward', 'sed diam nonummy nibh euismod', 'forward', 'forward'),
            (None, None, None, None),
            ('Pan', 'tincidunt ut laoreet', 'move', 'pan'),
            ('Zoom', 'dolore magna aliquam', 'zoom_to_rect', 'zoom'),
            (None, None, None, None),
            ('Subplots', 'putamus parum claram', 'subplots', 'configure_subplots'),
            ('Save', 'sollemnes in futurum', 'filesave', 'save_figure'),
            ("Customize", "Edit axis, curve and image parameters",
             "qt4_editor_options", "edit_parameters"),
            ('Port', 'Select', "select", 'select_tool'),
        )
        NavigationToolbar2QT.__init__(self, canvas_, parent_)

    def select_tool(self):
        print("You clicked the selection tool")


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
        self.canvas.fig.canvas.mpl_connect(
            'motion_notify_event', self.on_mouse_move)

        self._createTreeList()
        self._createButton()
        self._createShiftGridGroupBox()

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
        vboxlayout_data.addWidget(self.btn_importKlippelData)
        vboxlayout_data.addWidget(self.btn_importLEAPData)
        vboxlayout_data.addWidget(self.btn_clearData)
        hboxLayout_btn.addLayout(vboxlayout_data)
        # 4
        hboxLayout_btn.addWidget(self.shiftGridGroupBox)
        hboxLayout_btn.addWidget(QGroupBox())
        mainLayout.addLayout(hboxLayout_btn)

        self.setLayout(mainLayout)

    def _createCanvas(self):
        self.canvas = MplCanvas(self)
        self.toolbar = MyToolBar(self.canvas, self)
        self.canvas.fig.canvas.mpl_connect(
            'button_press_event', self.canvas_handleClick)

    def _createShiftGridGroupBox(self):
        self.shiftGridGroupBox = QGroupBox()
        layout = QVBoxLayout()
        btn_shift = QPushButton('Shift')
        # btn_shift.clicked.connect(self.dialog_shift)
        btn_shift.clicked.connect(self.curveShift)
        self.cbox_shift = QComboBox()
        self.cbox_shift.currentIndexChanged.connect(self.cbox_handleChange)
        self.le_offsetInput = QLineEdit()

        layout.addWidget(btn_shift)
        layout.addWidget(self.cbox_shift)
        layout.addWidget(self.le_offsetInput)
        self.shiftGridGroupBox.setLayout(layout)

    def _createButton(self):
        self.btn_importKlippelData = QPushButton('Import Klippel data')
        self.btn_importLEAPData = QPushButton('Import LEAP data')
        self.btn_importKlippelData.clicked.connect(self.plotKlippelData)
        self.btn_importLEAPData.clicked.connect(self.plotLEAPData)
        self.btn_clearData = QPushButton('Clear data')
        self.btn_clearData.clicked.connect(self.clearData)

    def _createTreeList(self):
        self.tree = QTreeWidget()
        self.tree.setColumnCount(2)
        self.tree.setHeaderLabels(['Key', 'Value'])
        self.tree.setColumnWidth(0, 300)
        self.tree.setSelectionMode(
            QtWidgets.QAbstractItemView.ExtendedSelection)
        self.tree.itemSelectionChanged.connect(self.tree_handleSelect)
        self.tree.itemChanged.connect(self.tree_handleCheck)

# Reset Functions
    def _resetLineWidth(self):
        for line in self.canvas.ax.lines:
            line.set_linewidth(_defaultLineWidth)
            # self.canvas.draw()


# Handle Functions

    def _switchCheckStatusWithFigure(self, index, originStatus, legendName):
        if (originStatus == 0):
            self.canvas.ax.lines[index].set_visible(False)
            self.canvas.ax.lines[index].set_label('_nolegend_')
        else:
            self.canvas.ax.lines[index].set_visible(True)
            self.canvas.ax.lines[index].set_label(legendName)

    def tree_handleCheck(self, item):
        # print("Check")
        if not item.parent():
            for index in range(item.childCount()):
                it = item.child(index)
                if (item.checkState(0) == 0):
                    it.setCheckState(0, QtCore.Qt.Unchecked)
                else:
                    it.setCheckState(0, QtCore.Qt.Checked)
                print(it.text(0))
                self._switchCheckStatusWithFigure(
                    index, it.checkState(0), it.text(0))
        else:
            index = item.parent().indexOfChild(item)
            print(item.text(0))
            self._switchCheckStatusWithFigure(
                index, item.checkState(0), item.text(0))

        self.canvas.ax.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
        self.canvas.draw()

    def tree_handleSelect(self):
        # print("Select")
        if not self.tree.currentItem():
            pass
        items = self.tree.selectedItems()
        # x = []
        # for i in range(len(items)):
        #   if not items[i].parent():
        #     x.append(items[i].text(0))
        #   else:
        #     x.append(str(items[i].parent().text(0) + ' - ' + items[i].text(0)))
        index = self.tree.currentIndex().row()

        self._resetLineWidth()
        if (index != -1):
            self.canvas.ax.lines[index].set_linewidth(_highlightLineWidth)
            self.canvas.draw()

    def canvas_handleClick(self, event):
        print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
              ('double' if event.dblclick else 'single', event.button,
               event.x, event.y, event.xdata, event.ydata))
        if self.data.empty or not event.inaxes:
            return

        line_i = self._findSelectedLine(event.xdata, event.ydata)
        if (line_i == -1):
            self._resetLineWidth()
        elif (event.button == MouseButton.RIGHT and
              self.canvas.ax.lines[line_i].get_linewidth() == 4):
            self.canvas.ax.lines[line_i].set_linewidth(_defaultLineWidth)
        else:
            self.canvas.ax.lines[line_i].set_linewidth(_highlightLineWidth)
        self.canvas.draw()

    def _findSelectedLine(self, cursor_x, cursor_y):
        min_i = 0
        max_i = len(self.data['Frequency'])
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
        if (error > 1):
            return -1
        return line_i

    def _findYdata(self, cursor_x, cursor_y, line_index):
        left_x = 0
        right_x = len(self.data['Frequency'])
        while (right_x - left_x > 1):
            middle_freq = int((right_x - left_x)/2) + left_x
            if (cursor_x > float(self.data['Frequency'][middle_freq])):
                left_x = middle_freq
            else:
                right_x = middle_freq

        left_freq = self.data['Frequency'][left_x]
        right_freq = self.data['Frequency'][right_x]
        left_ydata = self.data.iloc[left_x][line_index]
        right_ydata = self.data.iloc[right_x][line_index]

        estimate_ydata = left_ydata + \
            ((cursor_x - left_freq) / (right_freq - left_freq)) * \
            (right_ydata - left_ydata)
        return estimate_ydata

    def on_mouse_move(self, event):
        if self.data.empty or not event.inaxes:
            return
        else:
            self.canvas.set_cross_hair_visible(True)
            x = event.xdata
            y = self._findYdata(event.xdata, event.ydata, 0)

            self.canvas.horizontal_line.set_ydata(y)
            self.canvas.vertical_line.set_xdata(x)
            self.canvas.text.set_text('x=%1.2f, y=%1.2f' % (x, y))
            self.canvas.draw()

    def cbox_handleChange(self):
        print(self.cbox_shift.currentText())

# Import data - data preprocessing
    def _get_LEAP_text_file(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setFilter(QtCore.QDir.Files)

        if dialog.exec_():
            file_name = dialog.selectedFiles()

            if file_name[0].endswith('.txt'):
                with open(file_name[0], 'r', encoding='UTF-8', errors='ignore') as file:
                    file_dir = file_name[0]
                    self.filename = file_name[0][file_dir.rfind(
                        '/')+1:file_dir.rfind('.')]

                    print(file_dir)
                    headers = file.readlines()[:11]
                    self.title = headers[0]

                    cols = headers[-1]
                    cols = cols.strip().split(" ")
                    cols = [x for x in cols if x][2:]
                    cols[0] = 'Frequency'
                    data = pd.read_csv(file_name[0],  skiprows=11)
                    data.columns = cols

                    file.close()
                    return data
            else:
                pass

    def _get_Klippel_text_file(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        dialog.setFilter(QtCore.QDir.Files)

        if dialog.exec_():
            file_name = dialog.selectedFiles()

            if file_name[0].endswith('.txt'):
                with open(file_name[0], 'r', encoding='UTF-8') as file:
                    file_dir = file_name[0]
                    self.filename = file_name[0][file_dir.rfind(
                        '/')+1:file_dir.rfind('.')]

                    headers = file.readlines()[:3]
                    self.title = headers[0]
                    curves = headers[1].split('\t\t')
                    curves = [c.replace('"', '').strip() for c in curves]

                    data = pd.read_table(file_name[0],  skiprows=2)
                    data = data.dropna()
                    freq = data.iloc[:, 0]
                    freq = [float(f.replace(',', '').strip()) for f in freq]
                    data = data.iloc[:, [i %
                                         2 == 1 for i in range(len(data.columns))]]
                    data.columns = curves

                    data.insert(0, 'Frequency', freq)
                    file.close()
                    return data
            else:
                pass

    def _get_bose(self):
        with open('bose.txt', 'r', encoding='UTF-8') as file:
            headers = file.readlines()[:3]
            self.filename = 'bose'
            self.title = headers[0]
            curves = headers[1].split('\t\t')
            curves = [c.replace('"', '').strip() for c in curves]

            data = pd.read_table('bose.txt',  skiprows=2)
            freq = data.iloc[:, 0]
            self.data['Frequency'] = [
                float(f.replace(',', '').strip()) for f in freq]
            data = data.iloc[:, [i % 2 == 1 for i in range(len(data.columns))]]
            data.columns = curves

            file.close()
        return data

# Import data - plot initialize
    def appendChildonTree(self):
        root = QTreeWidgetItem(self.tree)
        root.setText(0, self.filename)
        root.setCheckState(0, 2)
        for col in self.data.columns[1:]:
            child = QTreeWidgetItem()
            child.setText(0, col)
            child.setCheckState(0, 2)
            root.addChild(child)
        self.tree.addTopLevelItem(root)
        self.tree.expandAll()

        self.cbox_shift.addItems(self.data.columns[1:])

    def plotKlippelData(self):
        self.data = self._get_Klippel_text_file()
        # self.data = self._get_bose()
        # print(self.data)
        # print(self.data['Frequency'])

        for col in self.data.columns[1:]:
            line, = self.canvas.ax.plot(
                self.data['Frequency'], self.data[col], label=col)  # marker='o'

        self.canvas.ax.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
        self.canvas.draw()
        self.appendChildonTree()

    def plotLEAPData(self):
        self.data = self._get_LEAP_text_file()
        # self.data = self._get_bose()
        print(self.data)
        # print(self.data['Frequency'])

        for col in self.data.columns[1:]:
            self.canvas.ax.plot(
                self.data['Frequency'], self.data[col], label=col)  # marker='o'

        self.canvas.ax.legend(bbox_to_anchor=(1.04, 1), loc="upper left")
        self.canvas.draw()
        self.appendChildonTree()

# Clear data
    def clearData(self):
        self.canvas.ax.lines = []
        self.canvas.ax.legend().remove()
        self.canvas.draw()

        self.tree.clear()
        self.cbox_shift.clear()

# Operations
    def curveShift(self):
        #print("Shift", self.cbox_shift.currentText(), self.le_offsetInput.text())
        try:
            offset = float(self.le_offsetInput.text())
        except ValueError:
            print('ERROR: can not turn ' + self.le_offsetInput.text())
            return
        new_data = [d+offset for d in self.data[self.cbox_shift.currentText()]]
        # Also change origin data
        # self.data[self.cbox_shift.currentText()] = new_data

        self.canvas.ax.lines[self.cbox_shift.currentIndex()].set_data(
            self.data['Frequency'], new_data)
        self.canvas.draw()

    def dialog_shift(self):
        dialog = QDialog()
        L = QVBoxLayout()
        txt = QLineEdit()
        btn = QDialogButtonBox(QDialogButtonBox.Ok)
        btn.clicked.connect(dialog.reject)
        L.addWidget(btn)
        L.addWidget(txt)
        dialog.setLayout(L)

        print("dialog", dialog.exec(), dialog.result)


def contextMenuEvent(self, event):
    contextMenu = QMenu(self)
    newAct = contextMenu.addAction("New")
    openAct = contextMenu.addAction("Open")
    quitAct = contextMenu.addAction("Quit")
    action = contextMenu.exec_(self.mapToGlobal(event.pos()))
    if action == quitAct:
        self.close()


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