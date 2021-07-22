from PyQt5.QtWidgets import QComboBox
from .ui_conf import ICON_DIR, LINEWIDTHS
from PyQt5.QtCore import QSize, Qt, QEvent
from PyQt5.QtGui import QPixmap, QColor, QIcon
from .ui_conf import ICON_DIR, LINEWIDTHS, COLORS


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
        for _idx_, _icon in enumerate(LINEWIDTHS):
            icon_dir = ICON_DIR + f"linewidth_%s.png" % (_idx_)
            self.addItem(QIcon(icon_dir), "")
        self.setPlaceholderText("-- Select --")
        self.setIconSize(QSize(65, 20))

    def set_linewidth(self, linewidth):
        if linewidth in LINEWIDTHS:
            self.setCurrentIndex(LINEWIDTHS.index(linewidth))
