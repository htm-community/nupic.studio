import os
import datetime
import numpy
from PyQt4 import QtGui, QtCore
from nustudio import getInstantiatedClass
from nustudio.ui import Global
from nustudio.htm import maxStoredSteps
from nustudio.htm.node import Node, NodeType
from nustudio.htm.bit import Bit

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

		self.currentValue = None
		"""Raw value encoded to network."""

		self.predictedValue = None
		"""Raw value decoded from network."""

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
				if encoderSize != sensorSize:
					QtGui.QMessageBox.warning(None, "Warning", "'" + self.name + "': Encoder size (" + encoderSize + ") is different from sensor size (" + self.width + " x " + self.height + " = " + sensorSize + ").", QtGui.QMessageBox.Ok)
					return

		elif self.dataSourceType == DataSourceType.database:
			pass

	def nextStep(self):
		"""
		Performs actions related to time step progression.
		"""

		Node.nextStep(self)
		for bit in self.bits:
			bit.nextStep()

		if self.dataSourceType == DataSourceType.file:
			self.__getNextFileRecord()
		elif self.dataSourceType == DataSourceType.database:
			pass

	def calculateStatistics(self):
		"""
		Calculate statistics after an iteration.
		"""

		for bit in self.bits:
			bit.calculateStatistics()

	def __getNextFileRecord(self):
		"""
		Get the next record from file.
		If file end is reached then start reading from scratch again.
		"""

		if self.inputFormat == InputFormat.htm:

			# If end of file was reached then place cursor on the first record again
			if self._file.tell() == os.fstat(self._file.fileno()).st_size:
				self._file.seek(0)

			# Start reading from last position
			outputList = []
			character = 0
			for y in range(self.height):
				for x in range(self.width):
					bit = self.getBit(x, y)
					character = self._file.read(1)
					if character == '1':
						outputList.append(1.)
						bit.isActive[maxStoredSteps - 1] = True
					elif character == '0':
						outputList.append(0.)
						bit.isActive[maxStoredSteps - 1] = False
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

			# Initialize the vector for representing the current record
			self._output = numpy.array(outputList)

		elif self.inputFormat == InputFormat.raw:
			rawValue = self._file.readline()
			if self.inputRawDataType == InputRawDataType.boolean:
				rawValue = bool(rawValue)
			elif self.inputRawDataType == InputRawDataType.integer:
				rawValue = int(rawValue)
			elif self.inputRawDataType == InputRawDataType.decimal:
				rawValue = float(rawValue)
			elif self.inputRawDataType == InputRawDataType.dateTime:
				rawValue = datetime.datetime.strptime(rawValue, "%Y-%m-%d %H:%M:%S.%f")
			elif self.inputRawDataType == InputRawDataType.string:
				rawValue = str(rawValue)

			# Get array from encoder
			self._output = self.encoder.encode(rawValue)

	#endregion
