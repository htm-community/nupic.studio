from PyQt5 import QtGui, QtCore, QtWidgets
from nupic_studio.ui import Global


class SimulationLegendForm(QtWidgets.QDialog):

    def __init__(self):
        """
        Initializes a new instance of this class.
        """
        QtWidgets.QWidget.__init__(self)
        self.initUI()

    def initUI(self):

        # button_inactive_element
        self.button_inactive_element = QtWidgets.QPushButton()
        self.button_inactive_element.setStyleSheet("background-color: rgb(190, 190, 190)")
        self.button_inactive_element.setEnabled(False)

        # label_inactive_element
        self.label_inactive_element = QtWidgets.QLabel()
        self.label_inactive_element.setText("Inactive")

        # button_falsely_predicted_element
        self.button_falsely_predicted_element = QtWidgets.QPushButton()
        self.button_falsely_predicted_element.setStyleSheet("background-color: rgb(255, 0, 0)")
        self.button_falsely_predicted_element.setEnabled(False)

        # label_falsely_predicted_element
        self.label_falsely_predicted_element = QtWidgets.QLabel()
        self.label_falsely_predicted_element.setText("Falsely Predicted")

        # button_predicted_element
        self.button_predicted_element = QtWidgets.QPushButton()
        self.button_predicted_element.setStyleSheet("background-color: rgb(255, 215, 80)")
        self.button_predicted_element.setEnabled(False)

        # label_predicted_element
        self.label_predicted_element = QtWidgets.QLabel()
        self.label_predicted_element.setText("Predicted")

        # button_active_element
        self.button_active_element = QtWidgets.QPushButton()
        self.button_active_element.setStyleSheet("background-color: rgb(50, 205, 50)")
        self.button_active_element.setEnabled(False)

        # label_active_element
        self.label_active_element = QtWidgets.QLabel()
        self.label_active_element.setText("Active/Connected")

        # button_learning_element
        self.button_learning_element = QtWidgets.QPushButton()
        self.button_learning_element.setStyleSheet("background-color: rgb(125, 255, 0)")
        self.button_learning_element.setEnabled(False)

        # label_learning_element
        self.label_learning_element = QtWidgets.QLabel()
        self.label_learning_element.setText("Learning")

        # button_selected_element
        self.button_selected_element = QtWidgets.QPushButton()
        self.button_selected_element.setStyleSheet("background-color: rgb(0, 0, 255)")
        self.button_selected_element.setEnabled(False)

        # label_selected_element
        self.label_selected_element = QtWidgets.QLabel()
        self.label_selected_element.setText("Selected")

        # layout
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.button_inactive_element, 0, 0)
        layout.addWidget(self.label_inactive_element, 0, 1)
        layout.addWidget(self.button_falsely_predicted_element, 1, 0)
        layout.addWidget(self.label_falsely_predicted_element, 1, 1)
        layout.addWidget(self.button_predicted_element, 2, 0)
        layout.addWidget(self.label_predicted_element, 2, 1)
        layout.addWidget(self.button_active_element, 3, 0)
        layout.addWidget(self.label_active_element, 3, 1)
        layout.addWidget(self.button_learning_element, 4, 0)
        layout.addWidget(self.label_learning_element, 4, 1)
        layout.addWidget(self.button_selected_element, 5, 0)
        layout.addWidget(self.label_selected_element, 5, 1)
        layout.setRowStretch(1, 100)

        # SimulationLegendForm
        self.setLayout(layout)
        self.setWindowTitle("Simulation Legend")
        self.setWindowIcon(QtGui.QIcon(Global.app_path + '/images/logo.ico'))
        self.setMinimumWidth(100)
        self.setMinimumHeight(150)
