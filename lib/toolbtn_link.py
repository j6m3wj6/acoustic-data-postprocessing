from PyQt5.QtWidgets import QToolButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from .ui_conf import ICON_DIR


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
