from PyQt5 import QtGui, QtCore, QtWidgets

class NodeType:
    """
    Types of nodes in the hierarchy.
    """

    region = 1
    sensor = 2

class Node:
    """
    Node that represents region/sensors and their params.
    """

    def __init__(self, name, type):
        """
        Initializes a new instance of this class.
        """

        # The name of the Node.
        self.name = name

        # Type of the node (Region or Sensor).
        self.type = type

        # Width determines the number of columns in the X axis.
        self.width = 64

        # Height determines the number of columns in the Y axis.
        self.height = 64

        # An array representing the current output from this node.
        self._output = []

        self.tree2d_x = 0.
        self.tree2d_y = 0.
        self.tree2d_polygon = QtGui.QPolygon()

        self.tree3d_pos = (0, 0, 0)

    def initialize(self):
        """
        Initialize this node.
        """

        pass

    def nextStep(self):
        """
        Perfoms actions related to time step progression.
        """

        pass

    def getOutput(self):
        """
        Get output from this node.
        """

        return self._output
