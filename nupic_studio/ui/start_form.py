import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from nupic_studio.ui import Global


class StartForm(QtWidgets.QDialog):

    def __init__(self):
        """
        Initializes a new instance of this class.
        """
        QtWidgets.QDialog.__init__(self)
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

        # formLayout
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.button_new)
        layout.addWidget(self.button_open)
        layout.addWidget(self.button_close)

        # StartForm
        self.setLayout(layout)
        self.setWindowTitle("NuPIC Studio")
        self.setWindowIcon(QtGui.QIcon(Global.app_path + '/images/logo.ico'))
        self.resize(350, 50)

    def buttonNew_click(self, event):
        if Global.main_form.newProject():
            Global.main_form.showMaximized()
            self.close()

    def buttonOpen_click(self, event):
        if Global.main_form.openProject():
            Global.main_form.showMaximized()
            self.close()

    def buttonClose_click(self, event):
        sys.exit()
