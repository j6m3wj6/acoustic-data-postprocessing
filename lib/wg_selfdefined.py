from re import sub
from PyQt5.QtWidgets import QComboBox, QLabel, QSizePolicy, QToolButton
from .ui_conf import ICON_DIR, LINESTYLES, LINEWIDTHS
from PyQt5.QtCore import QSize, Qt, QMimeData
from PyQt5.QtGui import QPixmap, QColor, QIcon, QDrag, QMouseEvent
from .ui_conf import ICON_DIR, LINEWIDTHS, COLORS


class Draggable_lines:
    def __init__(self, canvas, ax):
        self.canvas = canvas
        # self.canvas.mpl_connect('pick_event', self.clickonline)
        if ax == canvas.ax_main:
            xcoord = 4000
            ycoord = (ax.get_ylim()[0]*1 + ax.get_ylim()[1]*2)/3
            self.text = ax.text(0, 1.01, 'x = {:6.2f}, y = {:6.2f}'.format(
                xcoord, ycoord), transform=ax.transAxes, ha='left', color='#0002fd')
            self.vline = ax.axvline(x=xcoord, picker=5, color="#0002fd")
            self.hline = ax.axhline(y=ycoord, picker=5, color="#0002fd")
        else:
            xcoord = 500
            ycoord = (self.canvas.ax_sub.get_ylim()[
                      0]*2 + self.canvas.ax_sub.get_ylim()[1]*1)/3
            self.text = ax.text(1, 1.01, 'x = {:6.2f}, y = {:6.2f}'.format(
                xcoord, ycoord), transform=canvas.ax_sub.transAxes, ha='right', color='#fd0002')
            self.vline = ax.axvline(x=xcoord, picker=5, color="#fd0002")
            self.hline = ax.axhline(y=ycoord, picker=5, color="#fd0002")

        self.vline.set_zorder(1000)
        self.hline.set_zorder(1000)
        self.xcoord = xcoord
        self.ycoord = ycoord

    def clickonline(self, event):
        print("pick")
        if event.artist in [self.hline, self.vline]:
            # print("line selected ", event.artist)
            self.follower = self.canvas.mpl_connect(
                "motion_notify_event", self.followmouse)
            self.releaser = self.canvas.mpl_connect(
                "button_press_event", self.releaseonclick)

    def followmouse(self, event):
        self.vline.set_xdata([event.xdata, event.xdata])
        self.hline.set_ydata([event.ydata, event.ydata])
        self.text.set_text('x = {:6.2f}, y = {:6.2f}'.format(
            event.xdata, event.ydata))
        # self.text.set_position((event.xdata*1.1, event.ydata*1.002))
        self.canvas.replot()

    def releaseonclick(self, event):
        self.xcoord = self.vline.get_xdata()[0]
        self.ycoord = self.hline.get_ydata()[0]
        self.canvas.mpl_disconnect(self.releaser)
        self.canvas.mpl_disconnect(self.follower)

    def sub_followmouse(self, event):
        x, sub_y = self.canvas.ax_sub.transData.inverted().transform((event.x, event.y))
        self.vline.set_xdata([x, x])
        self.hline.set_ydata([sub_y, sub_y])
        self.text.set_text('x = {:6.2f}, y = {:6.2f}'.format(
            x, sub_y))
        # self.text.set_position((event.xdata*1.1, event.ydata*1.002))
        self.canvas.replot()

    def sub_releaseonclick(self, event):
        self.xcoord = self.vline.get_xdata()[0]
        self.ycoord = self.hline.get_ydata()[0]
        self.canvas.mpl_disconnect(self.releaser)
        self.canvas.mpl_disconnect(self.follower)

    def set_visible(self, visible):
        self.vline.set_visible(visible)
        self.hline.set_visible(visible)
        self.text.set_visible(visible)
        self.canvas.replot()

    def get_coords(self):
        return [self.xcoord, self.ycoord]


class Cbox_Color(QComboBox):
    def __init__(self):
        super().__init__()
        self.setPlaceholderText("-- Select --")
        self.setIconSize(QSize(65, 20))
        for _col_ in COLORS:
            pixmap = QPixmap(65, 20)
            pixmap.fill(QColor(_col_))
            redIcon = QIcon(pixmap)
            self.addItem(redIcon, "")

    def set_color(self, color):
        if color in COLORS:
            self.setCurrentIndex(COLORS.index(color))


class Cbox_Linewidth(QComboBox):
    def __init__(self):
        super().__init__()
        for _style_ in LINESTYLES:
            for _idx_, _icon in enumerate(LINEWIDTHS):
                icon_dir = ICON_DIR + f"line_%s_%s.png" % (_idx_, _style_)

                self.addItem(QIcon(icon_dir), "")
        self.setPlaceholderText("-- Select --")
        self.setIconSize(QSize(65, 20))


class Lb_Draggable(QLabel):
    '''
    Self-defined Qlabel that use to represent app's canvas components on ``DockWidget_CanvasLayout``.
    User can drag this label onto the canvas component, which could change the arrangement in the layout.
    '''

    def __init__(self, text: str, idx: int) -> None:
        super().__init__(text)
        self.setText(text)

        self.idx = idx
        self.setStyleSheet("""
            border: 2px solid black;
            border-radius: 10px;
            padding: 5px;
            min-height: 50px;
            max-width: 300px;
        """)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setAlignment(Qt.AlignCenter)
        self.setWordWrap(True)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.LeftButton:
            mimeData = QMimeData()
            mimeData.setText(str(self.idx))
            drag = QDrag(self)
            drag.setMimeData(mimeData)
            drag.exec_(Qt.MoveAction)

    def set_text(self, text: str) -> None:
        """
        Set the displayed text.

        :param str text:
        """
        self.setText(text)


class Toolbtn_Link(QToolButton):
    def __init__(self, link=True):
        super(QToolButton, self).__init__()
        self.setObjectName("toolbtn_link")
        self.toggle_style(link)
        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.setCheckable(True)
        self.setChecked(link)
        self.clicked.connect(self.toggle_style)
        self.setStyleSheet("""
            QToolButton {
                background-color: #E49485;
                border: 1px solid #C31F39;
                padding: 0px 4px;
                width: 60px;
            }
            QToolButton::checked {
                background-color: #71C5EA;
                border: 1px solid #0078A8;
                padding: 0px 4px;
                width: 60px;
            }
        """)

    def toggle_style(self, link):
        if link:
            self.setText("  Link")
            self.setIcon(QIcon(ICON_DIR+"link.png"))

        else:
            self.setText("Unlink")
            self.setIcon(QIcon(ICON_DIR+"unlink.png"))
