from PyQt4 import QtGui, QtCore
from nustudio.ui import Global
from nustudio.htm.node_sensor import InputFormat, DataSourceType

class SensorForm(QtGui.QDialog):

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

		# labelSensorWidth
		self.labelSensorWidth = QtGui.QLabel()
		self.labelSensorWidth.setText("Sensor Width")
		self.labelSensorWidth.setAlignment(QtCore.Qt.AlignRight)

		# spinnerSensorWidth
		self.spinnerSensorWidth = QtGui.QSpinBox()
		self.spinnerSensorWidth.setAlignment(QtCore.Qt.AlignRight)
		self.spinnerSensorWidth.setToolTip("Number of output bits in the X direction for this sensor.")
		self.spinnerSensorWidth.setEnabled(not Global.simulationInitialized)

		# labelSensorHeight
		self.labelSensorHeight = QtGui.QLabel()
		self.labelSensorHeight.setText("Sensor Height")
		self.labelSensorHeight.setAlignment(QtCore.Qt.AlignRight)

		# spinnerSensorHeight
		self.spinnerSensorHeight = QtGui.QSpinBox()
		self.spinnerSensorHeight.setAlignment(QtCore.Qt.AlignRight)
		self.spinnerSensorHeight.setToolTip("Number of output bits in the Y direction for this sensor.")
		self.spinnerSensorHeight.setEnabled(not Global.simulationInitialized)

		# radioButtonInputFormatHtm
		self.radioButtonInputFormatHtm = QtGui.QRadioButton()
		self.radioButtonInputFormatHtm.setText("Htm")
		self.radioButtonInputFormatHtm.setEnabled(not Global.simulationInitialized)

		# radioButtonInputFormatRaw
		self.radioButtonInputFormatRaw = QtGui.QRadioButton()
		self.radioButtonInputFormatRaw.setText("Raw")
		self.radioButtonInputFormatRaw.setEnabled(not Global.simulationInitialized)

		# labelEncoder
		self.labelEncoder = QtGui.QLabel()
		self.labelEncoder.setText("Encoder:")
		self.labelEncoder.setAlignment(QtCore.Qt.AlignRight)

		# comboBoxEncoder
		self.comboBoxEncoder = QtGui.QComboBox()
		self.comboBoxEncoder.setEnabled(False)
		self.comboBoxEncoder.setEnabled(not Global.simulationInitialized)

		# groupBoxInputFormatLayout
		groupBoxInputFormatLayout = QtGui.QGridLayout()
		groupBoxInputFormatLayout.addWidget(self.radioButtonInputFormatHtm, 0, 0)
		groupBoxInputFormatLayout.addWidget(self.radioButtonInputFormatRaw, 1, 0)
		groupBoxInputFormatLayout.addWidget(self.labelEncoder, 2, 0)
		groupBoxInputFormatLayout.addWidget(self.comboBoxEncoder, 2, 1)

		# groupBoxInputFormat
		self.groupBoxInputFormat = QtGui.QGroupBox()
		self.groupBoxInputFormat.setLayout(groupBoxInputFormatLayout)
		self.groupBoxInputFormat.setTitle("Input Format")

		# radioButtonDataSourceFile
		self.radioButtonDataSourceFile = QtGui.QRadioButton()
		self.radioButtonDataSourceFile.setText("File")
		self.radioButtonDataSourceFile.setEnabled(not Global.simulationInitialized)

		# labelFile
		self.labelFile = QtGui.QLabel()
		self.labelFile.setText("File:")
		self.labelFile.setAlignment(QtCore.Qt.AlignRight)

		# textBoxFile
		self.textBoxFile = QtGui.QLineEdit()
		self.textBoxFile.setEnabled(False)
		self.textBoxFile.setEnabled(not Global.simulationInitialized)

		# buttonBrowseFile
		self.buttonBrowseFile = QtGui.QPushButton()
		self.buttonBrowseFile.setText("Browse...")
		self.buttonBrowseFile.setEnabled(not Global.simulationInitialized)
		self.buttonBrowseFile.clicked.connect(self.__buttonBrowseFile_Click)

		# radioButtonDataSourceDatabase
		self.radioButtonDataSourceDatabase = QtGui.QRadioButton()
		self.radioButtonDataSourceDatabase.setText("Database")
		self.radioButtonDataSourceDatabase.setEnabled(not Global.simulationInitialized)

		# labelDatabaseConnectionString
		self.labelDatabaseConnectionString = QtGui.QLabel()
		self.labelDatabaseConnectionString.setText("Connection String:")
		self.labelDatabaseConnectionString.setAlignment(QtCore.Qt.AlignRight)

		# textBoxDatabaseConnectionString
		self.textBoxDatabaseConnectionString = QtGui.QLineEdit()
		self.textBoxDatabaseConnectionString.setEnabled(False)
		self.textBoxDatabaseConnectionString.setEnabled(not Global.simulationInitialized)

		# labelDatabaseTable
		self.labelDatabaseTable = QtGui.QLabel()
		self.labelDatabaseTable.setText("Table:")
		self.labelDatabaseTable.setAlignment(QtCore.Qt.AlignRight)

		# textBoxDatabaseTable
		self.textBoxDatabaseTable = QtGui.QLineEdit()
		self.textBoxDatabaseTable.setEnabled(False)
		self.textBoxDatabaseTable.setEnabled(not Global.simulationInitialized)

		# labelDatabaseField
		self.labelDatabaseField = QtGui.QLabel()
		self.labelDatabaseField.setText("Field:")
		self.labelDatabaseField.setAlignment(QtCore.Qt.AlignRight)

		# textBoxDatabaseField
		self.textBoxDatabaseField = QtGui.QLineEdit()
		self.textBoxDatabaseField.setEnabled(False)
		self.textBoxDatabaseField.setEnabled(not Global.simulationInitialized)

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
		groupBoxDataSourceTypeLayout.addWidget(self.labelDatabaseField, 6, 0)
		groupBoxDataSourceTypeLayout.addWidget(self.textBoxDatabaseField, 6, 1)

		# groupBoxDataSourceType
		self.groupBoxDataSourceType = QtGui.QGroupBox()
		self.groupBoxDataSourceType.setLayout(groupBoxDataSourceTypeLayout)
		self.groupBoxDataSourceType.setTitle("Data Source Type")

		# groupBoxMainLayout
		self.groupBoxMainLayout = QtGui.QGridLayout()
		self.groupBoxMainLayout.addWidget(self.labelSensorWidth, 0, 0)
		self.groupBoxMainLayout.addWidget(self.spinnerSensorWidth, 0, 1)
		self.groupBoxMainLayout.addWidget(self.labelSensorHeight, 1, 0)
		self.groupBoxMainLayout.addWidget(self.spinnerSensorHeight, 1, 1)
		self.groupBoxMainLayout.addWidget(self.groupBoxInputFormat, 2, 1)
		self.groupBoxMainLayout.addWidget(self.groupBoxDataSourceType, 3, 1)

		# groupBoxMain
		self.groupBoxMain = QtGui.QGroupBox()
		self.groupBoxMain.setLayout(self.groupBoxMainLayout)

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
		node = Global.nodeSelectorForm.underMouseNode
		self.spinnerSensorWidth.setValue(node.width)
		self.spinnerSensorHeight.setValue(node.height)
		if node.inputFormat == InputFormat.htm:
			self.radioButtonInputFormatHtm.setChecked(True)
		elif node.inputFormat == InputFormat.raw:
			self.radioButtonInputFormatRaw.setChecked(True)
			self.comboBoxEncoder.setText(node.encoder)
		if node.dataSourceType == DataSourceType.file:
			self.radioButtonDataSourceFile.setChecked(True)
			self.textBoxFile.setText(node.fileName)
		elif node.dataSourceType == DataSourceType.database:
			self.radioButtonDataSourceDatabase.setChecked(True)
			self.textBoxDatabaseConnectionString.setText(node.databaseConnectionString)
			self.textBoxDatabaseTable.setText(node.databaseTable)
			self.textBoxDatabaseField.setText(node.databaseField)

	#endregion

	#region Events

	def __buttonOk_Click(self, event):
		"""
		Check if values changed and save the,.
		"""

		if self.radioButtonInputFormatRaw.isChecked():
			if self.comboBoxEncoder.currentText() == '':
				QtGui.QMessageBox.warning(self, "Warning", "Encoder was not found or specified.")
				return
		if self.radioButtonDataSourceFile.isChecked():
			if self.textBoxFile.text() == '':
				QtGui.QMessageBox.warning(self, "Warning", "Input stream file was not found or specified.")
				return
		elif self.radioButtonDataSourceDatabase.isChecked():
			pass

		width = self.spinnerSensorWidth.value()
		height = self.spinnerSensorHeight.value()
		inputFormat = None
		if self.radioButtonInputFormatHtm.isChecked():
			inputFormat = InputFormat.htm
		elif self.radioButtonInputFormatRaw.isChecked():
			inputFormat = InputFormat.raw
		encoder = str(self.comboBoxEncoder.currentText())
		dataSourceType = None
		if self.radioButtonDataSourceFile.isChecked():
			dataSourceType = DataSourceType.file
		elif self.radioButtonDataSourceDatabase.isChecked():
			dataSourceType = DataSourceType.database
		fileName = str(self.textBoxFile.text())
		databaseConnectionString = str(self.textBoxDatabaseConnectionString.text())
		databaseTable = str(self.textBoxDatabaseTable.text())
		databaseField = str(self.textBoxDatabaseField.text())

		# If anything has changed
		node = Global.nodeSelectorForm.underMouseNode
		if node.width != width or node.height != height or node.inputFormat != inputFormat or node.encoder != encoder or node.dataSourceType != dataSourceType or node.fileName != fileName or node.databaseConnectionString != databaseConnectionString or node.databaseTable != databaseTable or node.databaseField != databaseField:
			# Set region params with controls values
			node.width = width
			node.height = height
			node.inputFormat = inputFormat
			node.encoder = encoder
			node.dataSourceType = dataSourceType
			node.fileName = fileName
			node.databaseConnectionString = databaseConnectionString
			node.databaseTable = databaseTable
			node.databaseField = databaseField
			self.accept()

		self.close()

	def __buttonCancel_Click(self, event):
		self.reject()
		self.close()

	def __buttonBrowseFile_Click(self, event):
		# Ask user for an existing file
		selectedFile = QtGui.QFileDialog().getOpenFileName(self, "Open File", Global.appPath + '/projects', "Input files (*.txt)")

		# If file exists, set data source file
		if selectedFile != '':
			# Set file
			self.textBoxFile.setText(selectedFile)

	#endregion
