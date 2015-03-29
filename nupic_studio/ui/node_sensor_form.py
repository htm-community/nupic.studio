import copy
from PyQt4 import QtGui, QtCore
from nupic_studio.htm.node_sensor import DataSourceType, PredictionsMethod
from nupic_studio.ui import Global
from nupic_studio.ui.node_sensor_encoding_form import EncodingForm

class SensorForm(QtGui.QDialog):

  #region Constructor

  def __init__(self):
    """
    Initializes a new instance of this class.
    """

    QtGui.QDialog.__init__(self)

    self.initUI()

    #region Instance fields

    self.encodings = []
    """Temporary list of encodings that is being edited"""

    self.encodingsChanged = False
    """Flag to indicate if encodings list was edited"""

    #endregion

  #endregion

  #region Methods

  def initUI(self):

    # labelSensorWidth
    self.labelSensorWidth = QtGui.QLabel()
    self.labelSensorWidth.setText("Sensor Width")
    self.labelSensorWidth.setAlignment(QtCore.Qt.AlignRight)

    # spinnerSensorWidth
    self.spinnerSensorWidth = QtGui.QSpinBox()
    self.spinnerSensorWidth.setAlignment(QtCore.Qt.AlignRight)
    self.spinnerSensorWidth.setToolTip("Number of output bits in the X direction for this sensor.")
    self.spinnerSensorWidth.setMaximum(1000)
    self.spinnerSensorWidth.setEnabled(not Global.simulationInitialized)

    # labelSensorHeight
    self.labelSensorHeight = QtGui.QLabel()
    self.labelSensorHeight.setText("Sensor Height")
    self.labelSensorHeight.setAlignment(QtCore.Qt.AlignRight)

    # spinnerSensorHeight
    self.spinnerSensorHeight = QtGui.QSpinBox()
    self.spinnerSensorHeight.setAlignment(QtCore.Qt.AlignRight)
    self.spinnerSensorHeight.setToolTip("Number of output bits in the Y direction for this sensor.")
    self.spinnerSensorHeight.setMaximum(1000)
    self.spinnerSensorHeight.setEnabled(not Global.simulationInitialized)

    # radioButtonDataSourceFile
    self.radioButtonDataSourceFile = QtGui.QRadioButton()
    self.radioButtonDataSourceFile.setText("File")
    self.radioButtonDataSourceFile.toggled.connect(self.__radioButtonDataSource_Click)

    # labelFile
    self.labelFile = QtGui.QLabel()
    self.labelFile.setText("File:")
    self.labelFile.setAlignment(QtCore.Qt.AlignRight)

    # textBoxFile
    self.textBoxFile = QtGui.QLineEdit()

    # buttonBrowseFile
    self.buttonBrowseFile = QtGui.QPushButton()
    self.buttonBrowseFile.setText("Browse...")
    self.buttonBrowseFile.clicked.connect(self.__buttonBrowseFile_Click)

    # radioButtonDataSourceDatabase
    self.radioButtonDataSourceDatabase = QtGui.QRadioButton()
    self.radioButtonDataSourceDatabase.setText("Database")
    self.radioButtonDataSourceDatabase.toggled.connect(self.__radioButtonDataSource_Click)

    # labelDatabaseConnectionString
    self.labelDatabaseConnectionString = QtGui.QLabel()
    self.labelDatabaseConnectionString.setText("Connection String:")
    self.labelDatabaseConnectionString.setAlignment(QtCore.Qt.AlignRight)

    # textBoxDatabaseConnectionString
    self.textBoxDatabaseConnectionString = QtGui.QLineEdit()

    # labelDatabaseTable
    self.labelDatabaseTable = QtGui.QLabel()
    self.labelDatabaseTable.setText("Table:")
    self.labelDatabaseTable.setAlignment(QtCore.Qt.AlignRight)

    # textBoxDatabaseTable
    self.textBoxDatabaseTable = QtGui.QLineEdit()

    # groupBoxDataSourceTypeLayout
    groupBoxDataSourceTypeLayout = QtGui.QGridLayout()
    groupBoxDataSourceTypeLayout.addWidget(self.radioButtonDataSourceFile, 0, 0)
    groupBoxDataSourceTypeLayout.addWidget(self.labelFile, 1, 0)
    groupBoxDataSourceTypeLayout.addWidget(self.textBoxFile, 1, 1)
    groupBoxDataSourceTypeLayout.addWidget(self.buttonBrowseFile, 2, 1)
    groupBoxDataSourceTypeLayout.addWidget(self.radioButtonDataSourceDatabase, 3, 0)
    groupBoxDataSourceTypeLayout.addWidget(self.labelDatabaseConnectionString, 4, 0)
    groupBoxDataSourceTypeLayout.addWidget(self.textBoxDatabaseConnectionString, 4, 1)
    groupBoxDataSourceTypeLayout.addWidget(self.labelDatabaseTable, 5, 0)
    groupBoxDataSourceTypeLayout.addWidget(self.textBoxDatabaseTable, 5, 1)

    # groupBoxDataSourceType
    self.groupBoxDataSourceType = QtGui.QGroupBox()
    self.groupBoxDataSourceType.setLayout(groupBoxDataSourceTypeLayout)
    self.groupBoxDataSourceType.setTitle("Data Source Type")
    self.groupBoxDataSourceType.setEnabled(not Global.simulationInitialized)

    # labelPredictionsMethod
    self.labelPredictionsMethod = QtGui.QLabel()
    self.labelPredictionsMethod.setText("Predictions Method:")
    self.labelPredictionsMethod.setAlignment(QtCore.Qt.AlignRight)

    # comboBoxPredictionsMethod
    self.comboBoxPredictionsMethod = QtGui.QComboBox()
    self.comboBoxPredictionsMethod.addItem(PredictionsMethod.reconstruction)
    self.comboBoxPredictionsMethod.addItem(PredictionsMethod.classification)
    self.comboBoxPredictionsMethod.setEnabled(not Global.simulationInitialized)

    # buttonNewEncoding
    self.buttonNewEncoding = QtGui.QPushButton()
    self.buttonNewEncoding.setText("New...")
    self.buttonNewEncoding.clicked.connect(self.__buttonNewEncoding_Click)
    self.buttonNewEncoding.setEnabled(not Global.simulationInitialized)

    # buttonEditEncoding
    self.buttonEditEncoding = QtGui.QPushButton()
    self.buttonEditEncoding.setText("Edit...")
    self.buttonEditEncoding.clicked.connect(self.__buttonEditEncoding_Click)
    self.buttonEditEncoding.setEnabled(not Global.simulationInitialized)

    # buttonDeleteEncoding
    self.buttonDeleteEncoding = QtGui.QPushButton()
    self.buttonDeleteEncoding.setText("Delete")
    self.buttonDeleteEncoding.clicked.connect(self.__buttonDeleteEncoding_Click)
    self.buttonDeleteEncoding.setEnabled(not Global.simulationInitialized)

    # listBoxEncodings
    self.listBoxEncodings = QtGui.QListWidget()
    self.listBoxEncodings.setEnabled(not Global.simulationInitialized)

    # encodingsButtonsLayout
    encodingsButtonsLayout = QtGui.QHBoxLayout()
    encodingsButtonsLayout.addWidget(self.buttonNewEncoding)
    encodingsButtonsLayout.addWidget(self.buttonEditEncoding)
    encodingsButtonsLayout.addWidget(self.buttonDeleteEncoding)

    # groupBoxEncodingsLayout
    groupBoxEncodingsLayout = QtGui.QVBoxLayout()
    groupBoxEncodingsLayout.addLayout(encodingsButtonsLayout)
    groupBoxEncodingsLayout.addWidget(self.listBoxEncodings)

    # groupBoxEncodings
    self.groupBoxEncodings = QtGui.QGroupBox()
    self.groupBoxEncodings.setLayout(groupBoxEncodingsLayout)
    self.groupBoxEncodings.setTitle("Encodings")

    # groupBoxMainLayout
    groupBoxMainLayout = QtGui.QGridLayout()
    groupBoxMainLayout.addWidget(self.labelSensorWidth, 0, 0)
    groupBoxMainLayout.addWidget(self.spinnerSensorWidth, 0, 1)
    groupBoxMainLayout.addWidget(self.labelSensorHeight, 1, 0)
    groupBoxMainLayout.addWidget(self.spinnerSensorHeight, 1, 1)
    groupBoxMainLayout.addWidget(self.groupBoxDataSourceType, 2, 1)
    groupBoxMainLayout.addWidget(self.labelPredictionsMethod, 3, 0)
    groupBoxMainLayout.addWidget(self.comboBoxPredictionsMethod, 3, 1)
    groupBoxMainLayout.addWidget(self.groupBoxEncodings, 4, 1)

    # groupBoxMain
    self.groupBoxMain = QtGui.QGroupBox()
    self.groupBoxMain.setLayout(groupBoxMainLayout)

    # buttonBox
    self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
    self.buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self.__buttonOk_Click)
    self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(not Global.simulationInitialized)
    self.buttonBox.button(QtGui.QDialogButtonBox.Cancel).clicked.connect(self.__buttonCancel_Click)

    # layout
    layout = QtGui.QVBoxLayout()
    layout.addWidget(self.groupBoxMain)
    layout.addWidget(self.buttonBox)

    # SensorForm
    self.setLayout(layout)
    self.setModal(True)
    self.setWindowTitle("Sensor Properties")
    self.setWindowIcon(QtGui.QIcon(Global.appPath + '/images/logo.ico'))
    self.resize(400, 200)

  def setControlsValues(self):
    """
    Set controls values from a class instance.
    """

    # Set controls value with sensor params
    node = Global.architectureForm.designPanel.underMouseNode
    self.spinnerSensorWidth.setValue(node.width)
    self.spinnerSensorHeight.setValue(node.height)

    if node.dataSourceType == DataSourceType.file:
      self.radioButtonDataSourceFile.setChecked(True)
      self.textBoxFile.setText(node.fileName)
    elif node.dataSourceType == DataSourceType.database:
      self.radioButtonDataSourceDatabase.setChecked(True)
      self.textBoxDatabaseConnectionString.setText(node.databaseConnectionString)
      self.textBoxDatabaseTable.setText(node.databaseTable)

    self.comboBoxPredictionsMethod.setCurrentIndex(self.comboBoxPredictionsMethod.findText(node.predictionsMethod, QtCore.Qt.MatchFixedString))

    self.encodings = copy.deepcopy(node.encodings)
    self.__updateEncodingsListBox()

  def __updateEncodingsListBox(self):

    # Update the list box with the updated encodings
    self.listBoxEncodings.clear()
    for encoding in self.encodings:
      name = encoding.encoderFieldName.split('.')[0]
      self.listBoxEncodings.addItem(name)

    # Update controls according to list state
    if self.listBoxEncodings.count() > 0:
      if self.listBoxEncodings.currentRow() == -1:
        self.listBoxEncodings.setCurrentRow(0)
      self.buttonEditEncoding.setEnabled(not Global.simulationInitialized)
      self.buttonDeleteEncoding.setEnabled(not Global.simulationInitialized)
    else:
      self.buttonEditEncoding.setEnabled(False)
      self.buttonDeleteEncoding.setEnabled(False)

  #endregion

  #region Events

  def __buttonOk_Click(self, event):
    """
    Check if values changed and save the,.
    """

    if self.radioButtonDataSourceFile.isChecked() and self.textBoxFile.text() == '':
      QtGui.QMessageBox.warning(self, "Warning", "Input stream file was not specified.")
      return
    elif self.radioButtonDataSourceDatabase.isChecked() and self.textBoxDatabaseConnectionString.text() == '':
      QtGui.QMessageBox.warning(self, "Warning", "Database connection string was not specified.")
      return
    elif self.radioButtonDataSourceDatabase.isChecked() and self.textBoxDatabaseTable.text() == '':
      QtGui.QMessageBox.warning(self, "Warning", "Database table was not specified.")
      return
    elif self.listBoxEncodings.count() == 0:
      QtGui.QMessageBox.warning(self, "Warning", "Encodings list is empty. At least one encoding should be specified.")
      return
    else:
      hasFieldsWithInference = False
      for encoding in self.encodings:
        if encoding.enableInference:
          hasFieldsWithInference = True
          break
      if not hasFieldsWithInference:
        QtGui.QMessageBox.warning(self, "Warning", "At least one encoding should have inference enabled.")
        return

    width = self.spinnerSensorWidth.value()
    height = self.spinnerSensorHeight.value()
    dataSourceType = None
    if self.radioButtonDataSourceFile.isChecked():
      dataSourceType = DataSourceType.file
    elif self.radioButtonDataSourceDatabase.isChecked():
      dataSourceType = DataSourceType.database
    fileName = str(self.textBoxFile.text())
    databaseConnectionString = str(self.textBoxDatabaseConnectionString.text())
    databaseTable = str(self.textBoxDatabaseTable.text())
    predictionsMethod = str(self.comboBoxPredictionsMethod.currentText())

    # If anything has changed
    node = Global.architectureForm.designPanel.underMouseNode
    if node.width != width or node.height != height or node.predictionsMethod != predictionsMethod or node.dataSourceType != dataSourceType or node.fileName != fileName or node.databaseConnectionString != databaseConnectionString or node.databaseTable != databaseTable or self.encodingsChanged:
      # Set sensor params with controls values
      node.width = width
      node.height = height
      node.predictionsMethod = predictionsMethod
      node.dataSourceType = dataSourceType
      node.fileName = fileName
      node.databaseConnectionString = databaseConnectionString
      node.databaseTable = databaseTable
      node.encodings = copy.deepcopy(self.encodings)
      self.accept()

    self.close()

  def __buttonCancel_Click(self, event):
    self.reject()
    self.close()

  def __buttonBrowseFile_Click(self, event):
    # Ask user for an existing file
    selectedFile = QtGui.QFileDialog().getOpenFileName(self, "Open File", Global.appPath + '/projects', "Input files (*.csv)")

    # If file exists, set data source file
    if selectedFile != '':
      # Set file
      self.textBoxFile.setText(selectedFile)

  def __radioButtonDataSource_Click(self, event):
    if not Global.simulationInitialized:
      flag = self.radioButtonDataSourceFile.isChecked()
      self.textBoxFile.setEnabled(flag)
      self.buttonBrowseFile.setEnabled(flag)
      self.textBoxDatabaseConnectionString.setEnabled(not flag)
      self.textBoxDatabaseTable.setEnabled(not flag)

  def __buttonNewEncoding_Click(self, event):
    encodingForm = EncodingForm()
    encodingForm.encodingIdx = -1
    encodingForm.encodings = self.encodings
    dialogResult = encodingForm.exec_()
    if dialogResult == QtGui.QDialog.Accepted:
      self.encodingsChanged = True
      self.__updateEncodingsListBox()

  def __buttonEditEncoding_Click(self, event):
    encodingForm = EncodingForm()
    encodingForm.encodingIdx = self.listBoxEncodings.currentRow()
    encodingForm.encodings = self.encodings
    encodingForm.setControlsValues()
    dialogResult = encodingForm.exec_()
    if dialogResult == QtGui.QDialog.Accepted:
      self.encodingsChanged = True
      self.__updateEncodingsListBox()

  def __buttonDeleteEncoding_Click(self, event):
    self.encodings.remove(self.encodings[self.listBoxEncodings.currentRow()])
    self.encodingsChanged = True
    self.__updateEncodingsListBox()

  #endregion
