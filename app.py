# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import QLabel, QMainWindow, QApplication, QVBoxLayout, QWidget
from lib.mainwindow import MainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QFileInfo
import sys
import os
import traceback


class MyApp(QMainWindow):
    '''
    :ivar list(MainWindow) windows: store existing windows.
    '''

    def __init__(self):
        super().__init__()
        self.windows = []

        self.create_document()
        self.create_mainwindow()

    def create_document(self):
        self.document = QMainWindow()
        browser = QWebEngineView()
        relative_html = './doc/build/html/index.html'
        fileurl = QUrl.fromLocalFile(
            QFileInfo(relative_html).absoluteFilePath())
        browser.load(fileurl)
        self.document.setCentralWidget(browser)
        self.document.setWindowTitle("Document")
        self.document.resize(1100, 600)

    def create_mainwindow(self, path: str = None) -> None:
        """
        Create a new window for a project, and append it in the attrbute ``windows``.

        :param path: The absolute path to retrieve project file (*.pkl)
        """
        new_windows = MainWindow(app=self, project_path=path)
        self.windows.append(new_windows)
        new_windows.menutopbar.act_help.triggered.connect(self.show_document)

        new_windows.show()

    def show_document(self):
        self.document.show()


def main():
    print("APP", os.path.dirname(__file__))
    try:
        app = QApplication(sys.argv)
        app.setStyleSheet("""
            QWidget {
                font-family: Arial;
            }
            QMainWindow { 
                background-color: white;
                font-family: Arial;
            }
            QMainWindow QWidget#wg_central{
                background-color: #efefef;
                border: 2px solid #808080;
            }
            QDockWidget QWidget#wg_main {
                border-left: 2px solid #808080;
                border-bottom: 2px solid #808080;
                border-right: 2px solid #808080;
            }
            QMenuBar QMenu {
                padding: 2px 5px
            }
            QTabBar::scroller QToolButton  {
                background-color: white;
            }


        """)
        MyApp()
        sys.exit(app.exec_())

    except Exception as e:
        error_class = e.__class__.__name__
        detail = e.args[0]
        cl, exc, tb = sys.exc_info()
        # print(cl, exc, tb)
        lastCallStack = traceback.extract_tb(tb)[-1]
        fileName = lastCallStack[0]
        lineName = lastCallStack[1]
        funcName = lastCallStack[2]
        print("#########  Error Message   #########\n")
        errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(
            fileName, lineName, funcName, error_class, detail)
        print(errMsg)
        print("\n####################################")


if __name__ == '__main__':
    main()
