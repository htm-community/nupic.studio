from nupic_studio import MachineState
from nupic_studio.htm import maxPreviousSteps
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
        self.indexSP = -1

        # Index of this synapse in the temporal pooler.
        self.indexTP = -1

        # An input element is a cell in case of the source be a column or then a bit in case of the source be a sensor.
        self.inputElem = None

        # Permanence of this synapse.
        self.permanence = MachineState(0., maxPreviousSteps)

        # States of this element
        self.isConnected = MachineState(False, maxPreviousSteps)
        self.isPredicted = MachineState(False, maxPreviousSteps)
        self.isFalselyPredicted = MachineState(False, maxPreviousSteps)
        self.isRemoved = MachineState(False, maxPreviousSteps)

        self.statsConnectionCount = 0
        self.statsConnectionRate = 0.
        self.statsPreditionCount = 0
        self.statsPrecisionRate = 0.

        self.tree3d_initialized = False
        self.tree3d_item_np = None
        self.tree3d_selected = False

    def nextStep(self):
        """
        Perfoms actions related to time step progression.
        """

        # Update states machine by remove the first element and add a new element in the end
        self.permanence.rotate()
        self.isConnected.rotate()
        self.isPredicted.rotate()
        self.isFalselyPredicted.rotate()
        self.isRemoved.rotate()

    def calculateStatistics(self):
        """
        Calculate statistics after an iteration.
        """

        # Calculate statistics
        if self.isConnected.atCurrStep():
            self.statsConnectionCount += 1
        if self.isPredicted.atCurrStep():
            self.statsPreditionCount += 1
        if Global.currStep > 0:
            self.statsConnectionRate = self.statsConnectionCount / float(Global.currStep)
        if self.statsConnectionCount > 0:
            self.statsPrecisionRate = self.statsPreditionCount / float(self.statsConnectionCount)
