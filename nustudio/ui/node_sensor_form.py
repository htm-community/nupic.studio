﻿import ast
from PyQt4 import QtGui, QtCore
from nustudio import ArrayTableModel
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

		# radioButtonDataSourceFile
		self.radioButtonDataSourceFile = QtGui.QRadioButton()
		self.radioButtonDataSourceFile.setText("File")
		self.radioButtonDataSourceFile.setEnabled(not Global.simulationInitialized)
		self.radioButtonDataSourceFile.toggled.connect(self.__radioButtonDataSource_Click)

		# labelFile
		self.labelFile = QtGui.QLabel()
		self.labelFile.setText("File:")
		self.labelFile.setAlignment(QtCore.Qt.AlignRight)

		# textBoxFile
		self.textBoxFile = QtGui.QLineEdit()
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
		self.radioButtonDataSourceDatabase.toggled.connect(self.__radioButtonDataSource_Click)

		# labelDatabaseConnectionString
		self.labelDatabaseConnectionString = QtGui.QLabel()
		self.labelDatabaseConnectionString.setText("Connection String:")
		self.labelDatabaseConnectionString.setAlignment(QtCore.Qt.AlignRight)

		# textBoxDatabaseConnectionString
		self.textBoxDatabaseConnectionString = QtGui.QLineEdit()
		self.textBoxDatabaseConnectionString.setEnabled(not Global.simulationInitialized)

		# labelDatabaseTable
		self.labelDatabaseTable = QtGui.QLabel()
		self.labelDatabaseTable.setText("Table:")
		self.labelDatabaseTable.setAlignment(QtCore.Qt.AlignRight)

		# textBoxDatabaseTable
		self.textBoxDatabaseTable = QtGui.QLineEdit()
		self.textBoxDatabaseTable.setEnabled(not Global.simulationInitialized)

		# labelDatabaseField
		self.labelDatabaseField = QtGui.QLabel()
		self.labelDatabaseField.setText("Field:")
		self.labelDatabaseField.setAlignment(QtCore.Qt.AlignRight)

		# textBoxDatabaseField
		self.textBoxDatabaseField = QtGui.QLineEdit()
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

		# radioButtonInputFormatHtm
		self.radioButtonInputFormatHtm = QtGui.QRadioButton()
		self.radioButtonInputFormatHtm.setText("Htm")
		self.radioButtonInputFormatHtm.setEnabled(not Global.simulationInitialized)
		self.radioButtonInputFormatHtm.toggled.connect(self.__radioButtonInputFormat_Click)

		# radioButtonInputFormatRaw
		self.radioButtonInputFormatRaw = QtGui.QRadioButton()
		self.radioButtonInputFormatRaw.setText("Raw")
		self.radioButtonInputFormatRaw.setEnabled(not Global.simulationInitialized)
		self.radioButtonInputFormatRaw.toggled.connect(self.__radioButtonInputFormat_Click)

		# labelEncoderModule
		self.labelEncoderModule = QtGui.QLabel()
		self.labelEncoderModule.setText("Module:")
		self.labelEncoderModule.setAlignment(QtCore.Qt.AlignRight)

		# textBoxEncoderModule
		self.textBoxEncoderModule = QtGui.QLineEdit()
		self.textBoxEncoderModule.setEnabled(not Global.simulationInitialized)
		self.textBoxEncoderModule.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp('[a-zA-Z0-9._]+')))

		# labelEncoderClass
		self.labelEncoderClass = QtGui.QLabel()
		self.labelEncoderClass.setText("Class:")
		self.labelEncoderClass.setAlignment(QtCore.Qt.AlignRight)

		# textBoxEncoderClass
		self.textBoxEncoderClass = QtGui.QLineEdit()
		self.textBoxEncoderClass.setEnabled(not Global.simulationInitialized)
		self.textBoxEncoderClass.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp('[a-zA-Z0-9_]+')))

		# labelEncoderParams
		self.labelEncoderParams = QtGui.QLabel()
		self.labelEncoderParams.setText("Params:")
		self.labelEncoderParams.setAlignment(QtCore.Qt.AlignRight)

		# dataGridEncoderParams
		data = []
		data.append(['', ''])
		data.append(['', ''])
		data.append(['', ''])
		data.append(['', ''])
		data.append(['', ''])
		data.append(['', ''])
		self.dataGridEncoderParams = QtGui.QTableView()
		self.dataGridEncoderParams.setModel(ArrayTableModel(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable))
		self.dataGridEncoderParams.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
		self.dataGridEncoderParams.verticalHeader().setDefaultSectionSize(18)
		self.dataGridEncoderParams.model().update(['Parameter', 'Value'], data)
		self.dataGridEncoderParams.resizeColumnsToContents()
		self.dataGridEncoderParams.setEnabled(not Global.simulationInitialized)

		self.groupRadioButtonInputFormat = QtGui.QButtonGroup()
		self.groupRadioButtonInputFormat.addButton(self.radioButtonInputFormatHtm)
		self.groupRadioButtonInputFormat.addButton(self.radioButtonInputFormatRaw)

		# groupBoxInputFormatLayout
		groupBoxInputFormatLayout = QtGui.QGridLayout()
		groupBoxInputFormatLayout.addWidget(self.radioButtonInputFormatHtm, 0, 0)
		groupBoxInputFormatLayout.addWidget(self.radioButtonInputFormatRaw, 1, 0)
		groupBoxInputFormatLayout.addWidget(self.labelEncoderModule, 2, 0)
		groupBoxInputFormatLayout.addWidget(self.textBoxEncoderModule, 2, 1)
		groupBoxInputFormatLayout.addWidget(self.labelEncoderClass, 3, 0)
		groupBoxInputFormatLayout.addWidget(self.textBoxEncoderClass, 3, 1)
		groupBoxInputFormatLayout.addWidget(self.labelEncoderParams, 4, 0)
		groupBoxInputFormatLayout.addWidget(self.dataGridEncoderParams, 4, 1)

		# groupBoxInputFormat
		self.groupBoxInputFormat = QtGui.QGroupBox()
		self.groupBoxInputFormat.setLayout(groupBoxInputFormatLayout)
		self.groupBoxInputFormat.setTitle("Input Format")

		# groupBoxMainLayout
		self.groupBoxMainLayout = QtGui.QGridLayout()
		self.groupBoxMainLayout.addWidget(self.labelSensorWidth, 0, 0)
		self.groupBoxMainLayout.addWidget(self.spinnerSensorWidth, 0, 1)
		self.groupBoxMainLayout.addWidget(self.labelSensorHeight, 1, 0)
		self.groupBoxMainLayout.addWidget(self.spinnerSensorHeight, 1, 1)
		self.groupBoxMainLayout.addWidget(self.groupBoxDataSourceType, 3, 1)
		self.groupBoxMainLayout.addWidget(self.groupBoxInputFormat, 2, 1)

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

			# Set encoder parameters
			self.textBoxEncoderModule.setText(node.encoderModule)
			self.textBoxEncoderClass.setText(node.encoderClass)
			encoderParams = ast.literal_eval(node.encoderParams)
			gridData = self.dataGridEncoderParams.model().data
			row = 0
			for key, value in encoderParams.iteritems():
				gridData[row][0] = key
				gridData[row][1] = value
				row += 1

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

		encoderParamsDict = {}
		if self.radioButtonInputFormatRaw.isChecked():
			if self.textBoxEncoderModule.text() == '':
				QtGui.QMessageBox.warning(self, "Warning", "Encoder module was not specified.")
				return
			elif self.textBoxEncoderClass.text() == '':
				QtGui.QMessageBox.warning(self, "Warning", "Encoder class was not specified.")
				return
			else:
				gridData = self.dataGridEncoderParams.model().data
				for row in range(len(gridData)):
					if gridData[row][0] != '':
						# Valid parameter name
						try:
							gridData[row][0] = gridData[row][0].toString()
						except:
							pass
						param = str(gridData[row][0])
						validExpr = QtCore.QRegExp('[a-zA-Z0-9_]+')
						if not validExpr.exactMatch(param):
							QtGui.QMessageBox.warning(self, "Warning", "'" + param + "' is not a valid name.")
							return

						# Valid parameter value
						try:
							gridData[row][1] = gridData[row][1].toString()
						except:
							pass
						value = str(gridData[row][1])
						if value == '':
							QtGui.QMessageBox.warning(self, "Warning", "'" + param + "' value is empty.")
							return

						# Add param name and its value to dictionary
						encoderParamsDict[param] = value
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
		encoderModule = str(self.textBoxEncoderModule.text())
		encoderClass = str(self.textBoxEncoderClass.text())
		encoderParams = str(encoderParamsDict)
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
		if node.width != width or node.height != height or node.inputFormat != inputFormat or node.encoderModule != encoderModule or node.encoderClass != encoderClass or node.encoderParams != encoderParams or node.dataSourceType != dataSourceType or node.fileName != fileName or node.databaseConnectionString != databaseConnectionString or node.databaseTable != databaseTable or node.databaseField != databaseField:
			# Set region params with controls values
			node.width = width
			node.height = height
			node.inputFormat = inputFormat
			node.encoderModule = encoderModule
			node.encoderClass = encoderClass
			node.encoderParams = encoderParams
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
			
	def __radioButtonDataSource_Click(self, event):
		if not Global.simulationInitialized:
			flag = self.radioButtonDataSourceFile.isChecked()
			self.textBoxFile.setEnabled(flag)
			self.buttonBrowseFile.setEnabled(flag)
			self.textBoxDatabaseConnectionString.setEnabled(not flag)
			self.textBoxDatabaseTable.setEnabled(not flag)
			self.textBoxDatabaseField.setEnabled(not flag)
		
	def __radioButtonInputFormat_Click(self, event):
		if not Global.simulationInitialized:
			flag = self.radioButtonInputFormatHtm.isChecked()
			self.textBoxEncoderModule.setEnabled(not flag)
			self.textBoxEncoderClass.setEnabled(not flag)
			self.dataGridEncoderParams.setEnabled(not flag)

	#endregion
