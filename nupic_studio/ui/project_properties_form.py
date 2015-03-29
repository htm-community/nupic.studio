from PyQt4 import QtGui, QtCore
from nupic_studio.ui import Global

class ProjectPropertiesForm(QtGui.QDialog):

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

    # labelName
    self.labelName = QtGui.QLabel()
    self.labelName.setText("Name")
    self.labelName.setAlignment(QtCore.Qt.AlignRight)

    # textBoxName
    self.textBoxName = QtGui.QLineEdit()

    # labelAuthor
    self.labelAuthor = QtGui.QLabel()
    self.labelAuthor.setText("Author")
    self.labelAuthor.setAlignment(QtCore.Qt.AlignRight)

    # textBoxAuthor
    self.textBoxAuthor = QtGui.QLineEdit()

    # labelDescription
    self.labelDescription = QtGui.QLabel()
    self.labelDescription.setText("Description")
    self.labelDescription.setAlignment(QtCore.Qt.AlignRight)

    # textBoxDescription
    self.textBoxDescription = QtGui.QTextEdit()

    # groupBoxMainLayout
    groupBoxMainLayout = QtGui.QGridLayout()
    groupBoxMainLayout.addWidget(self.labelName, 0, 0)
    groupBoxMainLayout.addWidget(self.textBoxName, 0, 1)
    groupBoxMainLayout.addWidget(self.labelAuthor, 1, 0)
    groupBoxMainLayout.addWidget(self.textBoxAuthor, 1, 1)
    groupBoxMainLayout.addWidget(self.labelDescription, 2, 0)
    groupBoxMainLayout.addWidget(self.textBoxDescription, 2, 1)

    # groupBoxMain
    self.groupBoxMain = QtGui.QGroupBox()
    self.groupBoxMain.setLayout(groupBoxMainLayout)

    # buttonBox
    self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
    self.buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self.__buttonOk_Click)
    self.buttonBox.button(QtGui.QDialogButtonBox.Cancel).clicked.connect(self.__buttonCancel_Click)

    # layout
    layout = QtGui.QVBoxLayout()
    layout.addWidget(self.groupBoxMain)
    layout.addWidget(self.buttonBox)

    # ProjectPropertiesForm
    self.setLayout(layout)
    self.setModal(True)
    self.setWindowTitle("Project Properties")
    self.setWindowIcon(QtGui.QIcon(Global.appPath + '/images/logo.ico'))
    self.resize(450, 200)

  def setControlsValues(self):
    """
    Set controls values from a class instance.
    """

    # Set controls values with project properties
    self.textBoxName.setText(Global.project.name)
    self.textBoxAuthor.setText(Global.project.author)
    self.textBoxDescription.setText(Global.project.description)

  #endregion

  #region Events

  def __buttonOk_Click(self, event):
    name = self.textBoxName.text()
    author = self.textBoxAuthor.text()
    description = self.textBoxDescription.toPlainText()

    # If anything has changed
    if Global.project.name != name or Global.project.author != author or Global.project.description != description:
      # Set project properties with controls values
      Global.project.name = name
      Global.project.author = author
      Global.project.description = description
      self.accept()

    self.close()

  def __buttonCancel_Click(self, event):
    self.reject()
    self.close()

  #endregion
