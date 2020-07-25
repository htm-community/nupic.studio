import pyqtgraph as pg
from PyQt5 import QtGui, QtCore, QtWidgets
from nupic_studio import ArrayTableModel
from nupic_studio.ui import Global
from nupic_studio.htm import MAX_PREVIOUS_STEPS, MAX_FUTURE_STEPS, MAX_PREVIOUS_STEPS_WITH_INFERENCE
from nupic_studio.htm.node import NodeType, Node
from nupic_studio.htm.node_sensor import PredictionsMethod
from nupic_studio.htm.encoding import FieldDataType


class NodeInformationWindow(QtWidgets.QWidget):

    def __init__(self):
        """
        Initializes a new instance of this class.
        """
        QtWidgets.QWidget.__init__(self)

        self.previous_selected_node = None
        self.selected_sensor = None
        self.selected_encoding = None
        self.selected_region = None
        self.selected_column = None
        self.selected_proximal_synapse = None
        self.selected_cell = None
        self.selected_distal_segment = None
        self.selected_distal_synapse = None

        # Predictions variables used for the predictions chart
        self.current_values_plot_item = None
        self.predicted_values_plot_item = None

        self.initUI()

    def initUI(self):

        # label_sensor_name
        self.label_sensor_name = QtWidgets.QLabel()
        self.label_sensor_name.setText("Name")
        self.label_sensor_name.setAlignment(QtCore.Qt.AlignRight)

        # text_box_sensor_name
        self.text_box_sensor_name = QtWidgets.QLineEdit()
        self.text_box_sensor_name.setEnabled(False)
        self.text_box_sensor_name.setAlignment(QtCore.Qt.AlignLeft)

        # label_sensor_precision_rate
        self.label_sensor_precision_rate = QtWidgets.QLabel()
        self.label_sensor_precision_rate.setText("Precision Rate (%)")
        self.label_sensor_precision_rate.setAlignment(QtCore.Qt.AlignRight)

        # text_box_sensor_precision_rate
        self.text_box_sensor_precision_rate = QtWidgets.QLineEdit()
        self.text_box_sensor_precision_rate.setEnabled(False)
        self.text_box_sensor_precision_rate.setAlignment(QtCore.Qt.AlignRight)

        # check_box_enable_classification_learning
        self.check_box_enable_classification_learning = QtWidgets.QCheckBox()
        self.check_box_enable_classification_learning.setText("Enable Classification Learning")
        self.check_box_enable_classification_learning.toggled.connect(self.checkBoxEnableClassificationLearning_toggled)

        # check_box_enable_classification_inference
        self.check_box_enable_classification_inference = QtWidgets.QCheckBox()
        self.check_box_enable_classification_inference.setText("Enable Classification Inference")
        self.check_box_enable_classification_inference.toggled.connect(self.checkBoxEnableClassificationInference_toggled)

        # sensor_layout
        sensor_layout = QtWidgets.QGridLayout()
        sensor_layout.addWidget(self.label_sensor_name, 0, 0)
        sensor_layout.addWidget(self.text_box_sensor_name, 0, 1)
        sensor_layout.addWidget(self.label_sensor_precision_rate, 1, 0)
        sensor_layout.addWidget(self.text_box_sensor_precision_rate, 1, 1)
        sensor_layout.addWidget(self.check_box_enable_classification_learning, 2, 1)
        sensor_layout.addWidget(self.check_box_enable_classification_inference, 3, 1)
        sensor_layout.setRowStretch(4, 100)

        # tab_page_sensor_layout
        tab_page_sensor_layout = QtWidgets.QGridLayout()
        tab_page_sensor_layout.addLayout(sensor_layout, 0, 0)
        tab_page_sensor_layout.setColumnStretch(1, 100)

        # tab_page_sensor
        self.tab_page_sensor = QtWidgets.QWidget()
        self.tab_page_sensor.setLayout(tab_page_sensor_layout)

        # data_grid_bits
        self.data_grid_bits = QtWidgets.QTableView()
        self.data_grid_bits.setModel(ArrayTableModel(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable))
        self.data_grid_bits.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.data_grid_bits.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.data_grid_bits.setToolTip("Click on a row to see more details")
        self.data_grid_bits.verticalHeader().setDefaultSectionSize(20)

        # tab_page_bits_layout
        tab_page_bits_layout = QtWidgets.QHBoxLayout()
        tab_page_bits_layout.addWidget(self.data_grid_bits)

        # tab_page_bits
        self.tab_page_bits = QtWidgets.QWidget()
        self.tab_page_bits.setLayout(tab_page_bits_layout)

        # label_encoding
        self.label_encoding = QtWidgets.QLabel()
        self.label_encoding.setText("Encoding:")
        self.label_encoding.setAlignment(QtCore.Qt.AlignRight)

        # combo_box_encoding
        self.combo_box_encoding = QtWidgets.QComboBox()
        self.combo_box_encoding.currentIndexChanged.connect(self.comboBoxEncoding_currentIndexChanged)

        # label_current_value
        self.label_current_value = QtWidgets.QLabel()
        self.label_current_value.setText("Current Value")
        self.label_current_value.setAlignment(QtCore.Qt.AlignRight)

        # text_box_current_value
        self.text_box_current_value = QtWidgets.QLineEdit()
        self.text_box_current_value.setEnabled(False)
        self.text_box_current_value.setAlignment(QtCore.Qt.AlignRight)

        # label_predicted_values
        self.label_predicted_values = QtWidgets.QLabel()
        self.label_predicted_values.setText("Predicted Values")
        self.label_predicted_values.setAlignment(QtCore.Qt.AlignRight)

        # data_grid_predicted_values
        self.data_grid_predicted_values = QtWidgets.QTableView()
        self.data_grid_predicted_values.setModel(ArrayTableModel(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable))
        self.data_grid_predicted_values.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.data_grid_predicted_values.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.data_grid_predicted_values.verticalHeader().setDefaultSectionSize(20)

        # encoding_1_layout
        encoding_1_layout = QtWidgets.QGridLayout()
        encoding_1_layout.addWidget(self.label_encoding, 0, 0)
        encoding_1_layout.addWidget(self.combo_box_encoding, 0, 1)
        encoding_1_layout.addWidget(self.label_current_value, 1, 0)
        encoding_1_layout.addWidget(self.text_box_current_value, 1, 1)
        encoding_1_layout.setRowStretch(2, 100)

        # slider_step
        self.slider_step = QtWidgets.QSlider()
        self.slider_step.setOrientation(QtCore.Qt.Horizontal)
        self.slider_step.setSingleStep(1)
        self.slider_step.setRange(1, MAX_FUTURE_STEPS)
        self.slider_step.valueChanged.connect(self.sliderStep_valueChanged)

        # encoding_2_layout
        encoding_2_layout = QtWidgets.QGridLayout()
        encoding_2_layout.addWidget(self.slider_step, 0, 1)
        encoding_2_layout.addWidget(self.label_predicted_values, 1, 0)
        encoding_2_layout.addWidget(self.data_grid_predicted_values, 1, 1)

        # predictions_chart
        self.predictions_chart = pg.PlotWidget()
        self.predictions_chart.showGrid(x=True, y=True)
        self.predictions_chart.getAxis('left').setGrid(1)

        # encoding_3_layout
        encoding_3_layout = QtWidgets.QGridLayout()
        encoding_3_layout.addWidget(self.predictions_chart, 0, 1)

        # tab_page_encodings_layout
        tab_page_encodings_layout = QtWidgets.QHBoxLayout()
        tab_page_encodings_layout.addLayout(encoding_1_layout)
        tab_page_encodings_layout.addLayout(encoding_2_layout)
        tab_page_encodings_layout.addLayout(encoding_3_layout)

        # tab_page_encodings
        self.tab_page_encodings = QtWidgets.QWidget()
        self.tab_page_encodings.setLayout(tab_page_encodings_layout)

        # label_region_name
        self.label_region_name = QtWidgets.QLabel()
        self.label_region_name.setText("Name")
        self.label_region_name.setAlignment(QtCore.Qt.AlignRight)

        # text_box_region_name
        self.text_box_region_name = QtWidgets.QLineEdit()
        self.text_box_region_name.setEnabled(False)
        self.text_box_region_name.setAlignment(QtCore.Qt.AlignLeft)

        # label_region_precision_rate
        self.label_region_precision_rate = QtWidgets.QLabel()
        self.label_region_precision_rate.setText("Precision Rate (%)")
        self.label_region_precision_rate.setAlignment(QtCore.Qt.AlignRight)

        # text_box_region_precision_rate
        self.text_box_region_precision_rate = QtWidgets.QLineEdit()
        self.text_box_region_precision_rate.setEnabled(False)
        self.text_box_region_precision_rate.setAlignment(QtCore.Qt.AlignRight)

        # check_box_enable_spatial_learning
        self.check_box_enable_spatial_learning = QtWidgets.QCheckBox()
        self.check_box_enable_spatial_learning.setText("Enable Spatial Learning")
        self.check_box_enable_spatial_learning.toggled.connect(self.checkBoxEnableSpatialLearning_toggled)

        # check_box_enable_temporal_learning
        self.check_box_enable_temporal_learning = QtWidgets.QCheckBox()
        self.check_box_enable_temporal_learning.setText("Enable Temporal Learning")
        self.check_box_enable_temporal_learning.toggled.connect(self.checkBoxEnableTemporalLearning_toggled)

        # tab_page_regions_layout
        tab_page_regions_layout = QtWidgets.QGridLayout()
        tab_page_regions_layout.addWidget(self.label_region_name, 0, 0)
        tab_page_regions_layout.addWidget(self.text_box_region_name, 0, 1)
        tab_page_regions_layout.addWidget(self.label_region_precision_rate, 1, 0)
        tab_page_regions_layout.addWidget(self.text_box_region_precision_rate, 1, 1)
        tab_page_regions_layout.addWidget(self.check_box_enable_spatial_learning, 2, 1)
        tab_page_regions_layout.addWidget(self.check_box_enable_temporal_learning, 3, 1)
        tab_page_regions_layout.setRowStretch(4, 100)
        tab_page_regions_layout.setColumnStretch(2, 100)

        # tab_page_regions
        self.tab_page_regions = QtWidgets.QWidget()
        self.tab_page_regions.setLayout(tab_page_regions_layout)

        # data_grid_columns
        self.data_grid_columns = QtWidgets.QTableView()
        self.data_grid_columns.setModel(ArrayTableModel(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable))
        self.data_grid_columns.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.data_grid_columns.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.data_grid_columns.setToolTip("Click on a row to see more details")
        self.data_grid_columns.verticalHeader().setDefaultSectionSize(20)
        self.data_grid_columns.selectionModel().selectionChanged.connect(self.dataGridColumns_selectionChanged)

        # tab_page_columns_layout
        tab_page_columns_layout = QtWidgets.QHBoxLayout()
        tab_page_columns_layout.addWidget(self.data_grid_columns)

        # tab_page_columns
        self.tab_page_columns = QtWidgets.QWidget()
        self.tab_page_columns.setLayout(tab_page_columns_layout)

        # data_grid_proximal_synapses
        self.data_grid_proximal_synapses = QtWidgets.QTableView()
        self.data_grid_proximal_synapses.setModel(ArrayTableModel(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable))
        self.data_grid_proximal_synapses.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.data_grid_proximal_synapses.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.data_grid_proximal_synapses.setToolTip("Click on a row to see more details")
        self.data_grid_proximal_synapses.verticalHeader().setDefaultSectionSize(20)
        self.data_grid_proximal_synapses.selectionModel().selectionChanged.connect(self.dataGridProximalSynapses_selectionChanged)

        # tab_page_proximal_synapses_layout
        tab_page_proximal_synapses_layout = QtWidgets.QHBoxLayout()
        tab_page_proximal_synapses_layout.addWidget(self.data_grid_proximal_synapses)

        # tab_page_proximal_synapses
        self.tab_page_proximal_synapses = QtWidgets.QWidget()
        self.tab_page_proximal_synapses.setLayout(tab_page_proximal_synapses_layout)

        # data_grid_cells
        self.data_grid_cells = QtWidgets.QTableView()
        self.data_grid_cells.setModel(ArrayTableModel(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable))
        self.data_grid_cells.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.data_grid_cells.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.data_grid_cells.setToolTip("Click on a row to see more details")
        self.data_grid_cells.verticalHeader().setDefaultSectionSize(20)
        self.data_grid_cells.selectionModel().selectionChanged.connect(self.dataGridCells_selectionChanged)

        # tab_page_cells_layout
        tab_page_cells_layout = QtWidgets.QHBoxLayout()
        tab_page_cells_layout.addWidget(self.data_grid_cells)

        # tab_page_cells
        self.tab_page_cells = QtWidgets.QWidget()
        self.tab_page_cells.setLayout(tab_page_cells_layout)

        # data_grid_distal_segments
        self.data_grid_distal_segments = QtWidgets.QTableView()
        self.data_grid_distal_segments.setModel(ArrayTableModel(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable))
        self.data_grid_distal_segments.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.data_grid_distal_segments.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.data_grid_distal_segments.setToolTip("Click on a row to see more details")
        self.data_grid_distal_segments.verticalHeader().setDefaultSectionSize(20)
        self.data_grid_distal_segments.selectionModel().selectionChanged.connect(self.dataGridDistalSegments_selectionChanged)

        # tab_page_distal_segments_layout
        tab_page_distal_segments_layout = QtWidgets.QHBoxLayout()
        tab_page_distal_segments_layout.addWidget(self.data_grid_distal_segments)

        # tab_page_distal_segments
        self.tab_page_distal_segments = QtWidgets.QWidget()
        self.tab_page_distal_segments.setLayout(tab_page_distal_segments_layout)

        # data_grid_distal_synapses
        self.data_grid_distal_synapses = QtWidgets.QTableView()
        self.data_grid_distal_synapses.setModel(ArrayTableModel(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable))
        self.data_grid_distal_synapses.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.data_grid_distal_synapses.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.data_grid_distal_synapses.setToolTip("Click on a row to see more details")
        self.data_grid_distal_synapses.verticalHeader().setDefaultSectionSize(20)
        self.data_grid_distal_synapses.selectionModel().selectionChanged.connect(self.dataGridDistalSynapses_selectionChanged)

        # tab_page_distal_synapses_layout
        tab_page_distal_synapses_layout = QtWidgets.QHBoxLayout()
        tab_page_distal_synapses_layout.addWidget(self.data_grid_distal_synapses)

        # tab_page_distal_synapses
        self.tab_page_distal_synapses = QtWidgets.QWidget()
        self.tab_page_distal_synapses.setLayout(tab_page_distal_synapses_layout)

        # tab_control_main
        self.tab_control_main = QtWidgets.QTabWidget()

        # layout
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.tab_control_main)

        # self
        self.setLayout(layout)
        self.setWindowTitle("Node Information")
        self.setWindowIcon(QtGui.QIcon(Global.app_path + '/images/logo.ico'))
        self.setMinimumHeight(200)
        self.setMaximumHeight(300)

    def clearControls(self):
        """
        Reset all controls.
        """
        self.text_box_current_value.setText("")
        self.slider_step.setEnabled(False)
        self.data_grid_predicted_values.model().update([], [])
        self.predictions_chart.setVisible(False)

    def refreshControls(self):
        """
        Refresh controls for each time step.
        """
        selected_node = Global.architecture_window.design_panel.selected_node

        # Show information according to note type
        if selected_node != self.previous_selected_node:
            while True:
                self.tab_control_main.removeTab(0)
                if self.tab_control_main.count() == 0:
                    break
            if selected_node.type == NodeType.REGION:
                self.selected_region = selected_node

                self.text_box_region_name.setText(self.selected_region.name)
                self.check_box_enable_spatial_learning.setChecked(self.selected_region.enable_spatial_learning)
                self.check_box_enable_temporal_learning.setChecked(self.selected_region.enable_temporal_learning)
                self.showTab(self.tab_page_regions, "Region")
                self.showTab(self.tab_page_columns, "Columns")
                self.data_grid_columns.clearSelection()
            elif selected_node.type == NodeType.SENSOR:
                self.selected_sensor = selected_node

                self.text_box_sensor_name.setText(self.selected_sensor.name)
                self.showTab(self.tab_page_sensor, "Sensor")
                self.showTab(self.tab_page_bits, "Bits")
                self.showTab(self.tab_page_encodings, "Encodings")
                self.data_grid_bits.clearSelection()
                if self.selected_sensor.predictions_method == PredictionsMethod.CLASSIFICATION:
                    self.check_box_enable_classification_learning.setVisible(True)
                    self.check_box_enable_classification_learning.setChecked(self.selected_sensor.enable_classification_learning)
                    self.check_box_enable_classification_inference.setVisible(True)
                    self.check_box_enable_classification_inference.setChecked(self.selected_sensor.enable_classification_inference)
                else:
                    self.check_box_enable_classification_learning.setVisible(False)
                    self.check_box_enable_classification_inference.setVisible(False)

                # Populate encodings combobox
                self.combo_box_encoding.clear()
                for encoding in self.selected_sensor.encodings:
                    if encoding.enable_inference:
                        name = encoding.encoder_field_name.split('.')[0]
                        self.combo_box_encoding.addItem(name)
                self.selected_encoding = None
            self.tab_control_main.selectedIndex = 0

            self.previous_selected_node = selected_node

        if Global.simulation_initialized:
            if selected_node.type == NodeType.REGION:
                self.text_box_region_precision_rate.setText("{0:.3f}".format(self.selected_region.stats_precision_rate))

                # Bind the columns from this region
                header, data = self.getColumnsData(self.selected_region)
                self.data_grid_columns.model().update(header, data)
                self.data_grid_columns.resizeColumnsToContents()

            elif selected_node.type == NodeType.SENSOR:
                self.text_box_sensor_precision_rate.setText("{0:.3f}".format(self.selected_sensor.stats_precision_rate))

                # Bind the bits from this sensor
                header, data = self.getBitsData(self.selected_sensor)
                self.data_grid_bits.model().update(header, data)
                self.data_grid_bits.resizeColumnsToContents()

                # Reset step slider state
                self.slider_step.setEnabled(True)
                self.slider_step.setValue(self.slider_step.minimum())
                if self.selected_sensor.predictions_method == PredictionsMethod.CLASSIFICATION:
                    self.slider_step.setEnabled(True)
                else:
                    self.slider_step.setEnabled(False)

                # Set default encoding
                if self.selected_encoding == None:
                    self.selected_encoding = self.selected_sensor.encodings[0]
                self.updateEncodingControls()

    def formatValue(self, data_type, value):
        formatted_value = None

        if value == None:
            formatted_value = "None"
        elif data_type == FieldDataType.BOOLEAN:
            if value == 0:
                formatted_value = "False"
            else:
                formatted_value = "True"
        elif data_type == FieldDataType.INTEGER:
            formatted_value = "{0}".format(value)
        elif data_type == FieldDataType.DECIMAL:
            formatted_value = "{0:.3f}".format(value)
        elif data_type == FieldDataType.DATE_TIME:
            formatted_value = value.strftime("%Y-%m-%d %H:%M:%S")
        else:
            formatted_value = str(value)

        return formatted_value

    def getBitsData(self, selected_sensor):
        header = ['Pos (x,y)', 'Was Predicted', 'Is Active', 'Activation Rate', 'Precision Rate']
        data = []
        for bit in selected_sensor.bits:
            pos = str(bit.x) + ", " + str(bit.y)
            was_predicted = bit.is_predicted.atGivenStepAgo(Global.sel_step + 1)
            is_active = bit.is_active.atGivenStepAgo(Global.sel_step)
            activation_rate = "{0:.3f}".format(bit.stats_activation_rate)
            precision_rate = "{0:.3f}".format(bit.stats_precision_rate)
            data.append([pos, was_predicted, is_active, activation_rate, precision_rate])
        return header, data

    def updateEncodingControls(self):
        self.text_box_current_value.setText(self.formatValue(self.selected_encoding.encoder_field_data_type, self.selected_encoding.current_value.atGivenStepAgo(Global.sel_step)))
        self.slider_step.setVisible(self.selected_encoding.enable_inference)
        self.label_predicted_values.setVisible(self.selected_encoding.enable_inference)
        self.data_grid_predicted_values.setVisible(self.selected_encoding.enable_inference)
        self.predictions_chart.setVisible(False)
        if Global.simulation_initialized and self.selected_encoding.enable_inference:
            self.updatePredictedValuesGrid()
            if self.selected_encoding.encoder_field_data_type == FieldDataType.INTEGER or self.selected_encoding.encoder_field_data_type == FieldDataType.DECIMAL:
                self.updatePredictionsChart()
                self.predictions_chart.setVisible(True)

    def updatePredictedValuesGrid(self):
        step = self.slider_step.value()
        header, data = self.getPredictedValuesData(step)
        self.data_grid_predicted_values.model().update(header, data)
        self.data_grid_predicted_values.resizeColumnsToContents()

    def updatePredictionsChart(self):

        # Update the chart with the updated predictions history
        if self.current_values_plot_item == None:
            # Set plot lines
            self.current_values_plot_item = self.predictions_chart.plot(Global.time_steps_predictions_chart.getList(), self.selected_encoding.current_value.getList())
            self.current_values_plot_item.setPen(QtGui.QColor.fromRgb(0, 100, 0)) # green color
            self.predicted_values_plot_item = self.predictions_chart.plot(Global.time_steps_predictions_chart.getList(), self.selected_encoding.best_predicted_value.getList())
            self.predicted_values_plot_item.setPen(QtGui.QColor.fromRgb(255, 215, 80)) # yellow color

            # Set legend
            legend = self.predictions_chart.addLegend(size=None, offset=(0, 0))
            legend.addItem(self.current_values_plot_item, "Current")
            legend.addItem(self.predicted_values_plot_item, "Predicted")
        else:
            self.current_values_plot_item.setData(Global.time_steps_predictions_chart.getList(), self.selected_encoding.current_value.getList())
            self.predicted_values_plot_item.setData(Global.time_steps_predictions_chart.getList(), self.selected_encoding.best_predicted_value.getList())

        # Set X axis visible range
        min_x = Global.time_steps_predictions_chart.atFirstStep()
        max_x = min_x + MAX_PREVIOUS_STEPS_WITH_INFERENCE
        max_x += 30 # Increase space to avoid plot lines overlap the legend
        self.predictions_chart.setXRange(min_x, max_x)

    def getPredictedValuesData(self, future_step):
        header = []
        if self.selected_sensor.predictions_method == PredictionsMethod.RECONSTRUCTION:
            header = ['Value']
        elif self.selected_sensor.predictions_method == PredictionsMethod.CLASSIFICATION:
            header = ['Value', 'Probability']

        data = []
        predictions = self.selected_encoding.predicted_values.atGivenStepAgo(Global.sel_step)[future_step]
        for predicted_value in predictions:
            if self.selected_sensor.predictions_method == PredictionsMethod.RECONSTRUCTION:
                value = predicted_value[1]
                data.append([value])
            elif self.selected_sensor.predictions_method == PredictionsMethod.CLASSIFICATION:
                value = self.formatValue(self.selected_encoding.encoder_field_data_type, predicted_value[0])
                probability = "{0:.3f}".format(predicted_value[1] * 100)
                data.append([value, probability])

        return header, data

    def getColumnsData(self, selected_region):
        header = ['Pos (x,y)', 'Was Predicted', 'Is Active', 'Activation Rate', 'Precision Rate']
        data = []
        for column in selected_region.columns:
            pos = str(column.x) + ", " + str(column.y)
            was_predicted = column.segment.is_predicted.atGivenStepAgo(Global.sel_step + 1)
            is_active = column.segment.is_active.atGivenStepAgo(Global.sel_step)
            activation_rate = "{0:.3f}".format(column.segment.stats_activation_rate)
            precision_rate = "{0:.3f}".format(column.segment.stats_precision_rate)
            data.append([pos, was_predicted, is_active, activation_rate, precision_rate])
        return header, data

    def getProximalSynapsesData(self, selected_segment):
        #TODO: Put sensor bit position (x,y,z)
        header = ['Permanence', 'Is Connected', 'Connection Rate', 'Precision Rate']
        data = []
        for synapse in selected_segment.synapses:
            permanence = "{0:.3f}".format(synapse.permanence.atGivenStepAgo(Global.sel_step))
            is_connected = synapse.is_connected.atGivenStepAgo(Global.sel_step)
            connection_rate = "{0:.3f}".format(synapse.stats_connection_rate)
            precision_rate = "{0:.3f}".format(synapse.stats_precision_rate)
            data.append([permanence, is_connected, connection_rate, precision_rate])
        return header, data

    def getCellsData(self, selected_column):
        header = ['Pos (z)', 'Was Predicted', 'Is Active', 'Activation Rate', 'Precision Rate']
        data = []
        for cell in selected_column.cells:
            pos = str(cell.z)
            was_predicted = cell.is_predicted.atGivenStepAgo(Global.sel_step + 1)
            is_active = cell.is_active.atGivenStepAgo(Global.sel_step)
            activation_rate = "{0:.3f}".format(cell.stats_activation_rate)
            precision_rate = "{0:.3f}".format(cell.stats_precision_rate)
            data.append([pos, was_predicted, is_active, activation_rate, precision_rate])
        return header, data

    def getDistalSegmetsData(self, selected_cell):
        header = ['Is Active', 'Activation Rate', 'Activation Rate']
        data = []
        for segment in selected_cell.segments:
            is_active = segment.is_active.atGivenStepAgo(Global.sel_step)
            activation_rate = "{0:.3f}".format(segment.stats_activation_rate)
            data.append([is_active, activation_rate, activation_rate])
        return header, data

    def getDistalSynapsesData(self, selected_segment):
        #TODO: Put lateral cell position (x,y,z)
        header = ['Permanence', 'Is Connected', 'Connection Rate']
        data = []
        for synapse in selected_segment.synapses:
            permanence = "{0:.3f}".format(synapse.permanence.atGivenStepAgo(Global.sel_step))
            is_connected = synapse.is_connected.atGivenStepAgo(Global.sel_step)
            connection_rate = "{0:.3f}".format(synapse.stats_connection_rate)
            data.append([permanence, is_connected, connection_rate])
        return header, data

    def showTab(self, tab, title):
        tab_found = False
        for idx in range(self.tab_control_main.count()):
            if self.tab_control_main.tabText(idx) == title:
                tab_found = True
        if not tab_found:
            self.tab_control_main.addTab(tab, title)

    def closeEvent(self, event):
        self.Hide()
        self.Parent = None
        event.Cancel = True

    def sliderStep_valueChanged(self, value):
        self.updatePredictedValuesGrid()

    def comboBoxEncoding_currentIndexChanged(self, event):
        if Global.simulation_initialized:
            idx = self.combo_box_encoding.currentIndex()
            self.selected_encoding = self.selected_sensor.encodings[idx]
            self.updateEncodingControls()

    def checkBoxEnableSpatialLearning_toggled(self, event):
        self.selected_region.enable_spatial_learning = self.check_box_enable_spatial_learning.isChecked()

    def checkBoxEnableTemporalLearning_toggled(self, event):
        self.selected_region.enable_temporal_learning = self.check_box_enable_temporal_learning.isChecked()

    def checkBoxEnableClassificationLearning_toggled(self, event):
        self.selected_sensor.enable_classification_learning = self.check_box_enable_classification_learning.isChecked()

    def checkBoxEnableClassificationInference_toggled(self, event):
        self.selected_sensor.enable_classification_inference = self.check_box_enable_classification_inference.isChecked()

    def dataGridColumns_selectionChanged(self, event):
        if self.selected_column != None:
            self.selected_column.segment.tree3d_selected = False

        self.data_grid_proximal_synapses.clearSelection()
        self.data_grid_cells.clearSelection()

        selected_rows = self.data_grid_columns.selectionModel().selectedRows()
        if len(selected_rows) > 0:
            index = selected_rows[0].row()
            self.selected_column = self.selected_region.columns[index]
            self.selected_column.segment.tree3d_selected = True

            # Bind the synapses of the selected segment
            self.showTab(self.tab_page_proximal_synapses, "Proximal Synapses")
            header, data = self.getProximalSynapsesData(self.selected_column.segment)
            self.data_grid_proximal_synapses.model().update(header, data)
            self.data_grid_proximal_synapses.resizeColumnsToContents()

            # Bind the cells of the selected column
            self.showTab(self.tab_page_cells, "Cells")
            header, data = self.getCellsData(self.selected_column)
            self.data_grid_cells.model().update(header, data)
            self.data_grid_cells.resizeColumnsToContents()

        Global.simulation_window.refreshControls()

    def dataGridProximalSynapses_selectionChanged(self, event):
        if self.selected_proximal_synapse != None:
            self.selected_proximal_synapse.tree3d_selected = False

        selected_rows = self.data_grid_proximal_synapses.selectionModel().selectedRows()
        if len(selected_rows) > 0:
            index = selected_rows[0].row()
            self.selected_proximal_synapse = self.selected_column.segment.synapses[index]
            self.selected_proximal_synapse.tree3d_selected = True

        Global.simulation_window.refreshControls()

    def dataGridCells_selectionChanged(self, event):
        if self.selected_cell != None:
            self.selected_cell.tree3d_selected = False

        self.data_grid_distal_segments.clearSelection()

        selected_rows = self.data_grid_cells.selectionModel().selectedRows()
        if len(selected_rows) > 0:
            index = selected_rows[0].row()
            self.selected_cell = self.selected_column.cells[index]
            self.selected_cell.tree3d_selected = True

            # Bind the segments of the selected cell
            self.showTab(self.tab_page_distal_segments, "Distal Segments")
            header, data = self.getDistalSegmetsData(self.selected_cell)
            self.data_grid_distal_segments.model().update(header, data)
            self.data_grid_distal_segments.resizeColumnsToContents()

        Global.simulation_window.refreshControls()

    def dataGridDistalSegments_selectionChanged(self, event):
        if self.selected_distal_segment != None:
            self.selected_distal_segment.tree3d_selected = False

        self.data_grid_distal_synapses.clearSelection()

        selected_rows = self.data_grid_distal_segments.selectionModel().selectedRows()
        if len(selected_rows) > 0:
            index = selected_rows[0].row()
            self.selected_distal_segment = self.selected_cell.segments[index]

            # Bind the synapses of the selected segment
            self.showTab(self.tab_page_distal_synapses, "Distal Synapses")
            header, data = self.getDistalSynapsesData(self.selected_distal_segment)
            self.data_grid_distal_synapses.model().update(header, data)
            self.data_grid_distal_synapses.resizeColumnsToContents()

        Global.simulation_window.refreshControls()

    def dataGridDistalSynapses_selectionChanged(self, event):
        if self.selected_distal_synapse != None:
            self.selected_distal_synapse.tree3d_selected = False

        selected_rows = self.data_grid_distal_synapses.selectionModel().selectedRows()
        if len(selected_rows) > 0:
            index = selected_rows[0].row()
            self.selected_distal_synapse = self.selected_distal_segment.synapses[index]
            self.selected_distal_synapse.tree3d_selected = True

        Global.simulation_window.refreshControls()
