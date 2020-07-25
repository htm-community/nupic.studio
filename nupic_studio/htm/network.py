import os
import collections
import json
from nupic_studio.htm.node import NodeType
from nupic_studio.htm.link import Link
from nupic_studio.ui import Global


class Network:
    """
    The mains class for represent a HTM network composed by nodes and the links among them.
    """

    def __init__(self):
        """
        Initializes a new instance of this class.
        """

        # All regions/sensors in hierarchy which compose this network.
        self.nodes = []

        # All links among all regions/sensors in hierarchy.
        self.links = []

        # Phases stores the processing order of one or more nodes.
        # For example, in the Phase #0 all sensors should be processed.
        # In turn, in the phase #1 all regions that are fed by the processed nodes in the previous phase also are processed.
        # The last phase is the phase where top nodes (that do not feed nothing but only receive inputs) are processed.
        self.phases = []

        # Statistics
        self.stats_precision_rate = 0.0

    def initialize(self):
        """
        Initialize this network.
        """

        # Initialize nodes using phases order
        for nodes in self.phases:
            for node in nodes:
                initialized = node.initialize()
                if not initialized:
                    return False

        return True

    def nextStep(self):
        """
        Perfoms actions related to time step progression.
        """

        # Process nodes using phases order
        for nodes in self.phases:
            for node in nodes:
                node.nextStep()

    def preparePhases(self):
        """
        Prepare phases analysing links between nodes.
        """
        self.phases = []

        # First put all sensors as non allocated nodes
        non_allocated_nodes = [node for node in self.nodes if node.type == NodeType.SENSOR]

        # Now find the regions that these sensors feed and process them recursively
        self.processPhase(non_allocated_nodes)

    def processPhase(self, non_allocated_nodes):

        # Check what nodes in the temporary list could be allocated into next phase
        # Only allocate a node to the next phase if this node not receives inputs of other non allocated node
        # if the node depends of other nodes, the latter ones has priority to be allocated into next phase
        phase_nodes = []
        for node in non_allocated_nodes:
            can_allocate = True
            for link in self.links:
                if link.in_node == node and link.out_node in non_allocated_nodes:
                    can_allocate = False
                    break
            if can_allocate:
                phase_nodes.append(node)
        self.phases.append(phase_nodes)

        # Remove allocated nodes from non allocated list
        for node in phase_nodes:
            if node in non_allocated_nodes:
                non_allocated_nodes.remove(node)

        # Add higher regions of the phase nodes into non allocated nodes list
        non_allocated_nodes = [link.in_node
                               for link in self.links
                               for node in phase_nodes
                               if link.out_node == node and not link.in_node in non_allocated_nodes]

        # Process recursively the remaining nodes
        if len(non_allocated_nodes) > 0:
            self.processPhase(non_allocated_nodes)

    def calculateStatistics(self):
        """
        Calculate statistics after an iteration.
        """

        # The network prediction precision is the average between all nodes precision
        precision_rate = 0.0
        nodes_count = 0
        for nodes in self.phases:
            for node in nodes:
                node.calculateStatistics()
                precision_rate += node.stats_precision_rate
                nodes_count += 1
        self.stats_precision_rate = precision_rate / nodes_count

    def addFeederNode(self, feeder_node, fed_node):
        """
        Delete a node from hierarchy.
        """

        # Link the first node to the target node which it receive its output
        link = Link()
        link.out_node = feeder_node
        link.in_node = fed_node

        # Add the node and the link to the network
        self.nodes.append(feeder_node)
        self.links.append(link)

        self.preparePhases()

    def deleteFeederNode(self, node):
        """
        Delete a node from hierarchy.
        """

        # Delete first all nodes under the node
        for feeder in self.getFeederNodes(node):
            self.deleteFeederNode(feeder)

        # Remove all links involving this node
        for link in self.links:
            if link.out_node == node or link.in_node == node:
                self.links.remove(link)

        # Delete the node
        self.nodes.remove(node)
        del node

        self.preparePhases()

    def getFeederNodes(self, node):
        """
        Delete a node from hierarchy.
        """

        # Get all nodes that feed the specified node
        feeders = [link.out_node
                   for link in self.links
                   if link.in_node == node]

        return feeders

    def getFedNodes(self, node):
        """
        Delete a node from hierarchy.
        """

        # Get all nodes that feed the specified node
        feds = [link.in_node
                for link in self.links
                if link.out_node == node]

        return feds

    def getSourceCode(self):
        """
        Generate the source code of this network to help users to quickly integrate
        it into their applications using the NuPIC Network API.
        """

        code = ""

        # Generate instructions
        code += "###\n" \
                "The code below is automatically generated by NuPIC Studio and aims to help you to quickly integrate\n" \
                "this HTM network into your application using the NuPIC Network API.\n" \
                "For use this code, just create a new Python file and copy/paste these lines into it. Run it and voila!\n" \
                "###\n" \
                "\n"

        # Generate 'import's
        code += "import json\n" \
                "import copy\n" \
                "from nupic.algorithms.anomaly import computeRawAnomalyScore\n" \
                "from nupic.data.file_record_stream import FileRecordStream\n" \
                "from nupic.engine import Network\n" \
                "from nupic.encoders import MultiEncoder\n" \
                "\n"

        # Generate 'network' creation
        code += "def createNetwork():\n" \
                "\t###\n" \
                "\tCreate the Network instance.\n" \
                "\t###\n" \
                "\n" \
                "\tnetwork = Network()\n" \
                "\n"

        # Generate 'nodes'
        for nodes in reversed(self.phases):
            for node in nodes:
                if node.type == NodeType.REGION:

                    # Generate the spatial process params
                    sp_params = "{ " \
                                "'spatialImp': 'py', " \
                                "'columnCount': " + str(node.width * node.height) + ", " \
                                "'inputWidth': " + str(node.getInputSize()) + ", " \
                                "'potentialRadius': " + str(node.potential_radius) + ", " \
                                "'potentialPct': " + str(node.potential_pct) + ", " \
                                "'globalInhibition': " + str(int(node.global_inhibition)) + ", " \
                                "'localAreaDensity': " + str(node.local_area_density) + ", " \
                                "'numActiveColumnsPerInhArea': " + str(node.num_active_columns_per_inh_area) + ", " \
                                "'stimulusThreshold': " + str(node.stimulus_threshold) + ", " \
                                "'synPermInactiveDec': " + str(node.proximal_syn_perm_decrement) + ", " \
                                "'synPermActiveInc': " + str(node.proximal_syn_perm_increment) + ", " \
                                "'synPermConnected': " + str(node.proximal_syn_connected_perm) + ", " \
                                "'minPctOverlapDutyCycle': " + str(node.min_pct_overlap_duty_cycle) + ", " \
                                "'minPctActiveDutyCycle': " + str(node.min_pct_active_duty_cycle) + ", " \
                                "'dutyCyclePeriod': " + str(node.duty_cycle_period) + ", " \
                                "'maxBoost': " + str(node.max_boost) + ", " \
                                "'seed': " + str(node.sp_seed) + ", " \
                                "'spVerbosity': 0" \
                                " }"

                    # Generate the temporal process params
                    tp_params = "{ " \
                                "'temporalImp': 'py', " \
                                "'columnCount': " + str(node.width * node.height) + ", " \
                                "'inputWidth': " + str(node.getInputSize()) + ", " \
                                "'cellsPerColumn': " + str(node.cells_per_column) + ", " \
                                "'initialPerm': " + str(node.distal_syn_initial_perm) + ", " \
                                "'connectedPerm': " + str(node.distal_syn_connected_perm) + ", " \
                                "'minThreshold': " + str(node.min_threshold) + ", " \
                                "'newSynapseCount': " + str(node.max_new_synapses) + ", " \
                                "'permanenceInc': " + str(node.distal_syn_perm_increment) + ", " \
                                "'permanenceDec': " + str(node.distal_syn_perm_decrement) + ", " \
                                "'activationThreshold': " + str(node.activation_threshold) + ", " \
                                "'seed': " + str(node.tp_seed)+ "" \
                                " }"

                    code += "\t# Create '" + node.name + "' region\n" \
                            "\tcreateRegion(network=network, name='" + node.name + "', spParams=" + sp_params + ", tpParams=" + tp_params + ")\n"

                elif node.type == NodeType.SENSOR:

                    # Generate the sensor params
                    sensor_params = "{ " \
                                    "'verbosity': 0" \
                                    " }"

                    # If file name provided is a relative path, use project file path
                    data_source = ""
                    if node.file_name != "":
                        if os.path.dirname(node.file_name) == '':
                            data_source = os.path.dirname(Global.project.file_name) + '/' + node.file_name
                        else:
                            data_source = node.file_name

                    # Generate the encodings params
                    encodings_params = ""
                    for encoding in node.encodings:
                        name = encoding.encoder_field_name.split('.')[0]
                        params = encoding.encoder_params

                        encodings_params = "'" + name + "': { " \
                                           "'name': '" + name + "', " \
                                           "'fieldname': '" + encoding.data_source_field_name + "', "

                        for param_name in params:
                            param_value = params[param_name]
                            if param_value == "true":
                                param_value = 'True'
                            elif param_value == "false":
                                param_value = 'False'

                            encodings_params += "'" + param_name + "': " + str(param_value) + ", "

                        encodings_params += "'type': '" + encoding.encoder_class + "'" \
                                           " }, "

                    # Generate 'sensor'
                    code += "\t# Create '" + node.name + "' sensor\n" \
                            "\tcreateSensor(network=network, name='" + node.name + "', params=" + sensor_params + ", dataFile='" + data_source + "', encodings={ " + encodings_params + " })\n"

                for fed in self.getFedNodes(node):
                    if node.type == NodeType.REGION:

                        # Generate link between this region and the fed region
                        code += "\tlinkRegionToRegion(network=network, outName='" + node.name + "', inName='" + fed.name + "')\n"

                    elif node.type == NodeType.SENSOR:

                        # Generate link between this sensor and the fed region
                        code += "\tlinkSensorToRegion(network=network, outName='" + node.name + "', inName='" + fed.name + "')\n"

                code += "\n"

        code += "\treturn network\n" \
                "\n"

        # Generate function for 'region' creation
        code += "def createRegion(network, name, spParams, tpParams):\n" \
                "\t###\n" \
                "\tCreate a region given SP and TP parameters.\n" \
                "\t###\n" \
                "\n" \
                "\t# Create spatial node\n" \
                "\tspNode = network.addRegion(name='sp' + name, nodeType='py.SPRegion', nodeParams=json.dumps(spParams)).getSelf()\n" \
                "\tspNode.learningMode = True\n" \
                "\tspNode.anomalyMode = False\n" \
                "\n" \
                "\t# Create temporal node\n" \
                "\ttpNode = network.addRegion(name='tp' + name, nodeType='py.TPRegion', nodeParams=json.dumps(tpParams)).getSelf()\n" \
                "\ttpNode.learningMode = True\n" \
                "\ttpNode.inferenceMode = True\n" \
                "\ttpNode.topDownMode = True\n" \
                "\ttpNode.anomalyMode = True\n" \
                "\n" \
                "\t# Create link betwen SP and TP of the same region\n" \
                "\tnetwork.link(srcName='sp' + name, destName='tp' + name, linkType='UniformLink', linkParams='')\n" \
                "\tnetwork.link(srcName='tp' + name, destName='sp' + name, linkType='UniformLink', linkParams='', srcOutput='topDownOut', destInput='topDownIn')\n" \
                "\n"

        # Generate function for 'sensor' creation
        code += "def createSensor(network, name, params, dataFile, encodings):\n" \
                "\t###\n" \
                "\tCreate a sensor given its parameters.\n" \
                "\t###\n" \
                "\n" \
                "\t# Create database given file name\n" \
                "\tdataSource = FileRecordStream(streamID=dataFile)\n" \
                "\tdataSource.setAutoRewind(True)\n" \
                "\n" \
                "\t# Create multi-encoder to handle all sub-encoders\n" \
                "\tencoder = MultiEncoder()\n" \
                "\tencoder.addMultipleEncoders(fieldEncodings=encodings)\n" \
                "\n" \
                "\t# Create sensor node\n" \
                "\tsensor = network.addRegion(name='sensor' + name, nodeType='py.RecordSensor', nodeParams=json.dumps(params)).getSelf()\n" \
                "\tsensor.dataSource = dataSource\n" \
                "\tsensor.encoder = encoder\n" \
                "\n"

        # Generate function for link between regions function
        code += "def linkRegionToRegion(network, outName, inName):\n" \
                "\t###\n" \
                "\tCreate links between a region and another higher one in the hierarchy.\n" \
                "\t###\n" \
                "\n" \
                "\t# Create link between TP from first region and SP of second region\n" \
                "\tnetwork.link(srcName='tp' + outName, destName='sp' + inName, linkType='UniformLink', linkParams='')\n" \
                "\n"

        # Generate function for link between sensor and region
        code += "def linkSensorToRegion(network, outName, inName):\n" \
                "\t###\n" \
                "\tCreate links between sensor and region in the hierarchy.\n" \
                "\t###\n" \
                "\n" \
                "\t# Create link between Sensor and SP of the region\n" \
                "\tnetwork.link(srcName='sensor' + outName, destName='sp' + inName, linkType='UniformLink', linkParams='')\n" \
                "\tnetwork.link(srcName='sensor' + outName, destName='sp' + inName, linkType='UniformLink', linkParams='', srcOutput='resetOut', destInput='resetIn')\n" \
                "\tnetwork.link(srcName='sp' + inName, destName='sensor' + outName, linkType='UniformLink', linkParams='', srcOutput='spatialTopDownOut', destInput='spatialTopDownIn')\n" \
                "\tnetwork.link(srcName='sp' + inName, destName='sensor' + outName, linkType='UniformLink', linkParams='', srcOutput='temporalTopDownOut', destInput='temporalTopDownIn')\n" \
                "\n"

        # Generate 'network' runing
        code += "def runNetwork(network, numIterations):\n" \
                "\t###\n" \
                "\tRun the network up to n iterations.\n" \
                "\t###\n" \
                "\n"

        # Generate 'network' initialization
        code += "\tnetwork.initialize()\n" \
                "\n"

        # Generate list with sensors and regions that are fed by them
        code += "\t# Only encodings with 'EnableInference' turned 'ON' will be printed\n" \
                "\tlinks = []\n"
        for node in self.nodes:
            if node.type == NodeType.SENSOR:
                sensor_name = node.name
                region_name = self.getFedNodes(node)[0].name

                # Add to list only those encodings with inference enabled
                encodings = "["
                for idx in range(len(node.encodings)):
                    encoding = node.encodings[idx]
                    if encoding.enable_inference:
                        encodings += "['" + encoding.encoder_field_name + "', " + str(idx) + "], "
                encodings += "]"

                code += "\tlinks.append({ 'sensorName': '" + sensor_name + "', 'regionName': '" + region_name + "', 'encodings': " + encodings + ", 'prevPredictedColumns': [] })\n"
        code += "\n"

        # Generate 'network' iteration
        code += "\t# Run the network showing current values from sensors and their anomaly scores\n" \
                "\tprintRow('Iter', 'Sensor', 'Encoding', 'Current', 'Anomaly Score')\n" \
                "\tfor i in range(numIterations):\n" \
                "\t\tnetwork.run(1)\n" \
                "\n"

        # Generate iteration rows
        code += "\t\tfor link in links:\n" \
                "\t\t\tsensorName = link['sensorName']\n" \
                "\t\t\tregionName = link['regionName']\n" \
                "\t\t\tencodings = link['encodings']\n" \
                "\t\t\tprevPredictedColumns = link['prevPredictedColumns']\n" \
                "\n" \
                "\t\t\tsensorNode = network.regions['sensor' + sensorName]\n" \
                "\t\t\tspNode = network.regions['sp' + regionName]\n" \
                "\t\t\ttpNode = network.regions['tp' + regionName]\n" \
                "\n" \
                "\t\t\t# The anomaly score is relation of active columns over previous predicted columns\n" \
                "\t\t\tactiveColumns = spNode.getOutputData('bottomUpOut').nonzero()[0]\n" \
                "\t\t\tanomalyScore = computeRawAnomalyScore(activeColumns, prevPredictedColumns)\n" \
                "\n" \
                "\t\t\tfor encoding in encodings:\n" \
                "\t\t\t\tencodingFieldName = encoding[0]\n" \
                "\t\t\t\tencodingFieldIdx = encoding[1]\n" \
                "\n" \
                "\t\t\t\t# Print the anomaly score along with the iteration number and current value of this encoding.\n" \
                "\t\t\t\tcurrValue = sensorNode.getOutputData('sourceOut')[encodingFieldIdx]\n" \
                "\t\t\t\tprintRow(i, sensorName, encodingFieldName, currValue, anomalyScore)\n" \
                "\n" \
                "\t\t\t# Store the predicted columns for the next iteration\n" \
                "\t\t\tpredictedColumns = tpNode.getOutputData('topDownOut').nonzero()[0]\n" \
                "\t\t\tlink['prevPredictedColumns'] = copy.deepcopy(predictedColumns)\n" \
                "\n" \
                "def printRow(iter, sensorName, encodingFieldName, currValue, anomalyScore):\n" \
                "\t###\n" \
                "\tPrint a row with fixed-length fields to default output.\n" \
                "\t###\n" \
                "\n" \
                "\titer = str(iter).rjust(10) + ' '\n" \
                "\tsensorName = str(sensorName).ljust(20) + ' '\n" \
                "\tencodingFieldName = str(encodingFieldName).ljust(25) + ' '\n" \
                "\tcurrValue = str(currValue).rjust(15) + ' '\n" \
                "\tanomalyScore = str(anomalyScore).ljust(40)\n" \
                "\tprint iter, sensorName, encodingFieldName, currValue, anomalyScore\n" \
                "\n"

        # Generate 'main' method
        code += "if __name__ == '__main__':\n" \
                "\tnetwork = createNetwork()\n" \
                "\n" \
                "\tnumIterations = input('Type the number of iterations: ')\n" \
                "\trunNetwork(network, numIterations)\n"

        # Adjust special characters
        code = code.replace("\t", "    ")
        code = code.replace("###", "\"\"\"")

        return code
