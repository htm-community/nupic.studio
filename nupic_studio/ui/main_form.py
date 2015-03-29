import sys
import time
import webbrowser
from PyQt4 import QtGui, QtCore
from nupic_studio import MachineState
from nupic_studio.htm import maxPreviousSteps, maxPreviousStepsWithInference
from nupic_studio.ui import Global
from nupic_studio.ui.project_properties_form import ProjectPropertiesForm

class MainForm(QtGui.QMainWindow):

  #region Constructor

  def __init__(self):
    """
    Initializes a new instance of this class.
    """

    QtGui.QMainWindow.__init__(self)

    #region  Instance fields

    self._pendingProjectChanges = False
    self._numStepsPending = 0

    #endregion

    self.initUI()

  #endregion

  #region Methods

  def initUI(self):

    # menuFileNew
    self.menuFileNew = QtGui.QAction(self)
    self.menuFileNew.setText("&New Project")
    self.menuFileNew.setShortcut('Ctrl+N')
    self.menuFileNew.triggered.connect(self.newProject)

    # menuFileOpen
    self.menuFileOpen = QtGui.QAction(self)
    self.menuFileOpen.setText("&Open  Project")
    self.menuFileOpen.setShortcut('Ctrl+O')
    self.menuFileOpen.triggered.connect(self.openProject)

    # menuFileSave
    self.menuFileSave = QtGui.QAction(self)
    self.menuFileSave.setText("&Save Project")
    self.menuFileSave.setShortcut('Ctrl+S')
    self.menuFileSave.triggered.connect(self.saveProject)

    # menuFileExit
    self.menuFileExit = QtGui.QAction(self)
    self.menuFileExit.setText("&Exit")
    self.menuFileExit.setShortcut('Ctrl+Q')
    self.menuFileExit.triggered.connect(self.__menuFileExit_Click)

    # menuFile
    self.menuFile = QtGui.QMenu()
    self.menuFile.addAction(self.menuFileNew)
    self.menuFile.addAction(self.menuFileOpen)
    self.menuFile.addAction(self.menuFileSave)
    self.menuFile.addSeparator()
    self.menuFile.addAction(self.menuFileExit)
    self.menuFile.setTitle("&File")

    # menuViewArchitecture
    self.menuViewArchitecture = QtGui.QAction(self)
    self.menuViewArchitecture.setText("&Network Architecture")
    self.menuViewArchitecture.triggered.connect(self.__menuViewArchitecture_Click)

    # menuViewSimulation
    self.menuViewSimulation = QtGui.QAction(self)
    self.menuViewSimulation.setText("&Simulation")
    self.menuViewSimulation.triggered.connect(self.__menuViewSimulation_Click)

    # menuViewNodeInformation
    self.menuViewNodeInformation = QtGui.QAction(self)
    self.menuViewNodeInformation.setText("Node &Information")
    self.menuViewNodeInformation.triggered.connect(self.__menuViewNodeInformation_Click)

    # menuViewOutput
    self.menuViewOutput = QtGui.QAction(self)
    self.menuViewOutput.setText("&Output")
    self.menuViewOutput.triggered.connect(self.__menuViewOutput_Click)

    # menuViewToolWindows
    self.menuViewToolWindows = QtGui.QMenu()
    self.menuViewToolWindows.addAction(self.menuViewArchitecture)
    self.menuViewToolWindows.addAction(self.menuViewNodeInformation)
    self.menuViewToolWindows.addAction(self.menuViewSimulation)
    self.menuViewToolWindows.addAction(self.menuViewOutput)
    self.menuViewToolWindows.setTitle("Tool &Windows")

    # menuView
    self.menuView = QtGui.QMenu()
    self.menuView.addMenu(self.menuViewToolWindows)
    self.menuView.setTitle("&View")

    # menuEdit
    self.menuEdit = QtGui.QMenu()
    self.menuEdit.setTitle("&Edit")

    # menuProjectProperties
    self.menuProjectProperties = QtGui.QAction(self)
    self.menuProjectProperties.setText("Properties...")
    self.menuProjectProperties.triggered.connect(self.__menuProjectProperties_Click)

    # menuProject
    self.menuProject = QtGui.QMenu()
    self.menuProject.addAction(self.menuProjectProperties)
    self.menuProject.setTitle("&Project")

    # menuTools
    self.menuTools = QtGui.QMenu()
    self.menuTools.setTitle("&Tools")

    # menuUserWiki
    self.menuUserWiki = QtGui.QAction(self)
    self.menuUserWiki.setText("User Wiki")
    self.menuUserWiki.triggered.connect(self.__menuUserWiki_Click)

    # menuGoToWebsite
    self.menuGoToWebsite = QtGui.QAction(self)
    self.menuGoToWebsite.setText("Project Website")
    self.menuGoToWebsite.triggered.connect(self.__menuGoToWebsite_Click)

    # menuAbout
    self.menuAbout = QtGui.QAction(self)
    self.menuAbout.setText("About")
    self.menuAbout.triggered.connect(self.__menuAbout_Click)

    # menuHelp
    self.menuHelp = QtGui.QMenu()
    self.menuHelp.addAction(self.menuUserWiki)
    self.menuHelp.addAction(self.menuGoToWebsite)
    self.menuHelp.addAction(self.menuAbout)
    self.menuHelp.setTitle("&Help")

    # menuMain
    self.menuMain = self.menuBar()
    self.menuMain.addMenu(self.menuFile)
    self.menuMain.addMenu(self.menuView)
    self.menuMain.addMenu(self.menuProject)
    self.menuMain.addMenu(self.menuHelp)

    # buttonInitHTM
    self.buttonInitHTM = QtGui.QAction(self)
    self.buttonInitHTM.setEnabled(False)
    self.buttonInitHTM.setIcon(QtGui.QIcon(Global.appPath + '/images/buttonInitializeHTM.png'))
    self.buttonInitHTM.setToolTip("Initialize simulation")
    self.buttonInitHTM.triggered.connect(self.__buttonInitHTM_Click)

    # buttonStepHTM
    self.buttonStepHTM = QtGui.QAction(self)
    self.buttonStepHTM.setEnabled(False)
    self.buttonStepHTM.setIcon(QtGui.QIcon(Global.appPath + '/images/buttonStepHTM.png'))
    self.buttonStepHTM.setToolTip("Forward one time step")
    self.buttonStepHTM.triggered.connect(self.__buttonStepHTM_Click)

    # buttonMultipleStepsHTM
    self.buttonMultipleStepsHTM = QtGui.QAction(self)
    self.buttonMultipleStepsHTM.setEnabled(False)
    self.buttonMultipleStepsHTM.setIcon(QtGui.QIcon(Global.appPath + '/images/buttonStepFastHTM.png'))
    self.buttonMultipleStepsHTM.setToolTip("Forward a specific number of time steps")
    self.buttonMultipleStepsHTM.triggered.connect(self.__buttonMultipleStepsHTM_Click)

    # buttonStopHTM
    self.buttonStopHTM = QtGui.QAction(self)
    self.buttonStopHTM.setEnabled(False)
    self.buttonStopHTM.setIcon(QtGui.QIcon(Global.appPath + '/images/buttonStopHTM.png'))
    self.buttonStopHTM.setToolTip("Stop simulation")
    self.buttonStopHTM.triggered.connect(self.__buttonStopHTM_Click)

    # textBoxStep
    self.textBoxStep = QtGui.QLineEdit()
    self.textBoxStep.setEnabled(False)
    self.textBoxStep.setAlignment(QtCore.Qt.AlignRight)
    self.textBoxStep.setFixedSize(QtCore.QSize(80, 20))

    # sliderStep
    self.sliderStep = QtGui.QSlider()
    self.sliderStep.setEnabled(False)
    self.sliderStep.setOrientation(QtCore.Qt.Horizontal)
    self.sliderStep.setSingleStep(1)
    self.sliderStep.setRange(0, maxPreviousSteps - 1)
    self.sliderStep.setValue(maxPreviousSteps - 1)
    self.sliderStep.valueChanged.connect(self.__sliderStep_ValueChanged)

    # toolBar
    self.toolBar = QtGui.QToolBar()
    self.toolBar.addAction(self.buttonInitHTM)
    self.toolBar.addAction(self.buttonStepHTM)
    self.toolBar.addAction(self.buttonMultipleStepsHTM)
    self.toolBar.addAction(self.buttonStopHTM)
    self.toolBar.addWidget(self.textBoxStep)
    self.toolBar.addWidget(self.sliderStep)

    # dockArchitectureForm
    self.dockArchitectureForm = QtGui.QDockWidget()
    self.dockArchitectureForm.setWidget(Global.architectureForm)
    self.dockArchitectureForm.setWindowTitle(Global.architectureForm.windowTitle())

    # dockSimulationForm
    self.dockSimulationForm = QtGui.QDockWidget()
    self.dockSimulationForm.setWidget(Global.simulationForm)
    self.dockSimulationForm.setWindowTitle(Global.simulationForm.windowTitle())

    # dockNodeInformationForm
    self.dockNodeInformationForm = QtGui.QDockWidget()
    self.dockNodeInformationForm.setWidget(Global.nodeInformationForm)
    self.dockNodeInformationForm.setWindowTitle(Global.nodeInformationForm.windowTitle())

    # dockOutputForm
    self.dockOutputForm = QtGui.QDockWidget()
    self.dockOutputForm.setWidget(Global.outputForm)
    self.dockOutputForm.setWindowTitle(Global.outputForm.windowTitle())

    # MainForm
    self.addToolBar(self.toolBar)
    self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, self.dockArchitectureForm)
    self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.dockSimulationForm)
    self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.dockNodeInformationForm)
    self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, self.dockOutputForm)
    self.tabifyDockWidget(self.dockNodeInformationForm, self.dockOutputForm)
    self.setCentralWidget(self.dockSimulationForm)
    self.setWindowTitle("NuPIC Studio")
    self.setWindowIcon(QtGui.QIcon(Global.appPath + '/images/logo.ico'))

  def __cleanUp(self):
    """
    Prepare UI to load a new configuration.
    """

    self.__enableSimulationButtons(False)
    self.__enableSteeringButtons(False)

    # Update architecture controls
    Global.architectureForm.designPanel.topRegion = Global.project.network.nodes[0]
    Global.architectureForm.designPanel.selectedNode = Global.project.network.nodes[0]
    Global.architectureForm.designPanel.repaint()
    Global.architectureForm.updateCode()

    # Reset the controls
    self.clearControls()

  def __enableSimulationButtons(self, enable):
    """
    Enables or disables controls related to simulation.
    """

    Global.simulationInitialized = enable
    self.buttonInitHTM.setEnabled(not enable)
    if not enable:
      self.textBoxStep.setText("")
      self.sliderStep.setEnabled(False)
      self.sliderStep.setValue(self.sliderStep.maximum())

  def __enableSteeringButtons(self, enable):
    """
    Enables or disables buttons in toolbar.
    """

    self.buttonStepHTM.setEnabled(enable)
    self.buttonMultipleStepsHTM.setEnabled(enable)
    self.buttonStopHTM.setEnabled(enable)

  def clearControls(self):
    """
    Reset the controls.
    """

    Global.simulationForm.clearControls()
    Global.outputForm.clearControls()
    Global.nodeInformationForm.clearControls()

  def refreshControls(self):
    """
    Refresh controls for each time step.
    """

    if Global.simulationInitialized :
      maxTime = Global.currStep + 1
      selStep = maxTime - (self.sliderStep.maximum() - self.sliderStep.value())
      self.textBoxStep.setText(str(selStep) + "/" + str(maxTime))
    else:
      self.textBoxStep.setText("")

    if self.dockSimulationForm.isVisible():
      Global.simulationForm.refreshControls()
    if self.dockNodeInformationForm.isVisible():
      Global.nodeInformationForm.refreshControls()

  def markProjectChanges(self, hasChanges):
    """
    Provides an UI reaction to any project changes or a new or saved unchanged project.
    """

    self._pendingProjectChanges = hasChanges
    self.menuFileSave.setEnabled(hasChanges)

  def __checkCurrentConfigChanges(self):
    """
    Checks if the current file has changed.
    """

    result = QtGui.QMessageBox.No

    # If changes happened, ask to user if he wish saves them
    if self._pendingProjectChanges:
      result = QtGui.QMessageBox.question(self, "Question", "Current project has changed. Do you want save these changes?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No, QtGui.QMessageBox.Cancel)
      if result == QtGui.QMessageBox.Yes:
        self.saveProject()

    return result

  def newProject(self):
    """
    Creates a new project.
    """

    # Check if the current project has changed before continue operation
    if self.__checkCurrentConfigChanges() != QtGui.QMessageBox.Cancel:
      # Create new project
      Global.project.new()

      # Initialize project state
      self.setWindowTitle(Global.project.name + " - NuPIC Studio")
      self.markProjectChanges(False)
      self.__cleanUp()

      return True

    return False

  def openProject(self):
    """
    Open an existing project
    """

    # Check if the current project has changed before continue operation
    if self.__checkCurrentConfigChanges() != QtGui.QMessageBox.Cancel:

      # Ask user for an existing file
      selectedFile = str(QtGui.QFileDialog().getOpenFileName(self, "Open Project", Global.appPath + '/projects', "NuPIC project files (*.nuproj)"))

      # If file exists, continue operation
      if selectedFile != '':
        # Open the selected project
        Global.project.open(selectedFile)

        # Initialize project state
        self.setWindowTitle(Global.project.name + " - [" + Global.project.fileName + "] - NuPIC Studio")
        self.markProjectChanges(False)
        self.__cleanUp()

        return True

    return False

  def saveProject(self):
    """
    Save the current project
    """

    # If current project is new, ask user for valid file
    fileName = Global.project.fileName
    if fileName == '':
      # Ask user for valid file
      selectedFile = str(QtGui.QFileDialog().getSaveFileName(self, "Save Project", Global.appPath + '/projects', "NuPIC project files (*.nuproj)"))

      # If file exists, continue operation
      if selectedFile != '':
        fileName = selectedFile

    # If file is Ok, continue operation
    if fileName != '':
      # Save to the selected location
      Global.project.save(fileName)

      # Initialize project state
      self.setWindowTitle(Global.project.name + " - [" + Global.project.fileName + "] - NuPIC Studio")
      self.markProjectChanges(False)

      return True

    return False

  def stopSimulation(self):

    # Disable relevant buttons to reset
    self.__enableSteeringButtons(False)
    self.__enableSimulationButtons(False)

    # Reset controls
    self.clearControls()

  #endregion

  #region Events

  #region Form

  def closeEvent(self, event):
    if self.__checkCurrentConfigChanges() == QtGui.QMessageBox.Cancel:
      event.ignore()
    else:
      if self.buttonStopHTM.isEnabled():
        self.stopSimulation()
      sys.exit()

  #endregion

  #region Menus

  def __menuFileExit_Click(self, event):
    self.close()

  def __menuProjectProperties_Click(self, event):
    # Open Project properties form
    projectPropertiesForm = ProjectPropertiesForm()
    projectPropertiesForm.setControlsValues()
    dialogResult = projectPropertiesForm.exec_()

    if dialogResult == QtGui.QDialog.Accepted:
      Global.mainForm.markProjectChanges(True)

  def __menuViewArchitecture_Click(self, event):
    self.dockArchitectureForm.show()

  def __menuViewSimulation_Click(self, event):
    self.dockSimulationForm.show()
    Global.simulationForm.refreshControls()

  def __menuViewNodeInformation_Click(self, event):
    self.dockNodeInformationForm.show()
    Global.nodeInformationForm.refreshControls()

  def __menuViewOutput_Click(self, event):
    self.dockOutputForm.show()

  def __menuUserWiki_Click(self, event):
    webbrowser.open('https://github.com/nupic-community/nupic.studio/wiki')

  def __menuGoToWebsite_Click(self, event):
    webbrowser.open('https://github.com/nupic-community/nupic.studio')

  def __menuAbout_Click(self, event):
    QtGui.QMessageBox.information(self, "Information", "v. " + Global.version + "\nGet more info at our home page.")

  #endregion

  #region Toolbar

  def __buttonInitHTM_Click(self, event):
    """
    Initializes the HTM-Network by creating the htm-controller to connect to events database
    """

    # Initialize the network starting from top region.
    startTime = time.time()
    endTime = time.time()
    initialized = Global.project.network.initialize()

    if initialized:

      # Initialize time steps parameters
      Global.currStep = 0
      Global.selStep = 0
      Global.timeStepsPredictionsChart = MachineState(0, maxPreviousStepsWithInference)

      Global.outputForm.addText("Initialization: " + "{0:.3f}".format(endTime - startTime) + " secs")
      Global.outputForm.addText("")
      Global.outputForm.addText("Step\tTime (secs)\tAccuracy (%)")

      # Perfoms actions related to time step progression.
      startTime = time.time()
      Global.project.network.nextStep()
      Global.project.network.calculateStatistics()
      endTime = time.time()
      Global.outputForm.addText(str(Global.currStep + 1) + "\t{0:.3f}".format(endTime - startTime) + "\t{0:.3f}".format(Global.project.network.statsPrecisionRate))

      # Disable relevant buttons:
      self.__enableSteeringButtons(True)
      self.__enableSimulationButtons(True)

      # Update controls
      Global.simulationForm.topRegion = Global.project.network.nodes[0]
      Global.simulationForm.initializeControls()
      self.refreshControls()

  def __buttonStepHTM_Click(self, event):
    """
    Performs a single simulation step.
    """

    # Update time steps parameters
    Global.currStep += 1
    if Global.currStep >= (maxPreviousSteps - 1):
      self.sliderStep.setEnabled(True)
    Global.selStep = self.sliderStep.maximum() - self.sliderStep.value()
    Global.timeStepsPredictionsChart.rotate()
    Global.timeStepsPredictionsChart.setForCurrStep(Global.currStep)

    # Perfoms actions related to time step progression.
    startTime = time.time()
    Global.project.network.nextStep()
    Global.project.network.calculateStatistics()
    endTime = time.time()
    Global.outputForm.addText(str(Global.currStep + 1) + "\t{0:.3f}".format(endTime - startTime) + "\t{0:.3f}".format(Global.project.network.statsPrecisionRate))

    # Update controls
    self.refreshControls()

  def __buttonMultipleStepsHTM_Click(self, event):
    """
    Performs full HTM simulation.
    """

    # Get number of steps to perform simulation
    self._numStepsPending = -1
    enteredInteger, ok = QtGui.QInputDialog.getInt(self, "Input Dialog", "Enter number of steps:")
    if ok:
      if enteredInteger < 2:
        QtGui.QMessageBox.warning(self, "Warning", "Invalid value specified!")
      else:
        self._numStepsPending = enteredInteger

    while self._numStepsPending > 0:
      self.__buttonStepHTM_Click(event)
      Global.app.processEvents()
      self._numStepsPending -= 1

  def __buttonStopHTM_Click(self, event):
    # If multiple steps processing is running just stop the loop
    # otherwise, ask user to stop the simulation
    if self._numStepsPending > 0:
      self._numStepsPending = 0
    else:
      dialogResult = QtGui.QMessageBox.question(self, "Question", "Current simulation (learning) will stop!\r\nDo you want proceed?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
      if dialogResult == QtGui.QMessageBox.Yes:
        self.stopSimulation()

  def __sliderStep_ValueChanged(self, value):
    Global.selStep = Global.selStep = self.sliderStep.maximum() - self.sliderStep.value()
    self.refreshControls()

  #endregion

  #endregion
