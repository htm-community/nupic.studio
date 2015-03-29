from nupic_studio import MachineState
from nupic_studio.htm import maxPreviousSteps
from nupic_studio.ui import Global

class Bit:
  """
  A class only to group properties related to input bits of sensors.
  """

  #region Constructor

  def __init__(self):
    """
    Initializes a new instance of this class.
    """

    self.initialize()

  #endregion

  #region Methods

  def initialize(self):
    """
    Initialize this bit.
    """

    self.x = -1
    """Position on X axis"""

    self.y = -1
    """Position on Y axis"""

    # States of this element
    self.isActive = MachineState(False, maxPreviousSteps)
    self.isPredicted = MachineState(False, maxPreviousSteps)
    self.isFalselyPredicted = MachineState(False, maxPreviousSteps)

    #region Statistics properties

    self.statsActivationCount = 0
    self.statsActivationRate = 0.
    self.statsPreditionCount = 0
    self.statsPrecisionRate = 0.

    #endregion

    #region 3d-tree properties (simulation form)

    self.tree3d_initialized = False
    self.tree3d_x = 0
    self.tree3d_y = 0
    self.tree3d_z = 0
    self.tree3d_item = None
    self.tree3d_selected = False

    #endregion

  def nextStep(self):
    """
    Perfoms actions related to time step progression.
    """

    # Update states machine by remove the first element and add a new element in the end
    self.isActive.rotate()
    self.isPredicted.rotate()
    self.isFalselyPredicted.rotate()

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

  #endregion
