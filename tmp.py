# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MicePipelineMain.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1311, 911)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName("gridLayout_3")

        self.mdiArea = QtWidgets.QMdiArea(self.centralwidget)
        self.mdiArea.setObjectName("mdiArea")
        self.gridLayout_3.addWidget(self.mdiArea, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1311, 30))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)

        # self.dockWidget_3 = QtWidgets.QDockWidget(MainWindow)
        # self.dockWidget_3.setObjectName("dockWidget_3")
        # self.dockWidgetContents_3 = QtWidgets.QWidget()
        # self.dockWidgetContents_3.setObjectName("dockWidgetContents_3")

        # self.gridLayout = QtWidgets.QGridLayout(self.dockWidgetContents_3)
        # self.gridLayout.setContentsMargins(0, 0, 0, 0)
        # self.gridLayout.setObjectName("gridLayout")
        # self.listView1 = QtWidgets.QTreeWidget(self.dockWidgetContents_3)
        # self.listView1.setObjectName("listView1")
        # item_0 = QtWidgets.QTreeWidgetItem(self.listView1)
        # item_1 = QtWidgets.QTreeWidgetItem(item_0)
        # item_1 = QtWidgets.QTreeWidgetItem(item_0)
        # item_1 = QtWidgets.QTreeWidgetItem(item_0)
        # self.gridLayout.addWidget(self.listView1, 0, 0, 1, 1)
        # self.dockWidget_3.setWidget(self.dockWidgetContents_3)
        # MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.dockWidget_3)
        # self.dockWidget = QtWidgets.QDockWidget(MainWindow)
        # self.dockWidget.setObjectName("dockWidget")
        # self.dockWidgetContents = QtWidgets.QWidget()
        # self.dockWidgetContents.setObjectName("dockWidgetContents")

        # self.gridLayout_4 = QtWidgets.QGridLayout(self.dockWidgetContents)
        # self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        # self.gridLayout_4.setObjectName("gridLayout_4")
        # self.graphicsView_2 = ParameterTree(self.dockWidgetContents)
        # self.graphicsView_2.setObjectName("graphicsView_2")
        # self.gridLayout_4.addWidget(self.graphicsView_2, 0, 0, 1, 1)
        # self.dockWidget.setWidget(self.dockWidgetContents)
        # MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidget)
        # self.dockWidget_2 = QtWidgets.QDockWidget(MainWindow)
        # self.dockWidget_2.setObjectName("dockWidget_2")
        # self.dockWidgetContents_2 = QtWidgets.QWidget()
        # self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        # self.gridLayout_5 = QtWidgets.QGridLayout(self.dockWidgetContents_2)
        # self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        # self.gridLayout_5.setObjectName("gridLayout_5")
        # self.graphicsView_3 = ImageView(self.dockWidgetContents_2)
        # self.graphicsView_3.setObjectName("graphicsView_3")
        # self.gridLayout_5.addWidget(self.graphicsView_3, 0, 0, 1, 1)
        # self.dockWidget_2.setWidget(self.dockWidgetContents_2)
        # MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.dockWidget_2)
        # self.actionLoad = QtWidgets.QAction(MainWindow)
        # self.actionLoad.setObjectName("actionLoad")
        # self.menuFile.addAction(self.actionLoad)
        # self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        # self.listView1.headerItem().setText(0, _translate("MainWindow", "rootPath"))
        # __sortingEnabled = self.listView1.isSortingEnabled()
        # self.listView1.setSortingEnabled(False)
        # self.listView1.topLevelItem(0).setText(0, _translate("MainWindow", "d0001"))
        # self.listView1.topLevelItem(0).child(0).setText(0, _translate("MainWindow", "1 2020-01-11 14-24-07.236.avi"))
        # self.listView1.topLevelItem(0).child(1).setText(0, _translate("MainWindow", "2 2020-01-11 14-29-31.977.avi"))
        # self.listView1.topLevelItem(0).child(2).setText(0, _translate("MainWindow", "3 2020-01-11 14-34-55.968.avi"))

        # self.listView1.setSortingEnabled(__sortingEnabled)
        # self.actionLoad.setText(_translate("MainWindow", "Load"))

from pyqtgraph import ImageView
from pyqtgraph.parametertree import ParameterTree

from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType
import pyqtgraph.parametertree.parameterTypes as pTypes

class ComplexParameter(pTypes.GroupParameter):
    def __init__(self, **opts):
        opts['type'] = 'bool'
        opts['value'] = True
        pTypes.GroupParameter.__init__(self, **opts)

        self.addChild({'name': 'A = 1/B', 'type': 'float', 'value': 7, 'suffix': 'Hz', 'siPrefix': True})
        self.addChild({'name': 'B = 1/A', 'type': 'float', 'value': 1 / 7., 'suffix': 's', 'siPrefix': True})
        self.a = self.param('A = 1/B')
        self.b = self.param('B = 1/A')
        self.a.sigValueChanged.connect(self.aChanged)
        self.b.sigValueChanged.connect(self.bChanged)

    def aChanged(self):
        self.b.setValue(1.0 / self.a.value(), blockSignal=self.bChanged)

    def bChanged(self):
        self.a.setValue(1.0 / self.b.value(), blockSignal=self.aChanged)


## test add/remove
## this group includes a menu allowing the user to add new parameters into its child list
class ScalableGroup(pTypes.GroupParameter):
    def __init__(self, **opts):
        opts['type'] = 'group'
        opts['addText'] = "Add"
        opts['addList'] = ['str', 'float', 'int']
        pTypes.GroupParameter.__init__(self, **opts)

    def addNew(self, typ):
        val = {
            'str': '',
            'float': 0.0,
            'int': 0
        }[typ]
        self.addChild(
            dict(name="ScalableParam %d" % (len(self.childs) + 1), type=typ, value=val, removable=True, renamable=True))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    #####
    params = [
        {'name': 'Basic parameter data types', 'type': 'group', 'children': [
            {'name': 'Integer', 'type': 'int', 'value': 10},
            {'name': 'Float', 'type': 'float', 'value': 10.5, 'step': 0.1},
            {'name': 'String', 'type': 'str', 'value': "hi"},
            {'name': 'List', 'type': 'list', 'values': [1, 2, 3], 'value': 2},
            {'name': 'Named List', 'type': 'list', 'values': {"one": 1, "two": "twosies", "three": [3, 3, 3]},
             'value': 2},
            {'name': 'Boolean', 'type': 'bool', 'value': True, 'tip': "This is a checkbox"},
            {'name': 'Color', 'type': 'color', 'value': "FF0", 'tip': "This is a color button"},
            {'name': 'Gradient', 'type': 'colormap'},
            {'name': 'Subgroup', 'type': 'group', 'children': [
                {'name': 'Sub-param 1', 'type': 'int', 'value': 10},
                {'name': 'Sub-param 2', 'type': 'float', 'value': 1.2e6},
            ]},
            {'name': 'Text Parameter', 'type': 'text', 'value': 'Some text...'},
            {'name': 'Action Parameter', 'type': 'action'},
        ]},
        {'name': 'Numerical Parameter Options', 'type': 'group', 'children': [
            {'name': 'Units + SI prefix', 'type': 'float', 'value': 1.2e-6, 'step': 1e-6, 'siPrefix': True,
             'suffix': 'V'},
            {'name': 'Limits (min=7;max=15)', 'type': 'int', 'value': 11, 'limits': (7, 15), 'default': -6},
            {'name': 'DEC stepping', 'type': 'float', 'value': 1.2e6, 'dec': True, 'step': 1, 'siPrefix': True,
             'suffix': 'Hz'},

        ]},
        {'name': 'Save/Restore functionality', 'type': 'group', 'children': [
            {'name': 'Save State', 'type': 'action'},
            {'name': 'Restore State', 'type': 'action', 'children': [
                {'name': 'Add missing items', 'type': 'bool', 'value': True},
                {'name': 'Remove extra items', 'type': 'bool', 'value': True},
            ]},
        ]},
        {'name': 'Extra Parameter Options', 'type': 'group', 'children': [
            {'name': 'Read-only', 'type': 'float', 'value': 1.2e6, 'siPrefix': True, 'suffix': 'Hz', 'readonly': True},
            {'name': 'Renamable', 'type': 'float', 'value': 1.2e6, 'siPrefix': True, 'suffix': 'Hz', 'renamable': True},
            {'name': 'Removable', 'type': 'float', 'value': 1.2e6, 'siPrefix': True, 'suffix': 'Hz', 'removable': True},
        ]},
        ComplexParameter(name='Custom parameter group (reciprocal values)'),
        ScalableGroup(name="Expandable Parameter Group", children=[
            {'name': 'ScalableParam 1', 'type': 'str', 'value': "default param 1"},
            {'name': 'ScalableParam 2', 'type': 'str', 'value': "default param 2"},
        ]),
    ]

    p = Parameter.create(name='params', type='group', children=params)



    # ui.graphicsView_2.setParameters(p, showTop=False)
    MainWindow.show()
    sys.exit(app.exec_())
