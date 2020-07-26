import collections
import json
from PyQt5 import QtGui, QtCore, QtWidgets
from nupic_studio import ArrayTableModel
from nupic_studio.ui import ICON, Global
from nupic_studio.htm.encoding import Encoding, FieldDataType


class EncodingWindow(QtWidgets.QDialog):

    def __init__(self):
        """
        Initializes a new instance of this class.
        """
        QtWidgets.QDialog.__init__(self)
        self.initUI()

        # Index of the encoding that is being edited. If index is -1 the user is creating a new encoding.
        self.encoding_idx = -1

        # Temporary list of encodings that is being edited.
        self.encodings = []

    def initUI(self):

        # label_data_source_field_name
        self.label_data_source_field_name = QtWidgets.QLabel()
        self.label_data_source_field_name.setText("Datasource Field Name:")
        self.label_data_source_field_name.setAlignment(QtCore.Qt.AlignRight)

        # text_box_data_source_field_name
        self.text_box_data_source_field_name = QtWidgets.QLineEdit()
        self.text_box_data_source_field_name.setAlignment(QtCore.Qt.AlignLeft)

        # label_data_source_field_data_type
        self.label_data_source_field_data_type = QtWidgets.QLabel()
        self.label_data_source_field_data_type.setText("Field Data Type:")
        self.label_data_source_field_data_type.setAlignment(QtCore.Qt.AlignRight)

        # combo_box_data_source_field_data_type
        self.combo_box_data_source_field_data_type = QtWidgets.QComboBox()
        self.combo_box_data_source_field_data_type.addItem(FieldDataType.BOOLEAN)
        self.combo_box_data_source_field_data_type.addItem(FieldDataType.INTEGER)
        self.combo_box_data_source_field_data_type.addItem(FieldDataType.DECIMAL)
        self.combo_box_data_source_field_data_type.addItem(FieldDataType.DATE_TIME)
        self.combo_box_data_source_field_data_type.addItem(FieldDataType.STRING)

        # check_box_enable_inference
        self.check_box_enable_inference = QtWidgets.QCheckBox()
        self.check_box_enable_inference.setText("Enable Inference")

        # label_encoder_module
        self.label_encoder_module = QtWidgets.QLabel()
        self.label_encoder_module.setText("Module:")
        self.label_encoder_module.setAlignment(QtCore.Qt.AlignRight)

        # text_box_encoder_module
        self.text_box_encoder_module = QtWidgets.QLineEdit()
        self.text_box_encoder_module.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp('[a-zA-Z0-9._]+')))

        # label_encoder_class
        self.label_encoder_class = QtWidgets.QLabel()
        self.label_encoder_class.setText("Class:")
        self.label_encoder_class.setAlignment(QtCore.Qt.AlignRight)

        # text_box_encoder_class
        self.text_box_encoder_class = QtWidgets.QLineEdit()
        self.text_box_encoder_class.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp('[a-zA-Z0-9_]+')))

        # label_encoder_params
        self.label_encoder_params = QtWidgets.QLabel()
        self.label_encoder_params.setText("Params:")
        self.label_encoder_params.setAlignment(QtCore.Qt.AlignRight)

        # data_grid_encoder_params
        data = [['', ''] for i in xrange(6)]
        self.data_grid_encoder_params = QtWidgets.QTableView()
        self.data_grid_encoder_params.setModel(ArrayTableModel(QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable))
        self.data_grid_encoder_params.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.data_grid_encoder_params.verticalHeader().setDefaultSectionSize(18)
        self.data_grid_encoder_params.model().update(['Parameter', 'Value'], data)
        self.data_grid_encoder_params.resizeColumnsToContents()
        self.data_grid_encoder_params.setMinimumHeight(140)

        # label_encoder_field_name
        self.label_encoder_field_name = QtWidgets.QLabel()
        self.label_encoder_field_name.setText("Field Name:")
        self.label_encoder_field_name.setAlignment(QtCore.Qt.AlignRight)

        # text_box_encoder_field_name
        self.text_box_encoder_field_name = QtWidgets.QLineEdit()
        self.text_box_encoder_field_name.setAlignment(QtCore.Qt.AlignLeft)

        # label_encoder_field_data_type
        self.label_encoder_field_data_type = QtWidgets.QLabel()
        self.label_encoder_field_data_type.setText("Field Data Type:")
        self.label_encoder_field_data_type.setAlignment(QtCore.Qt.AlignRight)

        # combo_box_encoder_field_data_type
        self.combo_box_encoder_field_data_type = QtWidgets.QComboBox()
        self.combo_box_encoder_field_data_type.addItem(FieldDataType.BOOLEAN)
        self.combo_box_encoder_field_data_type.addItem(FieldDataType.INTEGER)
        self.combo_box_encoder_field_data_type.addItem(FieldDataType.DECIMAL)
        self.combo_box_encoder_field_data_type.addItem(FieldDataType.DATE_TIME)
        self.combo_box_encoder_field_data_type.addItem(FieldDataType.STRING)

        # group_box_encoder_layout
        group_box_encoder_layout = QtWidgets.QGridLayout()
        group_box_encoder_layout.addWidget(self.label_encoder_module, 0, 0)
        group_box_encoder_layout.addWidget(self.text_box_encoder_module, 0, 1)
        group_box_encoder_layout.addWidget(self.label_encoder_class, 1, 0)
        group_box_encoder_layout.addWidget(self.text_box_encoder_class, 1, 1)
        group_box_encoder_layout.addWidget(self.label_encoder_params, 2, 0)
        group_box_encoder_layout.addWidget(self.data_grid_encoder_params, 2, 1)
        group_box_encoder_layout.addWidget(self.label_encoder_field_name, 3, 0)
        group_box_encoder_layout.addWidget(self.text_box_encoder_field_name, 3, 1)
        group_box_encoder_layout.addWidget(self.label_encoder_field_data_type, 4, 0)
        group_box_encoder_layout.addWidget(self.combo_box_encoder_field_data_type, 4, 1)

        # group_box_encoder
        self.group_box_encoder = QtWidgets.QGroupBox()
        self.group_box_encoder.setLayout(group_box_encoder_layout)
        self.group_box_encoder.setTitle("Encoder")

        # group_box_main_layout
        group_box_main_layout = QtWidgets.QGridLayout()
        group_box_main_layout.addWidget(self.label_data_source_field_name, 0, 0)
        group_box_main_layout.addWidget(self.text_box_data_source_field_name, 0, 1)
        group_box_main_layout.addWidget(self.label_data_source_field_data_type, 1, 0)
        group_box_main_layout.addWidget(self.combo_box_data_source_field_data_type, 1, 1)
        group_box_main_layout.addWidget(self.check_box_enable_inference, 2, 1)
        group_box_main_layout.addWidget(self.group_box_encoder, 3, 1)

        # group_box_main
        self.group_box_main = QtWidgets.QGroupBox()
        self.group_box_main.setLayout(group_box_main_layout)

        # button_box
        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.button_box.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.buttonOk_click)
        self.button_box.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(not self.main_window.isRunning())
        self.button_box.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.buttonCancel_click)

        # layout
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.group_box_main)
        layout.addWidget(self.button_box)

        # self
        self.setLayout(layout)
        self.setModal(True)
        self.setWindowTitle("Sensor Properties")
        self.setWindowIcon(ICON)
        self.resize(400, 200)

    def setControlsValues(self):
        """
        Set controls values from a class instance.
        """

        # Set controls value with encoding params
        if self.encoding_idx >= 0:
            encoding = self.encodings[self.encoding_idx]
            self.check_box_enable_inference.setChecked(encoding.enable_inference)
            self.text_box_data_source_field_name.setText(encoding.data_source_field_name)
            self.combo_box_data_source_field_data_type.setCurrentIndex(self.combo_box_data_source_field_data_type.findText(encoding.data_source_field_data_type, QtCore.Qt.MatchFixedString))

            # Set encoding parameters
            self.text_box_encoder_module.setText(encoding.encoder_module)
            self.text_box_encoder_class.setText(encoding.encoder_class)
            encoder_params = encoding.encoder_params
            grid_data = self.data_grid_encoder_params.model().data
            row = 0
            for key, value in encoder_params.iteritems():
                grid_data[row][0] = key
                grid_data[row][1] = value
                row += 1
            self.text_box_encoder_field_name.setText(encoding.encoder_field_name)
            self.combo_box_encoder_field_data_type.setCurrentIndex(self.combo_box_encoder_field_data_type.findText(encoding.encoder_field_data_type, QtCore.Qt.MatchFixedString))

    def duplicatedFieldName(self, field_name):
        """
        Check if exists an encoding with the same name.
        """
        duplicated = False
        if len(self.encodings) > 0:
            for i in range(len(self.encodings)):
                if self.encodings[i].encoder_field_name == field_name and i != self.encoding_idx:
                    duplicated = True
                    break
        return duplicated

    def buttonOk_click(self, event):
        """
        Check if values changed and save the,.
        """

        encoder_params = collections.OrderedDict()
        if self.text_box_data_source_field_name.text() == '':
            QtWidgets.QMessageBox.warning(self, "Warning", "Record field name was not specified.")
            return
        elif self.text_box_encoder_module.text() == '':
            QtWidgets.QMessageBox.warning(self, "Warning", "Encoder module was not specified.")
            return
        elif self.text_box_encoder_class.text() == '':
            QtWidgets.QMessageBox.warning(self, "Warning", "Encoder class was not specified.")
            return
        elif self.text_box_encoder_field_name.text() == '':
            QtWidgets.QMessageBox.warning(self, "Warning", "Encoder field name was not specified.")
            return
        elif self.duplicatedFieldName(self.text_box_encoder_field_name.text()):
            QtWidgets.QMessageBox.warning(self, "Warning", "Encoder field name already is used by other encoding.")
            return
        else:
            grid_data = self.data_grid_encoder_params.model().data
            for row in range(len(grid_data)):
                if grid_data[row][0] != '':
                    # Valid parameter name
                    try:
                        grid_data[row][0] = grid_data[row][0].toString()
                    except:
                        pass
                    param = str(grid_data[row][0])
                    valid_expr = QtCore.QRegExp('[a-zA-Z0-9_]+')
                    if not valid_expr.exactMatch(param):
                        QtWidgets.QMessageBox.warning(self, "Warning", "'" + param + "' is not a valid name.")
                        return

                    # Valid parameter value
                    try:
                        grid_data[row][1] = grid_data[row][1].toString()
                    except:
                        pass
                    value = str(grid_data[row][1])
                    if len(value) == 0:
                        QtWidgets.QMessageBox.warning(self, "Warning", "'" + param + "' value is empty.")
                        return

                    # Add param name and its value to dictionary
                    encoder_params[param] = value

        data_source_field_name = str(self.text_box_data_source_field_name.text())
        data_source_field_data_type = str(self.combo_box_data_source_field_data_type.currentText())
        enable_inference = self.check_box_enable_inference.isChecked()
        encoder_module = str(self.text_box_encoder_module.text())
        encoder_class = str(self.text_box_encoder_class.text())
        encoder_field_name = str(self.text_box_encoder_field_name.text())
        encoder_field_data_type = str(self.combo_box_encoder_field_data_type.currentText())

        # If this is a new encoding get it from list else create a new one
        if self.encoding_idx >= 0:
            encoding = self.encodings[self.encoding_idx]
        else:
            encoding = Encoding()
            self.encodings.append(encoding)

        # If anything has changed
        if encoding.data_source_field_name != data_source_field_name or encoding.data_source_field_data_type != data_source_field_data_type or encoding.enable_inference != enable_inference or encoding.encoder_module != encoder_module or encoding.encoder_class != encoder_class or encoding.encoder_params != encoder_params or encoding.encoder_field_name != encoder_field_name or encoding.encoder_field_data_type != encoder_field_data_type:

            # Set encoding params with controls values
            encoding.data_source_field_name = data_source_field_name
            encoding.data_source_field_data_type = data_source_field_data_type
            encoding.enable_inference = enable_inference
            encoding.encoder_module = encoder_module
            encoding.encoder_class = encoder_class
            encoding.encoder_params = encoder_params
            encoding.encoder_field_name = encoder_field_name
            encoding.encoder_field_data_type = encoder_field_data_type

            self.accept()

        self.close()

    def buttonCancel_click(self, event):
        self.reject()
        self.close()
