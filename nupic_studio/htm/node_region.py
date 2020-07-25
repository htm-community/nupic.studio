import numpy
import time
from PyQt5 import QtGui, QtCore, QtWidgets
from nupic_studio.htm import MAX_PREVIOUS_STEPS
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

    def __init__(self, name):
        """
        Initializes a new instance of this class.
        """

        Node.__init__(self, name, NodeType.REGION)

        # List of columns that compose this region.
        self.columns = []

        # An array representing the input map for this region.
        self.input_map = []

        # Switch for spatial learning.
        self.enable_spatial_learning = True

        # This parameter determines the extent of the input that each column can potentially be connected to. This
        # can be thought of as the input bits that are visible to each column, or a 'receptiveField' of the field of
        # vision. A large enough value will result in 'global coverage', meaning that each column can potentially be
        # connected to every input bit. This parameter defines a square (or hyper square) area: a column will have a
        # max square potential pool with sides of length 2 * potential_radius + 1.
        self.potential_radius = 0

        # The percent of the inputs, within a column's potential radius, that a column can be connected to. If set
        # to 1, the column will be connected to every input within its potential radius. This parameter is used to
        # give each column a unique potential pool when a large potential_radius causes overlap between the columns.
        # At initialization time we choose ((2*potential_radius + 1)^(# inputDimensions) * potential_pct) input bits to
        # comprise the column's potential pool.
        self.potential_pct = 0.5

        # If true, then during inhibition phase the winning columns are selected as the most active columns from the
        # region as a whole. Otherwise, the winning columns are selected with respect to their local neighborhoods.
        # Using global inhibition boosts performance x60.
        self.global_inhibition = False

        # The desired density of active columns within a local inhibition area (the size of which is set by the
        # internally calculated inhibitionRadius, which is in turn determined from the average size of the connected
        # potential pools of all columns). The inhibition logic will insure that at most N columns remain ON within a
        # local inhibition area, where N = local_area_density * (total number of columns in inhibition area).
        self.local_area_density = -1.0

        # An alternate way to control the density of the active columns. If num_active_columns_per_inh_area is specified
        # then local_area_density must be less than 0, and vice versa. When using num_active_columns_per_inh_area, the
        # inhibition logic will insure that at most 'num_active_columns_per_inh_area' columns remain ON within a local
        # inhibition area (the size of which is set by the internally calculated inhibitionRadius, which is in turn
        # determined from the average size of the connected receptive fields of all columns). When using this method,
        # as columns learn and grow their effective receptive fields, the inhibitionRadius will grow, and hence the net
        # density of the active columns will *decrease*. This is in contrast to the local_area_density method, which
        # keeps the density of active columns the same regardless of the size of their receptive fields.
        self.num_active_columns_per_inh_area = int(0.02 * (self.width * self.height))

        # This is a number specifying the minimum number of synapses that must be on in order for a columns to turn ON.
        # The purpose of this is to prevent noise input from activating columns. Specified as a percent of a fully grown
        # synapse.
        self.stimulus_threshold = 0

        self.proximal_syn_connected_perm = 0.10
        # The default connected threshold. Any synapse whose permanence value is above the connected threshold is a
        # "connected synapse", meaning it can contribute to the cell's firing.

        self.proximal_syn_perm_increment = 0.1
        # The amount by which an active synapse is incremented in each round. Specified as a percent of a fully grown
        # synapse.

        self.proximal_syn_perm_decrement = 0.01
        # The amount by which an inactive synapse is decremented in each round. Specified as a percent of a fully grown
        # synapse.

        # A number between 0 and 1.0, used to set a floor on how often a column should have at least stimulus_threshold
        # active inputs. Periodically, each column looks at the overlap duty cycle of all other columns within its
        # inhibition radius and sets its own internal minimal acceptable duty cycle to:
        #     min_pct_duty_cycle_before_inh * max(other columns' duty cycles).
        # On each iteration, any column whose overlap duty cycle falls below this computed value will get all of its
        # permanence values boosted up by synPermActiveInc. Raising all permanences in response to a sub-par duty cycle
        # before inhibition allows a cell to search for new inputs when either its previously learned inputs are no
        # longer ever active, or when the vast majority of them have been "hijacked" by other columns.
        self.min_pct_overlap_duty_cycle = 0.001

        # A number between 0 and 1.0, used to set a floor on how often a column should be activate. Periodically, each
        # column looks at the activity duty cycle of all other columns within its inhibition radius and sets its own
        # internal minimal acceptable duty cycle to:
        #     min_pct_duty_cycle_after_inh * max(other columns' duty cycles).
        # On each iteration, any column whose duty cycle after inhibition falls below this computed value will get its
        # internal boost factor increased.
        self.min_pct_active_duty_cycle = 0.001

        # The period used to calculate duty cycles. Higher values make it take longer to respond to changes in boost or
        # synPerConnectedCell. Shorter values make it more unstable and likely to oscillate.
        self.duty_cycle_period = 1000

        # The maximum overlap boost factor. Each column's overlap gets multiplied by a boost factor before it gets
        # considered for inhibition. The actual boost factor for a column is number between 1.0 and max_boost. A boost
        # factor of 1.0 is used if the duty cycle is >= minOverlapDutyCycle, max_boost is used if the duty cycle is 0,
        # and any duty cycle in between is linearly extrapolated from these 2 endpoints.
        self.max_boost = 10.0

        # Seed for generate random values.
        self.sp_seed = -1

        # Switch for temporal learning.
        self.enable_temporal_learning = True

        # Number of cells per column. More cells, more contextual information.
        self.cells_per_column = 10

        # The initial permanence of an distal synapse.
        self.distal_syn_initial_perm = 0.11

        # The default connected threshold. Any synapse whose permanence value is above the connected threshold is a
        # "connected synapse", meaning it can contribute to the cell's firing.
        self.distal_syn_connected_perm = 0.50

        # The amount by which an active synapse is incremented in each round. Specified as a percent of a fully grown
        # synapse.
        self.distal_syn_perm_increment = 0.10

        # The amount by which an inactive synapse is decremented in each round. Specified as a percent of a fully grown
        # synapse.
        self.distal_syn_perm_decrement = 0.10

        # If the number of synapses active on a segment is at least this threshold, it is selected as the best matching
        # cell in a bursing column.
        self.min_threshold = 8

        # If the number of active connected synapses on a segment is at least this threshold, the segment is said to be active.
        self.activation_threshold = 12

        # The maximum number of synapses added to a segment during learning.
        self.max_new_synapses = 15

        # Seed for generate random values.
        self.tp_seed = 42

        # Spatial Pooler instance.
        self.spatial_pooler = None

        # Temporal Pooler instance.
        self.temporal_pooler = None

        # Statistics
        self.stats_precision_rate = 0.0

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
        sum_sizes = 0
        for feeder in Global.project.network.getFeederNodes(self):
            sum_sizes += feeder.width * feeder.height
        return sum_sizes

    def initialize(self):
        """
        Initialize this node.
        """

        # Check if this region has nodes that feed it
        feeders_count = len(Global.project.network.getFeederNodes(self))
        if feeders_count == 0:
            QtWidgets.QMessageBox.warning(None, "Warning", "Region '" + self.name + "' does not have any child!")
            return

        # Initialize this node and the nodes that feed it
        Node.initialize(self)

        # Create the input map
        # An input map is a set of input elements (cells or sensor bits) that should are grouped
        # For example, if we have 2 nodes that feed this region (#1 and #2) with dimensions 6 and 12 respectively,
        # a input map would be something like:
        #   111111222222222222
        self.input_map = []
        for feeder in Global.project.network.getFeederNodes(self):
            # Arrange input from feeder into input map of this region
            if feeder.type == NodeType.REGION:
                for column in feeder.columns:
                    input_elem = column.cells[0]
                    self.input_map.append(input_elem)
            else:
                for bit in feeder.bits:
                    input_elem = bit
                    self.input_map.append(input_elem)

        # Initialize elements
        self.columns = []
        idx = 0
        for x in range(self.width):
            for y in range(self.height):
                column = Column()
                column.x = x
                column.y = y
                for z in range(self.cells_per_column):
                    cell = Cell()
                    cell.index = (idx * self.cells_per_column) + z
                    cell.z = z
                    column.cells.append(cell)
                self.columns.append(column)
                idx += 1

        # Create Spatial Pooler instance with appropriate parameters
        self.spatial_pooler = SpatialPooler(
            inputDimensions=(self.getInputSize(), 1),
            columnDimensions=(self.width, self.height),
            potentialRadius=self.potential_radius,
            potentialPct=self.potential_pct,
            globalInhibition=self.global_inhibition,
            localAreaDensity=self.local_area_density,
            numActiveColumnsPerInhArea=self.num_active_columns_per_inh_area,
            stimulusThreshold=self.stimulus_threshold,
            synPermInactiveDec=self.proximal_syn_perm_decrement,
            synPermActiveInc=self.proximal_syn_perm_increment,
            synPermConnected=self.proximal_syn_connected_perm,
            minPctOverlapDutyCycle=self.min_pct_overlap_duty_cycle,
            minPctActiveDutyCycle=self.min_pct_active_duty_cycle,
            dutyCyclePeriod=self.duty_cycle_period,
            maxBoost=self.max_boost,
            seed=self.sp_seed,
            spVerbosity=False)

        # Create Temporal Pooler instance with appropriate parameters
        self.temporal_pooler = TemporalPooler(
            columnDimensions=(self.width, self.height),
            cellsPerColumn=self.cells_per_column,
            initialPermanence=self.distal_syn_initial_perm,
            connectedPermanence=self.distal_syn_connected_perm,
            minThreshold=self.min_threshold,
            maxNewSynapseCount=self.max_new_synapses,
            permanenceIncrement=self.distal_syn_perm_increment,
            permanenceDecrement=self.distal_syn_perm_decrement,
            activation_threshold=self.activation_threshold,
            seed=self.tp_seed)

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
        column_dimensions = (self.width, self.height)
        column_number = numpy.array(column_dimensions).prod()
        active_columns = numpy.zeros(column_number)
        self.spatial_pooler.compute(input, self.enable_spatial_learning, active_columns)

        # Send active columns to Temporal Pooler and get processed output (i.e. the predicting cells)
        # First convert active columns from float array to integer set
        active_columns_set = set()
        for idx in range(len(active_columns)):
            if active_columns[idx] == 1:
                active_columns_set.add(idx)
        self.temporal_pooler.compute(active_columns_set, self.enable_temporal_learning)

        # Update elements regarding spatial pooler
        self.updateSpatialElements(active_columns)

        # Update elements regarding temporal pooler
        self.updateTemporalElements()

        # Get the predicted values
        self.getPredictions()

        #TODO: self.output = self.temporal_pooler.getPredictedState()

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
        precision_rate = 0.0
        feeders_count = 0
        for feeder in Global.project.network.getFeederNodes(self):
            precision_rate += feeder.stats_precision_rate
            feeders_count += 1
        self.stats_precision_rate = precision_rate / feeders_count

        for column in self.columns:
            column.calculateStatistics()

    def getInput(self):
        """
        Get input from sensors or lower regions and put into a single input map.
        """

        # Initialize the vector for representing the current input map
        input_list = []
        for input_elem in self.input_map:
            if input_elem.is_active.atCurrStep():
                input_list.append(1)
            else:
                input_list.append(0)
        input = numpy.array(input_list)

        return input

    def updateSpatialElements(self, active_columns):
        """
        Update elements regarding spatial pooler
        """

        # Update proximal segments and synapses according to active columns
        for col_idx in range(len(self.columns)):
            column = self.columns[col_idx]

            # Update proximal segment
            segment = column.segment
            if active_columns[col_idx] == 1:
                segment.is_active.setForCurrStep(True)
            else:
                segment.is_active.setForCurrStep(False)

            # Check if proximal segment is predicted by check if the column has any predicted cell
            for cell in column.cells:
                if cell.index in self.temporal_pooler.predictiveCells:
                    segment.is_predicted.setForCurrStep(True)

            # Update proximal synapses
            if segment.is_active.atCurrStep() or segment.is_predicted.atCurrStep():
                permanences_synapses = []
                self.spatial_pooler.getPermanence(col_idx, permanences_synapses)
                connected_synapses = []
                self.spatial_pooler.getConnectedSynapses(col_idx, connected_synapses)
                for syn_idx in range(len(permanences_synapses)):
                    # Get the proximal synapse given its position in the input map
                    # Create a new one if it doesn't exist
                    synapse = segment.getSynapse(syn_idx)

                    # Update proximal synapse
                    if permanences_synapses[syn_idx] > 0.0:
                        if synapse == None:
                            # Create a new synapse to a input element
                            # An input element is a column if feeder is a region
                            # or then a bit if feeder is a sensor
                            synapse = Synapse()
                            synapse.input_elem = self.input_map[syn_idx]
                            synapse.index_sp = syn_idx
                            segment.synapses.append(synapse)

                        # Update state
                        synapse.is_removed.setForCurrStep(False)
                        synapse.permanence.setForCurrStep(permanences_synapses[syn_idx])
                        if connected_synapses[syn_idx] == 1:
                            synapse.is_connected.setForCurrStep(True)
                        else:
                            synapse.is_connected.setForCurrStep(False)
                    else:
                        if synapse != None:
                            synapse.is_removed.setForCurrStep(True)

    def updateTemporalElements(self):
        """
        Update elements regarding temporal pooler
        """

        # Update cells, distal segments and synapses according to active columns
        for col_idx in range(len(self.columns)):
            column = self.columns[col_idx]

            # Mark proximal segment and its connected synapses as predicted
            if column.segment.is_predicted.atCurrStep():
                for synapse in column.segment.synapses:
                    if synapse.is_connected.atCurrStep():
                        synapse.is_predicted.setForCurrStep(True)
                        synapse.input_elem.is_predicted.setForCurrStep(True)

            # Mark proximal segment and its connected synapses that were predicted but are not active now
            if column.segment.is_predicted.atPreviousStep():
                if not column.segment.is_active.atCurrStep():
                    column.segment.is_falsely_predicted.setForCurrStep(True)
                for synapse in column.segment.synapses:
                    if (synapse.is_predicted.atPreviousStep() and not synapse.is_connected.atCurrStep()) or (synapse.is_connected.atCurrStep() and synapse.input_elem.is_falsely_predicted.atCurrStep()):
                        synapse.is_falsely_predicted.setForCurrStep(True)

            for cell in column.cells:
                cell_idx = cell.index

                # Update cell's states
                if cell_idx in self.temporal_pooler.winnerCells:
                    cell.is_learning.setForCurrStep(True)
                if cell_idx in self.temporal_pooler.activeCells:
                    cell.is_active.setForCurrStep(True)
                if cell_idx in self.temporal_pooler.predictiveCells:
                    cell.is_predicted.setForCurrStep(True)
                if cell.is_predicted.atPreviousStep() and not cell.is_active.atCurrStep():
                    cell.is_falsely_predicted.setForCurrStep(True)

                # Get the indexes of the distal segments of this cell
                segments_for_cell = self.temporal_pooler.connections.segmentsForCell(cell_idx)

                # Add the segments that appeared after last iteration
                for seg_idx in segments_for_cell:
                    # Check if segment already exists in the cell
                    seg_found = False
                    for segment in cell.segments:
                        if segment.index_tp == seg_idx:
                            seg_found = True
                            break

                    # If segment is new, add it to cell
                    if not seg_found:
                        segment = Segment(SegmentType.DISTAL)
                        segment.index_tp = seg_idx
                        cell.segments.append(segment)

                # Update distal segments
                for segment in cell.segments:
                    seg_idx = segment.index_tp

                    # If segment not found in segments indexes returned in last iteration mark it as removed
                    if seg_idx in segments_for_cell:

                        # Update segment's state
                        if seg_idx in self.temporal_pooler.activeSegments:
                            segment.is_active.setForCurrStep(True)
                        else:
                            segment.is_active.setForCurrStep(False)

                        # Get the indexes of the synapses of this segment
                        synapses_for_segment = self.temporal_pooler.connections.synapsesForSegment(seg_idx)

                        # Add the synapses that appeared after last iteration
                        for syn_idx in synapses_for_segment:
                            # Check if synapse already exists in the segment
                            syn_found = False
                            for synapse in segment.synapses:
                                if synapse.index_tp == syn_idx:
                                    syn_found = True
                                    break

                            # If synapse is new, add it to segment
                            if not syn_found:
                                synapse = Synapse()
                                synapse.index_tp = syn_idx
                                segment.synapses.append(synapse)

                        # Update synapses
                        for synapse in segment.synapses:
                            syn_idx = synapse.index_tp

                            # If synapse not found in synapses indexes returned in last iteration mark it as removed
                            if syn_idx in synapses_for_segment:

                                # Update synapse's state
                                synapse_data = self.temporal_pooler.connections.dataForSynapse(syn_idx)
                                synapse.permanence.setForCurrStep(synapse_data.permanence)
                                if synapse_data.permanence >= self.distal_syn_connected_perm:
                                    synapse.is_connected.setForCurrStep(True)
                                else:
                                    synapse.is_connected.setForCurrStep(False)

                                # Get cell given cell's index
                                source_col_idx = synapse_data.presynapticCell / self.cells_per_column
                                source_cell_rel_idx = synapse_data.presynapticCell % self.cells_per_column
                                source_cell = self.columns[source_col_idx].cells[source_cell_rel_idx]
                                synapse.input_elem = source_cell
                            else:
                                synapse.is_removed.setForCurrStep(True)
                    else:
                        segment.is_removed.setForCurrStep(True)
