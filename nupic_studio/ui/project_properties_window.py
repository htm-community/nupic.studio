from PyQt5 import QtGui, QtCore, QtWidgets
from nupic_studio.ui import ICON, Global


class ProjectPropertiesWindow(QtWidgets.QDialog):

    def __init__(self):
        """
        Initializes a new instance of this class.
        """
        QtWidgets.QDialog.__init__(self)
        self.initUI()

    def initUI(self):

        # label_name
        self.label_name = QtWidgets.QLabel()
        self.label_name.setText("Name")
        self.label_name.setAlignment(QtCore.Qt.AlignRight)

        # text_box_name
        self.text_box_name = QtWidgets.QLineEdit()

        # label_author
        self.label_author = QtWidgets.QLabel()
        self.label_author.setText("Author")
        self.label_author.setAlignment(QtCore.Qt.AlignRight)

        # text_box_author
        self.text_box_author = QtWidgets.QLineEdit()

        # label_description
        self.label_description = QtWidgets.QLabel()
        self.label_description.setText("Description")
        self.label_description.setAlignment(QtCore.Qt.AlignRight)

        # text_box_description
        self.text_box_description = QtWidgets.QTextEdit()

        # group_box_main_layout
        group_box_main_layout = QtWidgets.QGridLayout()
        group_box_main_layout.addWidget(self.label_name, 0, 0)
        group_box_main_layout.addWidget(self.text_box_name, 0, 1)
        group_box_main_layout.addWidget(self.label_author, 1, 0)
        group_box_main_layout.addWidget(self.text_box_author, 1, 1)
        group_box_main_layout.addWidget(self.label_description, 2, 0)
        group_box_main_layout.addWidget(self.text_box_description, 2, 1)

        # group_box_main
        self.group_box_main = QtWidgets.QGroupBox()
        self.group_box_main.setLayout(group_box_main_layout)

        # button_box
        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.button_box.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.buttonOk_click)
        self.button_box.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.buttonCancel_click)

        # layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.group_box_main)
        layout.addWidget(self.button_box)

        # self
        self.setLayout(layout)
        self.setModal(True)
        self.setWindowTitle("Project Properties")
        self.setWindowIcon(ICON)
        self.resize(450, 200)

    def setControlsValues(self):
        """
        Set controls values from a class instance.
        """

        # Set controls values with project properties
        self.text_box_name.setText(Global.project.name)
        self.text_box_author.setText(Global.project.author)
        self.text_box_description.setText(Global.project.description)

    def buttonOk_click(self, event):
        name = self.text_box_name.text()
        author = self.text_box_author.text()
        description = self.text_box_description.toPlainText()

        # If anything has changed
        if Global.project.name != name or Global.project.author != author or Global.project.description != description:
            # Set project properties with controls values
            Global.project.name = name
            Global.project.author = author
            Global.project.description = description
            self.accept()

        self.close()

    def buttonCancel_click(self, event):
        self.reject()
        self.close()
