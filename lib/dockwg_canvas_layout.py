from PyQt5.QtWidgets import QWidget, QWidgetItem, QLabel, QPushButton,\
    QHBoxLayout, QVBoxLayout, QGridLayout, QScrollArea,\
    QDockWidget, QSizePolicy
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag


class Draggable_Label(QLabel):
    def __init__(self, text, idx, parent=None):
        super().__init__(text, parent=None)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setText(text)

        self.idx = idx
        # self.setContentsMargins(10, 10, 15, 15)
        self.setStyleSheet("""
            border: 2px solid black;
            border-radius: 10px;
            padding: 5px;
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

    def set_text(self, text):
        # self.text = text
        self.setText(text)


class DockWidget_CanvasLayout(QDockWidget):
    def __init__(self, mainwindow, Position):
        super().__init__("Canvas Properties", mainwindow)
        self.mainwindow = mainwindow
        self.initUI(mainwindow, Position)

        mainwindow.addDockWidget(Qt.DockWidgetArea(Position), self)
        self._set_canvas_mode(mainwindow.wg_canvas.mode)

    def initUI(self, mainwindow, Position):
      # Create Component
        btn_Main = QPushButton('Main')
        btn_UpAndDown = QPushButton('Up and Down')
        self.lb_canvas = []
        for c in mainwindow.wg_canvas.canvasPool[:-1]:
            self.lb_canvas.append(Draggable_Label(c.get_name(), c.id))

        btn_Quater = QPushButton('Quater')
        btn_MainwithThreeSmallWindows = QPushButton('Main + 3')

        btn_axis_setting = QPushButton("Axis Setting")
        btn_processing = QPushButton("Post-Processing")

        # btn_MainwithScrollArea = QPushButton('Main + Scroll')

        vbly = QVBoxLayout()
        vbly.addWidget(QLabel("Setting ————————"))
        btnGroup = [btn_Main, btn_UpAndDown]
        for btn in btnGroup:
            vbly.addWidget(btn)
        vbly.addWidget(btn_axis_setting)

        vbly.addWidget(QLabel("Operation ————————"))
        vbly.addWidget(btn_processing)

        vbly.addWidget(QLabel("Canvas ————————"))
        for lb in self.lb_canvas:
            vbly.addWidget(lb)

        wg = QWidget()
        wg.setLayout(vbly)
        wg.setObjectName("wg_main")
        self.setWidget(wg)

      # Connect Functions
        btn_Main.clicked.connect(
            lambda: self._set_canvas_mode("Main"))
        btn_UpAndDown.clicked.connect(
            lambda: self._set_canvas_mode("UpAndDown"))
        btn_Quater.clicked.connect(
            lambda: self._set_canvas_mode("Quater"))
        btn_MainwithThreeSmallWindows.clicked.connect(
            lambda: self._set_canvas_mode("MainwithThreeSmallWindows"))
        # btn_MainwithScrollArea.clicked.connect(
        #     lambda: self._setCanvasLayout_MainwithScrollArea(mainwindow.wg_canvas))
        btn_axis_setting.clicked.connect(
            self.mainwindow.btn_axis_setting_handleClicked)
        btn_processing.clicked.connect(
            self.mainwindow.btn_processingDlg_handleClicked)
      # Style and Setting
        vbly.setAlignment(Qt.AlignTop)
        self.setMinimumWidth(120)

    def clearLayout(self, layout):
        for i in reversed(range(layout.count())):
            # print(i, layout.itemAt(i))
            if (type(layout.itemAt(i)) == QWidgetItem):
                widget = layout.itemAt(i).widget()
                layout.removeWidget(widget)
                widget.setParent(None)
            elif (type(layout.itemAt(i)) == QGridLayout):
                self.clearLayout(layout.itemAt(i))

    def _set_canvas_mode(self, mode):
        func = {
            "Main": self._setCanvasLayout_Main,
            "UpAndDown": self._setCanvasLayout_UpAndDown,
            "Quater": self._setCanvasLayout_Quater,
            "MainwithThreeSmall": self._setCanvasLayout_MainwithThreeSmall
        }
        func[mode](self.mainwindow.wg_canvas)

    def _setCanvasLayout_Main(self, wg_canvas):
        self.clearLayout(wg_canvas.gdly_canvasPool)
        active_canvas = wg_canvas.status["Main"][0]
        layout = wg_canvas.gdly_canvasPool
        layout.addWidget(active_canvas, 0, 0, -1, 1)
        layout.setColumnStretch(0, 6)
        layout.setColumnStretch(1, 0)
        layout.setColumnStretch(2, 0)
        layout.setRowStretch(0, 4)
        layout.setContentsMargins(10, 10, 10, 10)

        wg_canvas.set_mode("Main")

    def _setCanvasLayout_UpAndDown(self, wg_canvas):
        self.clearLayout(wg_canvas.gdly_canvasPool)
        active_canvas1 = wg_canvas.status["UpAndDown"][0]
        active_canvas2 = wg_canvas.status["UpAndDown"][1]

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

    def _setCanvasLayout_Quater(self, wg_canvas):
        self.clearLayout(wg_canvas.gdly_canvasPool)

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

    def _setCanvasLayout_MainwithScrollArea(self, wg_canvas):
        self.clearLayout(wg_canvas.gdly_canvasPool)
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

    def _setCanvasLayout_MainwithThreeSmall(self, wg_canvas):
        self.clearLayout(wg_canvas.gdly_canvasPool)

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
