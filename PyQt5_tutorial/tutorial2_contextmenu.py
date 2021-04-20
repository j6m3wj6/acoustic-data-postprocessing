from PyQt5 import QtCore
from PyQt5.QtWidgets import *
import sys

class MyApp(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self._createContextMenu()
        self.customContextMenuRequested.connect(self.contextMenuEvent)

    def _createContextMenu(self):
        self.contextMenu = QMenu(self)
        self.newAct = self.contextMenu.addAction("New")
        self.closeAct = self.contextMenu.addAction("Close")
        self.quitAct = self.contextMenu.addAction("Quit window")

    def contextMenuEvent(self, event):
        action = self.contextMenu.exec_(self.mapToGlobal(event))
        if action == self.closeAct:
            self.contextMenu.close()

        elif action == self.quitAct:
            self.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MyApp()
    main.show()
    sys.exit(app.exec_())

