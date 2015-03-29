from PyQt4 import QtGui, QtCore
from nupic_studio.htm.network import Network
from nupic_studio.htm.node import NodeType, Node
from nupic_studio.htm.node_region import Region
from nupic_studio.htm.node_sensor import Sensor, DataSourceType, PredictionsMethod
from nupic_studio.htm.encoding import Encoding
from nupic_studio.htm.link import Link

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

    self.network = Network()
    """The network created for the project."""

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

    # Create the top region
    topRegion = Region("TopRegion")

    # Create the network and add topRegion as its starting node
    self.network = Network()
    self.network.nodes.append(topRegion)
    self.network.preparePhases()

  def open(self, fileName):
    """
    Loads the content from XML file to Project instance.
    """

    # Create the network
    self.network = Network()

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
            while xmlReader.readNextStartElement():
              if xmlReader.name().toString() == 'Node':
                node = self.__readNode(xmlReader)
                self.network.nodes.append(node)
              elif xmlReader.name().toString() == 'Link':
                link = self.__readLink(xmlReader)
                self.network.links.append(link)

        xmlReader.readNext()
      if (xmlReader.hasError()):
        QtGui.QMessageBox.critical(self, "Critical", "Ocurred a XML error: " + xmlReader.errorString().data(), QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default, QtGui.QMessageBox.NoButton)
    else:
      QtGui.QMessageBox.critical(self, "Critical", "Cannot read the project file!", QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default, QtGui.QMessageBox.NoButton)

    self.network.preparePhases()

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

  def __readNode(self, xmlReader):

    # Read type of node
    name = self.__getStringAttribute(xmlReader.attributes(), 'name')
    type = self.__getStringAttribute(xmlReader.attributes(), 'type')

    # Create a node from parameters
    node = None
    if type == 'Region':
      node = Region(name)
    elif type == 'Sensor':
      node = Sensor(name)
    node.width = self.__getIntegerAttribute(xmlReader.attributes(), 'width')
    node.height = self.__getIntegerAttribute(xmlReader.attributes(), 'height')

    # Read specific parameters according to node type
    if type == 'Region':
      node.enableSpatialLearning = self.__getBooleanAttribute(xmlReader.attributes(), 'enableSpatialLearning')
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
      node.spSeed = self.__getIntegerAttribute(xmlReader.attributes(), 'spSeed')
      node.enableTemporalLearning = self.__getBooleanAttribute(xmlReader.attributes(), 'enableTemporalLearning')
      node.numCellsPerColumn = self.__getIntegerAttribute(xmlReader.attributes(), 'numCellsPerColumn')
      node.learningRadius = self.__getIntegerAttribute(xmlReader.attributes(), 'learningRadius')
      node.distalSynInitialPerm = self.__getFloatAttribute(xmlReader.attributes(), 'distalSynInitialPerm')
      node.distalSynConnectedPerm = self.__getFloatAttribute(xmlReader.attributes(), 'distalSynConnectedPerm')
      node.distalSynPermIncrement = self.__getFloatAttribute(xmlReader.attributes(), 'distalSynPermIncrement')
      node.distalSynPermDecrement = self.__getFloatAttribute(xmlReader.attributes(), 'distalSynPermDecrement')
      node.minThreshold = self.__getIntegerAttribute(xmlReader.attributes(), 'minThreshold')
      node.activationThreshold = self.__getIntegerAttribute(xmlReader.attributes(), 'activationThreshold')
      node.maxNumNewSynapses = self.__getIntegerAttribute(xmlReader.attributes(), 'maxNumNewSynapses')
      node.tpSeed = self.__getIntegerAttribute(xmlReader.attributes(), 'tpSeed')
    elif type == 'Sensor':
      dataSourceType = self.__getStringAttribute(xmlReader.attributes(), 'dataSourceType')
      if dataSourceType == "File":
        node.dataSourceType = DataSourceType.file
        node.fileName = self.__getStringAttribute(xmlReader.attributes(), 'fileName')
      elif dataSourceType == "Database":
        node.dataSourceType = DataSourceType.database
        node.databaseConnectionString = self.__getStringAttribute(xmlReader.attributes(), 'databaseConnectionString')
        node.databaseTable = self.__getStringAttribute(xmlReader.attributes(), 'databaseTable')
      node.predictionsMethod = self.__getStringAttribute(xmlReader.attributes(), 'predictionsMethod')
      if node.predictionsMethod == PredictionsMethod.classification:
        node.enableClassificationLearning = self.__getBooleanAttribute(xmlReader.attributes(), 'enableClassificationLearning')
        node.enableClassificationInference = self.__getBooleanAttribute(xmlReader.attributes(), 'enableClassificationInference')

      # If still is not end of element it's because this node has encodings
      token = xmlReader.readNext()
      if not xmlReader.isEndElement():
        while xmlReader.readNextStartElement():
          encoding = self.__readEncoding(xmlReader)
          node.encodings.append(encoding)

    token = xmlReader.readNext()

    return node

  def __readEncoding(self, xmlReader):

    # Create a encoding from parameters
    encoding = Encoding()
    encoding.dataSourceFieldName = self.__getStringAttribute(xmlReader.attributes(), 'dataSourceFieldName')
    encoding.dataSourceFieldDataType = self.__getStringAttribute(xmlReader.attributes(), 'dataSourceFieldDataType')
    encoding.enableInference = self.__getBooleanAttribute(xmlReader.attributes(), 'enableInference')
    encoding.encoderModule = self.__getStringAttribute(xmlReader.attributes(), 'encoderModule')
    encoding.encoderClass = self.__getStringAttribute(xmlReader.attributes(), 'encoderClass')
    encoding.encoderParams = self.__getStringAttribute(xmlReader.attributes(), 'encoderParams')
    encoding.encoderFieldName = self.__getStringAttribute(xmlReader.attributes(), 'encoderFieldName')
    encoding.encoderFieldDataType = self.__getStringAttribute(xmlReader.attributes(), 'encoderFieldDataType')
    token = xmlReader.readNext()

    return encoding

  def __readLink(self, xmlReader):

    # Read link parameters
    outNodeName = self.__getStringAttribute(xmlReader.attributes(), 'outNode')
    inNodeName = self.__getStringAttribute(xmlReader.attributes(), 'inNode')
    token = xmlReader.readNext()

    # Find output node instance
    outNode = None
    for node in self.network.nodes:
      if node.name == outNodeName:
        outNode = node
        break

    # Find input node instance
    inNode = None
    for node in self.network.nodes:
      if node.name == inNodeName:
        inNode = node
        break

    # Create a link from parameters
    link = Link()
    link.outNode = outNode
    link.inNode = inNode

    return link

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
    for node in self.network.nodes:
      self.__writeNode(node, xmlWriter)
    for link in self.network.links:
      self.__writeLink(link, xmlWriter)
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
      xmlWriter.writeAttribute('enableSpatialLearning', str(node.enableSpatialLearning))
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
      xmlWriter.writeAttribute('spSeed', str(node.spSeed))
      xmlWriter.writeAttribute('enableTemporalLearning', str(node.enableTemporalLearning))
      xmlWriter.writeAttribute('numCellsPerColumn', str(node.numCellsPerColumn))
      xmlWriter.writeAttribute('learningRadius', str(node.learningRadius))
      xmlWriter.writeAttribute('distalSynInitialPerm', str(node.distalSynInitialPerm))
      xmlWriter.writeAttribute('distalSynConnectedPerm', str(node.distalSynConnectedPerm))
      xmlWriter.writeAttribute('distalSynPermIncrement', str(node.distalSynPermIncrement))
      xmlWriter.writeAttribute('distalSynPermDecrement', str(node.distalSynPermDecrement))
      xmlWriter.writeAttribute('minThreshold', str(node.minThreshold))
      xmlWriter.writeAttribute('activationThreshold', str(node.activationThreshold))
      xmlWriter.writeAttribute('maxNumNewSynapses', str(node.maxNumNewSynapses))
      xmlWriter.writeAttribute('tpSeed', str(node.tpSeed))
    elif node.type == NodeType.sensor:
      xmlWriter.writeAttribute('type', 'Sensor')
      xmlWriter.writeAttribute('width', str(node.width))
      xmlWriter.writeAttribute('height', str(node.height))
      if node.dataSourceType == DataSourceType.file:
        xmlWriter.writeAttribute('dataSourceType', "File")
        xmlWriter.writeAttribute('fileName', node.fileName)
      elif node.dataSourceType == DataSourceType.database:
        xmlWriter.writeAttribute('dataSourceType', "Database")
        xmlWriter.writeAttribute('databaseConnectionString', node.databaseConnectionString)
        xmlWriter.writeAttribute('databaseTable', node.databaseTable)
      xmlWriter.writeAttribute('predictionsMethod', node.predictionsMethod)
      if node.predictionsMethod == PredictionsMethod.classification:
        xmlWriter.writeAttribute('enableClassificationLearning', str(node.enableClassificationLearning))
        xmlWriter.writeAttribute('enableClassificationInference', str(node.enableClassificationInference))

      # Tranverse all encodings
      for encoding in node.encodings:
        self.__writeEncoding(encoding, xmlWriter)

    xmlWriter.writeEndElement()

  def __writeEncoding(self, encoding, xmlWriter):

    # Write encoding parameters
    xmlWriter.writeStartElement('Encoding')
    xmlWriter.writeAttribute('dataSourceFieldName', encoding.dataSourceFieldName)
    xmlWriter.writeAttribute('dataSourceFieldDataType', encoding.dataSourceFieldDataType)
    xmlWriter.writeAttribute('enableInference', str(encoding.enableInference))
    xmlWriter.writeAttribute('encoderModule', encoding.encoderModule)
    xmlWriter.writeAttribute('encoderClass', encoding.encoderClass)
    xmlWriter.writeAttribute('encoderParams', encoding.encoderParams)
    xmlWriter.writeAttribute('encoderFieldName', encoding.encoderFieldName)
    xmlWriter.writeAttribute('encoderFieldDataType', encoding.encoderFieldDataType)
    xmlWriter.writeEndElement()

  def __writeLink(self, link, xmlWriter):

    # Write encoding parameters
    xmlWriter.writeStartElement('Link')
    xmlWriter.writeAttribute('outNode', link.outNode.name)
    xmlWriter.writeAttribute('inNode', link.inNode.name)
    xmlWriter.writeEndElement()

  #endregion
