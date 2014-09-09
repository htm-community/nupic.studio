from PyQt4 import QtGui, QtCore

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

	#region Constructor

	def __init__(self, parentNode, name, type):
		"""
		Initializes a new instance of this class.
		"""

		#region Instance fields

		self.parentNode = parentNode
		"""A higher region in hierarchy which this region will feed-forward it. This field must be ignored in XML serialization because it causes circular reference error."""

		self.children = []
		"""All lower regions/sensors in hierarchy which this region will receive feed-forward input."""

		self.name = name
		"""The name of the Node."""

		self.type = type
		"""Type of the node (Region or Sensor)"""

		self.width = 64
		"""Width determines the number of columns in the X axis"""

		self.height = 64
		"""Height determines the number of columns in the Y axis"""

		self._output = []
		"""An array representing the current output from this node."""

		#region 2d-tree properties (node tree form)

		self.tree2d_x = 0.
		self.tree2d_y = 0.
		self.tree2d_polygon = QtGui.QPolygon()

		#endregion

		#region 3d-tree properties (simulation form)

		self.tree3d_x = 0
		self.tree3d_y = 0
		self.tree3d_z = 0

		#endregion

		#endregion

	#endregion

	#region Methods

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

	def addChild(self, node):
		"""
		Add a new child to this node.
		"""

		self.children.append(node)

	def delete(self):
		"""
		Delete this node and its child nodes from tree.
		"""

		# If this region is parent of lower regions/sensors in the hierarchy then delete their nodes.
		for child in self.children:
			del child

		# Delete this node from parent's children.
		self.parentNode.children.remove(self)

	#endregion

