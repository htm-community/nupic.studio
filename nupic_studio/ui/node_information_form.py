import pyqtgraph as pg
from PyQt4 import Qt, QtGui, QtCore
from nupic_studio import ArrayTableModel
from nupic_studio.ui import Global
from nupic_studio.htm import maxPreviousSteps, maxFutureSteps, maxPreviousStepsWithInference
from nupic_studio.htm.node import NodeType, Node
from nupic_studio.htm.node_sensor import PredictionsMethod
from nupic_studio.htm.encoding import FieldDataType

class NodeInformationForm(QtGui.QWidget):

  #region Constructor

  def __init__(self):
    """
    Initializes a new instance of this class.
    """

    QtGui.QWidget.__init__(self)

    #region Instance fields

    self.previousSelectedNode = None
    self.selectedSensor = None
    self.selectedEncoding = None
    self.selectedRegion = None
    self.selectedColumn = None
    self.selectedProximalSynapse = None
    self.selectedCell = None
    self.selectedDistalSegment = None
    self.selectedDistalSynapse = None

    # Predictions variables used for the predictions chart
    self.currentValuesPlotItem = None
    self.predictedValuesPlotItem = None

    #endregion

    self.initUI()

  #endregion

  #region Methods

  def initUI(self):

    # labelSensorName
    self.labelSensorName = QtGui.QLabel()
    self.labelSensorName.setText("Name")
    self.labelSensorName.setAlignment(QtCore.Qt.AlignRight)

    # textBoxSensorName
    self.textBoxSensorName = QtGui.QLineEdit()
    self.textBoxSensorName.setEnabled(False)
    self.textBoxSensorName.setAlignment(QtCore.Qt.AlignLeft)

    # labelSensorPrecisionRate
    self.labelSensorPrecisionRate = QtGui.QLabel()
    self.labelSensorPrecisionRate.setText("Precision Rate (%)")
    self.labelSensorPrecisionRate.setAlignment(QtCore.Qt.AlignRight)

    # textBoxSensorPrecisionRate
    self.textBoxSensorPrecisionRate = QtGui.QLineEdit()
    self.textBoxSensorPrecisionRate.setEnabled(False)
    self.textBoxSensorPrecisionRate.setAlignment(QtCore.Qt.AlignRight)

    # checkBoxEnableClassificationLearning
    self.checkBoxEnableClassificationLearning = QtGui.QCheckBox()
    self.checkBoxEnableClassificationLearning.setText("Enable Classification Learning")
    self.checkBoxEnableClassificationLearning.toggled.connect(self.__checkBoxEnableClassificationLearning_Toggled)

    # checkBoxEnableClassificationInference
    self.checkBoxEnableClassificationInference = QtGui.QCheckBox()
    self.checkBoxEnableClassificationInference.setText("Enable Classification Inference")
    self.checkBoxEnableClassificationInference.toggled.connect(self.__checkBoxEnableClassificationInference_Toggled)

    # tabPageSensor1Layout
    tabPageSensor1Layout = QtGui.QGridLayout()
    tabPageSensor1Layout.addWidget(self.labelSensorName, 0, 0)
    tabPageSensor1Layout.addWidget(self.textBoxSensorName, 0, 1)
    tabPageSensor1Layout.addWidget(self.labelSensorPrecisionRate, 1, 0)
    tabPageSensor1Layout.addWidget(self.textBoxSensorPrecisionRate, 1, 1)
    tabPageSensor1Layout.addWidget(self.checkBoxEnableClassificationLearning, 2, 1)
    tabPageSensor1Layout.addWidget(self.checkBoxEnableClassificationInference, 3, 1)
    tabPageSensor1Layout.setRowStretch(4, 100)

    # tabPageSensorLayout
    tabPageSensorLayout = QtGui.QGridLayout()
    tabPageSensorLayout.addLayout(tabPageSensor1Layout, 0, 0)
    tabPageSensorLayout.setColumnStretch(1, 100)

    # tabPageSensor
    self.tabPageSensor = QtGui.QWidget()
    self.tabPageSensor.setLayout(tabPageSensorLayout)

    # dataGridBits
    self.dataGridBits = QtGui.QTableView()
    self.dataGridBits.setModel(ArrayTableModel(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable))
    self.dataGridBits.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
    self.dataGridBits.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
    self.dataGridBits.setToolTip("Click on a row to see more details")
    self.dataGridBits.verticalHeader().setDefaultSectionSize(20)

    # tabPageBitsLayout
    tabPageBitsLayout = QtGui.QHBoxLayout()
    tabPageBitsLayout.addWidget(self.dataGridBits)

    # tabPageBits
    self.tabPageBits = QtGui.QWidget()
    self.tabPageBits.setLayout(tabPageBitsLayout)

    # labelEncoding
    self.labelEncoding = QtGui.QLabel()
    self.labelEncoding.setText("Encoding:")
    self.labelEncoding.setAlignment(QtCore.Qt.AlignRight)

    # comboBoxEncoding
    self.comboBoxEncoding = QtGui.QComboBox()
    self.comboBoxEncoding.currentIndexChanged.connect(self.__comboBoxEncoding_CurrentIndexChanged)

    # labelCurrentValue
    self.labelCurrentValue = QtGui.QLabel()
    self.labelCurrentValue.setText("Current Value")
    self.labelCurrentValue.setAlignment(QtCore.Qt.AlignRight)

    # textBoxCurrentValue
    self.textBoxCurrentValue = QtGui.QLineEdit()
    self.textBoxCurrentValue.setEnabled(False)
    self.textBoxCurrentValue.setAlignment(QtCore.Qt.AlignRight)

    # labelPredictedValues
    self.labelPredictedValues = QtGui.QLabel()
    self.labelPredictedValues.setText("Predicted Values")
    self.labelPredictedValues.setAlignment(QtCore.Qt.AlignRight)

    # dataGridPredictedValues
    self.dataGridPredictedValues = QtGui.QTableView()
    self.dataGridPredictedValues.setModel(ArrayTableModel(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable))
    self.dataGridPredictedValues.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
    self.dataGridPredictedValues.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
    self.dataGridPredictedValues.verticalHeader().setDefaultSectionSize(20)

    # encoding1Layout
    encoding1Layout = QtGui.QGridLayout()
    encoding1Layout.addWidget(self.labelEncoding, 0, 0)
    encoding1Layout.addWidget(self.comboBoxEncoding, 0, 1)
    encoding1Layout.addWidget(self.labelCurrentValue, 1, 0)
    encoding1Layout.addWidget(self.textBoxCurrentValue, 1, 1)
    encoding1Layout.setRowStretch(2, 100)

    # sliderStep
    self.sliderStep = QtGui.QSlider()
    self.sliderStep.setOrientation(QtCore.Qt.Horizontal)
    self.sliderStep.setSingleStep(1)
    self.sliderStep.setRange(1, maxFutureSteps)
    self.sliderStep.valueChanged.connect(self.__sliderStep_ValueChanged)

    # encoding2Layout
    encoding2Layout = QtGui.QGridLayout()
    encoding2Layout.addWidget(self.sliderStep, 0, 1)
    encoding2Layout.addWidget(self.labelPredictedValues, 1, 0)
    encoding2Layout.addWidget(self.dataGridPredictedValues, 1, 1)

    # predictionsChart
    self.predictionsChart = pg.PlotWidget()
    self.predictionsChart.showGrid(x=True, y=True)
    self.predictionsChart.getAxis('left').setGrid(1)

    # encoding3Layout
    encoding3Layout = QtGui.QGridLayout()
    encoding3Layout.addWidget(self.predictionsChart, 0, 1)

    # tabPageEncodingsLayout
    tabPageEncodingsLayout = QtGui.QHBoxLayout()
    tabPageEncodingsLayout.addLayout(encoding1Layout)
    tabPageEncodingsLayout.addLayout(encoding2Layout)
    tabPageEncodingsLayout.addLayout(encoding3Layout)

    # tabPageEncodings
    self.tabPageEncodings = QtGui.QWidget()
    self.tabPageEncodings.setLayout(tabPageEncodingsLayout)

    # labelRegionName
    self.labelRegionName = QtGui.QLabel()
    self.labelRegionName.setText("Name")
    self.labelRegionName.setAlignment(QtCore.Qt.AlignRight)

    # textBoxRegionName
    self.textBoxRegionName = QtGui.QLineEdit()
    self.textBoxRegionName.setEnabled(False)
    self.textBoxRegionName.setAlignment(QtCore.Qt.AlignLeft)

    # labelRegionPrecisionRate
    self.labelRegionPrecisionRate = QtGui.QLabel()
    self.labelRegionPrecisionRate.setText("Precision Rate (%)")
    self.labelRegionPrecisionRate.setAlignment(QtCore.Qt.AlignRight)

    # textBoxRegionPrecisionRate
    self.textBoxRegionPrecisionRate = QtGui.QLineEdit()
    self.textBoxRegionPrecisionRate.setEnabled(False)
    self.textBoxRegionPrecisionRate.setAlignment(QtCore.Qt.AlignRight)

    # checkBoxEnableSpatialLearning
    self.checkBoxEnableSpatialLearning = QtGui.QCheckBox()
    self.checkBoxEnableSpatialLearning.setText("Enable Spatial Learning")
    self.checkBoxEnableSpatialLearning.toggled.connect(self.__checkBoxEnableSpatialLearning_Toggled)

    # checkBoxEnableTemporalLearning
    self.checkBoxEnableTemporalLearning = QtGui.QCheckBox()
    self.checkBoxEnableTemporalLearning.setText("Enable Temporal Learning")
    self.checkBoxEnableTemporalLearning.toggled.connect(self.__checkBoxEnableTemporalLearning_Toggled)

    # tabPageRegionsLayout
    tabPageRegionsLayout = QtGui.QGridLayout()
    tabPageRegionsLayout.addWidget(self.labelRegionName, 0, 0)
    tabPageRegionsLayout.addWidget(self.textBoxRegionName, 0, 1)
    tabPageRegionsLayout.addWidget(self.labelRegionPrecisionRate, 1, 0)
    tabPageRegionsLayout.addWidget(self.textBoxRegionPrecisionRate, 1, 1)
    tabPageRegionsLayout.addWidget(self.checkBoxEnableSpatialLearning, 2, 1)
    tabPageRegionsLayout.addWidget(self.checkBoxEnableTemporalLearning, 3, 1)
    tabPageRegionsLayout.setRowStretch(4, 100)
    tabPageRegionsLayout.setColumnStretch(2, 100)

    # tabPageRegions
    self.tabPageRegions = QtGui.QWidget()
    self.tabPageRegions.setLayout(tabPageRegionsLayout)

    # dataGridColumns
    self.dataGridColumns = QtGui.QTableView()
    self.dataGridColumns.setModel(ArrayTableModel(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable))
    self.dataGridColumns.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
    self.dataGridColumns.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
    self.dataGridColumns.setToolTip("Click on a row to see more details")
    self.dataGridColumns.verticalHeader().setDefaultSectionSize(20)
    self.dataGridColumns.selectionModel().selectionChanged.connect(self.__dataGridColumns_SelectionChanged)

    # tabPageColumnsLayout
    tabPageColumnsLayout = QtGui.QHBoxLayout()
    tabPageColumnsLayout.addWidget(self.dataGridColumns)

    # tabPageColumns
    self.tabPageColumns = QtGui.QWidget()
    self.tabPageColumns.setLayout(tabPageColumnsLayout)

    # dataGridProximalSynapses
    self.dataGridProximalSynapses = QtGui.QTableView()
    self.dataGridProximalSynapses.setModel(ArrayTableModel(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable))
    self.dataGridProximalSynapses.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
    self.dataGridProximalSynapses.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
    self.dataGridProximalSynapses.setToolTip("Click on a row to see more details")
    self.dataGridProximalSynapses.verticalHeader().setDefaultSectionSize(20)
    self.dataGridProximalSynapses.selectionModel().selectionChanged.connect(self.__dataGridProximalSynapses_SelectionChanged)

    # tabPageProximalSynapsesLayout
    tabPageProximalSynapsesLayout = QtGui.QHBoxLayout()
    tabPageProximalSynapsesLayout.addWidget(self.dataGridProximalSynapses)

    # tabPageProximalSynapses
    self.tabPageProximalSynapses = QtGui.QWidget()
    self.tabPageProximalSynapses.setLayout(tabPageProximalSynapsesLayout)

    # dataGridCells
    self.dataGridCells = QtGui.QTableView()
    self.dataGridCells.setModel(ArrayTableModel(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable))
    self.dataGridCells.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
    self.dataGridCells.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
    self.dataGridCells.setToolTip("Click on a row to see more details")
    self.dataGridCells.verticalHeader().setDefaultSectionSize(20)
    self.dataGridCells.selectionModel().selectionChanged.connect(self.__dataGridCells_SelectionChanged)

    # tabPageCellsLayout
    tabPageCellsLayout = QtGui.QHBoxLayout()
    tabPageCellsLayout.addWidget(self.dataGridCells)

    # tabPageCells
    self.tabPageCells = QtGui.QWidget()
    self.tabPageCells.setLayout(tabPageCellsLayout)

    # dataGridDistalSegments
    self.dataGridDistalSegments = QtGui.QTableView()
    self.dataGridDistalSegments.setModel(ArrayTableModel(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable))
    self.dataGridDistalSegments.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
    self.dataGridDistalSegments.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
    self.dataGridDistalSegments.setToolTip("Click on a row to see more details")
    self.dataGridDistalSegments.verticalHeader().setDefaultSectionSize(20)
    self.dataGridDistalSegments.selectionModel().selectionChanged.connect(self.__dataGridDistalSegments_SelectionChanged)

    # tabPageDistalSegmentsLayout
    tabPageDistalSegmentsLayout = QtGui.QHBoxLayout()
    tabPageDistalSegmentsLayout.addWidget(self.dataGridDistalSegments)

    # tabPageDistalSegments
    self.tabPageDistalSegments = QtGui.QWidget()
    self.tabPageDistalSegments.setLayout(tabPageDistalSegmentsLayout)

    # dataGridDistalSynapses
    self.dataGridDistalSynapses = QtGui.QTableView()
    self.dataGridDistalSynapses.setModel(ArrayTableModel(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable))
    self.dataGridDistalSynapses.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
    self.dataGridDistalSynapses.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
    self.dataGridDistalSynapses.setToolTip("Click on a row to see more details")
    self.dataGridDistalSynapses.verticalHeader().setDefaultSectionSize(20)
    self.dataGridDistalSynapses.selectionModel().selectionChanged.connect(self.__dataGridDistalSynapses_SelectionChanged)

    # tabPageDistalSynapsesLayout
    tabPageDistalSynapsesLayout = QtGui.QHBoxLayout()
    tabPageDistalSynapsesLayout.addWidget(self.dataGridDistalSynapses)

    # tabPageDistalSynapses
    self.tabPageDistalSynapses = QtGui.QWidget()
    self.tabPageDistalSynapses.setLayout(tabPageDistalSynapsesLayout)

    # tabControlMain
    self.tabControlMain = QtGui.QTabWidget()

    # layout
    layout = QtGui.QHBoxLayout()
    layout.addWidget(self.tabControlMain)

    # NodeInformationForm
    self.setLayout(layout)
    self.setWindowTitle("Node Information")
    self.setWindowIcon(QtGui.QIcon(Global.appPath + '/images/logo.ico'))
    self.setMinimumHeight(200)
    self.setMaximumHeight(300)

  def clearControls(self):
    """
    Reset all controls.
    """

    self.textBoxCurrentValue.setText("")
    self.sliderStep.setEnabled(False)
    self.dataGridPredictedValues.model().update([], [])
    self.predictionsChart.setVisible(False)

  def refreshControls(self):
    """
    Refresh controls for each time step.
    """

    selectedNode = Global.architectureForm.designPanel.selectedNode

    # Show information according to note type
    if selectedNode != self.previousSelectedNode:
      while True:
        self.tabControlMain.removeTab(0)
        if self.tabControlMain.count() == 0:
          break
      if selectedNode.type == NodeType.region:
        self.selectedRegion = selectedNode

        self.textBoxRegionName.setText(self.selectedRegion.name)
        self.checkBoxEnableSpatialLearning.setChecked(self.selectedRegion.enableSpatialLearning)
        self.checkBoxEnableTemporalLearning.setChecked(self.selectedRegion.enableTemporalLearning)
        self.showTab(self.tabPageRegions, "Region")
        self.showTab(self.tabPageColumns, "Columns")
        self.dataGridColumns.clearSelection()
      elif selectedNode.type == NodeType.sensor:
        self.selectedSensor = selectedNode

        self.textBoxSensorName.setText(self.selectedSensor.name)
        self.showTab(self.tabPageSensor, "Sensor")
        self.showTab(self.tabPageBits, "Bits")
        self.showTab(self.tabPageEncodings, "Encodings")
        self.dataGridBits.clearSelection()
        if self.selectedSensor.predictionsMethod == PredictionsMethod.classification:
          self.checkBoxEnableClassificationLearning.setVisible(True)
          self.checkBoxEnableClassificationLearning.setChecked(self.selectedSensor.enableClassificationLearning)
          self.checkBoxEnableClassificationInference.setVisible(True)
          self.checkBoxEnableClassificationInference.setChecked(self.selectedSensor.enableClassificationInference)
        else:
          self.checkBoxEnableClassificationLearning.setVisible(False)
          self.checkBoxEnableClassificationInference.setVisible(False)

        # Populate encodings combobox
        self.comboBoxEncoding.clear()
        for encoding in self.selectedSensor.encodings:
          if encoding.enableInference:
            name = encoding.encoderFieldName.split('.')[0]
            self.comboBoxEncoding.addItem(name)
        self.selectedEncoding = None
      self.tabControlMain.selectedIndex = 0

      self.previousSelectedNode = selectedNode

    if Global.simulationInitialized:
      if selectedNode.type == NodeType.region:
        self.textBoxRegionPrecisionRate.setText("{0:.3f}".format(self.selectedRegion.statsPrecisionRate))

        # Bind the columns from this region
        header, data = self.getColumnsData(self.selectedRegion)
        self.dataGridColumns.model().update(header, data)
        self.dataGridColumns.resizeColumnsToContents()

      elif selectedNode.type == NodeType.sensor:
        self.textBoxSensorPrecisionRate.setText("{0:.3f}".format(self.selectedSensor.statsPrecisionRate))

        # Bind the bits from this sensor
        header, data = self.getBitsData(self.selectedSensor)
        self.dataGridBits.model().update(header, data)
        self.dataGridBits.resizeColumnsToContents()

        # Reset step slider state
        self.sliderStep.setEnabled(True)
        self.sliderStep.setValue(self.sliderStep.minimum())
        if self.selectedSensor.predictionsMethod == PredictionsMethod.classification:
          self.sliderStep.setEnabled(True)
        else:
          self.sliderStep.setEnabled(False)

        # Set default encoding
        if self.selectedEncoding == None:
          self.selectedEncoding = self.selectedSensor.encodings[0]
        self.updateEncodingControls()

  def formatValue(self, dataType, value):
    formattedValue = None

    if value == None:
      formattedValue = "None"
    elif dataType == FieldDataType.boolean:
      if value == 0:
        formattedValue = "False"
      else:
        formattedValue = "True"
    elif dataType == FieldDataType.integer:
      formattedValue = "{0}".format(value)
    elif dataType == FieldDataType.decimal:
      formattedValue = "{0:.3f}".format(value)
    elif dataType == FieldDataType.dateTime:
      formattedValue = value.strftime("%Y-%m-%d %H:%M:%S")
    else:
      formattedValue = str(value)

    return formattedValue

  def getBitsData(self, selectedSensor):
    header = ['Pos (x,y)', 'Was Predicted', 'Is Active', 'Activation Rate', 'Precision Rate']
    data = []
    for bit in selectedSensor.bits:
      pos = str(bit.x) + ", " + str(bit.y)
      wasPredicted = bit.isPredicted.atGivenStepAgo(Global.selStep + 1)
      isActive = bit.isActive.atGivenStepAgo(Global.selStep)
      activationRate = "{0:.3f}".format(bit.statsActivationRate)
      precisionRate = "{0:.3f}".format(bit.statsPrecisionRate)
      data.append([pos, wasPredicted, isActive, activationRate, precisionRate])

    return header, data

  def updateEncodingControls(self):
    self.textBoxCurrentValue.setText(self.formatValue(self.selectedEncoding.encoderFieldDataType, self.selectedEncoding.currentValue.atGivenStepAgo(Global.selStep)))
    self.sliderStep.setVisible(self.selectedEncoding.enableInference)
    self.labelPredictedValues.setVisible(self.selectedEncoding.enableInference)
    self.dataGridPredictedValues.setVisible(self.selectedEncoding.enableInference)
    self.predictionsChart.setVisible(False)
    if Global.simulationInitialized and self.selectedEncoding.enableInference:
      self.updatePredictedValuesGrid()
      if self.selectedEncoding.encoderFieldDataType == FieldDataType.integer or self.selectedEncoding.encoderFieldDataType == FieldDataType.decimal:
        self.updatePredictionsChart()
        self.predictionsChart.setVisible(True)

  def updatePredictedValuesGrid(self):
    step = self.sliderStep.value()
    header, data = self.getPredictedValuesData(step)
    self.dataGridPredictedValues.model().update(header, data)
    self.dataGridPredictedValues.resizeColumnsToContents()

  def updatePredictionsChart(self):

    # Update the chart with the updated predictions history
    if self.currentValuesPlotItem == None:
      # Set plot lines
      self.currentValuesPlotItem = self.predictionsChart.plot(Global.timeStepsPredictionsChart.getList(), self.selectedEncoding.currentValue.getList())
      self.currentValuesPlotItem.setPen(QtGui.QColor.fromRgb(0, 100, 0)) # green color
      self.predictedValuesPlotItem = self.predictionsChart.plot(Global.timeStepsPredictionsChart.getList(), self.selectedEncoding.bestPredictedValue.getList())
      self.predictedValuesPlotItem.setPen(QtGui.QColor.fromRgb(255, 215, 80)) # yellow color

      # Set legend
      legend = self.predictionsChart.addLegend(size=None, offset=(0, 0))
      legend.addItem(self.currentValuesPlotItem, "Current")
      legend.addItem(self.predictedValuesPlotItem, "Predicted")
    else:
      self.currentValuesPlotItem.setData(Global.timeStepsPredictionsChart.getList(), self.selectedEncoding.currentValue.getList())
      self.predictedValuesPlotItem.setData(Global.timeStepsPredictionsChart.getList(), self.selectedEncoding.bestPredictedValue.getList())

    # Set X axis visible range
    minX = Global.timeStepsPredictionsChart.atFirstStep()
    maxX = minX + maxPreviousStepsWithInference
    maxX += 30 # Increase space to avoid plot lines overlap the legend
    self.predictionsChart.setXRange(minX, maxX)

  def getPredictedValuesData(self, futureStep):
    header = []
    if self.selectedSensor.predictionsMethod == PredictionsMethod.reconstruction:
      header = ['Value']
    elif self.selectedSensor.predictionsMethod == PredictionsMethod.classification:
      header = ['Value', 'Probability']

    data = []
    predictions = self.selectedEncoding.predictedValues.atGivenStepAgo(Global.selStep)[futureStep]
    for predictedValue in predictions:
      if self.selectedSensor.predictionsMethod == PredictionsMethod.reconstruction:
        value = predictedValue[1]
        data.append([value])
      elif self.selectedSensor.predictionsMethod == PredictionsMethod.classification:
        value = self.formatValue(self.selectedEncoding.encoderFieldDataType, predictedValue[0])
        probability = "{0:.3f}".format(predictedValue[1] * 100)
        data.append([value, probability])

    return header, data

  def getColumnsData(self, selectedRegion):
    header = ['Pos (x,y)', 'Was Predicted', 'Is Active', 'Activation Rate', 'Precision Rate']
    data = []
    for column in selectedRegion.columns:
      pos = str(column.x) + ", " + str(column.y)
      wasPredicted = column.segment.isPredicted.atGivenStepAgo(Global.selStep + 1)
      isActive = column.segment.isActive.atGivenStepAgo(Global.selStep)
      activationRate = "{0:.3f}".format(column.segment.statsActivationRate)
      precisionRate = "{0:.3f}".format(column.segment.statsPrecisionRate)
      data.append([pos, wasPredicted, isActive, activationRate, precisionRate])

    return header, data

  def getProximalSynapsesData(self, selectedSegment):
    #TODO: Put sensor bit position (x,y,z)
    header = ['Permanence', 'Is Connected', 'Connection Rate', 'Precision Rate']
    data = []
    for synapse in selectedSegment.synapses:
      permanence = "{0:.3f}".format(synapse.permanence.atGivenStepAgo(Global.selStep))
      isConnected = synapse.isConnected.atGivenStepAgo(Global.selStep)
      connectionRate = "{0:.3f}".format(synapse.statsConnectionRate)
      precisionRate = "{0:.3f}".format(synapse.statsPrecisionRate)
      data.append([permanence, isConnected, connectionRate, precisionRate])

    return header, data

  def getCellsData(self, selectedColumn):
    header = ['Pos (z)', 'Was Predicted', 'Is Active', 'Activation Rate', 'Precision Rate']
    data = []
    for cell in selectedColumn.cells:
      pos = str(cell.z)
      wasPredicted = cell.isPredicted.atGivenStepAgo(Global.selStep + 1)
      isActive = cell.isActive.atGivenStepAgo(Global.selStep)
      activationRate = "{0:.3f}".format(cell.statsActivationRate)
      precisionRate = "{0:.3f}".format(cell.statsPrecisionRate)
      data.append([pos, wasPredicted, isActive, activationRate, precisionRate])

    return header, data

  def getDistalSegmetsData(self, selectedCell):
    header = ['Is Active', 'Activation Rate', 'Activation Rate']
    data = []
    for segment in selectedCell.segments:
      isActive = segment.isActive.atGivenStepAgo(Global.selStep)
      activationRate = "{0:.3f}".format(segment.statsActivationRate)
      data.append([isActive, activationRate, activationRate])

    return header, data

  def getDistalSynapsesData(self, selectedSegment):
    #TODO: Put lateral cell position (x,y,z)
    header = ['Permanence', 'Is Connected', 'Connection Rate']
    data = []
    for synapse in selectedSegment.synapses:
      permanence = "{0:.3f}".format(synapse.permanence.atGivenStepAgo(Global.selStep))
      isConnected = synapse.isConnected.atGivenStepAgo(Global.selStep)
      connectionRate = "{0:.3f}".format(synapse.statsConnectionRate)
      data.append([permanence, isConnected, connectionRate])

    return header, data

  def showTab(self, tab, title):
    tabFound = False
    for tabIdx in range(self.tabControlMain.count()):
      if self.tabControlMain.tabText(tabIdx) == title:
        tabFound = True
    if not tabFound:
      self.tabControlMain.addTab(tab, title)

  #endregion

  #region Events

  def closeEvent(self, event):
    self.Hide()
    self.Parent = None
    event.Cancel = True

  def __sliderStep_ValueChanged(self, value):
    self.updatePredictedValuesGrid()

  def __comboBoxEncoding_CurrentIndexChanged(self, event):
    if Global.simulationInitialized:
      encodingIdx = self.comboBoxEncoding.currentIndex()
      self.selectedEncoding = self.selectedSensor.encodings[encodingIdx]
      self.updateEncodingControls()

  def __checkBoxEnableSpatialLearning_Toggled(self, event):
    self.selectedRegion.enableSpatialLearning = self.checkBoxEnableSpatialLearning.isChecked()

  def __checkBoxEnableTemporalLearning_Toggled(self, event):
    self.selectedRegion.enableTemporalLearning = self.checkBoxEnableTemporalLearning.isChecked()

  def __checkBoxEnableClassificationLearning_Toggled(self, event):
    self.selectedSensor.enableClassificationLearning = self.checkBoxEnableClassificationLearning.isChecked()

  def __checkBoxEnableClassificationInference_Toggled(self, event):
    self.selectedSensor.enableClassificationInference = self.checkBoxEnableClassificationInference.isChecked()

  def __dataGridColumns_SelectionChanged(self, event):
    if self.selectedColumn != None:
      self.selectedColumn.segment.tree3d_selected = False

    self.dataGridProximalSynapses.clearSelection()
    self.dataGridCells.clearSelection()

    selectedRows = self.dataGridColumns.selectionModel().selectedRows()
    if len(selectedRows) > 0:
      index = selectedRows[0].row()
      self.selectedColumn = self.selectedRegion.columns[index]
      self.selectedColumn.segment.tree3d_selected = True

      # Bind the synapses of the selected segment
      self.showTab(self.tabPageProximalSynapses, "Proximal Synapses")
      header, data = self.getProximalSynapsesData(self.selectedColumn.segment)
      self.dataGridProximalSynapses.model().update(header, data)
      self.dataGridProximalSynapses.resizeColumnsToContents()

      # Bind the cells of the selected column
      self.showTab(self.tabPageCells, "Cells")
      header, data = self.getCellsData(self.selectedColumn)
      self.dataGridCells.model().update(header, data)
      self.dataGridCells.resizeColumnsToContents()

    Global.simulationForm.refreshControls()

  def __dataGridProximalSynapses_SelectionChanged(self, event):
    if self.selectedProximalSynapse != None:
      self.selectedProximalSynapse.tree3d_selected = False

    selectedRows = self.dataGridProximalSynapses.selectionModel().selectedRows()
    if len(selectedRows) > 0:
      index = selectedRows[0].row()
      self.selectedProximalSynapse = self.selectedColumn.segment.synapses[index]
      self.selectedProximalSynapse.tree3d_selected = True

    Global.simulationForm.refreshControls()

  def __dataGridCells_SelectionChanged(self, event):
    if self.selectedCell != None:
      self.selectedCell.tree3d_selected = False

    self.dataGridDistalSegments.clearSelection()

    selectedRows = self.dataGridCells.selectionModel().selectedRows()
    if len(selectedRows) > 0:
      index = selectedRows[0].row()
      self.selectedCell = self.selectedColumn.cells[index]
      self.selectedCell.tree3d_selected = True

      # Bind the segments of the selected cell
      self.showTab(self.tabPageDistalSegments, "Distal Segments")
      header, data = self.getDistalSegmetsData(self.selectedCell)
      self.dataGridDistalSegments.model().update(header, data)
      self.dataGridDistalSegments.resizeColumnsToContents()

    Global.simulationForm.refreshControls()

  def __dataGridDistalSegments_SelectionChanged(self, event):
    if self.selectedDistalSegment != None:
      self.selectedDistalSegment.tree3d_selected = False

    self.dataGridDistalSynapses.clearSelection()

    selectedRows = self.dataGridDistalSegments.selectionModel().selectedRows()
    if len(selectedRows) > 0:
      index = selectedRows[0].row()
      self.selectedDistalSegment = self.selectedCell.segments[index]

      # Bind the synapses of the selected segment
      self.showTab(self.tabPageDistalSynapses, "Distal Synapses")
      header, data = self.getDistalSynapsesData(self.selectedDistalSegment)
      self.dataGridDistalSynapses.model().update(header, data)
      self.dataGridDistalSynapses.resizeColumnsToContents()

    Global.simulationForm.refreshControls()

  def __dataGridDistalSynapses_SelectionChanged(self, event):
    if self.selectedDistalSynapse != None:
      self.selectedDistalSynapse.tree3d_selected = False

    selectedRows = self.dataGridDistalSynapses.selectionModel().selectedRows()
    if len(selectedRows) > 0:
      index = selectedRows[0].row()
      self.selectedDistalSynapse = self.selectedDistalSegment.synapses[index]
      self.selectedDistalSynapse.tree3d_selected = True

    Global.simulationForm.refreshControls()

  #endregion
