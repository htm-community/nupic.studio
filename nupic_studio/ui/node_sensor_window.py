import copy
from PyQt5 import QtGui, QtCore, QtWidgets
from nupic_studio.htm.node_sensor import DataSourceType, PredictionsMethod
from nupic_studio.ui import Global
from nupic_studio.ui.node_sensor_encoding_window import EncodingWindow


class SensorWindow(QtWidgets.QDialog):

    def __init__(self):
        """
        Initializes a new instance of this class.
        """
        QtWidgets.QDialog.__init__(self)
        self.initUI()

        # Temporary list of encodings that is being edited.
        self.encodings = []

        # Flag to indicate if encodings list was edited.
        self.encodings_changed = False

    def initUI(self):

        # label_sensor_width
        self.label_sensor_width = QtWidgets.QLabel()
        self.label_sensor_width.setText("Sensor Width")
        self.label_sensor_width.setAlignment(QtCore.Qt.AlignRight)

        # spinner_sensor_width
        self.spinner_sensor_width = QtWidgets.QSpinBox()
        self.spinner_sensor_width.setAlignment(QtCore.Qt.AlignRight)
        self.spinner_sensor_width.setToolTip("Number of output bits in the X direction for this sensor.")
        self.spinner_sensor_width.setMaximum(1000)
        self.spinner_sensor_width.setEnabled(not Global.simulation_initialized)

        # label_sensor_height
        self.label_sensor_height = QtWidgets.QLabel()
        self.label_sensor_height.setText("Sensor Height")
        self.label_sensor_height.setAlignment(QtCore.Qt.AlignRight)

        # spinner_sensor_height
        self.spinner_sensor_height = QtWidgets.QSpinBox()
        self.spinner_sensor_height.setAlignment(QtCore.Qt.AlignRight)
        self.spinner_sensor_height.setToolTip("Number of output bits in the Y direction for this sensor.")
        self.spinner_sensor_height.setMaximum(1000)
        self.spinner_sensor_height.setEnabled(not Global.simulation_initialized)

        # radio_button_data_source_file
        self.radio_button_data_source_file = QtWidgets.QRadioButton()
        self.radio_button_data_source_file.setText("File")
        self.radio_button_data_source_file.toggled.connect(self.radioButtonDataSource_click)

        # label_file
        self.label_file = QtWidgets.QLabel()
        self.label_file.setText("File:")
        self.label_file.setAlignment(QtCore.Qt.AlignRight)

        # text_box_file
        self.text_box_file = QtWidgets.QLineEdit()

        # button_browse_file
        self.button_browse_file = QtWidgets.QPushButton()
        self.button_browse_file.setText("Browse...")
        self.button_browse_file.clicked.connect(self.buttonBrowseFile_click)

        # radio_button_data_source_database
        self.radio_button_data_source_database = QtWidgets.QRadioButton()
        self.radio_button_data_source_database.setText("Database")
        self.radio_button_data_source_database.toggled.connect(self.radioButtonDataSource_click)

        # label_database_connection_string
        self.label_database_connection_string = QtWidgets.QLabel()
        self.label_database_connection_string.setText("Connection String:")
        self.label_database_connection_string.setAlignment(QtCore.Qt.AlignRight)

        # text_box_database_connection_string
        self.text_box_database_connection_string = QtWidgets.QLineEdit()

        # label_database_table
        self.label_database_table = QtWidgets.QLabel()
        self.label_database_table.setText("Table:")
        self.label_database_table.setAlignment(QtCore.Qt.AlignRight)

        # text_box_database_table
        self.text_box_database_table = QtWidgets.QLineEdit()

        # group_box_data_source_type_layout
        group_box_data_source_type_layout = QtWidgets.QGridLayout()
        group_box_data_source_type_layout.addWidget(self.radio_button_data_source_file, 0, 0)
        group_box_data_source_type_layout.addWidget(self.label_file, 1, 0)
        group_box_data_source_type_layout.addWidget(self.text_box_file, 1, 1)
        group_box_data_source_type_layout.addWidget(self.button_browse_file, 2, 1)
        group_box_data_source_type_layout.addWidget(self.radio_button_data_source_database, 3, 0)
        group_box_data_source_type_layout.addWidget(self.label_database_connection_string, 4, 0)
        group_box_data_source_type_layout.addWidget(self.text_box_database_connection_string, 4, 1)
        group_box_data_source_type_layout.addWidget(self.label_database_table, 5, 0)
        group_box_data_source_type_layout.addWidget(self.text_box_database_table, 5, 1)

        # group_box_data_source_type
        self.group_box_data_source_type = QtWidgets.QGroupBox()
        self.group_box_data_source_type.setLayout(group_box_data_source_type_layout)
        self.group_box_data_source_type.setTitle("Data Source Type")
        self.group_box_data_source_type.setEnabled(not Global.simulation_initialized)

        # label_predictions_method
        self.label_predictions_method = QtWidgets.QLabel()
        self.label_predictions_method.setText("Predictions Method:")
        self.label_predictions_method.setAlignment(QtCore.Qt.AlignRight)

        # combo_box_predictions_method
        self.combo_box_predictions_method = QtWidgets.QComboBox()
        self.combo_box_predictions_method.addItem(PredictionsMethod.RECONSTRUCTION)
        self.combo_box_predictions_method.addItem(PredictionsMethod.CLASSIFICATION)
        self.combo_box_predictions_method.setEnabled(not Global.simulation_initialized)

        # button_new_encoding
        self.button_new_encoding = QtWidgets.QPushButton()
        self.button_new_encoding.setText("New...")
        self.button_new_encoding.clicked.connect(self.buttonNewEncoding_click)
        self.button_new_encoding.setEnabled(not Global.simulation_initialized)

        # button_edit_encoding
        self.button_edit_encoding = QtWidgets.QPushButton()
        self.button_edit_encoding.setText("Edit...")
        self.button_edit_encoding.clicked.connect(self.buttonEditEncoding_click)
        self.button_edit_encoding.setEnabled(not Global.simulation_initialized)

        # button_delete_encoding
        self.button_delete_encoding = QtWidgets.QPushButton()
        self.button_delete_encoding.setText("Delete")
        self.button_delete_encoding.clicked.connect(self.buttonDeleteEncoding_click)
        self.button_delete_encoding.setEnabled(not Global.simulation_initialized)

        # list_box_encodings
        self.list_box_encodings = QtWidgets.QListWidget()
        self.list_box_encodings.setEnabled(not Global.simulation_initialized)

        # encodings_buttons_layout
        encodings_buttons_layout = QtWidgets.QHBoxLayout()
        encodings_buttons_layout.addWidget(self.button_new_encoding)
        encodings_buttons_layout.addWidget(self.button_edit_encoding)
        encodings_buttons_layout.addWidget(self.button_delete_encoding)

        # group_box_encodings_layout
        group_box_encodings_layout = QtWidgets.QVBoxLayout()
        group_box_encodings_layout.addLayout(encodings_buttons_layout)
        group_box_encodings_layout.addWidget(self.list_box_encodings)

        # group_box_encodings
        self.group_box_encodings = QtWidgets.QGroupBox()
        self.group_box_encodings.setLayout(group_box_encodings_layout)
        self.group_box_encodings.setTitle("Encodings")

        # group_box_main_layout
        group_box_main_layout = QtWidgets.QGridLayout()
        group_box_main_layout.addWidget(self.label_sensor_width, 0, 0)
        group_box_main_layout.addWidget(self.spinner_sensor_width, 0, 1)
        group_box_main_layout.addWidget(self.label_sensor_height, 1, 0)
        group_box_main_layout.addWidget(self.spinner_sensor_height, 1, 1)
        group_box_main_layout.addWidget(self.group_box_data_source_type, 2, 1)
        group_box_main_layout.addWidget(self.label_predictions_method, 3, 0)
        group_box_main_layout.addWidget(self.combo_box_predictions_method, 3, 1)
        group_box_main_layout.addWidget(self.group_box_encodings, 4, 1)

        # group_box_main
        self.group_box_main = QtWidgets.QGroupBox()
        self.group_box_main.setLayout(group_box_main_layout)

        # button_box
        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.button_box.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.buttonOk_click)
        self.button_box.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(not Global.simulation_initialized)
        self.button_box.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.buttonCancel_click)

        # layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.group_box_main)
        layout.addWidget(self.button_box)

        # self
        self.setLayout(layout)
        self.setModal(True)
        self.setWindowTitle("Sensor Properties")
        self.setWindowIcon(QtGui.QIcon(Global.app_path + '/images/logo.ico'))
        self.resize(400, 200)

    def setControlsValues(self):
        """
        Set controls values from a class instance.
        """

        # Set controls value with sensor params
        node = Global.architecture_window.design_panel.under_mouse_node
        self.spinner_sensor_width.setValue(node.width)
        self.spinner_sensor_height.setValue(node.height)

        if node.data_source_type == DataSourceType.FILE:
            self.radio_button_data_source_file.setChecked(True)
            self.text_box_file.setText(node.file_name)
        elif node.data_source_type == DataSourceType.DATABASE:
            self.radio_button_data_source_database.setChecked(True)
            self.text_box_database_connection_string.setText(node.database_connection_string)
            self.text_box_database_table.setText(node.database_table)

        self.combo_box_predictions_method.setCurrentIndex(self.combo_box_predictions_method.findText(node.predictions_method, QtCore.Qt.MatchFixedString))

        self.encodings = copy.deepcopy(node.encodings)
        self.updateEncodingsListBox()

    def updateEncodingsListBox(self):

        # Update the list box with the updated encodings
        self.list_box_encodings.clear()
        for encoding in self.encodings:
            name = encoding.encoder_field_name.split('.')[0]
            self.list_box_encodings.addItem(name)

        # Update controls according to list state
        if self.list_box_encodings.count() > 0:
            if self.list_box_encodings.currentRow() == -1:
                self.list_box_encodings.setCurrentRow(0)
            self.button_edit_encoding.setEnabled(not Global.simulation_initialized)
            self.button_delete_encoding.setEnabled(not Global.simulation_initialized)
        else:
            self.button_edit_encoding.setEnabled(False)
            self.button_delete_encoding.setEnabled(False)

    def buttonOk_click(self, event):
        """
        Check if values changed and save the,.
        """

        if self.radio_button_data_source_file.isChecked() and self.text_box_file.text() == '':
            QtWidgets.QMessageBox.warning(self, "Warning", "Input stream file was not specified.")
            return
        elif self.radio_button_data_source_database.isChecked() and self.text_box_database_connection_string.text() == '':
            QtWidgets.QMessageBox.warning(self, "Warning", "Database connection string was not specified.")
            return
        elif self.radio_button_data_source_database.isChecked() and self.text_box_database_table.text() == '':
            QtWidgets.QMessageBox.warning(self, "Warning", "Database table was not specified.")
            return
        elif self.list_box_encodings.count() == 0:
            QtWidgets.QMessageBox.warning(self, "Warning", "Encodings list is empty. At least one encoding should be specified.")
            return
        else:
            has_fields_with_inference = False
            for encoding in self.encodings:
                if encoding.enable_inference:
                    has_fields_with_inference = True
                    break
            if not has_fields_with_inference:
                QtWidgets.QMessageBox.warning(self, "Warning", "At least one encoding should have inference enabled.")
                return

        width = self.spinner_sensor_width.value()
        height = self.spinner_sensor_height.value()
        data_source_type = None
        if self.radio_button_data_source_file.isChecked():
            data_source_type = DataSourceType.FILE
        elif self.radio_button_data_source_database.isChecked():
            data_source_type = DataSourceType.DATABASE
        file_name = str(self.text_box_file.text())
        database_connection_string = str(self.text_box_database_connection_string.text())
        database_table = str(self.text_box_database_table.text())
        predictions_method = str(self.combo_box_predictions_method.currentText())

        # If anything has changed
        node = Global.architecture_window.design_panel.under_mouse_node
        if node.width != width or node.height != height or node.predictions_method != predictions_method or node.data_source_type != data_source_type or node.file_name != file_name or node.database_connection_string != database_connection_string or node.database_table != database_table or self.encodings_changed:
            # Set sensor params with controls values
            node.width = width
            node.height = height
            node.predictions_method = predictions_method
            node.data_source_type = data_source_type
            node.file_name = file_name
            node.database_connection_string = database_connection_string
            node.database_table = database_table
            node.encodings = copy.deepcopy(self.encodings)
            self.accept()

        self.close()

    def buttonCancel_click(self, event):
        self.reject()
        self.close()

    def buttonBrowseFile_click(self, event):
        # Ask user for an existing file
        selected_file = QtWidgets.QFileDialog().getOpenFileName(self, "Open File", Global.app_path + '/projects', "Input files (*.csv)")[0]

        # If file exists, set data source file
        if selected_file != '':
            # Set file
            self.text_box_file.setText(selected_file)

    def radioButtonDataSource_click(self, event):
        if not Global.simulation_initialized:
            flag = self.radio_button_data_source_file.isChecked()
            self.text_box_file.setEnabled(flag)
            self.button_browse_file.setEnabled(flag)
            self.text_box_database_connection_string.setEnabled(not flag)
            self.text_box_database_table.setEnabled(not flag)

    def buttonNewEncoding_click(self, event):
        encoding_window = EncodingWindow()
        encoding_window.encoding_idx = -1
        encoding_window.encodings = self.encodings
        dialog_result = encoding_window.exec_()
        if dialog_result == QtWidgets.QDialog.Accepted:
            self.encodings_changed = True
            self.updateEncodingsListBox()

    def buttonEditEncoding_click(self, event):
        encoding_window = EncodingWindow()
        encoding_window.encoding_idx = self.list_box_encodings.currentRow()
        encoding_window.encodings = self.encodings
        encoding_window.setControlsValues()
        dialog_result = encoding_window.exec_()
        if dialog_result == QtWidgets.QDialog.Accepted:
            self.encodings_changed = True
            self.updateEncodingsListBox()

    def buttonDeleteEncoding_click(self, event):
        self.encodings.remove(self.encodings[self.list_box_encodings.currentRow()])
        self.encodings_changed = True
        self.updateEncodingsListBox()
