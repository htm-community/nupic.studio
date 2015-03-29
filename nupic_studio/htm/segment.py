from nupic_studio import MachineState
from nupic_studio.htm import maxPreviousSteps
from nupic_studio.ui import Global

class SegmentType:
  proximal = 0
  distal = 1

class Segment:
  """
  A class only to group properties related to segments.
  """

  #region Constructor

  def __init__(self, type):
    """
    Initializes a new instance of this class.
    """

    #region Instance fields

    self.type = type
    """Determine if this segment is proximal or distal."""

    self.indexTP = -1
    """Index of this segment in the temporal pooler."""

    self.synapses = []
    """List of distal synapses of this segment."""

    # States of this element
    self.isActive = MachineState(False, maxPreviousSteps)
    self.isPredicted = MachineState(False, maxPreviousSteps)
    self.isFalselyPredicted = MachineState(False, maxPreviousSteps)
    self.isRemoved = MachineState(False, maxPreviousSteps)

    #region Statistics properties

    self.statsActivationCount = 0
    self.statsActivationRate = 0.
    self.statsPreditionCount = 0
    self.statsPrecisionRate = 0.

    #endregion

    #region 3d-tree properties (simulation form)

    self.tree3d_initialized = False
    self.tree3d_x1 = 0
    self.tree3d_y1 = 0
    self.tree3d_z1 = 0
    self.tree3d_x2 = 0
    self.tree3d_y2 = 0
    self.tree3d_z2 = 0
    self.tree3d_item = None
    self.tree3d_selected = False

    #endregion

    #endregion

  #endregion

  #region Methods

  def getSynapse(self, indexSP):
    """
    Return the synapse connected to a given cell or sensor bit
    """

    synapse = None
    for synapse in self.synapses:
      if synapse.indexSP == indexSP:
        return synapse

  def nextStep(self):
    """
    Perfoms actions related to time step progression.
    """

    # Update states machine by remove the first element and add a new element in the end
    self.isActive.rotate()
    self.isPredicted.rotate()
    self.isFalselyPredicted.rotate()
    self.isRemoved.rotate()

    # Remove synapses that are marked to be removed
    for synapse in self.synapses:
      if synapse.isRemoved.atFirstStep():
        self.synapses.remove(synapse)
        del synapse

    for synapse in self.synapses:
      synapse.nextStep()

  def calculateStatistics(self):
    """
    Calculate statistics after an iteration.
    """

    # Calculate statistics
    if self.isActive.atCurrStep():
      self.statsActivationCount += 1
    if self.isPredicted.atCurrStep():
      self.statsPreditionCount += 1
    if Global.currStep > 0:
      self.statsActivationRate = self.statsActivationCount / float(Global.currStep)
    if self.statsActivationCount > 0:
      self.statsPrecisionRate = self.statsPreditionCount / float(self.statsActivationCount)

    for synapse in self.synapses:
      synapse.calculateStatistics()

  #endregion
