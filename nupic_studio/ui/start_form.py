import sys
from PyQt4 import QtGui, QtCore
from nupic_studio.ui import Global

class StartForm(QtGui.QDialog):

  #region Constructor

  def __init__(self):
    """
    Initializes a new instance of this class.
    """

    QtGui.QDialog.__init__(self)

    self.initUI()

  #endregion

  #region Methods

  def initUI(self):

    # buttonNew
    self.buttonNew = QtGui.QPushButton()
    self.buttonNew.setText("New Project")
    self.buttonNew.clicked.connect(self.__buttonNew_Click)

    # buttonOpen
    self.buttonOpen = QtGui.QPushButton()
    self.buttonOpen.setText("Open Project")
    self.buttonOpen.clicked.connect(self.__buttonOpen_Click)

    # buttonClose
    self.buttonClose = QtGui.QPushButton()
    self.buttonClose.setText("Close")
    self.buttonClose.clicked.connect(self.__buttonClose_Click)

    # formLayout
    layout = QtGui.QHBoxLayout()
    layout.addWidget(self.buttonNew)
    layout.addWidget(self.buttonOpen)
    layout.addWidget(self.buttonClose)

    # StartForm
    self.setLayout(layout)
    self.setWindowTitle("NuPIC Studio")
    self.setWindowIcon(QtGui.QIcon(Global.appPath + '/images/logo.ico'))
    self.resize(350, 50)

  #endregion

  #region Events

  def __buttonNew_Click(self, event):
    if Global.mainForm.newProject():
      Global.mainForm.showMaximized()
      self.close()

  def __buttonOpen_Click(self, event):
    if Global.mainForm.openProject():
      Global.mainForm.showMaximized()
      self.close()

  def __buttonClose_Click(self, event):
    sys.exit()


  #endregion
