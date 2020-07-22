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

    def __init__(self):
        """
        Initializes a new instance of this class.
        """

        # Target field of the database table or file.
        self.dataSourceFieldName = ''

        # Data type of the field returned by database table or file.
        self.dataSourceFieldDataType = FieldDataType.string

        # Optional encoder to convert raw data to htm input and vice-versa.
        self.encoder = None

        # Module name which encoder class is imported.
        self.encoderModule = ""

        # Class name which encode or decode values.
        self.encoderClass = ""

        # Parameters passed to the encoder class constructor.
        self.encoderParams = ""

        # Field name returned by encoder when decode() function.
        self.encoderFieldName = ""

        # Data type of the field returned by encoder.
        self.encoderFieldDataType = FieldDataType.string

        # Enable inference for this field.
        self.enableInference = False

        # Value read currently from database.
        self.currentValue = MachineState(None, maxPreviousSteps)

        # Best value predicted by network. This is need to build predictions chart.
        self.bestPredictedValue = MachineState(None, maxPreviousSteps)

        # Values predicted by network.
        self.predictedValues = MachineState(None, maxPreviousSteps)

    def initialize(self):
        """
        Initialize this node.
        """

        # Create Classifier instance with appropriate parameters
        self.minProbabilityThreshold = 0.0001
        self.steps = [step+1 for step in range(maxFutureSteps)]
        self.classifier = CLAClassifier(steps=self.steps)

        # Increase history according to inference flag
        if self.enableInference:
            maxLen = maxPreviousStepsWithInference
            self.bestPredictedValue = MachineState(0, maxLen)
        else:
            maxLen = maxPreviousSteps
        self.currentValue = MachineState(0, maxLen)
