import collections
import json
from PyQt4 import QtGui, QtCore
from nupic_studio import ArrayTableModel
from nupic_studio.ui import Global
from nupic_studio.htm.encoding import Encoding, FieldDataType

class EncodingForm(QtGui.QDialog):

  #region Constructor

  def __init__(self):
    """
    Initializes a new instance of this class.
    """

    QtGui.QDialog.__init__(self)

    self.initUI()

    #region Instance fields

    self.encodingIdx = -1
    """Index of the encoding that is being edited. If index is -1 the user is creating a new encoding."""

    self.encodings = []
    """Temporary list of encodings that is being edited"""

    #endregion

  #endregion

  #region Methods

  def initUI(self):

    # labelDataSourceFieldName
    self.labelDataSourceFieldName = QtGui.QLabel()
    self.labelDataSourceFieldName.setText("Datasource Field Name:")
    self.labelDataSourceFieldName.setAlignment(QtCore.Qt.AlignRight)

    # textBoxDataSourceFieldName
    self.textBoxDataSourceFieldName = QtGui.QLineEdit()
    self.textBoxDataSourceFieldName.setAlignment(QtCore.Qt.AlignLeft)

    # labelDataSourceFieldDataType
    self.labelDataSourceFieldDataType = QtGui.QLabel()
    self.labelDataSourceFieldDataType.setText("Field Data Type:")
    self.labelDataSourceFieldDataType.setAlignment(QtCore.Qt.AlignRight)

    # comboBoxDataSourceFieldDataType
    self.comboBoxDataSourceFieldDataType = QtGui.QComboBox()
    self.comboBoxDataSourceFieldDataType.addItem(FieldDataType.boolean)
    self.comboBoxDataSourceFieldDataType.addItem(FieldDataType.integer)
    self.comboBoxDataSourceFieldDataType.addItem(FieldDataType.decimal)
    self.comboBoxDataSourceFieldDataType.addItem(FieldDataType.dateTime)
    self.comboBoxDataSourceFieldDataType.addItem(FieldDataType.string)

    # checkBoxEnableInference
    self.checkBoxEnableInference = QtGui.QCheckBox()
    self.checkBoxEnableInference.setText("Enable Inference")

    # labelEncoderModule
    self.labelEncoderModule = QtGui.QLabel()
    self.labelEncoderModule.setText("Module:")
    self.labelEncoderModule.setAlignment(QtCore.Qt.AlignRight)

    # textBoxEncoderModule
    self.textBoxEncoderModule = QtGui.QLineEdit()
    self.textBoxEncoderModule.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp('[a-zA-Z0-9._]+')))

    # labelEncoderClass
    self.labelEncoderClass = QtGui.QLabel()
    self.labelEncoderClass.setText("Class:")
    self.labelEncoderClass.setAlignment(QtCore.Qt.AlignRight)

    # textBoxEncoderClass
    self.textBoxEncoderClass = QtGui.QLineEdit()
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
    self.dataGridEncoderParams.setMinimumHeight(140)

    # labelEncoderFieldName
    self.labelEncoderFieldName = QtGui.QLabel()
    self.labelEncoderFieldName.setText("Field Name:")
    self.labelEncoderFieldName.setAlignment(QtCore.Qt.AlignRight)

    # textBoxEncoderFieldName
    self.textBoxEncoderFieldName = QtGui.QLineEdit()
    self.textBoxEncoderFieldName.setAlignment(QtCore.Qt.AlignLeft)

    # labelEncoderFieldDataType
    self.labelEncoderFieldDataType = QtGui.QLabel()
    self.labelEncoderFieldDataType.setText("Field Data Type:")
    self.labelEncoderFieldDataType.setAlignment(QtCore.Qt.AlignRight)

    # comboBoxEncoderFieldDataType
    self.comboBoxEncoderFieldDataType = QtGui.QComboBox()
    self.comboBoxEncoderFieldDataType.addItem(FieldDataType.boolean)
    self.comboBoxEncoderFieldDataType.addItem(FieldDataType.integer)
    self.comboBoxEncoderFieldDataType.addItem(FieldDataType.decimal)
    self.comboBoxEncoderFieldDataType.addItem(FieldDataType.dateTime)
    self.comboBoxEncoderFieldDataType.addItem(FieldDataType.string)

    # groupBoxEncoderLayout
    groupBoxEncoderLayout = QtGui.QGridLayout()
    groupBoxEncoderLayout.addWidget(self.labelEncoderModule, 0, 0)
    groupBoxEncoderLayout.addWidget(self.textBoxEncoderModule, 0, 1)
    groupBoxEncoderLayout.addWidget(self.labelEncoderClass, 1, 0)
    groupBoxEncoderLayout.addWidget(self.textBoxEncoderClass, 1, 1)
    groupBoxEncoderLayout.addWidget(self.labelEncoderParams, 2, 0)
    groupBoxEncoderLayout.addWidget(self.dataGridEncoderParams, 2, 1)
    groupBoxEncoderLayout.addWidget(self.labelEncoderFieldName, 3, 0)
    groupBoxEncoderLayout.addWidget(self.textBoxEncoderFieldName, 3, 1)
    groupBoxEncoderLayout.addWidget(self.labelEncoderFieldDataType, 4, 0)
    groupBoxEncoderLayout.addWidget(self.comboBoxEncoderFieldDataType, 4, 1)

    # groupBoxEncoder
    self.groupBoxEncoder = QtGui.QGroupBox()
    self.groupBoxEncoder.setLayout(groupBoxEncoderLayout)
    self.groupBoxEncoder.setTitle("Encoder")

    # groupBoxMainLayout
    groupBoxMainLayout = QtGui.QGridLayout()
    groupBoxMainLayout.addWidget(self.labelDataSourceFieldName, 0, 0)
    groupBoxMainLayout.addWidget(self.textBoxDataSourceFieldName, 0, 1)
    groupBoxMainLayout.addWidget(self.labelDataSourceFieldDataType, 1, 0)
    groupBoxMainLayout.addWidget(self.comboBoxDataSourceFieldDataType, 1, 1)
    groupBoxMainLayout.addWidget(self.checkBoxEnableInference, 2, 1)
    groupBoxMainLayout.addWidget(self.groupBoxEncoder, 3, 1)

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

    # Set controls value with encoding params
    if self.encodingIdx >= 0:
      encoding = self.encodings[self.encodingIdx]
      self.checkBoxEnableInference.setChecked(encoding.enableInference)
      self.textBoxDataSourceFieldName.setText(encoding.dataSourceFieldName)
      self.comboBoxDataSourceFieldDataType.setCurrentIndex(self.comboBoxDataSourceFieldDataType.findText(encoding.dataSourceFieldDataType, QtCore.Qt.MatchFixedString))

      # Set encoding parameters
      self.textBoxEncoderModule.setText(encoding.encoderModule)
      self.textBoxEncoderClass.setText(encoding.encoderClass)
      encoderParams = json.loads(encoding.encoderParams.replace("'", "\""), object_pairs_hook=collections.OrderedDict)
      gridData = self.dataGridEncoderParams.model().data
      row = 0
      for key, value in encoderParams.iteritems():
        gridData[row][0] = key
        gridData[row][1] = value
        row += 1
      self.textBoxEncoderFieldName.setText(encoding.encoderFieldName)
      self.comboBoxEncoderFieldDataType.setCurrentIndex(self.comboBoxEncoderFieldDataType.findText(encoding.encoderFieldDataType, QtCore.Qt.MatchFixedString))

  def duplicatedFieldName(self, fieldName):
    """
    Check if exists an encoding with the same name.
    """
    duplicated = False

    if len(self.encodings) > 0:
      for i in range(len(self.encodings)):
        if self.encodings[i].encoderFieldName == fieldName and i != self.encodingIdx:
          duplicated = True
          break

    return duplicated

  #endregion

  #region Events

  def __buttonOk_Click(self, event):
    """
    Check if values changed and save the,.
    """

    encoderParamsDict = collections.OrderedDict()
    if self.textBoxDataSourceFieldName.text() == '':
      QtGui.QMessageBox.warning(self, "Warning", "Record field name was not specified.")
      return
    elif self.textBoxEncoderModule.text() == '':
      QtGui.QMessageBox.warning(self, "Warning", "Encoder module was not specified.")
      return
    elif self.textBoxEncoderClass.text() == '':
      QtGui.QMessageBox.warning(self, "Warning", "Encoder class was not specified.")
      return
    elif self.textBoxEncoderFieldName.text() == '':
      QtGui.QMessageBox.warning(self, "Warning", "Encoder field name was not specified.")
      return
    elif self.duplicatedFieldName(self.textBoxEncoderFieldName.text()):
      QtGui.QMessageBox.warning(self, "Warning", "Encoder field name already is used by other encoding.")
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
          if len(value) == 0:
            QtGui.QMessageBox.warning(self, "Warning", "'" + param + "' value is empty.")
            return

          # Add param name and its value to dictionary
          encoderParamsDict[param] = value

    dataSourceFieldName = str(self.textBoxDataSourceFieldName.text())
    dataSourceFieldDataType = str(self.comboBoxDataSourceFieldDataType.currentText())
    enableInference = self.checkBoxEnableInference.isChecked()
    encoderModule = str(self.textBoxEncoderModule.text())
    encoderClass = str(self.textBoxEncoderClass.text())
    encoderParams = json.dumps(encoderParamsDict)
    encoderFieldName = str(self.textBoxEncoderFieldName.text())
    encoderFieldDataType = str(self.comboBoxEncoderFieldDataType.currentText())

    # Remove double quotes from param values
    encoderParams = encoderParams.replace("\"", "'")
    encoderParams = encoderParams.replace("True", "true")
    encoderParams = encoderParams.replace("False", "false")

    # If this is a new encoding get it from list else create a new one
    if self.encodingIdx >= 0:
      encoding = self.encodings[self.encodingIdx]
    else:
      encoding = Encoding()
      self.encodings.append(encoding)

    # If anything has changed
    if encoding.dataSourceFieldName != dataSourceFieldName or encoding.dataSourceFieldDataType != dataSourceFieldDataType or encoding.enableInference != enableInference or encoding.encoderModule != encoderModule or encoding.encoderClass != encoderClass or encoding.encoderParams != encoderParams or encoding.encoderFieldName != encoderFieldName or encoding.encoderFieldDataType != encoderFieldDataType:
      # Set encoding params with controls values
      encoding.dataSourceFieldName = dataSourceFieldName
      encoding.dataSourceFieldDataType = dataSourceFieldDataType
      encoding.enableInference = enableInference
      encoding.encoderModule = encoderModule
      encoding.encoderClass = encoderClass
      encoding.encoderParams = encoderParams
      encoding.encoderFieldName = encoderFieldName
      encoding.encoderFieldDataType = encoderFieldDataType

      self.accept()

    self.close()

  def __buttonCancel_Click(self, event):
    self.reject()
    self.close()

  #endregion
