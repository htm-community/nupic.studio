from PyQt5 import QtGui, QtCore, QtWidgets
from nupic_studio.ui import Global

class ProjectPropertiesForm(QtWidgets.QDialog):

    def __init__(self):
        """
        Initializes a new instance of this class.
        """

        QtWidgets.QDialog.__init__(self)

        self.initUI()

    def initUI(self):

        # labelName
        self.labelName = QtWidgets.QLabel()
        self.labelName.setText("Name")
        self.labelName.setAlignment(QtCore.Qt.AlignRight)

        # textBoxName
        self.textBoxName = QtWidgets.QLineEdit()

        # labelAuthor
        self.labelAuthor = QtWidgets.QLabel()
        self.labelAuthor.setText("Author")
        self.labelAuthor.setAlignment(QtCore.Qt.AlignRight)

        # textBoxAuthor
        self.textBoxAuthor = QtWidgets.QLineEdit()

        # labelDescription
        self.labelDescription = QtWidgets.QLabel()
        self.labelDescription.setText("Description")
        self.labelDescription.setAlignment(QtCore.Qt.AlignRight)

        # textBoxDescription
        self.textBoxDescription = QtWidgets.QTextEdit()

        # groupBoxMainLayout
        groupBoxMainLayout = QtWidgets.QGridLayout()
        groupBoxMainLayout.addWidget(self.labelName, 0, 0)
        groupBoxMainLayout.addWidget(self.textBoxName, 0, 1)
        groupBoxMainLayout.addWidget(self.labelAuthor, 1, 0)
        groupBoxMainLayout.addWidget(self.textBoxAuthor, 1, 1)
        groupBoxMainLayout.addWidget(self.labelDescription, 2, 0)
        groupBoxMainLayout.addWidget(self.textBoxDescription, 2, 1)

        # groupBoxMain
        self.groupBoxMain = QtWidgets.QGroupBox()
        self.groupBoxMain.setLayout(groupBoxMainLayout)

        # buttonBox
        self.buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.__buttonOk_Click)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.__buttonCancel_Click)

        # layout
        layout = QtWidgets.QVBoxLayout()
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
