from PyQt5 import QtGui, QtCore, QtWidgets
from nupic_studio.ui import Global

class SimulationLegendForm(QtWidgets.QDialog):

    #region Constructor

    def __init__(self):
        """
        Initializes a new instance of this class.
        """

        QtWidgets.QWidget.__init__(self)

        self.initUI()

    #endregion

    #region Methods

    def initUI(self):

        # buttonInactiveElement
        self.buttonInactiveElement = QtWidgets.QPushButton()
        self.buttonInactiveElement.setStyleSheet("background-color: rgb(190, 190, 190)")
        self.buttonInactiveElement.setEnabled(False)

        # labelInactiveElement
        self.labelInactiveElement = QtWidgets.QLabel()
        self.labelInactiveElement.setText("Inactive")

        # buttonFalselyPredictedElement
        self.buttonFalselyPredictedElement = QtWidgets.QPushButton()
        self.buttonFalselyPredictedElement.setStyleSheet("background-color: rgb(255, 0, 0)")
        self.buttonFalselyPredictedElement.setEnabled(False)

        # labelFalselyPredictedElement
        self.labelFalselyPredictedElement = QtWidgets.QLabel()
        self.labelFalselyPredictedElement.setText("Falsely Predicted")

        # buttonPredictedElement
        self.buttonPredictedElement = QtWidgets.QPushButton()
        self.buttonPredictedElement.setStyleSheet("background-color: rgb(255, 215, 80)")
        self.buttonPredictedElement.setEnabled(False)

        # labelPredictedElement
        self.labelPredictedElement = QtWidgets.QLabel()
        self.labelPredictedElement.setText("Predicted")

        # buttonActiveElement
        self.buttonActiveElement = QtWidgets.QPushButton()
        self.buttonActiveElement.setStyleSheet("background-color: rgb(50, 205, 50)")
        self.buttonActiveElement.setEnabled(False)

        # labelActiveElement
        self.labelActiveElement = QtWidgets.QLabel()
        self.labelActiveElement.setText("Active/Connected")

        # buttonLearningElement
        self.buttonLearningElement = QtWidgets.QPushButton()
        self.buttonLearningElement.setStyleSheet("background-color: rgb(125, 255, 0)")
        self.buttonLearningElement.setEnabled(False)

        # labelLearningElement
        self.labelLearningElement = QtWidgets.QLabel()
        self.labelLearningElement.setText("Learning")

        # buttonSelectedElement
        self.buttonSelectedElement = QtWidgets.QPushButton()
        self.buttonSelectedElement.setStyleSheet("background-color: rgb(0, 0, 255)")
        self.buttonSelectedElement.setEnabled(False)

        # labelSelectedElement
        self.labelSelectedElement = QtWidgets.QLabel()
        self.labelSelectedElement.setText("Selected")

        # layout
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.buttonInactiveElement, 0, 0)
        layout.addWidget(self.labelInactiveElement, 0, 1)
        layout.addWidget(self.buttonFalselyPredictedElement, 1, 0)
        layout.addWidget(self.labelFalselyPredictedElement, 1, 1)
        layout.addWidget(self.buttonPredictedElement, 2, 0)
        layout.addWidget(self.labelPredictedElement, 2, 1)
        layout.addWidget(self.buttonActiveElement, 3, 0)
        layout.addWidget(self.labelActiveElement, 3, 1)
        layout.addWidget(self.buttonLearningElement, 4, 0)
        layout.addWidget(self.labelLearningElement, 4, 1)
        layout.addWidget(self.buttonSelectedElement, 5, 0)
        layout.addWidget(self.labelSelectedElement, 5, 1)
        layout.setRowStretch(1, 100)

        # SimulationLegendForm
        self.setLayout(layout)
        self.setWindowTitle("Simulation Legend")
        self.setWindowIcon(QtGui.QIcon(Global.appPath + '/images/logo.ico'))
        self.setMinimumWidth(100)
        self.setMinimumHeight(150)

    #endregion
