import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

# class Example(QWidget):

#     def __init__(self):
#         super(Example, self).__init__()
		
#         self.initUI()
	
#     def initUI(self):
	
#         hbox = QHBoxLayout(self)
			
#         topleft = QFrame()
#         topleft.setFrameShape(QFrame.StyledPanel)
#         bottom = QFrame()
#         bottom.setFrameShape(QFrame.StyledPanel)
			
#         splitter1 = QSplitter(Qt.Horizontal)
#         textedit = QTextEdit()
#         splitter1.addWidget(topleft)
#         splitter1.addWidget(textedit)
#         splitter1.setSizes([100,200])
			
#         splitter2 = QSplitter(Qt.Vertical)
#         splitter2.addWidget(splitter1)
#         splitter2.addWidget(bottom)
			
#         hbox.addWidget(splitter2)
			
#         self.setLayout(hbox)
#         QApplication.setStyle(QStyleFactory.create('Cleanlooks'))
			
#         self.setGeometry(300, 300, 300, 200)
#         self.setWindowTitle('QSplitter demo')
#         self.show()
		
# def main():
#    app = QApplication(sys.argv)
#    ex = Example()
#    sys.exit(app.exec_())
	
# if __name__ == '__main__':
#    main()


# from PyQt5 import QtCore, QtGui
class Window(QWidget):
	def __init__(self):
		QWidget.__init__(self)
		self.splitter = QSplitter(self)
		self.splitter.addWidget(QTextEdit(self))
		self.splitter.addWidget(QTextEdit(self))
		layout = QVBoxLayout(self)
		layout.addWidget(self.splitter)
		handle = self.splitter.handle(1)
		layout = QVBoxLayout()
		layout.setContentsMargins(0, 0, 0, 0)
		button = QToolButton(handle)
		button.setArrowType(QtCore.Qt.LeftArrow)
		button.clicked.connect(
			lambda: self.handleSplitterButton(True))
		layout.addWidget(button)

		button = QToolButton(handle)
		button.setArrowType(QtCore.Qt.RightArrow)
		button.clicked.connect(
			lambda: self.handleSplitterButton(False))
		layout.addWidget(button)
		
		handle.setLayout(layout)

	def handleSplitterButton(self, left=True):
		if not all(self.splitter.sizes()):
			self.splitter.setSizes([1, 1])
		elif left:
			self.splitter.setSizes([0, 1])
		else:
			self.splitter.setSizes([1, 0])

if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = Window()
	window.setGeometry(500, 300, 300, 300)
	window.show()
	sys.exit(app.exec_())