import numpy
import time
from PyQt4 import QtGui, QtCore
from nustudio.htm import maxStoredSteps
from nustudio.htm.node import Node, NodeType
from nustudio.htm.column import Column
from nustudio.htm.cell import Cell
from nustudio.htm.segment import Segment, SegmentType
from nustudio.htm.synapse import Synapse
from nustudio.ui import Global
from nupic.research.spatial_pooler import SpatialPooler
from nupic.research.temporal_memory import TemporalMemory as TemporalPooler

class InputMapType:
	"""
	Types of input map.
	An input map is a set of input elements (cells or sensor bits) that can be are grouped or combined.
	For example, if we have 2 children (#1 and #2) with dimensions 6 and 12 respectively,
	a grouped input map would be something like:
	   111111222222222222
	while a combined one would be something like: 
	   122122122122122122
	"""

	grouped = 1
	combined = 2

class Region(Node):
	"""
	A class only to group properties related to regions.
	"""

	#region Constructor

	def __init__(self, parentNode, name):
		"""
		Initializes a new instance of this class.
		"""

		Node.__init__(self, parentNode, name, NodeType.region)

		#region Instance fields

		self.columns = []
		"""List of columns that compose this region"""

		self.inputMapType = InputMapType.combined
		"""Specify how the inputs are organized in the input map"""

		self._inputMap = []
		"""An array representing the input map for this region."""

		#region Spatial Parameters

		self.enableSpatialPooling = True
		"""Switch for spatial pooling"""

		self.potentialRadius = 0
		"""This parameter determines the extent of the input that each column can potentially be connected to. This can be thought of as the input bits that are visible to each column, or a 'receptiveField' of the field of vision. A large enough value will result in 'global coverage', meaning that each column can potentially be connected to every input bit. This parameter defines a square (or hyper square) area: a column will have a max square potential pool with sides of length 2 * potentialRadius + 1."""

		self.potentialPct = 0.5
		"""The percent of the inputs, within a column's potential radius, that a column can be connected to. If set to 1, the column will be connected to every input within its potential radius. This parameter is used to give each column a unique potential pool when a large potentialRadius causes overlap between the columns. At initialization time we choose ((2*potentialRadius + 1)^(# inputDimensions) * potentialPct) input bits to comprise the column's potential pool."""

		self.globalInhibition = False
		"""If true, then during inhibition phase the winning columns are selected as the most active columns from the region as a whole. Otherwise, the winning columns are selected with respect to their local neighborhoods. Using global inhibition boosts performance x60."""

		self.localAreaDensity = -1.0
		"""The desired density of active columns within a local inhibition area (the size of which is set by the internally calculated inhibitionRadius, which is in turn determined from the average size of the connected potential pools of all columns). The inhibition logic will insure that at most N columns remain ON within a local inhibition area, where N = localAreaDensity * (total number of columns in inhibition area)."""

		self.numActiveColumnsPerInhArea = int(0.02 * (self.width * self.height))
		"""An alternate way to control the density of the active columns. If numActiveColumnsPerInhArea is specified then localAreaDensity must be less than 0, and vice versa. When using numActiveColumnsPerInhArea, the inhibition logic will insure that at most 'numActiveColumnsPerInhArea' columns remain ON within a local inhibition area (the size of which is set by the internally calculated inhibitionRadius, which is in turn determined from the average size of the connected receptive fields of all columns). When using this method, as columns learn and grow their effective receptive fields, the inhibitionRadius will grow, and hence the net density of the active columns will *decrease*. This is in contrast to the localAreaDensity method, which keeps the density of active columns the same regardless of the size of their receptive fields."""

		self.stimulusThreshold = 0
		"""This is a number specifying the minimum number of synapses that must be on in order for a columns to turn ON. The purpose of this is to prevent noise input from activating columns. Specified as a percent of a fully grown synapse."""

		self.proximalSynConnectedPerm = 0.10
		"""The default connected threshold. Any synapse whose permanence value is above the connected threshold is a "connected synapse", meaning it can contribute to the cell's firing."""

		self.proximalSynPermIncrement = 0.1
		"""The amount by which an active synapse is incremented in each round. Specified as a percent of a fully grown synapse."""

		self.proximalSynPermDecrement = 0.01
		"""The amount by which an inactive synapse is decremented in each round. Specified as a percent of a fully grown synapse."""

		self.minPctOverlapDutyCycle = 0.001
		"""A number between 0 and 1.0, used to set a floor on how often a column should have at least stimulusThreshold active inputs. Periodically, each column looks at the overlap duty cycle of all other columns within its inhibition radius and sets its own internal minimal acceptable duty cycle to:
		  minPctDutyCycleBeforeInh * max(other columns' duty cycles).
		On each iteration, any column whose overlap duty cycle falls below this computed value will get all of its permanence values boosted up by synPermActiveInc. Raising all permanences in response to a sub-par duty cycle before inhibition allows a cell to search for new inputs when either its previously learned inputs are no longer ever active, or when the vast majority of them have been "hijacked" by other columns."""

		self.minPctActiveDutyCycle = 0.001
		"""A number between 0 and 1.0, used to set a floor on how often a column should be activate. Periodically, each column looks at the activity duty cycle of all other columns within its inhibition radius and sets its own internal minimal acceptable duty cycle to:
		  minPctDutyCycleAfterInh * max(other columns' duty cycles).
		On each iteration, any column whose duty cycle after inhibition falls below this computed value will get its internal boost factor increased."""

		self.dutyCyclePeriod = 1000
		"""The period used to calculate duty cycles. Higher values make it take longer to respond to changes in boost or synPerConnectedCell. Shorter values make it more unstable and likely to oscillate."""

		self.maxBoost = 10.0
		"""The maximum overlap boost factor. Each column's overlap gets multiplied by a boost factor before it gets considered for inhibition. The actual boost factor for a column is number between 1.0 and maxBoost. A boost factor of 1.0 is used if the duty cycle is >= minOverlapDutyCycle, maxBoost is used if the duty cycle is 0, and any duty cycle in between is linearly extrapolated from these 2 endpoints."""

		#endregion

		#region Temporal Parameters

		self.enableTemporalPooling = True
		"""Switch for temporal pooling"""

		self.numCellsPerColumn = 10
		"""Number of cells per column. More cells, more contextual information"""

		self.learningRadius = min(self.width, self.height)
		"""Radius around cell from which it can sample to form distal dendrite connections."""

		self.distalSynInitialPerm = 0.11
		"""The initial permanence of an distal synapse."""

		self.distalSynConnectedPerm = 0.50
		"""The default connected threshold. Any synapse whose permanence value is above the connected threshold is a "connected synapse", meaning it can contribute to the cell's firing."""

		self.distalSynPermIncrement = 0.10
		"""The amount by which an active synapse is incremented in each round. Specified as a percent of a fully grown synapse."""

		self.distalSynPermDecrement = 0.10
		"""The amount by which an inactive synapse is decremented in each round. Specified as a percent of a fully grown synapse."""

		self.minThreshold = 8
		"""If the number of synapses active on a segment is at least this threshold, it is selected as the best matching cell in a bursing column."""

		self.activationThreshold = 12
		"""If the number of active connected synapses on a segment is at least this threshold, the segment is said to be active."""

		self.maxNumNewSynapses = 15
		"""The maximum number of synapses added to a segment during learning."""

		#endregion

		self.spatialPooler = None
		"""Spatial Pooler instance"""

		self.temporalPooler = None
		"""Temporal Pooler instance"""

		#endregion

	#endregion

	#region Methods

	def getColumn(self, x, y):
		"""
		Return the column located at given position
		"""

		column = self.columns[(y * self.width) + x]

		return column

	def initialize(self):
		"""
		Initialize this node.
		"""

		if len(self.children) == 0:
			QtGui.QMessageBox.warning(None, "Warning", "Region '" + self.name + "' does not have any child!")
			return

		Node.initialize(self)
		for child in self.children:
			child.initialize()

		# Create the input map
		# An input map is a set of input elements (cells or sensor bits) that can be are grouped or combined
		# For example, if we have 2 children (#1 and #2) with dimensions 6 and 12 respectively,
		# a grouped input map would be something like:
		#   111111222222222222
		# while a combined one would be something like: 
		#   122122122122122122
		self._inputMap = []
		sumDimension = 0
		if self.inputMapType == InputMapType.grouped:
			elemIdx = 0
			for child in self.children:
				dimension = child.width * child.height
				sumDimension += dimension

				# Arrange input from child into input map of this region
				if child.type == NodeType.region:
					for column in child.columns:
						inputElem = column.cells[0]
						self._inputMap.append(inputElem)
				else:
					for bit in child.bits:
						inputElem = bit
						self._inputMap.append(inputElem)
				elemIdx += 1

		elif self.inputMapType == InputMapType.combined:
			# Get the overall dimension and the minimum dimension among all children
			minDimension = self.children[0].width * self.children[0].height
			for child in self.children:
				dimension = child.width * child.height
				sumDimension += dimension
				if dimension < minDimension:
					minDimension = dimension

			# Use the minimum dimension as a multiplication common factor to determine the frequency of each child element in a sequence
			frequencies = []
			nextIdx = []
			for child in self.children:
				dimension = child.width * child.height
				if dimension % minDimension == 0:
					frequency = dimension / minDimension
					frequencies.append(frequency)
					nextIdx.append(0)
				else:
					QtGui.QMessageBox.warning(None, "Warning", "Children dimensions should have a common multiple factor!")
					return

			# Distribute alternatively child elements into input map according to their frequencies
			childIdx = 0
			for elemIdx in range(sumDimension):
				if childIdx == len(self.children):
					childIdx = 0
				child = self.children[childIdx]

				# Start distribution taking in account the last inserted element
				i0 = nextIdx[childIdx]
				iN = i0 + frequencies[childIdx]
				nextIdx[childIdx] = iN
				for i in range(i0, iN):
					if child.type == NodeType.region:
						inputElem = child.columns[i].cells[0]
						self._inputMap.append(inputElem)
					else:
						inputElem = child.bits[i]
						self._inputMap.append(inputElem)

				# Alternate children
				childIdx += 1

		# Initialize elements
		self.columns = []
		colIdx = 0
		for x in range(self.width):
			for y in range(self.height):
				column = Column()
				column.x = x
				column.y = y
				for z in range(self.numCellsPerColumn):
					cell = Cell()
					cell.index = (colIdx * self.numCellsPerColumn) + z
					cell.z = z
					column.cells.append(cell)
				self.columns.append(column)
				colIdx += 1

		# Create Spatial Pooler instance with appropriate parameters
		self.spatialPooler = SpatialPooler(
			inputDimensions = (sumDimension, 1),
			columnDimensions = (self.width, self.height),
			potentialRadius = self.potentialRadius,
			potentialPct = self.potentialPct,
			globalInhibition = self.globalInhibition,
			localAreaDensity = self.localAreaDensity,
			numActiveColumnsPerInhArea = self.numActiveColumnsPerInhArea,
			stimulusThreshold = self.stimulusThreshold,
			synPermInactiveDec = self.proximalSynPermDecrement,
			synPermActiveInc = self.proximalSynPermIncrement,
			synPermConnected = self.proximalSynConnectedPerm,
			minPctOverlapDutyCycle = self.minPctOverlapDutyCycle,
			minPctActiveDutyCycle = self.minPctActiveDutyCycle,
			dutyCyclePeriod = self.dutyCyclePeriod,
			maxBoost = self.maxBoost,
			seed = -1,
			spVerbosity = False)

		# Create Temporal Pooler instance with appropriate parameters
		self.temporalPooler = TemporalPooler(
			columnDimensions = (self.width, self.height),
			cellsPerColumn = self.numCellsPerColumn,
			learningRadius = self.learningRadius,
			initialPermanence = self.distalSynInitialPerm,
			connectedPermanence = self.distalSynConnectedPerm,
			minThreshold = self.minThreshold,
			maxNewSynapseCount = self.maxNumNewSynapses,
			permanenceIncrement = self.distalSynPermIncrement,
			permanenceDecrement = self.distalSynPermDecrement,
			activationThreshold = self.activationThreshold,
			seed = 42)

		return True

	def nextStep(self):
		"""
		Perfoms actions related to time step progression.
		"""

		Node.nextStep(self)
		for child in self.children:
			child.nextStep()
		for column in self.columns:
			column.nextStep()

		# Get input from sensors or lower regions and put into a single input map.
		input = self.getInput()

		# Send input to Spatial Pooler and get processed output (i.e. the active columns)
		# First initialize the vector for representing the current record
		columnDimensions = (self.width, self.height)
		columnNumber = numpy.array(columnDimensions).prod()
		activeColumns = numpy.zeros(columnNumber)
		self.spatialPooler.compute(input, self.enableSpatialPooling, activeColumns)

		# Send active columns to Temporal Pooler and get processed output (i.e. the predicting cells)
		# First convert active columns from float array to integer set
		activeColumnsSet = set()
		for colIdx in range(len(activeColumns)):
			if activeColumns[colIdx] == 1:
				activeColumnsSet.add(colIdx)
		self.temporalPooler.compute(activeColumnsSet, self.enableTemporalPooling)

		# Update elements regarding spatial pooler
		self.updateSpatialElements(activeColumns)

		# Update elements regarding temporal pooler
		self.updateTemporalElements()

		#TODO: self._output = self.temporalPooler.getPredictedState()

	def calculateStatistics(self):
		"""
		Calculate statistics after an iteration.
		"""

		for child in self.children:
			child.calculateStatistics()
		for column in self.columns:
			column.calculateStatistics()

	def getInput(self):
		"""
		Get input from sensors or lower regions and put into a single input map.
		"""

		# Initialize the vector for representing the current input map
		inputList = []
		for inputElem in self._inputMap:
			if inputElem.isActive[maxStoredSteps - 1]:
				inputList.append(1)
			else:
				inputList.append(0)
		input = numpy.array(inputList)

		return input

	def updateSpatialElements(self, activeColumns):
		"""
		Update elements regarding spatial pooler
		"""

		# Update proximal segments and synapses according to active columns
		for colIdx in range(len(self.columns)):
			column = self.columns[colIdx]

			# Update proximal segment
			segment = column.segment
			if activeColumns[colIdx] == 1:
				segment.isActive[maxStoredSteps - 1] = True
			else:
				segment.isActive[maxStoredSteps - 1] = False

			# Check if proximal segment is predicted by check if the column has any predicted cell
			for cell in column.cells:
				if cell.index in self.temporalPooler.predictiveCells:
					segment.isPredicted[maxStoredSteps - 1] = True

			# Update proximal synapses
			if segment.isActive[maxStoredSteps - 1] or segment.isPredicted[maxStoredSteps - 1]:
				permanencesSynapses = []
				self.spatialPooler.getPermanence(colIdx, permanencesSynapses)
				connectedSynapses = []
				self.spatialPooler.getConnectedSynapses(colIdx, connectedSynapses)
				for synIdx in range(len(permanencesSynapses)):
					# Get the proximal synapse given its position in the input map
					# Create a new one if it doesn't exist
					synapse = segment.getSynapse(synIdx)

					# Update proximal synapse
					if permanencesSynapses[synIdx] > 0.:
						if synapse == None:
							# Create a new synapse to a input element
							# An input element is a column if child is a region
							# or then a bit if child is a sensor
							synapse = Synapse()
							synapse.inputElem = self._inputMap[synIdx]
							synapse.indexSP = synIdx
							segment.synapses.append(synapse)

						# Update state
						synapse.isRemoved[maxStoredSteps - 1] = False
						synapse.permanence[maxStoredSteps - 1] = permanencesSynapses[synIdx]
						if connectedSynapses[synIdx] == 1:
							synapse.isConnected[maxStoredSteps - 1] = True
						else:
							synapse.isConnected[maxStoredSteps - 1] = False
					else:
						if synapse != None:
							synapse.isRemoved[maxStoredSteps - 1] = True

	def updateTemporalElements(self):
		"""
		Update elements regarding temporal pooler
		"""

		# Update cells, distal segments and synapses according to active columns
		for colIdx in range(len(self.columns)):
			column = self.columns[colIdx]

			# Mark proximal segment and its connected synapses as predicted
			if column.segment.isPredicted[maxStoredSteps - 1]:
				for synapse in column.segment.synapses:
					if synapse.isConnected[maxStoredSteps - 1]:
						synapse.isPredicted[maxStoredSteps - 1] = True
						synapse.inputElem.isPredicted[maxStoredSteps - 1] = True

			for cell in column.cells:
				cellIdx = cell.index

				# Update cell's states
				if cellIdx in self.temporalPooler.winnerCells:
					cell.isLearning[maxStoredSteps - 1] = True
				if cellIdx in self.temporalPooler.activeCells:
					cell.isActive[maxStoredSteps - 1] = True
				if cellIdx in self.temporalPooler.predictiveCells:
					cell.isPredicted[maxStoredSteps - 1] = True

				# Get the indexes of the distal segments of this cell
				segmentsForCell = self.temporalPooler.connections.segmentsForCell(cellIdx)

				# Add the segments that appeared after last iteration
				for segIdx in segmentsForCell:
					# Check if segment already exists in the cell
					segFound = False
					for segment in cell.segments:
						if segment.indexTP == segIdx:
							segFound = True
							break

					# If segment is new, add it to cell
					if not segFound:
						segment = Segment(SegmentType.distal)
						segment.indexTP = segIdx
						cell.segments.append(segment)

				# Update distal segments
				for segment in cell.segments:
					segIdx = segment.indexTP

					# If segment not found in segments indexes returned in last iteration mark it as removed
					if segIdx in segmentsForCell:

						# Update segment's state
						if segIdx in self.temporalPooler.activeSegments:
							segment.isActive[maxStoredSteps - 1] = True
						else:
							segment.isActive[maxStoredSteps - 1] = False

						# Get the indexes of the synapses of this segment
						synapsesForSegment = self.temporalPooler.connections.synapsesForSegment(segIdx)

						# Add the synapses that appeared after last iteration
						for synIdx in synapsesForSegment:
							# Check if synapse already exists in the segment
							synFound = False
							for synapse in segment.synapses:
								if synapse.indexTP == synIdx:
									synFound = True
									break

							# If synapse is new, add it to segment
							if not synFound:
								synapse = Synapse()
								synapse.indexTP = synIdx
								segment.synapses.append(synapse)

						# Update synapses
						for synapse in segment.synapses:
							synIdx = synapse.indexTP

							# If synapse not found in synapses indexes returned in last iteration mark it as removed
							if synIdx in synapsesForSegment:

								# Update synapse's state
								(_, sourceCellIdx, permanence) = self.temporalPooler.connections.dataForSynapse(synIdx)
								synapse.permanence[maxStoredSteps - 1] = permanence
								if permanence >= self.distalSynConnectedPerm:
									synapse.isConnected[maxStoredSteps - 1] = True
								else:
									synapse.isConnected[maxStoredSteps - 1] = False

								# Get cell given cell's index
								for sourceColumn in self.columns:
									for sourceCell in sourceColumn.cells:
										if sourceCell.index == sourceCellIdx:
											synapse.inputElem = sourceCell
							else:
								synapse.isRemoved[maxStoredSteps - 1] = True
					else:
						segment.isRemoved[maxStoredSteps - 1] = True

	#endregion
