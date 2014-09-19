from PyQt4 import QtGui, QtCore
from nustudio.htm.node import NodeType, Node
from nustudio.htm.node_region import Region, InputMapType
from nustudio.htm.node_sensor import Sensor, InputFormat, DataSourceType

"""
Loads and saves the Elements of the .nuproj file, that contains user entries for project properties
Provides loaded elements as a structure to return.
"""

class Project:
	"""
	Loads and saves the Elements of the Project file, that contains user entries for Network configuration
	Provides loaded elements as a structure to return.
	"""

	#region Constructor

	def __init__(self):
		"""
		Initializes a new instance of this class.
		"""

		#region Instance fields

		self.fileName = ''
		"""Project file"""

		self.name = "Untitled"
		"""Name of the project."""

		self.author = ""
		"""Author of the project."""

		self.description = ""
		"""Description of the project."""

		self.topRegion = Region(None, "TopRegion")
		"""Parameters for the regions."""

		#endregion

	#endregion

	#region Methods

	def new(self):
		"""
		Initializes a new instance of this class.
		"""

		# Initialize metadata
		self.fileName = ''
		self.name = "Untitled"
		self.author = ""
		self.description = ""

		# Initialize top region params
		self.topRegion = Region(None, "TopRegion")

	def open(self, fileName):
		"""
		Loads the content from XML file to Project instance.
		"""

		self.fileName = fileName
		file = QtCore.QFile(self.fileName)
		if (file.open(QtCore.QIODevice.ReadOnly)):
			xmlReader = QtCore.QXmlStreamReader()
			xmlReader.setDevice(file)
			while (not xmlReader.isEndDocument()):
				if xmlReader.isStartElement():
					if xmlReader.name().toString() == 'MetaData':
						self.name = self.__getStringAttribute(xmlReader.attributes(), 'name')
						self.author = self.__getStringAttribute(xmlReader.attributes(), 'author')
						self.description = self.__getStringAttribute(xmlReader.attributes(), 'description')
					elif xmlReader.name().toString() == 'Net':
						xmlReader.readNextStartElement()
						self.topRegion = self.__readNode(None, xmlReader)

				xmlReader.readNext()
			if (xmlReader.hasError()):
				QtGui.QMessageBox.critical(self, "Critical", "Ocurred a XML error: " + xmlReader.errorString().data(), QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default, QtGui.QMessageBox.NoButton)
		else:
			QtGui.QMessageBox.critical(self, "Critical", "Cannot read the project file!", QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default, QtGui.QMessageBox.NoButton)

	def __getStringAttribute(self, attributes, attributeName):
		if attributes.value(attributeName).toString() != "":
			attributeValue = str(attributes.value(attributeName).toString())
		else:
			attributeValue = ""
		return attributeValue

	def __getIntegerAttribute(self, attributes, attributeName):
		attributeValue = 0
		if attributes.value(attributeName).toString() != "":
			attributeValue = int(attributes.value(attributeName).toString())
		return attributeValue

	def __getFloatAttribute(self, attributes, attributeName):
		attributeValue = 0.0
		if attributes.value(attributeName).toString() != "":
			attributeValue = float(attributes.value(attributeName).toString())
		return attributeValue

	def __getBooleanAttribute(self, attributes, attributeName):
		attributeValue = False
		if attributes.value(attributeName).toString() == "True":
			attributeValue = True
		return attributeValue

	def __readNode(self, parentNode, xmlReader):

		# Read type of node
		name = self.__getStringAttribute(xmlReader.attributes(), 'name')
		type = self.__getStringAttribute(xmlReader.attributes(), 'type')
		width = self.__getIntegerAttribute(xmlReader.attributes(), 'width')
		height = self.__getIntegerAttribute(xmlReader.attributes(), 'height')

		# Initialize node
		node = None
		if type == 'Region':
			node = Region(parentNode, name)
		elif type == 'Sensor':
			node = Sensor(parentNode, name)
		node.width = width
		node.height = height

		# Read specific parameters according to node type
		if type == 'Region':
			inputMapType = self.__getStringAttribute(xmlReader.attributes(), 'inputMapType')
			if inputMapType == "Grouped":
				node.inputMapType = InputMapType.grouped
			elif inputMapType == "Combined":
				node.inputMapType = InputMapType.combined
			node.enableSpatialPooling = self.__getBooleanAttribute(xmlReader.attributes(), 'enableSpatialPooling')
			node.potentialRadius = self.__getIntegerAttribute(xmlReader.attributes(), 'potentialRadius')
			node.potentialPct = self.__getFloatAttribute(xmlReader.attributes(), 'potentialPct')
			node.globalInhibition = self.__getBooleanAttribute(xmlReader.attributes(), 'globalInhibition')
			node.localAreaDensity = self.__getFloatAttribute(xmlReader.attributes(), 'localAreaDensity')
			node.numActiveColumnsPerInhArea = self.__getFloatAttribute(xmlReader.attributes(), 'numActiveColumnsPerInhArea')
			node.stimulusThreshold = self.__getIntegerAttribute(xmlReader.attributes(), 'stimulusThreshold')
			node.proximalSynConnectedPerm = self.__getFloatAttribute(xmlReader.attributes(), 'proximalSynConnectedPerm')
			node.proximalSynPermIncrement = self.__getFloatAttribute(xmlReader.attributes(), 'proximalSynPermIncrement')
			node.proximalSynPermDecrement = self.__getFloatAttribute(xmlReader.attributes(), 'proximalSynPermDecrement')
			node.minPctOverlapDutyCycle = self.__getFloatAttribute(xmlReader.attributes(), 'minPctOverlapDutyCycle')
			node.minPctActiveDutyCycle = self.__getFloatAttribute(xmlReader.attributes(), 'minPctActiveDutyCycle')
			node.dutyCyclePeriod = self.__getIntegerAttribute(xmlReader.attributes(), 'dutyCyclePeriod')
			node.maxBoost = self.__getFloatAttribute(xmlReader.attributes(), 'maxBoost')
			node.enableTemporalPooling = self.__getBooleanAttribute(xmlReader.attributes(), 'enableTemporalPooling')
			node.numCellsPerColumn = self.__getIntegerAttribute(xmlReader.attributes(), 'numCellsPerColumn')
			node.learningRadius = self.__getIntegerAttribute(xmlReader.attributes(), 'learningRadius')
			node.distalSynInitialPerm = self.__getFloatAttribute(xmlReader.attributes(), 'distalSynInitialPerm')
			node.distalSynConnectedPerm = self.__getFloatAttribute(xmlReader.attributes(), 'distalSynConnectedPerm')
			node.distalSynPermIncrement = self.__getFloatAttribute(xmlReader.attributes(), 'distalSynPermIncrement')
			node.distalSynPermDecrement = self.__getFloatAttribute(xmlReader.attributes(), 'distalSynPermDecrement')
			node.minThreshold = self.__getIntegerAttribute(xmlReader.attributes(), 'minThreshold')
			node.activationThreshold = self.__getIntegerAttribute(xmlReader.attributes(), 'activationThreshold')
			node.maxNumNewSynapses = self.__getIntegerAttribute(xmlReader.attributes(), 'maxNumNewSynapses')
		elif type == 'Sensor':
			inputFormat = self.__getStringAttribute(xmlReader.attributes(), 'inputFormat')
			if inputFormat == "Htm":
				node.inputFormat = InputFormat.htm
			elif inputFormat == "Raw":
				node.inputFormat = InputFormat.raw
				node.encoderModule = self.__getStringAttribute(xmlReader.attributes(), 'encoderModule')
				node.encoderClass = self.__getStringAttribute(xmlReader.attributes(), 'encoderClass')
				node.encoderParams = self.__getStringAttribute(xmlReader.attributes(), 'encoderParams')
			dataSourceType = self.__getStringAttribute(xmlReader.attributes(), 'dataSourceType')
			if dataSourceType == "File":
				node.dataSourceType = DataSourceType.file
				node.fileName = self.__getStringAttribute(xmlReader.attributes(), 'fileName')
			elif dataSourceType == "Database":
				node.dataSourceType = DataSourceType.database
				node.databaseConnectionString = self.__getStringAttribute(xmlReader.attributes(), 'databaseConnectionString')
				node.databaseTable = self.__getStringAttribute(xmlReader.attributes(), 'databaseTable')
				node.databaseField = self.__getStringAttribute(xmlReader.attributes(), 'databaseField')

		# If still is not end of element it's because this node has children
		token = xmlReader.readNext()
		if not xmlReader.isEndElement():
			while xmlReader.readNextStartElement():
				childNode = self.__readNode(node, xmlReader)
				node.children.append(childNode)

		return node
		
	def save(self, fileName):
		"""
		Saves the content from Project instance to XML file.
		"""

		self.fileName = fileName
		file = QtCore.QFile(self.fileName)
		file.open(QtCore.QIODevice.WriteOnly)
		xmlWriter = QtCore.QXmlStreamWriter(file)
		xmlWriter.setAutoFormatting(True)
		xmlWriter.writeStartDocument()
		xmlWriter.writeStartElement('Project')

		xmlWriter.writeStartElement('MetaData')
		xmlWriter.writeAttribute('name', self.name)
		xmlWriter.writeAttribute('author', self.author)
		xmlWriter.writeAttribute('description', self.description)
		xmlWriter.writeEndElement()

		xmlWriter.writeStartElement('Net')
		self.__writeNode(self.topRegion, xmlWriter)
		xmlWriter.writeEndElement()

		xmlWriter.writeEndElement()
		xmlWriter.writeEndDocument()
		file.close()

	def __writeNode(self, node, xmlWriter):

		# Write common parameters
		xmlWriter.writeStartElement('Node')
		xmlWriter.writeAttribute('name', node.name)

		# Write specific parameters according to node type
		if node.type == NodeType.region:
			xmlWriter.writeAttribute('type', 'Region')
			xmlWriter.writeAttribute('width', str(node.width))
			xmlWriter.writeAttribute('height', str(node.height))
			if node.inputMapType == InputMapType.grouped:
				xmlWriter.writeAttribute('inputMapType', "Grouped")
			elif node.inputMapType == InputMapType.combined:
				xmlWriter.writeAttribute('inputMapType', "Combined")
			xmlWriter.writeAttribute('enableSpatialPooling', str(node.enableSpatialPooling))
			xmlWriter.writeAttribute('potentialRadius', str(node.potentialRadius))
			xmlWriter.writeAttribute('potentialPct', str(node.potentialPct))
			xmlWriter.writeAttribute('globalInhibition', str(node.globalInhibition))
			xmlWriter.writeAttribute('localAreaDensity', str(node.localAreaDensity))
			xmlWriter.writeAttribute('numActiveColumnsPerInhArea', str(node.numActiveColumnsPerInhArea))
			xmlWriter.writeAttribute('stimulusThreshold', str(node.stimulusThreshold))
			xmlWriter.writeAttribute('proximalSynConnectedPerm', str(node.proximalSynConnectedPerm))
			xmlWriter.writeAttribute('proximalSynPermIncrement', str(node.proximalSynPermIncrement))
			xmlWriter.writeAttribute('proximalSynPermDecrement', str(node.proximalSynPermDecrement))
			xmlWriter.writeAttribute('minPctOverlapDutyCycle', str(node.minPctOverlapDutyCycle))
			xmlWriter.writeAttribute('minPctActiveDutyCycle', str(node.minPctActiveDutyCycle))
			xmlWriter.writeAttribute('dutyCyclePeriod', str(node.dutyCyclePeriod))
			xmlWriter.writeAttribute('maxBoost', str(node.maxBoost))
			xmlWriter.writeAttribute('enableTemporalPooling', str(node.enableTemporalPooling))
			xmlWriter.writeAttribute('numCellsPerColumn', str(node.numCellsPerColumn))
			xmlWriter.writeAttribute('learningRadius', str(node.learningRadius))
			xmlWriter.writeAttribute('distalSynInitialPerm', str(node.distalSynInitialPerm))
			xmlWriter.writeAttribute('distalSynConnectedPerm', str(node.distalSynConnectedPerm))
			xmlWriter.writeAttribute('distalSynPermIncrement', str(node.distalSynPermIncrement))
			xmlWriter.writeAttribute('distalSynPermDecrement', str(node.distalSynPermDecrement))
			xmlWriter.writeAttribute('minThreshold', str(node.minThreshold))
			xmlWriter.writeAttribute('activationThreshold', str(node.activationThreshold))
			xmlWriter.writeAttribute('maxNumNewSynapses', str(node.maxNumNewSynapses))
		elif node.type == NodeType.sensor:
			xmlWriter.writeAttribute('type', 'Sensor')
			xmlWriter.writeAttribute('width', str(node.width))
			xmlWriter.writeAttribute('height', str(node.height))
			if node.inputFormat == InputFormat.htm:
				xmlWriter.writeAttribute('inputFormat', "Htm")
			elif node.inputFormat == InputFormat.raw:
				xmlWriter.writeAttribute('inputFormat', "Raw")
				xmlWriter.writeAttribute('encoderModule', node.encoderModule)
				xmlWriter.writeAttribute('encoderClass', node.encoderClass)
				xmlWriter.writeAttribute('encoderParams', node.encoderParams)
			if node.dataSourceType == DataSourceType.file:
				xmlWriter.writeAttribute('dataSourceType', "File")
				xmlWriter.writeAttribute('fileName', node.fileName)
			elif node.dataSourceType == DataSourceType.database:
				xmlWriter.writeAttribute('dataSourceType', "Database")
				xmlWriter.writeAttribute('databaseConnectionString', node.databaseConnectionString)
				xmlWriter.writeAttribute('databaseTable', node.databaseTable)
				xmlWriter.writeAttribute('databaseField', node.databaseField)

		# Tranverse all child nodes
		for childNode in node.children:
			self.__writeNode(childNode, xmlWriter)

		xmlWriter.writeEndElement()

	#endregion
