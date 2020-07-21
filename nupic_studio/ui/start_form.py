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

        # buttonNew
        self.buttonNew = QtWidgets.QPushButton()
        self.buttonNew.setText("New Project")
        self.buttonNew.clicked.connect(self.__buttonNew_click)

        # buttonOpen
        self.buttonOpen = QtWidgets.QPushButton()
        self.buttonOpen.setText("Open Project")
        self.buttonOpen.clicked.connect(self.__buttonOpen_click)

        # buttonClose
        self.buttonClose = QtWidgets.QPushButton()
        self.buttonClose.setText("Close")
        self.buttonClose.clicked.connect(self.__buttonClose_click)

        # formLayout
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.buttonNew)
        layout.addWidget(self.buttonOpen)
        layout.addWidget(self.buttonClose)

        # StartForm
        self.setLayout(layout)
        self.setWindowTitle("NuPIC Studio")
        self.setWindowIcon(QtGui.QIcon(Global.appPath + '/images/logo.ico'))
        self.resize(350, 50)

    def __buttonNew_click(self, event):
        if Global.mainForm.newProject():
            Global.mainForm.showMaximized()
            self.close()

    def __buttonOpen_click(self, event):
        if Global.mainForm.openProject():
            Global.mainForm.showMaximized()
            self.close()

    def __buttonClose_click(self, event):
        sys.exit()

