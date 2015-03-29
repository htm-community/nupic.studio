from PyQt4 import Qt, QtGui, QtCore
from nupic_studio.ui import Global

class OutputForm(QtGui.QWidget):

  #region Constructor

  def __init__(self):
    """
    Initializes a new instance of this class.
    """

    QtGui.QWidget.__init__(self)

    self.initUI()

  #endregion

  #region Methods

  def initUI(self):

    # textBoxOutput
    self.textBoxOutput = QtGui.QTextEdit()
    self.textBoxOutput.setReadOnly(True)
    self.textBoxOutput.setAlignment(QtCore.Qt.AlignLeft)

    # layout
    layout = QtGui.QHBoxLayout()
    layout.addWidget(self.textBoxOutput)

    # OutputForm
    self.setLayout(layout)
    self.setWindowTitle("Output")
    self.setWindowIcon(QtGui.QIcon(Global.appPath + '/images/logo.ico'))
    self.setMinimumHeight(200)
    self.setMaximumHeight(300)

  def clearControls(self):
    """
    Reset all controls.
    """

    self.textBoxOutput.setText("")

  def addText(self, text):
    """
    Refresh controls for each time step.
    """

    self.textBoxOutput.append(text)
    cursor = self.textBoxOutput.textCursor()
    cursor.movePosition(QtGui.QTextCursor.End)
    self.textBoxOutput.setTextCursor(cursor)
    self.textBoxOutput.ensureCursorVisible()

  #endregion
