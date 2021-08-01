from PyQt5.QtWidgets import QWidget, QWidgetItem, QLabel, QPushButton,\
    QHBoxLayout, QVBoxLayout, QGridLayout, QScrollArea, QDockWidget
from PyQt5.QtCore import Qt
from .wg_selfdefined import Lb_Draggable


class DockWg_Canvas(QDockWidget):
    def __init__(self, mainwindow, Position: Qt.DockWidgetArea) -> None:
        super().__init__("Canvas Properties", mainwindow)
        self.mainwindow = mainwindow
        self.initUI()
        mainwindow.addDockWidget(Qt.DockWidgetArea(Position), self)

    def initUI(self) -> None:
        """Initial User Interface."""
      # Create Component
        btn_Main = QPushButton('Main')
        btn_UpAndDown = QPushButton('Up and Down')
        btn_Quater = QPushButton('Quater')
        btn_MainwithThreeSmallWindows = QPushButton('Main + 3')
        # btn_MainwithScrollArea = QPushButton('Main + Scroll')
        self.lb_canvas = []
        for c in self.mainwindow.wg_canvas.canvasPool[:-1]:
            self.lb_canvas.append(Lb_Draggable(c.get_name(), c.id))
        btn_axis_setting = QPushButton("Axis Setting")
        btn_processing = QPushButton("Post-Processing")

      # Layout
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
        wg_main = QWidget()
        wg_main.setLayout(vbly)
        self.setWidget(wg_main)
      # Connect Functions
        btn_Main.clicked.connect(
            lambda: self.set_canvas_mode("Main"))
        btn_UpAndDown.clicked.connect(
            lambda: self.set_canvas_mode("UpAndDown"))
        btn_Quater.clicked.connect(
            lambda: self.set_canvas_mode("Quater"))
        btn_MainwithThreeSmallWindows.clicked.connect(
            lambda: self.set_canvas_mode("MainwithThreeSmallWindows"))
        # btn_MainwithScrollArea.clicked.connect(
        #     lambda: self._setCanvasLayout_MainwithScrollArea(mainwindow.wg_canvas))
        btn_axis_setting.clicked.connect(
            self.mainwindow.btn_axis_setting_handleClicked)
        btn_processing.clicked.connect(
            self.mainwindow.btn_processingDlg_handleClicked)
      # Style and Setting
        vbly.setAlignment(Qt.AlignTop)
        self.setMinimumWidth(120)

    def set_canvas_mode(self, mode: str) -> None:
        """
        Set canvas layout mode, Main/UpAndDown/Quater/MainwithThreeSmall.\n
        >> *Quater/MainwithThreeSmall are not availibale for ver_0.2.0*

        :param str mode: The canvas layout mode user intends to set.
        """
        func = {
            "Main": self._setCanvasLayout_Main,
            "UpAndDown": self._setCanvasLayout_UpAndDown,
            "Quater": self._setCanvasLayout_Quater,
            "MainwithThreeSmall": self._setCanvasLayout_MainwithThreeSmall
        }
        func[mode]()
        self.mainwindow.wg_canvas.set_mode(mode)
        self.mainwindow.project.ui_conf["MyCanvas"]["mode"] = mode

    def _clear_layout(self, layout: QGridLayout) -> None:
        """
        Clear all the widgets in layout. \n
        If there is another layout inside, recursively clear it.

        :param QGridLayout layout: 
        """
        for i in reversed(range(layout.count())):
            # print(i, layout.itemAt(i))
            if (type(layout.itemAt(i)) == QWidgetItem):
                widget = layout.itemAt(i).widget()
                layout.removeWidget(widget)
                widget.setParent(None)
            elif (type(layout.itemAt(i)) == QGridLayout):
                self._clear_layout(layout.itemAt(i))

    def _setCanvasLayout_Main(self) -> None:
        """
        Move all the widgets out of the layout of mainwindow's wg_canvas. \n
        And then start-over putting canvas into it base on canvas layout mode Main.
        """
        wg_canvas = self.mainwindow.wg_canvas
        self._clear_layout(wg_canvas.gdly_canvasPool)
        active_canvas = wg_canvas.status["Main"][0]
        layout = wg_canvas.gdly_canvasPool
        layout.addWidget(active_canvas, 0, 0, -1, 1)
        layout.setColumnStretch(0, 6)
        layout.setColumnStretch(1, 0)
        layout.setColumnStretch(2, 0)
        layout.setRowStretch(0, 4)
        layout.setContentsMargins(10, 10, 10, 10)

    def _setCanvasLayout_UpAndDown(self) -> None:
        """
        Move all the widgets out of the layout of mainwindow's wg_canvas. \n
        And then start-over putting canvas into it base on canvas layout mode UpAndDown.
        """
        wg_canvas = self.mainwindow.wg_canvas
        self._clear_layout(wg_canvas.gdly_canvasPool)
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

    def _setCanvasLayout_Quater(self) -> None:
        """
        Move all the widgets out of the layout of mainwindow's wg_canvas. \n
        And then start-over putting canvas into it base on canvas layout mode Quater.

        >> Not support in ver_0.2.0
        """
        wg_canvas = self.mainwindow.wg_canvas
        self._clear_layout(wg_canvas.gdly_canvasPool)

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

    def _setCanvasLayout_MainwithScrollArea(self) -> None:
        """
        Move all the widgets out of the layout of mainwindow's wg_canvas. \n
        And then start-over putting canvas into it base on canvas layout mode MainwithScrollArea.

        >> Not support in ver_0.2.0
        """
        wg_canvas = self.mainwindow.wg_canvas
        self._clear_layout(wg_canvas.gdly_canvasPool)
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

    def _setCanvasLayout_MainwithThreeSmall(self) -> None:
        """
        Move all the widgets out of the layout of mainwindow's wg_canvas. \n
        And then start-over putting canvas into it base on canvas layout mode MainwithThreeSmall.

        >> Not support in ver_0.2.0
        """
        wg_canvas = self.mainwindow.wg_canvas
        self._clear_layout(wg_canvas.gdly_canvasPool)

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
