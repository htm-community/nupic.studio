from PyQt5 import QtGui, QtCore, QtWidgets
from nupic_studio.ui import Global


class OutputWindow(QtWidgets.QWidget):

    def __init__(self):
        """
        Initializes a new instance of this class.
        """
        QtWidgets.QWidget.__init__(self)
        self.initUI()

    def initUI(self):

        # text_box_output
        self.text_box_output = QtWidgets.QTextEdit()
        self.text_box_output.setReadOnly(True)
        self.text_box_output.setAlignment(QtCore.Qt.AlignLeft)

        # layout
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.text_box_output)

        # self
        self.setLayout(layout)
        self.setWindowTitle("Output")
        self.setWindowIcon(QtGui.QIcon(Global.app_path + '/images/logo.ico'))
        self.setMinimumHeight(200)
        self.setMaximumHeight(300)

    def clearControls(self):
        """
        Reset all controls.
        """
        self.text_box_output.setText("")

    def addText(self, text):
        """
        Refresh controls for each time step.
        """
        self.text_box_output.append(text)
        cursor = self.text_box_output.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        self.text_box_output.setTextCursor(cursor)
        self.text_box_output.ensureCursorVisible()
