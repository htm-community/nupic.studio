from nupic_studio import MachineState
from nupic_studio.htm import MAX_PREVIOUS_STEPS
from nupic_studio.ui import Global


class Bit:
    """
    A class only to group properties related to input bits of sensors.
    """

    def __init__(self):
        """
        Initializes a new instance of this class.
        """
        self.initialize()

    def initialize(self):
        """
        Initialize this bit.
        """

        # Position on X axis
        self.x = -1

        # Position on Y axis
        self.y = -1

        # States of this element
        self.is_active = MachineState(False, MAX_PREVIOUS_STEPS)
        self.is_predicted = MachineState(False, MAX_PREVIOUS_STEPS)
        self.is_falsely_predicted = MachineState(False, MAX_PREVIOUS_STEPS)

        # Statistics
        self.stats_activation_count = 0
        self.stats_activation_rate = 0.0
        self.stats_predition_count = 0
        self.stats_precision_rate = 0.0

        # 3D object reference
        self.tree3d_initialized = False
        self.tree3d_pos = (0, 0, 0)
        self.tree3d_item_np = None
        self.tree3d_selected = False

    def nextStep(self):
        """
        Perfoms actions related to time step progression.
        """

        # Update states machine by remove the first element and add a new element in the end
        self.is_active.rotate()
        self.is_predicted.rotate()
        self.is_falsely_predicted.rotate()

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
