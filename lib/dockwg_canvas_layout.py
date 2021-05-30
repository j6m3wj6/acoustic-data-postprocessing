import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from .dlg_load_files import *
from .wg_treelist import *


class Draggable_Label(QLabel):
    def __init__(self, text, idx, parent=None):
        super().__init__(text, parent=None)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.text = text
        self.idx = idx
        # self.setContentsMargins(10, 10, 15, 15)
        self.setStyleSheet("""
            border: 2px solid black;
            min-height: 50px;
        """)
        self.setAlignment(Qt.AlignCenter)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            mimeData = QMimeData()
            mimeData.setText(str(self.idx))
            drag = QDrag(self)
            drag.setMimeData(mimeData)
            drag.exec_(Qt.MoveAction)


class DockWidget_CanvasLayout(QDockWidget):
    def __init__(self, myApp, Position):
        super().__init__("Data", myApp)
        self.setMinimumWidth(100)
        self.myApp = myApp
        self.initUI(myApp, Position)

        myApp.addDockWidget(Qt.DockWidgetArea(Position), self)
        self._setCanvasLayout_Main(myApp.wg_canvas)

    def initUI(self, myApp, Position):
        self.setStyleSheet("""
            QVBoxLayout {
                border: 1px solid gray;
                padding: 10;
                margin: 0;
            }

        """)

        self.dockWidgetContents_data = QWidget()
        self.setWidget(self.dockWidgetContents_data)
        vbly = QVBoxLayout(self.dockWidgetContents_data)
        # vbly.setContentsMargins(10, 10, 0, 0)
        vbly.setAlignment(Qt.AlignTop)

        self.btn_Main = QPushButton('Main')
        self.btn_UpAndDown = QPushButton('Up and Down')
        self.lb_canvas = []
        for c in myApp.wg_canvas.canvasPool:
            self.lb_canvas.append(Draggable_Label(c.get_name(), c.id))
        self.btn_Quater = QPushButton('Quater')
        self.btn_MainwithThreeSmallWindows = QPushButton('Main + 3')
        self.btn_MainwithScrollArea = QPushButton('Main + Scroll')

        self.btn_Main.clicked.connect(
            lambda: self._setCanvasLayout_Main(myApp.wg_canvas))
        self.btn_UpAndDown.clicked.connect(
            lambda: self._setCanvasLayout_UpAndDown(myApp.wg_canvas))
        self.btn_Quater.clicked.connect(
            lambda: self._setCanvasLayout_Quater(myApp.wg_canvas))
        self.btn_MainwithThreeSmallWindows.clicked.connect(
            lambda: self._setCanvasLayout_MainwithThreeSmall(myApp.wg_canvas))
        # self.btn_MainwithScrollArea.clicked.connect(
        #     lambda: self._setCanvasLayout_MainwithScrollArea(myApp.wg_canvas))

        btnGroup = [self.btn_Main, self.btn_UpAndDown,  self.btn_Quater,
                    self.btn_MainwithThreeSmallWindows, self.btn_MainwithScrollArea]
        # btnGroup = [self.btn_Main, self.btn_UpAndDown]
        for btn in btnGroup:
            vbly.addWidget(btn)

        for lb in self.lb_canvas:
            vbly.addWidget(lb)

    def clearLayout(self, layout):
        for i in reversed(range(layout.count())):
            # print(i, layout.itemAt(i))
            if (type(layout.itemAt(i)) == QWidgetItem):
                widget = layout.itemAt(i).widget()
                layout.removeWidget(widget)
                widget.setParent(None)
            elif (type(layout.itemAt(i)) == QGridLayout):
                self.clearLayout(layout.itemAt(i))

    def _setCanvasLayout_Main(self, wg_canvas):
        self.clearLayout(wg_canvas.gdly_canvasPool)
        for c in wg_canvas.canvasPool:
            c.set_active(False)
        active_canvas = wg_canvas.status["Main"][0]
        active_canvas.set_active(True)
        layout = wg_canvas.gdly_canvasPool
        layout.addWidget(active_canvas, 0, 0, -1, 1)
        layout.setColumnStretch(0, 6)
        layout.setColumnStretch(1, 0)
        layout.setColumnStretch(2, 0)
        layout.setRowStretch(0, 4)
        layout.setContentsMargins(10, 10, 10, 10)

        wg_canvas.set_mode("Main")
        wg_canvas.toolbar.update_canvas()

    def _setCanvasLayout_UpAndDown(self, wg_canvas):
        self.clearLayout(wg_canvas.gdly_canvasPool)
        for c in wg_canvas.canvasPool:
            c.set_active(False)
        active_canvas1 = wg_canvas.status["UpAndDown"][0]
        active_canvas2 = wg_canvas.status["UpAndDown"][1]
        active_canvas1.set_active(True)
        active_canvas2.set_active(True)

        layout = wg_canvas.gdly_canvasPool
        layout.addWidget(active_canvas1, 0, 0, 1, 1)
        layout.addWidget(active_canvas2, 1, 0, 1, 1)
        layout.setColumnStretch(0, 6)
        layout.setColumnStretch(1, 0)
        layout.setColumnStretch(2, 0)
        layout.setRowStretch(0, 2)
        layout.setRowStretch(1, 2)
        layout.setContentsMargins(10, 10, 10, 10)

        wg_canvas.set_mode("UpAndDown")
        wg_canvas.toolbar.update_canvas()

    def _setCanvasLayout_Quater(self, wg_canvas):
        self.clearLayout(wg_canvas.gdly_canvasPool)
        for c in wg_canvas.canvasPool:
            c.set_active(True)

        active_canvas0 = wg_canvas.status["Quater"][0]
        active_canvas1 = wg_canvas.status["Quater"][1]
        active_canvas2 = wg_canvas.status["Quater"][2]
        active_canvas3 = wg_canvas.status["Quater"][3]

        layout = wg_canvas.gdly_canvasPool
        layout.addWidget(active_canvas0, 0, 0, 1, 1)
        layout.addWidget(active_canvas1, 1, 0, 1, 1)
        layout.addWidget(active_canvas2, 0, 1, 1, 1)
        layout.addWidget(active_canvas3, 1, 1, 1, 1)
        layout.setColumnStretch(0, 3)
        layout.setColumnStretch(1, 3)
        layout.setColumnStretch(2, 0)
        layout.setRowStretch(0, 2)
        layout.setRowStretch(1, 2)
        layout.setContentsMargins(10, 10, 10, 10)

        wg_canvas.set_mode("Quater")
        wg_canvas.toolbar.update_canvas()

    def _setCanvasLayout_MainwithScrollArea(self, wg_canvas):
        self.clearLayout(wg_canvas.gdly_canvasPool)
        for c in wg_canvas.canvasPool:
            c.set_active(False)
        scroll = QScrollArea()
        widget = QWidget()
        hboxLayout = QHBoxLayout()
        widget.setLayout(hboxLayout)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll.setWidget(widget)
        scroll.setWidgetResizable(True)

        for i in range(10):
            Label = QLabel(
                'BlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBlaBla')
            Label.setFixedWidth(200)
            hboxLayout.addWidget(Label)
        wg_canvas.canvasPool[0].set_active(True)
        layout = wg_canvas.gdly_canvasPool
        layout.addWidget(wg_canvas.canvasPool[0], 0, 0, 1, 1)
        layout.addWidget(scroll, 1, 0, 1, 1)
        layout.setColumnStretch(0, 6)
        layout.setColumnStretch(1, 0)
        layout.setColumnStretch(2, 0)
        layout.setRowStretch(0, 3)
        layout.setRowStretch(1, 1)
        layout.setContentsMargins(10, 10, 10, 10)

        wg_canvas.set_mode("MainwithScrollArea")
        wg_canvas.toolbar.update_canvas()

    def _setCanvasLayout_MainwithThreeSmall(self, wg_canvas):
        self.clearLayout(wg_canvas.gdly_canvasPool)
        for c in wg_canvas.canvasPool:
            c.set_active(True)

        active_canvas0 = wg_canvas.status["MainwithThreeSmall"][0]
        active_canvas1 = wg_canvas.status["MainwithThreeSmall"][1]
        active_canvas2 = wg_canvas.status["MainwithThreeSmall"][2]
        active_canvas3 = wg_canvas.status["MainwithThreeSmall"][3]
        layout = wg_canvas.gdly_canvasPool
        layout.addWidget(active_canvas0, 0, 0, 1, 3)
        layout.addWidget(active_canvas1, 1, 0, 1, 1)
        layout.addWidget(active_canvas2, 1, 1, 1, 1)
        layout.addWidget(active_canvas3, 1, 2, 1, 1)
        layout.setColumnStretch(0, 2)
        layout.setColumnStretch(1, 2)
        layout.setColumnStretch(2, 2)
        layout.setRowStretch(0, 5)
        layout.setRowStretch(1, 1)
        layout.setContentsMargins(10, 10, 10, 10)

        wg_canvas.set_mode("MainwithThreeSmall")
        wg_canvas.toolbar.update_canvas()
