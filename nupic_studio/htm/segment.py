from nupic_studio import MachineState
from nupic_studio.htm import MAX_PREVIOUS_STEPS
from nupic_studio.ui import Global


class SegmentType:
    PROXIMAL = 0
    DISTAL = 1


class Segment:
    """
    A class only to group properties related to segments.
    """

    def __init__(self, type):
        """
        Initializes a new instance of this class.
        """

        # Determine if this segment is proximal or distal.
        self.type = type

        # Index of this segment in the temporal pooler.
        self.index_tp = -1

        # List of distal synapses of this segment.
        self.synapses = []

        # States of this element
        self.is_active = MachineState(False, MAX_PREVIOUS_STEPS)
        self.is_predicted = MachineState(False, MAX_PREVIOUS_STEPS)
        self.is_falsely_predicted = MachineState(False, MAX_PREVIOUS_STEPS)
        self.is_removed = MachineState(False, MAX_PREVIOUS_STEPS)

        # Statistics
        self.stats_activation_count = 0
        self.stats_activation_rate = 0.0
        self.stats_predition_count = 0
        self.stats_precision_rate = 0.0

        # 3D object reference
        self.tree3d_initialized = False
        self.tree3d_start_pos = (0, 0, 0)
        self.tree3d_end_pos = (0, 0, 0)
        self.tree3d_item_np = None
        self.tree3d_selected = False

    def getSynapse(self, index_sp):
        """
        Return the synapse connected to a given cell or sensor bit
        """
        for synapse in self.synapses:
            if synapse.index_sp == index_sp:
                return synapse
        return None

    def nextStep(self):
        """
        Perfoms actions related to time step progression.
        """

        # Update states machine by remove the first element and add a new element in the end
        self.is_active.rotate()
        self.is_predicted.rotate()
        self.is_falsely_predicted.rotate()
        self.is_removed.rotate()

        # Remove synapses that are marked to be removed
        for synapse in self.synapses:
            if synapse.is_removed.atFirstStep():
                self.synapses.remove(synapse)
                del synapse

        for synapse in self.synapses:
            synapse.nextStep()

    def calculateStatistics(self):
        """
        Calculate statistics after an iteration.
        """

        # Calculate statistics
        if self.is_active.atCurrStep():
            self.stats_activation_count += 1
        if self.is_predicted.atCurrStep():
            self.stats_predition_count += 1
        if Global.curr_step > 0:
            self.stats_activation_rate = self.stats_activation_count / float(Global.curr_step)
        if self.stats_activation_count > 0:
            self.stats_precision_rate = self.stats_predition_count / float(self.stats_activation_count)

        for synapse in self.synapses:
            synapse.calculateStatistics()
