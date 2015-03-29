import numpy
import time
from PyQt4 import QtGui, QtCore
from nupic_studio.htm import maxPreviousSteps
from nupic_studio.htm.node import Node, NodeType
from nupic_studio.htm.column import Column
from nupic_studio.htm.cell import Cell
from nupic_studio.htm.segment import Segment, SegmentType
from nupic_studio.htm.synapse import Synapse
from nupic_studio.ui import Global
from nupic.research.spatial_pooler import SpatialPooler
from nupic.research.temporal_memory import TemporalMemory as TemporalPooler

class Region(Node):
  """
  A class only to group properties related to regions.
  """

  #region Constructor

  def __init__(self, name):
    """
    Initializes a new instance of this class.
    """

    Node.__init__(self, name, NodeType.region)

    #region Instance fields

    self.columns = []
    """List of columns that compose this region"""

    self._inputMap = []
    """An array representing the input map for this region."""

    #region Spatial Parameters

    self.enableSpatialLearning = True
    """Switch for spatial learning"""

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

    self.spSeed = -1
    """Seed for generate random values"""

    #endregion

    #region Temporal Parameters

    self.enableTemporalLearning = True
    """Switch for temporal learning"""

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

    self.tpSeed = 42
    """Seed for generate random values"""

    #endregion

    self.spatialPooler = None
    """Spatial Pooler instance"""

    self.temporalPooler = None
    """Temporal Pooler instance"""

    #endregion

    #region Statistics properties

    self.statsPrecisionRate = 0.

    #endregion

  #endregion

  #region Methods

  def getColumn(self, x, y):
    """
    Return the column located at given position
    """

    column = self.columns[(y * self.width) + x]

    return column

  def getInputSize(self):
    """
    Return the sum of sizes of all feeder nodes.
    """

    sumSizes = 0
    for feeder in Global.project.network.getFeederNodes(self):
      sumSizes += feeder.width * feeder.height

    return sumSizes

  def initialize(self):
    """
    Initialize this node.
    """

    # Check if this region has nodes that feed it
    numFeeders = len(Global.project.network.getFeederNodes(self))
    if numFeeders == 0:
      QtGui.QMessageBox.warning(None, "Warning", "Region '" + self.name + "' does not have any child!")
      return

    # Initialize this node and the nodes that feed it
    Node.initialize(self)

    # Create the input map
    # An input map is a set of input elements (cells or sensor bits) that should are grouped
    # For example, if we have 2 nodes that feed this region (#1 and #2) with dimensions 6 and 12 respectively,
    # a input map would be something like:
    #   111111222222222222
    self._inputMap = []
    elemIdx = 0
    for feeder in Global.project.network.getFeederNodes(self):

      # Arrange input from feeder into input map of this region
      if feeder.type == NodeType.region:
        for column in feeder.columns:
          inputElem = column.cells[0]
          self._inputMap.append(inputElem)
      else:
        for bit in feeder.bits:
          inputElem = bit
          self._inputMap.append(inputElem)
      elemIdx += 1

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
      inputDimensions = (self.getInputSize(), 1),
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
      seed = self.spSeed,
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
      seed = self.tpSeed)

    return True

  def nextStep(self):
    """
    Perfoms actions related to time step progression.
    """

    Node.nextStep(self)
    for column in self.columns:
      column.nextStep()

    # Get input from sensors or lower regions and put into a single input map.
    input = self.getInput()

    # Send input to Spatial Pooler and get processed output (i.e. the active columns)
    # First initialize the vector for representing the current record
    columnDimensions = (self.width, self.height)
    columnNumber = numpy.array(columnDimensions).prod()
    activeColumns = numpy.zeros(columnNumber)
    self.spatialPooler.compute(input, self.enableSpatialLearning, activeColumns)

    # Send active columns to Temporal Pooler and get processed output (i.e. the predicting cells)
    # First convert active columns from float array to integer set
    activeColumnsSet = set()
    for colIdx in range(len(activeColumns)):
      if activeColumns[colIdx] == 1:
        activeColumnsSet.add(colIdx)
    self.temporalPooler.compute(activeColumnsSet, self.enableTemporalLearning)

    # Update elements regarding spatial pooler
    self.updateSpatialElements(activeColumns)

    # Update elements regarding temporal pooler
    self.updateTemporalElements()

    # Get the predicted values
    self.getPredictions()

    #TODO: self._output = self.temporalPooler.getPredictedState()

  def getPredictions(self):
    """
    Get the predicted values after an iteration.
    """

    for feeder in Global.project.network.getFeederNodes(self):
      feeder.getPredictions()

  def calculateStatistics(self):
    """
    Calculate statistics after an iteration.
    """

    # The region's prediction precision is the average between the nodes that feed it
    precisionRate = 0.
    numFeeders = 0
    for feeder in Global.project.network.getFeederNodes(self):
      precisionRate += feeder.statsPrecisionRate
      numFeeders += 1
    self.statsPrecisionRate = precisionRate / numFeeders

    for column in self.columns:
      column.calculateStatistics()

  def getInput(self):
    """
    Get input from sensors or lower regions and put into a single input map.
    """

    # Initialize the vector for representing the current input map
    inputList = []
    for inputElem in self._inputMap:
      if inputElem.isActive.atCurrStep():
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
        segment.isActive.setForCurrStep(True)
      else:
        segment.isActive.setForCurrStep(False)

      # Check if proximal segment is predicted by check if the column has any predicted cell
      for cell in column.cells:
        if cell.index in self.temporalPooler.predictiveCells:
          segment.isPredicted.setForCurrStep(True)

      # Update proximal synapses
      if segment.isActive.atCurrStep() or segment.isPredicted.atCurrStep():
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
              # An input element is a column if feeder is a region
              # or then a bit if feeder is a sensor
              synapse = Synapse()
              synapse.inputElem = self._inputMap[synIdx]
              synapse.indexSP = synIdx
              segment.synapses.append(synapse)

            # Update state
            synapse.isRemoved.setForCurrStep(False)
            synapse.permanence.setForCurrStep(permanencesSynapses[synIdx])
            if connectedSynapses[synIdx] == 1:
              synapse.isConnected.setForCurrStep(True)
            else:
              synapse.isConnected.setForCurrStep(False)
          else:
            if synapse != None:
              synapse.isRemoved.setForCurrStep(True)

  def updateTemporalElements(self):
    """
    Update elements regarding temporal pooler
    """

    # Update cells, distal segments and synapses according to active columns
    for colIdx in range(len(self.columns)):
      column = self.columns[colIdx]

      # Mark proximal segment and its connected synapses as predicted
      if column.segment.isPredicted.atCurrStep():
        for synapse in column.segment.synapses:
          if synapse.isConnected.atCurrStep():
            synapse.isPredicted.setForCurrStep(True)
            synapse.inputElem.isPredicted.setForCurrStep(True)

      # Mark proximal segment and its connected synapses that were predicted but are not active now
      if column.segment.isPredicted.atPreviousStep():
        if not column.segment.isActive.atCurrStep():
          column.segment.isFalselyPredicted.setForCurrStep(True)
        for synapse in column.segment.synapses:
          if (synapse.isPredicted.atPreviousStep() and not synapse.isConnected.atCurrStep()) or (synapse.isConnected.atCurrStep() and synapse.inputElem.isFalselyPredicted.atCurrStep()):
            synapse.isFalselyPredicted.setForCurrStep(True)

      for cell in column.cells:
        cellIdx = cell.index

        # Update cell's states
        if cellIdx in self.temporalPooler.winnerCells:
          cell.isLearning.setForCurrStep(True)
        if cellIdx in self.temporalPooler.activeCells:
          cell.isActive.setForCurrStep(True)
        if cellIdx in self.temporalPooler.predictiveCells:
          cell.isPredicted.setForCurrStep(True)
        if cell.isPredicted.atPreviousStep() and not cell.isActive.atCurrStep():
          cell.isFalselyPredicted.setForCurrStep(True)

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
              segment.isActive.setForCurrStep(True)
            else:
              segment.isActive.setForCurrStep(False)

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
                (_, sourceCellAbsIdx, permanence) = self.temporalPooler.connections.dataForSynapse(synIdx)
                synapse.permanence.setForCurrStep(permanence)
                if permanence >= self.distalSynConnectedPerm:
                  synapse.isConnected.setForCurrStep(True)
                else:
                  synapse.isConnected.setForCurrStep(False)

                # Get cell given cell's index
                sourceColIdx = sourceCellAbsIdx / self.numCellsPerColumn
                sourceCellRelIdx = sourceCellAbsIdx % self.numCellsPerColumn
                sourceCell = self.columns[sourceColIdx].cells[sourceCellRelIdx]
                synapse.inputElem = sourceCell
              else:
                synapse.isRemoved.setForCurrStep(True)
          else:
            segment.isRemoved.setForCurrStep(True)

  #endregion
