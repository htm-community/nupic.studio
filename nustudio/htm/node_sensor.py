import os
import datetime
import numpy
import operator
import math
from PyQt4 import QtGui, QtCore
from nustudio import getInstantiatedClass
from nustudio.ui import Global
from nustudio.htm import maxPreviousSteps, maxFutureSteps
from nustudio.htm.node import Node, NodeType
from nustudio.htm.bit import Bit
from nupic.algorithms.CLAClassifier import CLAClassifier

class DataSourceType:
	"""
	Types of data sources which a sensor gets inputs.
	"""

	file = 1
	database = 2

class InputFormat:
	"""
	Types of input which a sensor should handle.
	"""

	htm = 1
	raw = 2

class InputRawDataType:
	"""
	Types of data which a raw input is composed.
	"""

	boolean = 1
	integer = 2
	decimal = 3
	dateTime = 4
	string = 5

class PredictionsMethod:
	"""
	Methods used to get predicted values and their probabilities
	"""

	reconstruction = 1
	classification = 2

class Sensor(Node):
	"""
	A super class only to group properties related to sensors.
	"""

	#region Constructor

	def __init__(self, parentNode, name):
		"""
		Initializes a new instance of this class.
		"""

		Node.__init__(self, parentNode, name, NodeType.sensor)

		#region Instance fields

		self.bits = []
		"""An array of the bit objects that compose the current output of this node."""

		self.dataSourceType = DataSourceType.file
		"""Type of the data source (File or Database)"""

		self.fileName = ''
		"""The input file name to be handled. Returns the input file name only if it is in the project directory, full path otherwise."""

		self._file = None
		"""File stream to handle the file."""

		self.databaseConnectionString = ""
		"""Connection string of the database."""

		self.databaseTable = ''
		"""Target table of the database."""

		self.databaseField = ''
		"""Target field of the database table."""

		self.inputFormat = InputFormat.htm
		"""Format of the node (HTM or raw data)"""

		self.inputRawDataType = InputRawDataType.string
		"""Data type of the raw input"""

		self.encoder = None
		"""Optional encoder to convert raw data to htm input and vice-versa."""

		self.encoderModule = ""
		"""Module name which encoder class is imported."""

		self.encoderClass = ""
		"""Class name which encode or decode values."""

		self.encoderParams = ""
		"""Parameters passed to the encoder class constructor."""

		self.predictionsMethod = PredictionsMethod.reconstruction
		"""Method used to get predicted values and their probabilities."""

		self.enableClassificationLearning = True
		"""Switch for classification learning"""

		self.enableClassificationInference = True
		"""Switch for classification inference"""

		self.currentValue = [None] * maxPreviousSteps
		"""Raw value encoded to network."""

		self.predictedValues = [None] * maxPreviousSteps
		"""Raw value decoded from network."""

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

			# Open file
			if not os.path.isfile(fullFileName):
				QtGui.QMessageBox.warning(None, "Warning", "Input stream file '" + fullFileName + "' was not found or specified.", QtGui.QMessageBox.Ok)
				return

			if self.inputFormat == InputFormat.htm:
				self._file = open(fullFileName, "rb")

				# Get dimensions of the record
				width = 0
				height = 0
				character = 0
				while True:
					# Read next character
					character = self._file.read(1)

					# Check if character is 'return' and not a number, i.e. if the first record was read
					if character == '\r':
						character = self._file.read(1)
					if character == '\n':
						break

					# Pass over the line until find a 'return' character in order to get the width
					width = 0
					while character != '\n':
						width += 1
						character = self._file.read(1)
						if character == '\r':
							character = self._file.read(1)

					# Increments height
					height += 1

				# If current file record dimensions is not the same to sensor size then throws exception
				if self.width != width or self.height != height:
					QtGui.QMessageBox.warning(None, "Warning", "'" + self.name + "': File input size (" + width + " x " + height + ") is different from sensor size (" + self.width + " x " + self.height + ").", QtGui.QMessageBox.Ok)
					return

				# Put the pointer back to initial position
				self._file.seek(0)
			elif self.inputFormat == InputFormat.raw:
				self._file = open(fullFileName)

				# Create an instance class for an encoder given its module, class and constructor params
				self.encoder = getInstantiatedClass(self.encoderModule, self.encoderClass, self.encoderParams)

				# If encoder size is not the same to sensor size then throws exception
				encoderSize = self.encoder.getWidth()
				sensorSize = self.width * self.height
				if encoderSize > sensorSize:
					QtGui.QMessageBox.warning(None, "Warning", "'" + self.name + "': Encoder size (" + str(encoderSize) + ") is different from sensor size (" + str(self.width) + " x " + str(self.height) + " = " + str(sensorSize) + ").", QtGui.QMessageBox.Ok)
					return

		elif self.dataSourceType == DataSourceType.database:
			pass

		# Create Classifier instance with appropriate parameters
		self.minProbabilityThreshold = 0.0001
		self.steps = []
		for step in range(maxFutureSteps):
			self.steps.append(step+1)
		self.classifier = CLAClassifier(steps=self.steps)

	def nextStep(self):
		"""
		Performs actions related to time step progression.
		"""

		# Update states machine by remove the first element and add a new element in the end
		if self.inputFormat == InputFormat.raw:
			if len(self.currentValue) > maxPreviousSteps:
				self.currentValue.remove(self.currentValue[0])
				self.predictedValues.remove(self.predictedValues[0])
			self.currentValue.append(None)
			self.predictedValues.append(None)

		Node.nextStep(self)
		for bit in self.bits:
			bit.nextStep()

		# Get record value from data source
		recordValue = None
		if self.dataSourceType == DataSourceType.file:
			recordValue = self.__getNextFileRecord()
		elif self.dataSourceType == DataSourceType.database:
			pass

		# Handle the value according to its type
		self._output = []
		if self.inputFormat == InputFormat.htm:

			# Initialize the array for representing the current record
			self._output = recordValue
		elif self.inputFormat == InputFormat.raw:

			# Convert the value to its respective data type
			rawValue = None
			if self.inputRawDataType == InputRawDataType.boolean:
				rawValue = bool(recordValue)
			elif self.inputRawDataType == InputRawDataType.integer:
				rawValue = int(recordValue)
			elif self.inputRawDataType == InputRawDataType.decimal:
				rawValue = float(recordValue)
			elif self.inputRawDataType == InputRawDataType.dateTime:
				rawValue = datetime.datetime.strptime(recordValue, "%m/%d/%y %H:%M")
			elif self.inputRawDataType == InputRawDataType.string:
				rawValue = str(recordValue)
			self.currentValue[maxPreviousSteps - 1] = rawValue

			# Pass raw value to encoder and get its respective array
			self._output = self.encoder.encode(rawValue)

		# Update sensor bits
		for i in range(len(self._output)):
			if self._output[i] > 0.:
				self.bits[i].isActive[maxPreviousSteps - 1] = True
			else:
				self.bits[i].isActive[maxPreviousSteps - 1] = False

		# Mark falsely predicted bits
		for bit in self.bits:
			if bit.isPredicted[maxPreviousSteps - 2] and not bit.isActive[maxPreviousSteps - 1]:
				bit.isFalselyPredicted[maxPreviousSteps - 1] = True

	def getPredictions(self):
		"""
		Get the predictions after an iteration.
		"""

		if self.inputFormat == InputFormat.raw:

			if self.predictionsMethod == PredictionsMethod.reconstruction:

				# Prepare list with predictions to be classified
				# This list contains the indexes of all bits that are predicted
				output = []
				for i in range(len(self.bits)):
					if self.bits[i].isPredicted[maxPreviousSteps - 1]:
						output.append(1)
					else:
						output.append(0)
				output = numpy.array(output)

				# Decode output and create predictions list
				fieldsDict, fieldsOrder = self.encoder.decode(output)
				self.predictedValues[maxPreviousSteps - 1] = dict()
				predictions = []
				if len(fieldsOrder) > 0:
					fieldName = fieldsOrder[0]
					predictedLabels = fieldsDict[fieldName][1].split(', ')
					predictedValues = fieldsDict[fieldName][0]
					for i in range(len(predictedLabels)):
						predictions.append([predictedValues[i], predictedLabels[i]])

				self.predictedValues[maxPreviousSteps - 1][1] = predictions

			elif self.predictionsMethod == PredictionsMethod.classification:
				# A classification involves estimate which are the likely values to occurs in the next time step.

				# Prepare list with predictions to be classified
				# This list contains the indexes of all bits that are predicted
				patternNZ = []
				for i in range(len(self.bits)):
					if self.bits[i].isActive[maxPreviousSteps - 1]:
						patternNZ.append(i)

				# Get the bucket index of the current value at the encoder
				actualValue = self.currentValue[maxPreviousSteps - 1]
				bucketIdx = self.encoder.getBucketIndices(actualValue)[0]

				# Perform classification
				clasResults = self.classifier.compute(recordNum=Global.currStep, patternNZ=patternNZ, classification={'bucketIdx': bucketIdx, 'actValue': actualValue}, learn=self.enableClassificationLearning, infer=self.enableClassificationInference)

				self.predictedValues[maxPreviousSteps - 1] = dict()
				for step in self.steps:

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
							if maxVal[0] is not None and maxVal[1] < self.minProbabilityThreshold:
								del predictions[maxVal[0]]
							maxVal = (actValue, prob)
						elif prob < self.minProbabilityThreshold:
							del predictions[actValue]

					# Sort the list of values from more probable to less probable values
					# an decrease the list length to max predictions per step limit
					predictions = sorted(predictions.iteritems(), key=operator.itemgetter(1), reverse=True)
					predictions = predictions[:maxFutureSteps]

					self.predictedValues[maxPreviousSteps - 1][step] = predictions

	def calculateStatistics(self):
		"""
		Calculate statistics after an iteration.
		"""

		if Global.currStep > 0:
			precision = 0.

			if self.inputFormat == InputFormat.htm:
				# Calculate the prediction precision comparing with bits are equal between the predicted array and the active array
				# The prediction precision is the percentage of shared bits over the sum of all bits
				numSharedBitStates = 0
				numNonSharedBitStates = 0
				for bit in self.bits:
					if bit.isPredicted[maxPreviousSteps - 2] or bit.isActive[maxPreviousSteps - 1]:
						if bit.isPredicted[maxPreviousSteps - 2] == bit.isActive[maxPreviousSteps - 1]:
							numSharedBitStates += 1
						else:
							numNonSharedBitStates += 1
				precision = (numSharedBitStates / float(numNonSharedBitStates + numSharedBitStates)) * 100

			elif self.inputFormat == InputFormat.raw:
				# Calculate the prediction precision comparing if the current value is in the range of any prediction.
				predictions = self.predictedValues[maxPreviousSteps - 2][1]
				for predictedValue in predictions:
					min = 0.
					max = 0.
					value = predictedValue[0]
					if self.predictionsMethod == PredictionsMethod.reconstruction:
						min = math.floor(value[0])
						max = math.ceil(value[1])
					elif self.predictionsMethod == PredictionsMethod.classification:
						min = math.floor(value)
						max = math.ceil(value)
					if min <= self.currentValue[maxPreviousSteps - 1] <= max:
						precision = 100.
						break

			# The precision rate is the average of the precision calculated in every step
			self.statsPrecisionRate = (self.statsPrecisionRate + precision) / 2
		else:
			self.statsPrecisionRate = 0.

		for bit in self.bits:
			bit.calculateStatistics()

	def __getNextFileRecord(self):
		"""
		Get the next record from file.
		If file end is reached then start reading from scratch again.
		"""

		recordValue = None

		# If end of file was reached then place cursor on the first byte again
		if self._file.tell() == os.fstat(self._file.fileno()).st_size:
			self._file.seek(0)

		if self.inputFormat == InputFormat.htm:

			# Start reading from last position
			outputList = []
			character = 0
			for y in range(self.height):
				for x in range(self.width):
					character = self._file.read(1)
					if character == '1':
						outputList.append(1.)
					elif character == '0':
						outputList.append(0.)
					else:
						raise Exception("Invalid file format.")

				# Check if next char is a 'return', i.e. the row end
				character = self._file.read(1)
				if character == '\r':
					character = self._file.read(1)
				if character != '\n':
					raise Exception("Invalid file format.")

			# Check if next char is a 'return' character, i.e. the record end
			character = self._file.read(1)
			if character == '\r':
				character = self._file.read(1)
			if character != '\n' and character != -1:
				raise Exception("Invalid file format.")

			# Return the output list as record value
			recordValue = numpy.array(outputList)

		elif self.inputFormat == InputFormat.raw:

			# Return the raw value as record value
			recordValue = self._file.readline()
			recordValue = recordValue.rstrip('\r\n').rstrip('\n')

		return recordValue

	#endregion