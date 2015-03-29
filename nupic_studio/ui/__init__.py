import os
import collections
from PyQt4 import QtGui, QtCore
from nupic_studio.htm import maxPreviousStepsWithInference

class View:
  """
  A class only to group properties related to pre-defined views.
  """

  #region Constructor

  def __init__(self):
    """
    Initializes a new instance of this class.
    """

    #region Instance fields

    self.menu = None
    self.name = ""
    self.showBitsNone = False
    self.showBitsActive = True
    self.showBitsPredicted = True
    self.showBitsFalselyPredicted = True
    self.showCellsNone = False
    self.showCellsLearning = True
    self.showCellsActive = True
    self.showCellsPredicted = True
    self.showCellsFalselyPredicted = True
    self.showCellsInactive = True
    self.showProximalSegmentsNone = False
    self.showProximalSegmentsActive = True
    self.showProximalSegmentsPredicted = True
    self.showProximalSegmentsFalselyPredicted = True
    self.showProximalSynapsesNone = False
    self.showProximalSynapsesConnected = True
    self.showProximalSynapsesActive = True
    self.showProximalSynapsesPredicted = True
    self.showProximalSynapsesFalselyPredicted = True
    self.showDistalSegmentsNone = False
    self.showDistalSegmentsActive = True
    self.showDistalSynapsesNone = False
    self.showDistalSynapsesConnected = True
    self.showDistalSynapsesActive = True

    #endregion

  #endregion

class Global:
  appPath = ''
  version = '0.1.0'

  simulationInitialized = False
  currStep = 0
  selStep = 0
  timeStepsPredictionsChart = None
  output = []

  views = []

  project = None
  architectureForm = None
  nodeInformationForm = None
  simulationForm = None
  outputForm = None
  mainForm = None

  @staticmethod
  def loadConfig():
    """
    Loads the content from XML file to config the program.
    """

    fileName = os.path.join(Global.appPath, "nupic_studio.config")
    file = QtCore.QFile(fileName)
    if (file.open(QtCore.QIODevice.ReadOnly)):
      xmlReader = QtCore.QXmlStreamReader()
      xmlReader.setDevice(file)
      while (not xmlReader.isEndDocument()):
        if xmlReader.isStartElement():
          if xmlReader.name().toString() == 'View':
            view = View()
            view.name = Global.__getStringAttribute(xmlReader.attributes(), 'name')
            view.showBitsNone = Global.__getBooleanAttribute(xmlReader.attributes(), 'showBitsNone')
            view.showBitsActive = Global.__getBooleanAttribute(xmlReader.attributes(), 'showBitsActive')
            view.showBitsPredicted = Global.__getBooleanAttribute(xmlReader.attributes(), 'showBitsPredicted')
            view.showBitsFalselyPredicted = Global.__getBooleanAttribute(xmlReader.attributes(), 'showBitsFalselyPredicted')
            view.showCellsNone = Global.__getBooleanAttribute(xmlReader.attributes(), 'showCellsNone')
            view.showCellsLearning = Global.__getBooleanAttribute(xmlReader.attributes(), 'showCellsLearning')
            view.showCellsActive = Global.__getBooleanAttribute(xmlReader.attributes(), 'showCellsActive')
            view.showCellsPredicted = Global.__getBooleanAttribute(xmlReader.attributes(), 'showCellsPredicted')
            view.showCellsFalselyPredicted = Global.__getBooleanAttribute(xmlReader.attributes(), 'showCellsFalselyPredicted')
            view.showCellsInactive = Global.__getBooleanAttribute(xmlReader.attributes(), 'showCellsInactive')
            view.showProximalSegmentsNone = Global.__getBooleanAttribute(xmlReader.attributes(), 'showProximalSegmentsNone')
            view.showProximalSegmentsActive = Global.__getBooleanAttribute(xmlReader.attributes(), 'showProximalSegmentsActive')
            view.showProximalSegmentsPredicted = Global.__getBooleanAttribute(xmlReader.attributes(), 'showProximalSegmentsPredicted')
            view.showProximalSegmentsFalselyPredicted = Global.__getBooleanAttribute(xmlReader.attributes(), 'showProximalSegmentsFalselyPredicted')
            view.showProximalSynapsesNone = Global.__getBooleanAttribute(xmlReader.attributes(), 'showProximalSynapsesNone')
            view.showProximalSynapsesConnected = Global.__getBooleanAttribute(xmlReader.attributes(), 'showProximalSynapsesConnected')
            view.showProximalSynapsesActive = Global.__getBooleanAttribute(xmlReader.attributes(), 'showProximalSynapsesActive')
            view.showProximalSynapsesPredicted = Global.__getBooleanAttribute(xmlReader.attributes(), 'showProximalSynapsesPredicted')
            view.showProximalSynapsesFalselyPredicted = Global.__getBooleanAttribute(xmlReader.attributes(), 'showProximalSynapsesFalselyPredicted')
            view.showDistalSegmentsNone = Global.__getBooleanAttribute(xmlReader.attributes(), 'showDistalSegmentsNone')
            view.showDistalSegmentsActive = Global.__getBooleanAttribute(xmlReader.attributes(), 'showDistalSegmentsActive')
            view.showDistalSynapsesNone = Global.__getBooleanAttribute(xmlReader.attributes(), 'showDistalSynapsesNone')
            view.showDistalSynapsesConnected = Global.__getBooleanAttribute(xmlReader.attributes(), 'showDistalSynapsesConnected')
            view.showDistalSynapsesActive = Global.__getBooleanAttribute(xmlReader.attributes(), 'showDistalSynapsesActive')
            Global.views.append(view)
        xmlReader.readNext()
      if (xmlReader.hasError()):
        QtGui.QMessageBox.critical(None, "Critical", "Ocurred a XML error: " + xmlReader.errorString().data(), QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default, QtGui.QMessageBox.NoButton)
    else:
      QtGui.QMessageBox.critical(None, "Critical", "Cannot read the config file!", QtGui.QMessageBox.Ok | QtGui.QMessageBox.Default, QtGui.QMessageBox.NoButton)

  @staticmethod
  def __getStringAttribute(attributes, attributeName):
    if attributes.value(attributeName).toString() != "":
      attributeValue = str(attributes.value(attributeName).toString())
    else:
      attributeValue = ""
    return attributeValue

  @staticmethod
  def __getIntegerAttribute(attributes, attributeName):
    attributeValue = 0
    if attributes.value(attributeName).toString() != "":
      attributeValue = int(attributes.value(attributeName).toString())
    return attributeValue

  @staticmethod
  def __getFloatAttribute(attributes, attributeName):
    attributeValue = 0.0
    if attributes.value(attributeName).toString() != "":
      attributeValue = float(attributes.value(attributeName).toString())
    return attributeValue

  @staticmethod
  def __getBooleanAttribute(attributes, attributeName):
    attributeValue = False
    if attributes.value(attributeName).toString() == "True":
      attributeValue = True
    return attributeValue

  @staticmethod
  def saveConfig():
    """
    Saves the content from current program's configuration.
    """

    fileName = os.path.join(Global.appPath, "nupic_studio.config")
    file = QtCore.QFile(fileName)
    file.open(QtCore.QIODevice.WriteOnly)
    xmlWriter = QtCore.QXmlStreamWriter(file)
    xmlWriter.setAutoFormatting(True)
    xmlWriter.writeStartDocument()
    xmlWriter.writeStartElement('Program')

    for view in Global.views:
      xmlWriter.writeStartElement('View')
      xmlWriter.writeAttribute('name', view.name)
      xmlWriter.writeAttribute('showBitsNone',  str(view.showBitsNone))
      xmlWriter.writeAttribute('showBitsActive',  str(view.showBitsActive))
      xmlWriter.writeAttribute('showBitsPredicted',  str(view.showBitsPredicted))
      xmlWriter.writeAttribute('showBitsFalselyPredicted',  str(view.showBitsFalselyPredicted))
      xmlWriter.writeAttribute('showCellsNone',  str(view.showCellsNone))
      xmlWriter.writeAttribute('showCellsLearning',  str(view.showCellsLearning))
      xmlWriter.writeAttribute('showCellsActive',  str(view.showCellsActive))
      xmlWriter.writeAttribute('showCellsPredicted',  str(view.showCellsPredicted))
      xmlWriter.writeAttribute('showCellsFalselyPredicted',  str(view.showCellsFalselyPredicted))
      xmlWriter.writeAttribute('showCellsInactive',  str(view.showCellsInactive))
      xmlWriter.writeAttribute('showProximalSegmentsNone',  str(view.showProximalSegmentsNone))
      xmlWriter.writeAttribute('showProximalSegmentsActive',  str(view.showProximalSegmentsActive))
      xmlWriter.writeAttribute('showProximalSegmentsPredicted',  str(view.showProximalSegmentsPredicted))
      xmlWriter.writeAttribute('showProximalSegmentsFalselyPredicted',  str(view.showProximalSegmentsFalselyPredicted))
      xmlWriter.writeAttribute('showProximalSynapsesNone',  str(view.showProximalSynapsesNone))
      xmlWriter.writeAttribute('showProximalSynapsesConnected',  str(view.showProximalSynapsesConnected))
      xmlWriter.writeAttribute('showProximalSynapsesActive',  str(view.showProximalSynapsesActive))
      xmlWriter.writeAttribute('showProximalSynapsesPredicted',  str(view.showProximalSynapsesPredicted))
      xmlWriter.writeAttribute('showProximalSynapsesFalselyPredicted',  str(view.showProximalSynapsesFalselyPredicted))
      xmlWriter.writeAttribute('showDistalSegmentsNone',  str(view.showDistalSegmentsNone))
      xmlWriter.writeAttribute('showDistalSegmentsActive',  str(view.showDistalSegmentsActive))
      xmlWriter.writeAttribute('showDistalSynapsesNone',  str(view.showDistalSynapsesNone))
      xmlWriter.writeAttribute('showDistalSynapsesConnected',  str(view.showDistalSynapsesConnected))
      xmlWriter.writeAttribute('showDistalSynapsesActive',  str(view.showDistalSynapsesActive))
      xmlWriter.writeEndElement()

    xmlWriter.writeEndElement()
    xmlWriter.writeEndDocument()
    file.close()
