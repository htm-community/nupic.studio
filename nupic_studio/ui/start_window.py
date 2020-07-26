import sys
from PyQt5 import QtGui, QtCore, QtWidgets


class StartWindow(QtWidgets.QDialog):

    def __init__(self, main_window):
        """
        Initializes a new instance of this class.
        """
        QtWidgets.QDialog.__init__(self)
        self.main_window = main_window
        self.initUI()

    def initUI(self):

        # button_new
        self.button_new = QtWidgets.QPushButton()
        self.button_new.setText("New Project")
        self.button_new.clicked.connect(self.buttonNew_click)

        # button_open
        self.button_open = QtWidgets.QPushButton()
        self.button_open.setText("Open Project")
        self.button_open.clicked.connect(self.buttonOpen_click)

        # button_close
        self.button_close = QtWidgets.QPushButton()
        self.button_close.setText("Close")
        self.button_close.clicked.connect(self.buttonClose_click)

        # layout
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.button_new)
        layout.addWidget(self.button_open)
        layout.addWidget(self.button_close)

        # self
        self.setLayout(layout)
        self.setWindowTitle("NuPIC Studio")
        self.resize(350, 50)

    def buttonNew_click(self, event):
        if self.main_window.newProject():
            self.main_window.showMaximized()
            self.close()

    def buttonOpen_click(self, event):
        if self.main_window.openProject():
            self.main_window.showMaximized()
            self.close()

    def buttonClose_click(self, event):
        sys.exit()
