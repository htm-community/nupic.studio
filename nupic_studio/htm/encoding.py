from nupic_studio import MachineState
from nupic_studio.htm import maxPreviousSteps, maxFutureSteps, maxPreviousStepsWithInference
from nupic.algorithms.CLAClassifier import CLAClassifier

class FieldDataType:
  """
  Types of data which a raw input is composed.
  """

  boolean = "Boolean"
  integer = "Integer"
  decimal = "Decimal"
  dateTime = "DateTime"
  string = "String"

class Encoding:
  """
  A class only to group properties related to encodings.
  """

  #region Constructor

  def __init__(self):
    """
    Initializes a new instance of this class.
    """

    #region Instance fields

    self.dataSourceFieldName = ''
    """Target field of the database table or file."""

    self.dataSourceFieldDataType = FieldDataType.string
    """Data type of the field returned by database table or file."""

    self.encoder = None
    """Optional encoder to convert raw data to htm input and vice-versa."""

    self.encoderModule = ""
    """Module name which encoder class is imported."""

    self.encoderClass = ""
    """Class name which encode or decode values."""

    self.encoderParams = ""
    """Parameters passed to the encoder class constructor."""

    self.encoderFieldName = ""
    """Field name returned by encoder when decode() function."""

    self.encoderFieldDataType = FieldDataType.string
    """Data type of the field returned by encoder."""

    self.enableInference = False
    """Enable inference for this field."""

    self.currentValue = MachineState(None, maxPreviousSteps)
    """Value read currently from database."""

    self.bestPredictedValue = MachineState(None, maxPreviousSteps)
    """Best value predicted by network. This is need to build predictions chart."""

    self.predictedValues = MachineState(None, maxPreviousSteps)
    """Values predicted by network."""

    #endregion

  #endregion

  #region Methods

  def initialize(self):
    """
    Initialize this node.
    """

    # Create Classifier instance with appropriate parameters
    self.minProbabilityThreshold = 0.0001
    self.steps = []
    for step in range(maxFutureSteps):
      self.steps.append(step+1)
    self.classifier = CLAClassifier(steps=self.steps)

    # Increase history according to inference flag
    if self.enableInference:
      maxLen = maxPreviousStepsWithInference
      self.bestPredictedValue = MachineState(0, maxLen)
    else:
      maxLen = maxPreviousSteps
    self.currentValue = MachineState(0, maxLen)

  #endregion
