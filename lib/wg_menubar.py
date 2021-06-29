from PyQt5.QtWidgets import QMenuBar, QMenu, QAction, QFileDialog


class MyMenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._createActions()
        fileMenu = QMenu("&File", self)
        self.addMenu(fileMenu)
        fileMenu.addAction(self.act_new)
        fileMenu.addAction(self.act_open)
        fileMenu.addAction(self.act_save)
        fileMenu.addAction(self.act_save_as)
        fileMenu.addAction(self.act_import)

        helpMenu = QMenu("&Help", self)
        helpMenu.addAction(self.act_help)
        self.addMenu(helpMenu)

    def _createActions(self):
      # Creating Components
        self.act_new = QAction("&New Project", self)
        self.act_open = QAction("&Open Project", self)
        self.act_save = QAction("&Save Project", self)
        self.act_save_as = QAction("&Save Project As...", self)
        self.act_import = QAction("&Import File", self)

        self.act_help = QAction("&Documnet", self)

      # Connect Functions
        # Connect File actions
        self.act_new.triggered.connect(self.new_file)
        self.act_open.triggered.connect(self.open_file)
        self.act_save.triggered.connect(self.save_file)
        self.act_save_as.triggered.connect(self.save_file_as)
        self.act_import.triggered.connect(
            self.parent().dwg_data.btn_importDlg_handleClicked)

    def new_file(self):
        self.parent().app.create_mainwindow()

    def open_file(self):
        # Logic for opening an existing file goes here...
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFile)
        # dialog.setOption(QFileDialog.DontUseNativeDialog)
        dialog.setNameFilter("PKL files (*.pkl)")

        if dialog.exec_():
            path = dialog.selectedFiles()[0]
            self.parent().app.create_mainwindow(path)
        else:
            pass

    def save_file(self):
        self.parent().save_file()

    def save_file_as(self):
        self.parent().save_file_as()
