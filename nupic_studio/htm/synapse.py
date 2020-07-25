from nupic_studio import MachineState
from nupic_studio.htm import MAX_PREVIOUS_STEPS
from nupic_studio.ui import Global


class Synapse:
    """
    A class only to group properties related to synapses.
    """

    def __init__(self):
        """
        Initializes a new instance of this class.
        """

        # Index of this cell in the spatial pooler.
        self.index_sp = -1

        # Index of this synapse in the temporal pooler.
        self.index_tp = -1

        # An input element is a cell in case of the source be a column or then a bit in case of the source be a sensor.
        self.input_elem = None

        # Permanence of this synapse.
        self.permanence = MachineState(0.0, MAX_PREVIOUS_STEPS)

        # States of this element
        self.is_connected = MachineState(False, MAX_PREVIOUS_STEPS)
        self.is_predicted = MachineState(False, MAX_PREVIOUS_STEPS)
        self.is_falsely_predicted = MachineState(False, MAX_PREVIOUS_STEPS)
        self.is_removed = MachineState(False, MAX_PREVIOUS_STEPS)

        # Statistics
        self.stats_connection_count = 0
        self.stats_connection_rate = 0.0
        self.stats_predition_count = 0
        self.stats_precision_rate = 0.0

        # 3D object reference
        self.tree3d_initialized = False
        self.tree3d_item_np = None
        self.tree3d_selected = False

    def nextStep(self):
        """
        Perfoms actions related to time step progression.
        """

        # Update states machine by remove the first element and add a new element in the end
        self.permanence.rotate()
        self.is_connected.rotate()
        self.is_predicted.rotate()
        self.is_falsely_predicted.rotate()
        self.is_removed.rotate()

    def calculateStatistics(self):
        """
        Calculate statistics after an iteration.
        """

        # Calculate statistics
        if self.is_connected.atCurrStep():
            self.stats_connection_count += 1
        if self.is_predicted.atCurrStep():
            self.stats_predition_count += 1
        if Global.curr_step > 0:
            self.stats_connection_rate = self.stats_connection_count / float(Global.curr_step)
        if self.stats_connection_count > 0:
            self.stats_precision_rate = self.stats_predition_count / float(self.stats_connection_count)
