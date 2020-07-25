import os
import collections
import numpy
import operator
import math
import dateutil.parser
from PyQt5 import QtGui, QtCore, QtWidgets
from nupic_studio import getInstantiatedClass
from nupic_studio.ui import Global
from nupic_studio.htm import MAX_PREVIOUS_STEPS, MAX_FUTURE_STEPS, MAX_PREVIOUS_STEPS_WITH_INFERENCE
from nupic_studio.htm.node import Node, NodeType
from nupic_studio.htm.bit import Bit
from nupic_studio.htm.encoding import FieldDataType
from nupic.encoders import MultiEncoder
from nupic.data.file_record_stream import FileRecordStream


class DataSourceType:
    """
    Types of data sources which a sensor gets inputs.
    """
    FILE = 1
    DATABASE = 2


class PredictionsMethod:
    """
    Methods used to get predicted values and their probabilities
    """
    RECONSTRUCTION = "Reconstruction"
    CLASSIFICATION = "Classification"


class Sensor(Node):
    """
    A super class only to group properties related to sensors.
    """

    def __init__(self, name):
        """
        Initializes a new instance of this class.
        """

        Node.__init__(self, name, NodeType.SENSOR)

        # An array of the bit objects that compose the current output of this node.
        self.bits = []

        # Data source which provides records to fed into a region.
        self.data_source = None

        # Type of the data source (File or Database).
        self.data_source_type = DataSourceType.FILE

        # The input file name to be handled. Returns the input file name only if it is in the project directory, full path otherwise.
        self.file_name = ''

        # Connection string of the database.
        self.database_connection_string = ""

        # Target table of the database.
        self.database_table = ''

        # Multi-encoder which concatenate sub-encodings to convert raw data to htm input and vice-versa.
        self.encoder = None

        # List of sub-encodings that handles the input from database.
        self.encodings = []

        # Method used to get predicted values and their probabilities.
        self.predictions_method = PredictionsMethod.RECONSTRUCTION

        # Switch for classification learning.
        self.enable_classification_learning = True

        # Switch for classification inference.
        self.enable_classification_inference = True

        # Statistics
        self.stats_precision_rate = 0.0

    def getBit(self, x, y):
        """
        Return the bit located at given position
        """
        bit = self.bits[(y * self.width) + x]
        return bit

    def initialize(self):
        """
        Initialize this node.
        """
        Node.initialize(self)

        # Initialize input bits
        self.bits = []
        for x in range(self.width):
            for y in range(self.height):
                bit = Bit()
                bit.x = x
                bit.y = y
                self.bits.append(bit)

        if self.data_source_type == DataSourceType.FILE:
            """
            Initialize this node opening the file and place cursor on the first record.
            """

            # If file name provided is a relative path, use project file path
            if self.file_name != '' and os.path.dirname(self.file_name) == '':
                full_file_name = os.path.dirname(Global.project.file_name) + '/' + self.file_name
            else:
                full_file_name = self.file_name

            # Check if file really exists
            if not os.path.isfile(full_file_name):
                QtWidgets.QMessageBox.warning(None, "Warning", "Input stream file '" + full_file_name + "' was not found or specified.", QtWidgets.QMessageBox.Ok)
                return

            # Create a data source for read the file
            self.data_source = FileRecordStream(full_file_name)

        elif self.data_source_type == DataSourceType.DATABASE:
            pass

        self.encoder = MultiEncoder()
        for encoding in self.encodings:
            encoding.initialize()

            # Create an instance class for an encoder given its module, class and constructor params
            encoding.encoder = getInstantiatedClass(encoding.encoder_module, encoding.encoder_class, encoding.encoder_params)

            # Take the first part of encoder field name as encoder name
            # Ex: timestamp_weekend.weekend => timestamp_weekend
            encoding.encoder.name = encoding.encoder_field_name.split('.')[0]

            # Add sub-encoder to multi-encoder list
            self.encoder.addEncoder(encoding.data_source_field_name, encoding.encoder)

        # If encoder size is not the same to sensor size then throws exception
        encoder_size = self.encoder.getWidth()
        sensor_size = self.width * self.height
        if encoder_size > sensor_size:
            QtWidgets.QMessageBox.warning(None, "Warning", "'" + self.name + "': Encoder size (" + str(encoder_size) + ") is different from sensor size (" + str(self.width) + " x " + str(self.height) + " = " + str(sensor_size) + ").", QtWidgets.QMessageBox.Ok)
            return

        return True

    def nextStep(self):
        """
        Performs actions related to time step progression.
        """

        # Update states machine by remove the first element and add a new element in the end
        for encoding in self.encodings:
            encoding.current_value.rotate()
            if encoding.enable_inference:
                encoding.predicted_values.rotate()
                encoding.best_predicted_value.rotate()

        Node.nextStep(self)
        for bit in self.bits:
            bit.nextStep()

        # Get record value from data source
        # If the last record was reached just rewind it
        data = self.data_source.getNextRecordDict()
        if not data:
            self.data_source.rewind()
            data = self.data_source.getNextRecordDict()

        # Pass raw values to encoder and get a concatenated array
        output_array = numpy.zeros(self.encoder.getWidth())
        self.encoder.encodeIntoArray(data, output_array)

        # Get values obtained from the data source.
        output_values = self.encoder.getScalars(data)

        # Get raw values and respective encoded bit array for each field
        for i in range(len(self.encodings)):
            encoding = self.encodings[i]

            # Convert the value to its respective data type
            curr_value = output_values[i]
            if encoding.encoder_field_data_type == FieldDataType.BOOLEAN:
                curr_value = bool(curr_value)
            elif encoding.encoder_field_data_type == FieldDataType.INTEGER:
                curr_value = int(curr_value)
            elif encoding.encoder_field_data_type == FieldDataType.DECIMAL:
                curr_value = float(curr_value)
            elif encoding.encoder_field_data_type == FieldDataType.DATE_TIME:
                curr_value = dateutil.parser.parse(str(curr_value))
            elif encoding.encoder_field_data_type == FieldDataType.STRING:
                curr_value = str(curr_value)
            encoding.current_value.setForCurrStep(curr_value)

        # Update sensor bits
        for i in range(len(output_array)):
            if output_array[i] > 0.0:
                self.bits[i].is_active.setForCurrStep(True)
            else:
                self.bits[i].is_active.setForCurrStep(False)

        # Mark falsely predicted bits
        for bit in self.bits:
            if bit.is_predicted.atPreviousStep() and not bit.is_active.atCurrStep():
                bit.is_falsely_predicted.setForCurrStep(True)

        self.output = output_array

    def getPredictions(self):
        """
        Get the predictions after an iteration.
        """

        if self.predictions_method == PredictionsMethod.RECONSTRUCTION:

            # Prepare list with predictions to be classified
            # This list contains the indexes of all bits that are predicted
            output = []
            for i in range(len(self.bits)):
                if self.bits[i].is_predicted.atCurrStep():
                    output.append(1)
                else:
                    output.append(0)
            output = numpy.array(output)

            # Decode output and create predictions list
            fields_dict, fields_order = self.encoder.decode(output)
            for encoding in self.encodings:
                if encoding.enable_inference:
                    predictions = []
                    encoding.predicted_values.setForCurrStep(dict())

                    # If encoder field name was returned by decode(), assign the the predictions to it
                    if encoding.encoder_field_name in fields_order:
                        predicted_labels = fields_dict[encoding.encoder_field_name][1].split(', ')
                        predicted_values = fields_dict[encoding.encoder_field_name][0]
                        for i in range(len(predicted_labels)):
                            predictions.append([predicted_values[i], predicted_labels[i]])

                    encoding.predicted_values.atCurrStep()[1] = predictions

                    # Get the predicted value with the biggest probability to happen
                    if len(predictions) > 0:
                        best_prediction_range = predictions[0][0]
                        min = best_prediction_range[0]
                        max = best_prediction_range[1]
                        best_predicted_value = (min + max) / 2.0
                        encoding.best_predicted_value.setForCurrStep(best_predicted_value)

        elif self.predictions_method == PredictionsMethod.CLASSIFICATION:
            # A classification involves estimate which are the likely values to occurs in the next time step.

            offset = 0
            for encoding in self.encodings:
                encoder_width = encoding.encoder.getWidth()

                if encoding.enable_inference:
                    # Prepare list with predictions to be classified
                    # This list contains the indexes of all bits that are predicted
                    pattern_n_z = [i
                                   for i in range(offset, encoder_width)
                                   if self.bits[i].is_active.atCurrStep()]

                    # Get the bucket index of the current value at the encoder
                    actual_value = encoding.current_value.atCurrStep()
                    bucket_idx = encoding.encoder.getBucketIndices(actual_value)[0]

                    # Perform classification
                    clas_results = encoding.classifier.compute(recordNum=Global.curr_step, patternNZ=pattern_n_z, classification={'bucketIdx': bucket_idx, 'actValue': actual_value}, learn=self.enable_classification_learning, infer=self.enable_classification_inference)

                    encoding.predicted_values.setForCurrStep(dict())
                    for step in encoding.steps:

                        # Calculate probability for each predicted value
                        predictions = dict()
                        for (act_value, prob) in zip(clas_results['actualValues'], clas_results[step]):
                            if act_value in predictions:
                                predictions[act_value] += prob
                            else:
                                predictions[act_value] = prob

                        # Remove predictions with low probabilities
                        max_val = (None, None)
                        for (act_value, prob) in predictions.items():
                            if len(predictions) <= 1:
                                break
                            if max_val[0] is None or prob >= max_val[1]:
                                if max_val[0] is not None and max_val[1] < encoding.min_probability_threshold:
                                    del predictions[max_val[0]]
                                max_val = (act_value, prob)
                            elif prob < encoding.min_probability_threshold:
                                del predictions[act_value]

                        # Sort the list of values from more probable to less probable values
                        # an decrease the list length to max predictions per step limit
                        predictions = sorted(predictions.iteritems(), key=operator.itemgetter(1), reverse=True)
                        predictions = predictions[:MAX_FUTURE_STEPS]

                        encoding.predicted_values.atCurrStep()[step] = predictions

                    # Get the predicted value with the biggest probability to happen
                    best_predicted_value = encoding.predicted_values.atCurrStep()[1][0][0]
                    encoding.best_predicted_value.setForCurrStep(best_predicted_value)

                offset += encoder_width

    def calculateStatistics(self):
        """
        Calculate statistics after an iteration.
        """

        if Global.curr_step > 0:
            precision = 0.0

            # Calculate the prediction precision comparing if the current value is in the range of any prediction.
            for encoding in self.encodings:
                if encoding.enable_inference:
                    predictions = encoding.predicted_values.atPreviousStep()[1]
                    for predicted_value in predictions:
                        min = None
                        max = None
                        value = predicted_value[0]
                        if self.predictions_method == PredictionsMethod.RECONSTRUCTION:
                            min = value[0]
                            max = value[1]
                        elif self.predictions_method == PredictionsMethod.CLASSIFICATION:
                            min = value
                            max = value
                        if isinstance(min, (int, long, float, complex)) and isinstance(max, (int, long, float, complex)):
                            min = math.floor(min)
                            max = math.ceil(max)
                        if min <= encoding.current_value.atCurrStep() <= max:
                            precision = 100.0
                            break

            # The precision rate is the average of the precision calculated in every step
            self.stats_precision_rate = (self.stats_precision_rate + precision) / 2
        else:
            self.stats_precision_rate = 0.0

        for bit in self.bits:
            bit.calculateStatistics()
