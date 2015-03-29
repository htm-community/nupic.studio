import os
import collections
import numpy
import operator
import math
import dateutil.parser
from PyQt4 import QtGui, QtCore
from nupic_studio import getInstantiatedClass
from nupic_studio.ui import Global
from nupic_studio.htm import maxPreviousSteps, maxFutureSteps, maxPreviousStepsWithInference
from nupic_studio.htm.node import Node, NodeType
from nupic_studio.htm.bit import Bit
from nupic_studio.htm.encoding import FieldDataType
from nupic.encoders import MultiEncoder
from nupic.data.file_record_stream import FileRecordStream

class DataSourceType:
  """
  Types of data sources which a sensor gets inputs.
  """

  file = 1
  database = 2

class PredictionsMethod:
  """
  Methods used to get predicted values and their probabilities
  """

  reconstruction = "Reconstruction"
  classification = "Classification"

class Sensor(Node):
  """
  A super class only to group properties related to sensors.
  """

  #region Constructor

  def __init__(self, name):
    """
    Initializes a new instance of this class.
    """

    Node.__init__(self, name, NodeType.sensor)

    #region Instance fields

    self.bits = []
    """An array of the bit objects that compose the current output of this node."""

    self.dataSource = None
    """Data source which provides records to fed into a region."""

    self.dataSourceType = DataSourceType.file
    """Type of the data source (File or Database)"""

    self.fileName = ''
    """The input file name to be handled. Returns the input file name only if it is in the project directory, full path otherwise."""

    self.databaseConnectionString = ""
    """Connection string of the database."""

    self.databaseTable = ''
    """Target table of the database."""

    self.encoder = None
    """Multi-encoder which concatenate sub-encodings to convert raw data to htm input and vice-versa."""

    self.encodings = []
    """List of sub-encodings that handles the input from database"""

    self.predictionsMethod = PredictionsMethod.reconstruction
    """Method used to get predicted values and their probabilities."""

    self.enableClassificationLearning = True
    """Switch for classification learning"""

    self.enableClassificationInference = True
    """Switch for classification inference"""

    #endregion

    #region Statistics properties

    self.statsPrecisionRate = 0.

    #endregion

  #endregion

  #region Methods

  def getBit(self, x, y):
    """
    Return the bit located at given position
    """

    bit = self.bits[(y * self.width) + x]

    return bit

  def initialize(self):
    """
    Initialize this node.
    """

    Node.initialize(self)

    # Initialize input bits
    self.bits = []
    for x in range(self.width):
      for y in range(self.height):
        bit = Bit()
        bit.x = x
        bit.y = y
        self.bits.append(bit)

    if self.dataSourceType == DataSourceType.file:
      """
      Initialize this node opening the file and place cursor on the first record.
      """

      # If file name provided is a relative path, use project file path
      if self.fileName != '' and os.path.dirname(self.fileName) == '':
        fullFileName = os.path.dirname(Global.project.fileName) + '/' + self.fileName
      else:
        fullFileName = self.fileName

      # Check if file really exists
      if not os.path.isfile(fullFileName):
        QtGui.QMessageBox.warning(None, "Warning", "Input stream file '" + fullFileName + "' was not found or specified.", QtGui.QMessageBox.Ok)
        return

      # Create a data source for read the file
      self.dataSource = FileRecordStream(fullFileName)

    elif self.dataSourceType == DataSourceType.database:
      pass

    self.encoder = MultiEncoder()
    for encoding in self.encodings:
      encoding.initialize()

      # Create an instance class for an encoder given its module, class and constructor params
      encoding.encoder = getInstantiatedClass(encoding.encoderModule, encoding.encoderClass, encoding.encoderParams)

      # Take the first part of encoder field name as encoder name
      # Ex: timestamp_weekend.weekend => timestamp_weekend
      encoding.encoder.name = encoding.encoderFieldName.split('.')[0]

      # Add sub-encoder to multi-encoder list
      self.encoder.addEncoder(encoding.dataSourceFieldName, encoding.encoder)

    # If encoder size is not the same to sensor size then throws exception
    encoderSize = self.encoder.getWidth()
    sensorSize = self.width * self.height
    if encoderSize > sensorSize:
      QtGui.QMessageBox.warning(None, "Warning", "'" + self.name + "': Encoder size (" + str(encoderSize) + ") is different from sensor size (" + str(self.width) + " x " + str(self.height) + " = " + str(sensorSize) + ").", QtGui.QMessageBox.Ok)
      return

    return True

  def nextStep(self):
    """
    Performs actions related to time step progression.
    """

    # Update states machine by remove the first element and add a new element in the end
    for encoding in self.encodings:
      encoding.currentValue.rotate()
      if encoding.enableInference:
        encoding.predictedValues.rotate()
        encoding.bestPredictedValue.rotate()

    Node.nextStep(self)
    for bit in self.bits:
      bit.nextStep()

    # Get record value from data source
    # If the last record was reached just rewind it
    data = self.dataSource.getNextRecordDict()
    if not data:
      self.dataSource.rewind()
      data = self.dataSource.getNextRecordDict()

    # Pass raw values to encoder and get a concatenated array
    outputArray = numpy.zeros(self.encoder.getWidth())
    self.encoder.encodeIntoArray(data, outputArray)

    # Get values obtained from the data source.
    outputValues = self.encoder.getScalars(data)

    # Get raw values and respective encoded bit array for each field
    prevOffset = 0
    for i in range(len(self.encodings)):
      encoding = self.encodings[i]

      # Convert the value to its respective data type
      currValue = outputValues[i]
      if encoding.encoderFieldDataType == FieldDataType.boolean:
        currValue = bool(currValue)
      elif encoding.encoderFieldDataType == FieldDataType.integer:
        currValue = int(currValue)
      elif encoding.encoderFieldDataType == FieldDataType.decimal:
        currValue = float(currValue)
      elif encoding.encoderFieldDataType == FieldDataType.dateTime:
        currValue = dateutil.parser.parse(str(currValue))
      elif encoding.encoderFieldDataType == FieldDataType.string:
        currValue = str(currValue)
      encoding.currentValue.setForCurrStep(currValue)

    # Update sensor bits
    for i in range(len(outputArray)):
      if outputArray[i] > 0.:
        self.bits[i].isActive.setForCurrStep(True)
      else:
        self.bits[i].isActive.setForCurrStep(False)

    # Mark falsely predicted bits
    for bit in self.bits:
      if bit.isPredicted.atPreviousStep() and not bit.isActive.atCurrStep():
        bit.isFalselyPredicted.setForCurrStep(True)

    self._output = outputArray

  def getPredictions(self):
    """
    Get the predictions after an iteration.
    """

    if self.predictionsMethod == PredictionsMethod.reconstruction:

      # Prepare list with predictions to be classified
      # This list contains the indexes of all bits that are predicted
      output = []
      for i in range(len(self.bits)):
        if self.bits[i].isPredicted.atCurrStep():
          output.append(1)
        else:
          output.append(0)
      output = numpy.array(output)

      # Decode output and create predictions list
      fieldsDict, fieldsOrder = self.encoder.decode(output)
      for encoding in self.encodings:
        if encoding.enableInference:
          predictions = []
          encoding.predictedValues.setForCurrStep(dict())

          # If encoder field name was returned by decode(), assign the the predictions to it
          if encoding.encoderFieldName in fieldsOrder:
            predictedLabels = fieldsDict[encoding.encoderFieldName][1].split(', ')
            predictedValues = fieldsDict[encoding.encoderFieldName][0]
            for i in range(len(predictedLabels)):
              predictions.append([predictedValues[i], predictedLabels[i]])

          encoding.predictedValues.atCurrStep()[1] = predictions

          # Get the predicted value with the biggest probability to happen
          if len(predictions) > 0:
            bestPredictionRange = predictions[0][0]
            min = bestPredictionRange[0]
            max = bestPredictionRange[1]
            bestPredictedValue = (min + max) / 2.0
            encoding.bestPredictedValue.setForCurrStep(bestPredictedValue)

    elif self.predictionsMethod == PredictionsMethod.classification:
      # A classification involves estimate which are the likely values to occurs in the next time step.

      offset = 0
      for encoding in self.encodings:
        encoderWidth = encoding.encoder.getWidth()

        if encoding.enableInference:
          # Prepare list with predictions to be classified
          # This list contains the indexes of all bits that are predicted
          patternNZ = []
          for i in range(offset, encoderWidth):
            if self.bits[i].isActive.atCurrStep():
              patternNZ.append(i)

          # Get the bucket index of the current value at the encoder
          actualValue = encoding.currentValue.atCurrStep()
          bucketIdx = encoding.encoder.getBucketIndices(actualValue)[0]

          # Perform classification
          clasResults = encoding.classifier.compute(recordNum=Global.currStep, patternNZ=patternNZ, classification={'bucketIdx': bucketIdx, 'actValue': actualValue}, learn=self.enableClassificationLearning, infer=self.enableClassificationInference)

          encoding.predictedValues.setForCurrStep(dict())
          for step in encoding.steps:

            # Calculate probability for each predicted value
            predictions = dict()
            for (actValue, prob) in zip(clasResults['actualValues'], clasResults[step]):
              if actValue in predictions:
                predictions[actValue] += prob
              else:
                predictions[actValue] = prob

            # Remove predictions with low probabilities
            maxVal = (None, None)
            for (actValue, prob) in predictions.items():
              if len(predictions) <= 1:
                break
              if maxVal[0] is None or prob >= maxVal[1]:
                if maxVal[0] is not None and maxVal[1] < encoding.minProbabilityThreshold:
                  del predictions[maxVal[0]]
                maxVal = (actValue, prob)
              elif prob < encoding.minProbabilityThreshold:
                del predictions[actValue]

            # Sort the list of values from more probable to less probable values
            # an decrease the list length to max predictions per step limit
            predictions = sorted(predictions.iteritems(), key=operator.itemgetter(1), reverse=True)
            predictions = predictions[:maxFutureSteps]

            encoding.predictedValues.atCurrStep()[step] = predictions

          # Get the predicted value with the biggest probability to happen
          bestPredictedValue = encoding.predictedValues.atCurrStep()[1][0][0]
          encoding.bestPredictedValue.setForCurrStep(bestPredictedValue)

        offset += encoderWidth

  def calculateStatistics(self):
    """
    Calculate statistics after an iteration.
    """

    if Global.currStep > 0:
      precision = 0.

      # Calculate the prediction precision comparing if the current value is in the range of any prediction.
      for encoding in self.encodings:
        if encoding.enableInference:
          predictions = encoding.predictedValues.atPreviousStep()[1]
          for predictedValue in predictions:
            min = None
            max = None
            value = predictedValue[0]
            if self.predictionsMethod == PredictionsMethod.reconstruction:
              min = value[0]
              max = value[1]
            elif self.predictionsMethod == PredictionsMethod.classification:
              min = value
              max = value
            if isinstance(min, (int, long, float, complex)) and isinstance(max, (int, long, float, complex)):
              min = math.floor(min)
              max = math.ceil(max)
            if min <= encoding.currentValue.atCurrStep() <= max:
              precision = 100.
              break

      # The precision rate is the average of the precision calculated in every step
      self.statsPrecisionRate = (self.statsPrecisionRate + precision) / 2
    else:
      self.statsPrecisionRate = 0.

    for bit in self.bits:
      bit.calculateStatistics()

  #endregion
