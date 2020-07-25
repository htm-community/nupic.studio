from nupic_studio import MachineState
from nupic_studio.htm import MAX_PREVIOUS_STEPS, MAX_FUTURE_STEPS, MAX_PREVIOUS_STEPS_WITH_INFERENCE
from nupic.algorithms.CLAClassifier import CLAClassifier


class FieldDataType:
    """
    Types of data which a raw input is composed.
    """
    BOOLEAN = "Boolean"
    INTEGER = "Integer"
    DECIMAL = "Decimal"
    DATE_TIME = "DateTime"
    STRING = "String"


class Encoding:
    """
    A class only to group properties related to encodings.
    """

    def __init__(self):
        """
        Initializes a new instance of this class.
        """

        # Target field of the database table or file.
        self.data_source_field_name = ''

        # Data type of the field returned by database table or file.
        self.data_source_field_data_type = FieldDataType.STRING

        # Optional encoder to convert raw data to htm input and vice-versa.
        self.encoder = None

        # Module name which encoder class is imported.
        self.encoder_module = ""

        # Class name which encode or decode values.
        self.encoder_class = ""

        # Parameters passed to the encoder class constructor.
        self.encoder_params = ""

        # Field name returned by encoder when decode() function.
        self.encoder_field_name = ""

        # Data type of the field returned by encoder.
        self.encoder_field_data_type = FieldDataType.STRING

        # Enable inference for this field.
        self.enable_inference = False

        # Value read currently from database.
        self.current_value = MachineState(None, MAX_PREVIOUS_STEPS)

        # Best value predicted by network. This is need to build predictions chart.
        self.best_predicted_value = MachineState(None, MAX_PREVIOUS_STEPS)

        # Values predicted by network.
        self.predicted_values = MachineState(None, MAX_PREVIOUS_STEPS)

    def initialize(self):
        """
        Initialize this node.
        """

        # Create Classifier instance with appropriate parameters
        self.min_probability_threshold = 0.0001
        self.steps = [step + 1 for step in range(MAX_FUTURE_STEPS)]
        self.classifier = CLAClassifier(steps=self.steps)

        # Increase history according to inference flag
        if self.enable_inference:
            max_len = MAX_PREVIOUS_STEPS_WITH_INFERENCE
            self.best_predicted_value = MachineState(0, max_len)
        else:
            max_len = MAX_PREVIOUS_STEPS
        self.current_value = MachineState(0, max_len)
