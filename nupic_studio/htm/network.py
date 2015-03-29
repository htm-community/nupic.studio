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

  #region Constructor

  def __init__(self):
    """
    Initializes a new instance of this class.
    """

    #region Instance fields

    self.nodes = []
    """All regions/sensors in hierarchy which compose this network."""

    self.links = []
    """All links among all regions/sensors in hierarchy."""

    self.phases = []
    """Phases stores the processing order of one or more nodes.
    For example, in the Phase #0 all sensors should be processed.
    In turn, in the phase #1 all regions that are fed by the processed nodes in the previous phase also are processed.
    The last phase is the phase where top nodes (that do not feed nothing but only receive inputs) are processed."""

    #endregion

    #region Statistics properties

    self.statsPrecisionRate = 0.

    #endregion

  #endregion

  #region Methods

  def initialize(self):
    """
    Initialize this network.
    """

    # Initialize nodes using phases order
    for phaseNodes in self.phases:
      for node in phaseNodes:
        initialized = node.initialize()
        if not initialized:
          return

    return True

  def nextStep(self):
    """
    Perfoms actions related to time step progression.
    """

    # Process nodes using phases order
    for phaseNodes in self.phases:
      for node in phaseNodes:
        node.nextStep()

  def preparePhases(self):
    """
    Prepare phases analysing links between nodes.
    """

    self.phases = []

    # First put all sensors as non allocated nodes
    nonAllocatedNodes = []
    for node in self.nodes:
      if node.type == NodeType.sensor:
        nonAllocatedNodes.append(node)

    # Now find the regions that these sensors feed and process them recursively
    self.__processPhase(nonAllocatedNodes)

  def __processPhase(self, nonAllocatedNodes):

    # Check what nodes in the temporary list could be allocated into next phase
    # Only allocate a node to the next phase if this node not receives inputs of other non allocated node
    # if the node depends of other nodes, the latter ones has priority to be allocated into next phase
    phaseNodes = []
    for node in nonAllocatedNodes:
      canAllocate = True
      for link in self.links:
        if link.inNode == node and link.outNode in nonAllocatedNodes:
          canAllocate = False
          break
      if canAllocate:
        phaseNodes.append(node)
    self.phases.append(phaseNodes)

    # Remove allocated nodes from non allocated list
    for node in phaseNodes:
      if node in nonAllocatedNodes:
        nonAllocatedNodes.remove(node)

    # Add higher regions of the phase nodes into non allocated nodes list
    for node in phaseNodes:
      for link in self.links:
        if link.outNode == node and not link.inNode in nonAllocatedNodes:
          nonAllocatedNodes.append(link.inNode)

    # Process recursively the remaining nodes
    if len(nonAllocatedNodes) > 0:
      self.__processPhase(nonAllocatedNodes)

  def calculateStatistics(self):
    """
    Calculate statistics after an iteration.
    """

    # The network prediction precision is the average between all nodes precision
    precisionRate = 0.
    numNodes = 0
    for phaseNodes in self.phases:
      for node in phaseNodes:
        node.calculateStatistics()
        precisionRate += node.statsPrecisionRate
        numNodes += 1
    self.statsPrecisionRate = precisionRate / numNodes

  def addFeederNode(self, feederNode, fedNode):
    """
    Delete a node from hierarchy.
    """

    # Link the first node to the target node which it receive its output
    link = Link()
    link.outNode = feederNode
    link.inNode = fedNode

    # Add the node and the link to the network
    self.nodes.append(feederNode)
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
      if link.outNode == node or link.inNode == node:
        self.links.remove(link)

    # Delete the node
    del node

    self.preparePhases()

  def getFeederNodes(self, node):
    """
    Delete a node from hierarchy.
    """

    # Get all nodes that feed the specified node
    feeders = []
    for link in self.links:
      if link.inNode == node:
        feeders.append(link.outNode)

    return feeders

  def getFedNodes(self, node):
    """
    Delete a node from hierarchy.
    """

    # Get all nodes that feed the specified node
    feds = []
    for link in self.links:
      if link.outNode == node:
        feds.append(link.inNode)

    return feds

  def getSourceCode(self):
    """
    Generate the source code of this network to help users to quickly integrate
    it into their applications using the NuPIC Network API.
    """

    code = ""

    # Generate instructions
    code += "'''\n"
    code += "The code below is automatically generated by NuPIC Studio and aims to help you to quickly integrate\n"
    code += "this HTM network into your application using the NuPIC Network API.\n"
    code += "For use this code, just create a new Python file and copy/paste these lines into it. Run it and voila!\n"
    code += "'''\n"
    code += "\n"

    # Generate 'import's
    code += "import json\n"
    code += "import copy\n"
    code += "from nupic.algorithms.anomaly import computeRawAnomalyScore\n"
    code += "from nupic.data.file_record_stream import FileRecordStream\n"
    code += "from nupic.engine import Network\n"
    code += "from nupic.encoders import MultiEncoder\n"
    code += "\n"

    # Generate 'network' creation
    code += "def createNetwork():\n"
    code += "\t'''\n"
    code += "\tCreate the Network instance.\n"
    code += "\t'''\n"
    code += "\n"
    code += "\tnetwork = Network()\n"
    code += "\n"

    # Generate 'nodes'
    for phaseNodes in reversed(self.phases):
      for node in phaseNodes:
        if node.type == NodeType.region:

          # Generate the spatial process params
          spParams = "{ "
          spParams += "\"spatialImp\": \"py\", "
          spParams += "\"columnCount\": " + str(node.width * node.height) + ", "
          spParams += "\"inputWidth\": " + str(node.getInputSize()) + ", "
          spParams += "\"potentialRadius\": " + str(node.potentialRadius) + ", "
          spParams += "\"potentialPct\": " + str(node.potentialPct) + ", "
          spParams += "\"globalInhibition\": " + str(int(node.globalInhibition)) + ", "
          spParams += "\"localAreaDensity\": " + str(node.localAreaDensity) + ", "
          spParams += "\"numActiveColumnsPerInhArea\": " + str(node.numActiveColumnsPerInhArea) + ", "
          spParams += "\"stimulusThreshold\": " + str(node.stimulusThreshold) + ", "
          spParams += "\"synPermInactiveDec\": " + str(node.proximalSynPermDecrement) + ", "
          spParams += "\"synPermActiveInc\": " + str(node.proximalSynPermIncrement) + ", "
          spParams += "\"synPermConnected\": " + str(node.proximalSynConnectedPerm) + ", "
          spParams += "\"minPctOverlapDutyCycle\": " + str(node.minPctOverlapDutyCycle) + ", "
          spParams += "\"minPctActiveDutyCycle\": " + str(node.minPctActiveDutyCycle) + ", "
          spParams += "\"dutyCyclePeriod\": " + str(node.dutyCyclePeriod) + ", "
          spParams += "\"maxBoost\": " + str(node.maxBoost) + ", "
          spParams += "\"seed\": " + str(node.spSeed) + ", "
          spParams += "\"spVerbosity\": 0"
          spParams += " }"

          # Generate the temporal process params
          tpParams = "{ "
          tpParams += "\"temporalImp\": \"py\", "
          tpParams += "\"columnCount\": " + str(node.width * node.height) + ", "
          tpParams += "\"inputWidth\": " + str(node.getInputSize()) + ", "
          tpParams += "\"cellsPerColumn\": " + str(node.numCellsPerColumn) + ", "
          #TODO: tpParams += "\"learningRadius\": " + str(node.learningRadius) + ", "
          tpParams += "\"initialPerm\": " + str(node.distalSynInitialPerm) + ", "
          tpParams += "\"connectedPerm\": " + str(node.distalSynConnectedPerm) + ", "
          tpParams += "\"minThreshold\": " + str(node.minThreshold) + ", "
          tpParams += "\"newSynapseCount\": " + str(node.maxNumNewSynapses) + ", "
          tpParams += "\"permanenceInc\": " + str(node.distalSynPermIncrement) + ", "
          tpParams += "\"permanenceDec\": " + str(node.distalSynPermDecrement) + ", "
          tpParams += "\"activationThreshold\": " + str(node.activationThreshold) + ", "
          tpParams += "\"seed\": " + str(node.tpSeed)
          tpParams += " }"

          code += "\t# Create '" + node.name + "' region\n"
          code += "\tcreateRegion(network=network, name='" + node.name + "', spParams=" + spParams + ", tpParams=" + tpParams + ")\n"

        elif node.type == NodeType.sensor:

          # Generate the sensor params
          sensorParams = "{ "
          sensorParams += "\"verbosity\": 0"
          sensorParams += " }"

          # If file name provided is a relative path, use project file path
          dataSource = ""
          if node.fileName != "":
            if os.path.dirname(node.fileName) == '':
              dataSource = os.path.dirname(Global.project.fileName) + '/' + node.fileName
            else:
              dataSource = node.fileName

          # Generate the encodings params
          encodingsParams = ""
          for encoding in node.encodings:
            name = encoding.encoderFieldName.split('.')[0]
            params = json.loads(encoding.encoderParams.replace("'", "\""), object_pairs_hook=collections.OrderedDict)

            encodingsParams = "\"" + name + "\": { "
            encodingsParams += "\"name\": \"" + name + "\", "
            encodingsParams += "\"fieldname\": \"" + encoding.dataSourceFieldName + "\", "

            for paramName in params:
              paramValue = params[paramName]
              if paramValue == "true":
                paramValue = 'True'
              elif paramValue == "false":
                paramValue = 'False'

              encodingsParams += "\"" + paramName + "\": " + str(paramValue) + ", "

            encodingsParams += "\"type\": \"" + encoding.encoderClass + "\""
            encodingsParams += " }, "

          # Generate 'sensor'
          code += "\t# Create '" + node.name + "' sensor\n"
          code += "\tcreateSensor(network=network, name='" + node.name + "', params=" + sensorParams + ", dataFile='" + dataSource + "', encodings={ " + encodingsParams + " })\n"

        for fed in self.getFedNodes(node):
          if node.type == NodeType.region:

            # Generate link between this region and the fed region
            code += "\tlinkRegionToRegion(network=network, outName='" + node.name + "', inName='" + fed.name + "')\n"

          elif node.type == NodeType.sensor:

            # Generate link between this sensor and the fed region
            code += "\tlinkSensorToRegion(network=network, outName='" + node.name + "', inName='" + fed.name + "')\n"

        code += "\n"

    code += "\treturn network\n"
    code += "\n"

    # Generate function for 'region' creation
    code += "def createRegion(network, name, spParams, tpParams):\n"
    code += "\t'''\n"
    code += "\tCreate a region given SP and TP parameters.\n"
    code += "\t'''\n"
    code += "\n"
    code += "\t# Create spatial node\n"
    code += "\tspNode = network.addRegion(name='sp' + name, nodeType='py.SPRegion', nodeParams=json.dumps(spParams)).getSelf()\n"
    code += "\tspNode.learningMode = True\n"
    code += "\tspNode.anomalyMode = False\n"
    code += "\n"
    code += "\t# Create temporal node\n"
    code += "\ttpNode = network.addRegion(name='tp' + name, nodeType='py.TPRegion', nodeParams=json.dumps(tpParams)).getSelf()\n"
    code += "\ttpNode.learningMode = True\n"
    code += "\ttpNode.inferenceMode = True\n"
    code += "\ttpNode.topDownMode = True\n"
    code += "\ttpNode.anomalyMode = True\n"
    code += "\n"
    code += "\t# Create link betwen SP and TP of the same region\n"
    code += "\tnetwork.link(srcName='sp' + name, destName='tp' + name, linkType='UniformLink', linkParams='')\n"
    code += "\tnetwork.link(srcName='tp' + name, destName='sp' + name, linkType='UniformLink', linkParams='', srcOutput='topDownOut', destInput='topDownIn')\n"
    code += "\n"

    # Generate function for 'sensor' creation
    code += "def createSensor(network, name, params, dataFile, encodings):\n"
    code += "\t'''\n"
    code += "\tCreate a sensor given its parameters.\n"
    code += "\t'''\n"
    code += "\n"
    code += "\t# Create database given file name\n"
    code += "\tdataSource = FileRecordStream(streamID=dataFile)\n"
    code += "\tdataSource.setAutoRewind(True)\n"
    code += "\n"
    code += "\t# Create multi-encoder to handle all sub-encoders\n"
    code += "\tencoder = MultiEncoder()\n"
    code += "\tencoder.addMultipleEncoders(fieldEncodings=encodings)\n"
    code += "\n"
    code += "\t# Create sensor node\n"
    code += "\tsensor = network.addRegion(name='sensor' + name, nodeType='py.RecordSensor', nodeParams=json.dumps(params)).getSelf()\n"
    code += "\tsensor.dataSource = dataSource\n"
    code += "\tsensor.encoder = encoder\n"
    code += "\n"

    # Generate function for link between regions function
    code += "def linkRegionToRegion(network, outName, inName):\n"
    code += "\t'''\n"
    code += "\tCreate links between a region and another higher one in the hierarchy.\n"
    code += "\t'''\n"
    code += "\n"
    code += "\t# Create link between TP from first region and SP of second region\n"
    code += "\tnetwork.link(srcName='tp' + outName, destName='sp' + inName, linkType='UniformLink', linkParams='')\n"
    code += "\n"

    # Generate function for link between sensor and region
    code += "def linkSensorToRegion(network, outName, inName):\n"
    code += "\t'''\n"
    code += "\tCreate links between sensor and region in the hierarchy.\n"
    code += "\t'''\n"
    code += "\n"
    code += "\t# Create link between Sensor and SP of the region\n"
    code += "\tnetwork.link(srcName='sensor' + outName, destName='sp' + inName, linkType='UniformLink', linkParams='')\n"
    code += "\tnetwork.link(srcName='sensor' + outName, destName='sp' + inName, linkType='UniformLink', linkParams='', srcOutput='resetOut', destInput='resetIn')\n"
    code += "\tnetwork.link(srcName='sp' + inName, destName='sensor' + outName, linkType='UniformLink', linkParams='', srcOutput='spatialTopDownOut', destInput='spatialTopDownIn')\n"
    code += "\tnetwork.link(srcName='sp' + inName, destName='sensor' + outName, linkType='UniformLink', linkParams='', srcOutput='temporalTopDownOut', destInput='temporalTopDownIn')\n"
    code += "\n"

    # Generate 'network' runing
    code += "def runNetwork(network, numIterations):\n"
    code += "\t'''\n"
    code += "\tRun the network up to n iterations.\n"
    code += "\t'''\n"
    code += "\n"

    # Generate 'network' initialization
    code += "\tnetwork.initialize()\n"
    code += "\n"

    # Generate list with sensors and regions that are fed by them
    code += "\t# Only encodings with 'EnableInference' turned 'ON' will be printed\n"
    code += "\tlinks = []\n"
    for node in self.nodes:
      if node.type == NodeType.sensor:
        sensorName = node.name
        regionName = self.getFedNodes(node)[0].name

        # Add to list only those encodings with inference enabled
        encodings = "["
        for encodingIdx in range(len(node.encodings)):
          encoding = node.encodings[encodingIdx]
          if encoding.enableInference:
            encodings += "['" + encoding.encoderFieldName + "', " + str(encodingIdx) + "], "
        encodings += "]"

        code += "\tlinks.append({ 'sensorName': '" + sensorName + "', 'regionName': '" + regionName + "', 'encodings': " + encodings + ", 'prevPredictedColumns': [] })\n"
    code += "\n"

    # Generate 'network' iteration
    code += "\t# Run the network showing current values from sensors and their anomaly scores\n"
    code += "\tprintRow('Iter', 'Sensor', 'Encoding', 'Current', 'Anomaly Score')\n"
    code += "\tfor i in range(numIterations):\n"
    code += "\t\tnetwork.run(1)\n"
    code += "\n"

    # Generate iteration rows
    code += "\t\tfor link in links:\n"
    code += "\t\t\tsensorName = link['sensorName']\n"
    code += "\t\t\tregionName = link['regionName']\n"
    code += "\t\t\tencodings = link['encodings']\n"
    code += "\t\t\tprevPredictedColumns = link['prevPredictedColumns']\n"
    code += "\n"
    code += "\t\t\tsensorNode = network.regions['sensor' + sensorName]\n"
    code += "\t\t\tspNode = network.regions['sp' + regionName]\n"
    code += "\t\t\ttpNode = network.regions['tp' + regionName]\n"
    code += "\n"
    code += "\t\t\t# The anomaly score is relation of active columns over previous predicted columns\n"
    code += "\t\t\tactiveColumns = spNode.getOutputData('bottomUpOut').nonzero()[0]\n"
    code += "\t\t\tanomalyScore = computeRawAnomalyScore(activeColumns, prevPredictedColumns)\n"
    code += "\n"
    code += "\t\t\tfor encoding in encodings:\n"
    code += "\t\t\t\tencodingFieldName = encoding[0]\n"
    code += "\t\t\t\tencodingFieldIdx = encoding[1]\n"
    code += "\n"
    code += "\t\t\t\t# Print the anomaly score along with the iteration number and current value of this encoding.\n"
    code += "\t\t\t\tcurrValue = sensorNode.getOutputData('sourceOut')[encodingFieldIdx]\n"
    code += "\t\t\t\tprintRow(i, sensorName, encodingFieldName, currValue, anomalyScore)\n"
    code += "\n"
    code += "\t\t\t# Store the predicted columns for the next iteration\n"
    code += "\t\t\tpredictedColumns = tpNode.getOutputData('topDownOut').nonzero()[0]\n"
    code += "\t\t\tlink['prevPredictedColumns'] = copy.deepcopy(predictedColumns)\n"
    code += "\n"
    code += "def printRow(iter, sensorName, encodingFieldName, currValue, anomalyScore):\n"
    code += "\t'''\n"
    code += "\tPrint a row with fixed-length fields to default output.\n"
    code += "\t'''\n"
    code += "\n"
    code += "\titer = str(iter).rjust(10) + ' '\n"
    code += "\tsensorName = str(sensorName).ljust(20) + ' '\n"
    code += "\tencodingFieldName = str(encodingFieldName).ljust(25) + ' '\n"
    code += "\tcurrValue = str(currValue).rjust(15) + ' '\n"
    code += "\tanomalyScore = str(anomalyScore).ljust(40)\n"
    code += "\tprint iter, sensorName, encodingFieldName, currValue, anomalyScore\n"
    code += "\n"

    # Generate 'main' method
    code += "if __name__ == '__main__':\n"
    code += "\tnetwork = createNetwork()\n"
    code += "\n"
    code += "\tnumIterations = input('Type the number of iterations: ')\n"
    code += "\trunNetwork(network, numIterations)\n"

    # Adjust special characters
    code = code.replace("\t", "  ")
    code = code.replace("\"", "[DOUBLE_QUOTE]") # Preserve double quotes before replace all single quotes to double quotes
    code = code.replace("'", "\"")
    code = code.replace("[DOUBLE_QUOTE]", "'")

    return code

  #endregion
