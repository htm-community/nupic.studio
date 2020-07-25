from PyQt5 import QtGui, QtCore, QtWidgets
from nupic_studio.htm.network import Network
from nupic_studio.htm.node import NodeType, Node
from nupic_studio.htm.node_region import Region
from nupic_studio.htm.node_sensor import Sensor, DataSourceType, PredictionsMethod
from nupic_studio.htm.encoding import Encoding
from nupic_studio.htm.link import Link

"""
Loads and saves the Elements of the .nuproj file, that contains user entries for project properties
Provides loaded elements as a structure to return.
"""


class Project:
    """
    Loads and saves the Elements of the Project file, that contains user entries for Network configuration
    Provides loaded elements as a structure to return.
    """

    def __init__(self):
        """
        Initializes a new instance of this class.
        """

        # Project file
        self.file_name = ''

        # Name of the project.
        self.name = "Untitled"

        # Author of the project.
        self.author = ""

        # Description of the project.
        self.description = ""

        # The network created for the project.
        self.network = Network()

    def new(self):
        """
        Initializes a new instance of this class.
        """

        # Initialize metadata
        self.file_name = ''
        self.name = "Untitled"
        self.author = ""
        self.description = ""

        # Create the top region
        top_region = Region("TopRegion")

        # Create the network and add top_region as its starting node
        self.network = Network()
        self.network.nodes.append(top_region)
        self.network.preparePhases()

    def open(self, file_name):
        """
        Loads the content from XML file to Project instance.
        """

        # Create the network
        self.network = Network()

        try:
            project = eval(open(file_name, 'r').read())
        except:
            QtWidgets.QMessageBox.warning(None, "Warning", "Cannot read the project file (" + file_name + ")!", QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Default, QtWidgets.QMessageBox.NoButton)
            project = {}

        self.file_name = file_name
        self.name = project['name']
        self.author = project['author']
        self.description = project['description']
        for node_dict in project['nodes']:
            node = self.readNode(node_dict)
            self.network.nodes.append(node)
        for link_dict in project['links']:
            link = self.readLink(link_dict)
            self.network.links.append(link)
        self.network.preparePhases()

    def readNode(self, node_dict):

        # Read type of node
        name = node_dict['name']
        type = node_dict['type']

        # Create a node from parameters
        node = None
        if type == 'Region':
            node = Region(name)
        elif type == 'Sensor':
            node = Sensor(name)
        node.width = node_dict['width']
        node.height = node_dict['height']

        # Read specific parameters according to node type
        if type == 'Region':
            node.enable_spatial_learning = node_dict['enable_spatial_learning']
            node.potential_radius = node_dict['potential_radius']
            node.potential_pct = node_dict['potential_pct']
            node.global_inhibition = node_dict['global_inhibition']
            node.local_area_density = node_dict['local_area_density']
            node.num_active_columns_per_inh_area = node_dict['num_active_columns_per_inh_area']
            node.stimulus_threshold = node_dict['stimulus_threshold']
            node.proximal_syn_connected_perm = node_dict['proximal_syn_connected_perm']
            node.proximal_syn_perm_increment = node_dict['proximal_syn_perm_increment']
            node.proximal_syn_perm_decrement = node_dict['proximal_syn_perm_decrement']
            node.min_pct_overlap_duty_cycle = node_dict['min_pct_overlap_duty_cycle']
            node.min_pct_active_duty_cycle = node_dict['min_pct_active_duty_cycle']
            node.duty_cycle_period = node_dict['duty_cycle_period']
            node.max_boost = node_dict['max_boost']
            node.sp_seed = node_dict['sp_seed']
            node.enable_temporal_learning = node_dict['enable_temporal_learning']
            node.cells_per_column = node_dict['cells_per_column']
            node.distal_syn_initial_perm = node_dict['distal_syn_initial_perm']
            node.distal_syn_connected_perm = node_dict['distal_syn_connected_perm']
            node.distal_syn_perm_increment = node_dict['distal_syn_perm_increment']
            node.distal_syn_perm_decrement = node_dict['distal_syn_perm_decrement']
            node.min_threshold = node_dict['min_threshold']
            node.activation_threshold = node_dict['activation_threshold']
            node.max_new_synapses = node_dict['max_new_synapses']
            node.tp_seed = node_dict['tp_seed']
        elif type == 'Sensor':
            data_source_type = node_dict['data_source_type']
            if data_source_type == "File":
                node.data_source_type = DataSourceType.FILE
                node.file_name = node_dict['file_name']
            elif data_source_type == "Database":
                node.data_source_type = DataSourceType.DATABASE
                node.database_connection_string = node_dict['database_connection_string']
                node.database_table = node_dict['database_table']
            node.predictions_method = node_dict['predictions_method']
            if node.predictions_method == PredictionsMethod.CLASSIFICATION:
                node.enable_classification_learning = node_dict['enable_classification_learning']
                node.enable_classification_inference = node_dict['enable_classification_inference']

            # If still is not end of element it's because this node has encodings
            for encoding_dict in node_dict['encodings']:
                encoding = self.readEncoding(encoding_dict)
                node.encodings.append(encoding)

        return node

    def readEncoding(self, encoding_dict):

        # Create a encoding from parameters
        encoding = Encoding()
        encoding.data_source_field_name = encoding_dict['data_source_field_name']
        encoding.data_source_field_data_type = encoding_dict['data_source_field_data_type']
        encoding.enable_inference = encoding_dict['enable_inference']
        encoding.encoder_module = encoding_dict['encoder_module']
        encoding.encoder_class = encoding_dict['encoder_class']
        encoding.encoder_params = encoding_dict['encoder_params']
        encoding.encoder_field_name = encoding_dict['encoder_field_name']
        encoding.encoder_field_data_type = encoding_dict['encoder_field_data_type']

        return encoding

    def readLink(self, link_dict):

        # Read link parameters
        out_node_name = link_dict['out_node']
        in_node_name = link_dict['in_node']

        # Find output node instance
        out_node = None
        for node in self.network.nodes:
            if node.name == out_node_name:
                out_node = node
                break

        # Find input node instance
        in_node = None
        for node in self.network.nodes:
            if node.name == in_node_name:
                in_node = node
                break

        # Create a link from parameters
        link = Link()
        link.out_node = out_node
        link.in_node = in_node

        return link

    def save(self, file_name):
        """
        Saves the content from Project instance to XML file.
        """

        self.file_name = file_name

        project = {}
        project['name'] = self.name
        project['author'] = self.author
        project['description'] = self.description
        project['nodes'] = []
        for node in self.network.nodes:
            node_dict = self.writeNode(node)
            project['nodes'].append(node_dict)
        project['links'] = []
        for link in self.network.links:
            link_dict = self.writeLink(link)
            project['links'].append(link_dict)

        open(file_name, 'w').write(str(project))

    def writeNode(self, node):
        node_dict = {}
        node_dict['name'] = node.name

        # Write specific parameters according to node type
        if node.type == NodeType.REGION:
            node_dict['type'] = 'Region'
            node_dict['width'] = str(node.width)
            node_dict['height'] = str(node.height)
            node_dict['enable_spatial_learning'] = str(node.enable_spatial_learning)
            node_dict['potential_radius'] = str(node.potential_radius)
            node_dict['potential_pct'] = str(node.potential_pct)
            node_dict['global_inhibition'] = str(node.global_inhibition)
            node_dict['local_area_density'] = str(node.local_area_density)
            node_dict['num_active_columns_per_inh_area'] = str(node.num_active_columns_per_inh_area)
            node_dict['stimulus_threshold'] = str(node.stimulus_threshold)
            node_dict['proximal_syn_connected_perm'] = str(node.proximal_syn_connected_perm)
            node_dict['proximal_syn_perm_increment'] = str(node.proximal_syn_perm_increment)
            node_dict['proximal_syn_perm_decrement'] = str(node.proximal_syn_perm_decrement)
            node_dict['min_pct_overlap_duty_cycle'] = str(node.min_pct_overlap_duty_cycle)
            node_dict['min_pct_active_duty_cycle'] = str(node.min_pct_active_duty_cycle)
            node_dict['duty_cycle_period'] = str(node.duty_cycle_period)
            node_dict['max_boost'] = str(node.max_boost)
            node_dict['sp_seed'] = str(node.sp_seed)
            node_dict['enable_temporal_learning'] = str(node.enable_temporal_learning)
            node_dict['cells_per_column'] = str(node.cells_per_column)
            node_dict['distal_syn_initial_perm'] = str(node.distal_syn_initial_perm)
            node_dict['distal_syn_connected_perm'] = str(node.distal_syn_connected_perm)
            node_dict['distal_syn_perm_increment'] = str(node.distal_syn_perm_increment)
            node_dict['distal_syn_perm_decrement'] = str(node.distal_syn_perm_decrement)
            node_dict['min_threshold'] = str(node.min_threshold)
            node_dict['activation_threshold'] = str(node.activation_threshold)
            node_dict['max_new_synapses'] = str(node.max_new_synapses)
            node_dict['tp_seed'] = str(node.tp_seed)
        elif node.type == NodeType.SENSOR:
            node_dict['type'] = 'Sensor'
            node_dict['width'] = str(node.width)
            node_dict['height'] = str(node.height)
            if node.data_source_type == DataSourceType.FILE:
                node_dict['data_source_type'] = "File"
                node_dict['file_name'] = node.file_name
            elif node.data_source_type == DataSourceType.DATABASE:
                node_dict['data_source_type'] = "Database"
                node_dict['database_connection_string'] = node.database_connection_string
                node_dict['database_table'] = node.database_table
            node_dict['predictions_method'] = node.predictions_method
            if node.predictions_method == PredictionsMethod.CLASSIFICATION:
                node_dict['enable_classification_learning'] = str(node.enable_classification_learning)
                node_dict['enable_classification_inference'] = str(node.enable_classification_inference)

            # Tranverse all encodings
            node_dict['encodings'] = []
            for encoding in node.encodings:
                encoding_dict = self.writeEncoding(encoding)
                node_dict['encodings'].append(encoding_dict)

        return node_dict

    def writeEncoding(self, encoding):
        encoding_dict = {}
        encoding_dict['data_source_field_name'] = encoding.data_source_field_name
        encoding_dict['data_source_field_data_type'] = encoding.data_source_field_data_type
        encoding_dict['enable_inference'] = str(encoding.enable_inference)
        encoding_dict['encoder_module'] = encoding.encoder_module
        encoding_dict['encoder_class'] = encoding.encoder_class
        encoding_dict['encoder_params'] = encoding.encoder_params
        encoding_dict['encoder_field_name'] = encoding.encoder_field_name
        encoding_dict['encoder_field_data_type'] = encoding.encoder_field_data_type
        return encoding_dict

    def writeLink(self, link):
        link_dict = {}
        link_dict['out_node'] = link.out_node.name
        link_dict['in_node'] = link.in_node.name
        return link_dict
