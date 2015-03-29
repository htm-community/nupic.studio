import collections
import numpy
import pyqtgraph.opengl as gl
import pyqtgraph as pg
from PyQt4 import QtGui, QtCore
from nupic_studio.htm.node import Node, NodeType
from nupic_studio.htm.segment import SegmentType
from nupic_studio.ui import Global, View
from nupic_studio.ui.simulation_legend_form import SimulationLegendForm

class SimulationForm(QtGui.QWidget):

  #region Constructor

  def __init__(self):
    """
    Initializes a new instance of this class.
    """

    QtGui.QWidget.__init__(self)

    #region Instance fields

    # Views
    self.defaultViewMenu = None
    self.selectedViewMenu = None

    # Tree
    self.topRegion = None
    self.treeWidth = 0
    self.treeHeight = 0

    # Space to skip horizontally between siblings and vertically between generations
    self.offsetHorizontalNodes = 20
    self.offsetVerticalNodes = 25

    # Horizontal space between two columns
    self.offsetColumns = 10

    # Vertical space between two cells
    self.offsetCells = 5

    # Colors
    colorGray = QtGui.QColor.fromRgb(190, 190, 190)
    colorBlue = QtGui.QColor.fromRgb(0, 0, 255)
    colorGreen = QtGui.QColor.fromRgb(50, 205, 50)
    colorLightGreen = QtGui.QColor.fromRgb(125, 255, 0)
    colorYellow = QtGui.QColor.fromRgb(255, 215, 80)
    colorRed = QtGui.QColor.fromRgb(255, 0, 0)

    # General color scheme
    self.colorInactive = colorGray
    self.colorSelected = colorBlue

    # Sensor bit color scheme
    self.colorBitActive = colorGreen
    self.colorBitPredicted = colorYellow
    self.colorBitFalselyPredicted = colorRed

    # Cell color scheme
    self.colorCellLearning = colorLightGreen
    self.colorCellActive = colorGreen
    self.colorCellPredicted = colorYellow
    self.colorCellFalselyPredicted = colorRed

    # Segment color scheme
    self.colorSegmentActive = colorGreen
    self.colorSegmentPredicted = colorYellow
    self.colorSegmentFalselyPredicted = colorRed

    # Synapse color scheme
    self.colorSynapseConnected = colorGreen
    self.colorSynapsePredicted = colorYellow
    self.colorSynapseFalselyPredicted = colorRed

    #endregion

    self.initUI()

    # Create views menus
    for view in Global.views:
      view.menu = QtGui.QAction(self)
      view.menu.setText(view.name)
      view.menu.setCheckable(True)
      view.menu.triggered.connect(self.menuView_Click)
      self.menuViews.addAction(view.menu)

      # If this is the first menu, set it as default
      if self.defaultViewMenu == None:
        self.defaultViewMenu = view.menu

    # Load default view
    self.selectView(self.defaultViewMenu)

  #endregion

  #region Methods

  def initUI(self):

    # simulationViewer
    self.simulationViewer = gl.GLViewWidget()
    self.simulationViewer.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    self.simulationViewer.customContextMenuRequested.connect(self.showContextMenu)

    # menuViewsNew
    self.menuViewsNew = QtGui.QAction(self)
    self.menuViewsNew.setText("Create new view")
    self.menuViewsNew.triggered.connect(self.menuViewsNew_Click)

    # menuViewsSave
    self.menuViewsSave = QtGui.QAction(self)
    self.menuViewsSave.setText("Save selected view")
    self.menuViewsSave.triggered.connect(self.menuViewsSave_Click)

    # menuViewsDelete
    self.menuViewsDelete = QtGui.QAction(self)
    self.menuViewsDelete.setText("Delete selected view")
    self.menuViewsDelete.triggered.connect(self.menuViewsDelete_Click)

    # menuViews
    self.menuViews = QtGui.QMenu()
    self.menuViews.addAction(self.menuViewsNew)
    self.menuViews.addAction(self.menuViewsSave)
    self.menuViews.addAction(self.menuViewsDelete)
    self.menuViews.addSeparator()
    self.menuViews.setTitle("&View")

    # menuCameraTop
    self.menuCameraTop = QtGui.QAction(self)
    self.menuCameraTop.setText("&Top")
    self.menuCameraTop.setShortcut('Ctrl+PgUp')
    self.menuCameraTop.triggered.connect(self.__updateCamera)

    # menuCameraBottom
    self.menuCameraBottom = QtGui.QAction(self)
    self.menuCameraBottom.setText("&Bottom")
    self.menuCameraBottom.setShortcut('Ctrl+PgDown')
    self.menuCameraBottom.triggered.connect(self.__updateCamera)

    # menuCameraPerspective
    self.menuCameraPerspective = QtGui.QAction(self)
    self.menuCameraPerspective.setText("&Perspective")
    self.menuCameraPerspective.setShortcut('Ctrl+End')
    self.menuCameraPerspective.triggered.connect(self.__updateCamera)

    # menuCameraDefault
    self.menuCameraDefault = QtGui.QAction(self)
    self.menuCameraDefault.setText("&Default")
    self.menuCameraDefault.setShortcut('Ctrl+Home')
    self.menuCameraDefault.triggered.connect(self.__updateCamera)

    # menuCamera
    self.menuCamera = QtGui.QMenu()
    self.menuCamera.addAction(self.menuCameraTop)
    self.menuCamera.addAction(self.menuCameraBottom)
    self.menuCamera.addAction(self.menuCameraPerspective)
    self.menuCamera.addAction(self.menuCameraDefault)
    self.menuCamera.setTitle("&Camera")

    # menuShowBitsNone
    self.menuShowBitsNone = QtGui.QAction(self)
    self.menuShowBitsNone.setText("&None")
    self.menuShowBitsNone.setCheckable(True)
    self.menuShowBitsNone.triggered.connect(self.menuShowBits_Click)

    # menuShowBitsActive
    self.menuShowBitsActive = QtGui.QAction(self)
    self.menuShowBitsActive.setText("&Active")
    self.menuShowBitsActive.setCheckable(True)
    self.menuShowBitsActive.triggered.connect(self.menuShowBits_Click)

    # menuShowBitsPredicted
    self.menuShowBitsPredicted = QtGui.QAction(self)
    self.menuShowBitsPredicted.setText("&Predicted")
    self.menuShowBitsPredicted.setCheckable(True)
    self.menuShowBitsPredicted.triggered.connect(self.menuShowBits_Click)

    # menuShowBitsFalselyPredicted
    self.menuShowBitsFalselyPredicted = QtGui.QAction(self)
    self.menuShowBitsFalselyPredicted.setText("&Falsely Predicted")
    self.menuShowBitsFalselyPredicted.setCheckable(True)
    self.menuShowBitsFalselyPredicted.triggered.connect(self.menuShowBits_Click)

    # menuShowBits
    self.menuShowBits = QtGui.QMenu()
    self.menuShowBits.addAction(self.menuShowBitsNone)
    self.menuShowBits.addAction(self.menuShowBitsActive)
    self.menuShowBits.addAction(self.menuShowBitsPredicted)
    self.menuShowBits.addAction(self.menuShowBitsFalselyPredicted)
    self.menuShowBits.setTitle("&Sensor bits")

    # menuShowCellsNone
    self.menuShowCellsNone = QtGui.QAction(self)
    self.menuShowCellsNone.setText("&None")
    self.menuShowCellsNone.setCheckable(True)
    self.menuShowCellsNone.triggered.connect(self.menuShowCells_Click)

    # menuShowCellsLearning
    self.menuShowCellsLearning = QtGui.QAction(self)
    self.menuShowCellsLearning.setText("&Learning")
    self.menuShowCellsLearning.setCheckable(True)
    self.menuShowCellsLearning.triggered.connect(self.menuShowCells_Click)

    # menuShowCellsActive
    self.menuShowCellsActive = QtGui.QAction(self)
    self.menuShowCellsActive.setText("&Active")
    self.menuShowCellsActive.setCheckable(True)
    self.menuShowCellsActive.triggered.connect(self.menuShowCells_Click)

    # menuShowCellsInactive
    self.menuShowCellsInactive = QtGui.QAction(self)
    self.menuShowCellsInactive.setText("&Inactive")
    self.menuShowCellsInactive.setCheckable(True)
    self.menuShowCellsInactive.triggered.connect(self.menuShowCells_Click)

    # menuShowCellsPredicted
    self.menuShowCellsPredicted = QtGui.QAction(self)
    self.menuShowCellsPredicted.setText("&Predicted")
    self.menuShowCellsPredicted.setCheckable(True)
    self.menuShowCellsPredicted.triggered.connect(self.menuShowCells_Click)

    # menuShowCellsFalselyPredicted
    self.menuShowCellsFalselyPredicted = QtGui.QAction(self)
    self.menuShowCellsFalselyPredicted.setText("&Falsely Predicted")
    self.menuShowCellsFalselyPredicted.setCheckable(True)
    self.menuShowCellsFalselyPredicted.triggered.connect(self.menuShowCells_Click)

    # menuShowCells
    self.menuShowCells = QtGui.QMenu()
    self.menuShowCells.addAction(self.menuShowCellsNone)
    self.menuShowCells.addAction(self.menuShowCellsLearning)
    self.menuShowCells.addAction(self.menuShowCellsActive)
    self.menuShowCells.addAction(self.menuShowCellsPredicted)
    self.menuShowCells.addAction(self.menuShowCellsFalselyPredicted)
    self.menuShowCells.addAction(self.menuShowCellsInactive)
    self.menuShowCells.setTitle("C&ells")

    # menuShowProximalSegmentsNone
    self.menuShowProximalSegmentsNone = QtGui.QAction(self)
    self.menuShowProximalSegmentsNone.setText("&None")
    self.menuShowProximalSegmentsNone.setCheckable(True)
    self.menuShowProximalSegmentsNone.triggered.connect(self.menuShowProximalSegments_Click)

    # menuShowProximalSegmentsActive
    self.menuShowProximalSegmentsActive = QtGui.QAction(self)
    self.menuShowProximalSegmentsActive.setText("&Active")
    self.menuShowProximalSegmentsActive.setCheckable(True)
    self.menuShowProximalSegmentsActive.triggered.connect(self.menuShowProximalSegments_Click)

    # menuShowProximalSegmentsPredicted
    self.menuShowProximalSegmentsPredicted = QtGui.QAction(self)
    self.menuShowProximalSegmentsPredicted.setText("&Predicted")
    self.menuShowProximalSegmentsPredicted.setCheckable(True)
    self.menuShowProximalSegmentsPredicted.triggered.connect(self.menuShowProximalSegments_Click)

    # menuShowProximalSegmentsFalselyPredicted
    self.menuShowProximalSegmentsFalselyPredicted = QtGui.QAction(self)
    self.menuShowProximalSegmentsFalselyPredicted.setText("&Falsely Predicted")
    self.menuShowProximalSegmentsFalselyPredicted.setCheckable(True)
    self.menuShowProximalSegmentsFalselyPredicted.triggered.connect(self.menuShowProximalSegments_Click)

    # menuShowProximalSegments
    self.menuShowProximalSegments = QtGui.QMenu()
    self.menuShowProximalSegments.addAction(self.menuShowProximalSegmentsNone)
    self.menuShowProximalSegments.addAction(self.menuShowProximalSegmentsActive)
    self.menuShowProximalSegments.addAction(self.menuShowProximalSegmentsPredicted)
    self.menuShowProximalSegments.addAction(self.menuShowProximalSegmentsFalselyPredicted)
    self.menuShowProximalSegments.setTitle("&Segments")

    # menuShowProximalSynapsesNone
    self.menuShowProximalSynapsesNone = QtGui.QAction(self)
    self.menuShowProximalSynapsesNone.setText("&None")
    self.menuShowProximalSynapsesNone.setCheckable(True)
    self.menuShowProximalSynapsesNone.triggered.connect(self.menuShowProximalSynapses_Click)

    # menuShowProximalSynapsesConnected
    self.menuShowProximalSynapsesConnected = QtGui.QAction(self)
    self.menuShowProximalSynapsesConnected.setText("&Connected")
    self.menuShowProximalSynapsesConnected.setCheckable(True)
    self.menuShowProximalSynapsesConnected.triggered.connect(self.menuShowProximalSynapses_Click)

    # menuShowProximalSynapsesActive
    self.menuShowProximalSynapsesActive = QtGui.QAction(self)
    self.menuShowProximalSynapsesActive.setText("&Active")
    self.menuShowProximalSynapsesActive.setCheckable(True)
    self.menuShowProximalSynapsesActive.triggered.connect(self.menuShowProximalSynapses_Click)

    # menuShowProximalSynapsesPredicted
    self.menuShowProximalSynapsesPredicted = QtGui.QAction(self)
    self.menuShowProximalSynapsesPredicted.setText("&Predicted")
    self.menuShowProximalSynapsesPredicted.setCheckable(True)
    self.menuShowProximalSynapsesPredicted.triggered.connect(self.menuShowProximalSynapses_Click)

    # menuShowProximalSynapsesFalselyPredicted
    self.menuShowProximalSynapsesFalselyPredicted = QtGui.QAction(self)
    self.menuShowProximalSynapsesFalselyPredicted.setText("&Falsely Predicted")
    self.menuShowProximalSynapsesFalselyPredicted.setCheckable(True)
    self.menuShowProximalSynapsesFalselyPredicted.triggered.connect(self.menuShowProximalSynapses_Click)

    # menuShowProximalSynapses
    self.menuShowProximalSynapses = QtGui.QMenu()
    self.menuShowProximalSynapses.addAction(self.menuShowProximalSynapsesNone)
    self.menuShowProximalSynapses.addAction(self.menuShowProximalSynapsesConnected)
    self.menuShowProximalSynapses.addAction(self.menuShowProximalSynapsesActive)
    self.menuShowProximalSynapses.addAction(self.menuShowProximalSynapsesPredicted)
    self.menuShowProximalSynapses.addAction(self.menuShowProximalSynapsesFalselyPredicted)
    self.menuShowProximalSynapses.setTitle("&Synapses")

    # menuShowProximal
    self.menuShowProximal = QtGui.QMenu()
    self.menuShowProximal.addMenu(self.menuShowProximalSegments)
    self.menuShowProximal.addMenu(self.menuShowProximalSynapses)
    self.menuShowProximal.setTitle("&Proximal")

    # menuShowDistalSegmentsNone
    self.menuShowDistalSegmentsNone = QtGui.QAction(self)
    self.menuShowDistalSegmentsNone.setText("&None")
    self.menuShowDistalSegmentsNone.setCheckable(True)
    self.menuShowDistalSegmentsNone.triggered.connect(self.menuShowDistalSegments_Click)

    # menuShowDistalSegmentsActive
    self.menuShowDistalSegmentsActive = QtGui.QAction(self)
    self.menuShowDistalSegmentsActive.setText("&Active")
    self.menuShowDistalSegmentsActive.setCheckable(True)
    self.menuShowDistalSegmentsActive.triggered.connect(self.menuShowDistalSegments_Click)

    # menuShowDistalSegments
    self.menuShowDistalSegments = QtGui.QMenu()
    self.menuShowDistalSegments.addAction(self.menuShowDistalSegmentsNone)
    self.menuShowDistalSegments.addAction(self.menuShowDistalSegmentsActive)
    self.menuShowDistalSegments.setTitle("&Segments")

    # menuShowDistalSynapsesNone
    self.menuShowDistalSynapsesNone = QtGui.QAction(self)
    self.menuShowDistalSynapsesNone.setText("&None")
    self.menuShowDistalSynapsesNone.setCheckable(True)
    self.menuShowDistalSynapsesNone.triggered.connect(self.menuShowDistalSynapses_Click)

    # menuShowDistalSynapsesConnected
    self.menuShowDistalSynapsesConnected = QtGui.QAction(self)
    self.menuShowDistalSynapsesConnected.setText("&Connected")
    self.menuShowDistalSynapsesConnected.setCheckable(True)
    self.menuShowDistalSynapsesConnected.triggered.connect(self.menuShowDistalSynapses_Click)

    # menuShowDistalSynapsesActive
    self.menuShowDistalSynapsesActive = QtGui.QAction(self)
    self.menuShowDistalSynapsesActive.setText("&Active")
    self.menuShowDistalSynapsesActive.setCheckable(True)
    self.menuShowDistalSynapsesActive.triggered.connect(self.menuShowDistalSynapses_Click)

    # menuShowDistalSynapses
    self.menuShowDistalSynapses = QtGui.QMenu()
    self.menuShowDistalSynapses.addAction(self.menuShowDistalSynapsesNone)
    self.menuShowDistalSynapses.addAction(self.menuShowDistalSynapsesConnected)
    self.menuShowDistalSynapses.addAction(self.menuShowDistalSynapsesActive)
    self.menuShowDistalSynapses.setTitle("&Synapses")

    # menuShowDistal
    self.menuShowDistal = QtGui.QMenu()
    self.menuShowDistal.addMenu(self.menuShowDistalSegments)
    self.menuShowDistal.addMenu(self.menuShowDistalSynapses)
    self.menuShowDistal.setTitle("&Distal")

    # menuShow
    self.menuShow = QtGui.QMenu()
    self.menuShow.addMenu(self.menuShowBits)
    self.menuShow.addMenu(self.menuShowCells)
    self.menuShow.addMenu(self.menuShowProximal)
    self.menuShow.addMenu(self.menuShowDistal)
    self.menuShow.setTitle("&Show")

    # menuLegend
    self.menuLegend = QtGui.QAction(self)
    self.menuLegend.setText("&Legend")
    self.menuLegend.triggered.connect(self.menuLegend_Click)

    # menuSimulation
    self.menuSimulation = QtGui.QMenu()
    self.menuSimulation.addMenu(self.menuViews)
    self.menuSimulation.addMenu(self.menuCamera)
    self.menuSimulation.addMenu(self.menuShow)
    self.menuSimulation.addAction(self.menuLegend)
    self.menuSimulation.setTitle("&Simulation")

    # layout
    layout = QtGui.QGridLayout()
    layout.addWidget(self.simulationViewer, 1, 0)
    layout.setRowStretch(1, 100)

    # SimulationForm
    self.setLayout(layout)
    self.setWindowTitle("Simulation")
    self.setWindowIcon(QtGui.QIcon(Global.appPath + '/images/logo.ico'))
    self.setMinimumWidth(400)
    self.setMinimumHeight(200)
    self.setToolTip("Left button drag: Rotates the scene around a central point.\r\nControl key + Middle button drag: Pan the scene by moving the central 'look-at' point within the plane.\r\nWheel spin: Zoom in/out.\r\nRight button: Shows menu.")

  def showContextMenu(self, pos):
    """
    Event handling right-click contextMenu
    """

    if Global.simulationInitialized:
      self.menuSimulation.exec_(self.mapToGlobal(pos))
    else:
      QtGui.QMessageBox.information(self, "Information", "Context menu available only during the simulation.")

  def __updateCamera(self, event):
    """
    Update camera position in the scene
    """

    menuClicked = self.sender()
    self.simulationViewer.setCameraPosition(distance = (self.treeHeight * 30))
    if menuClicked == self.menuCameraTop:
      self.simulationViewer.setCameraPosition(elevation = 90)
      self.simulationViewer.setCameraPosition(azimuth = 90)
    elif menuClicked == self.menuCameraBottom:
      self.simulationViewer.setCameraPosition(elevation = -90)
      self.simulationViewer.setCameraPosition(azimuth = 90)
    elif menuClicked == self.menuCameraPerspective:
      self.simulationViewer.setCameraPosition(elevation = 17)
      self.simulationViewer.setCameraPosition(azimuth = 45)
    else:
      self.simulationViewer.setCameraPosition(elevation = 17)
      self.simulationViewer.setCameraPosition(azimuth = 90)

  def clearControls(self):
    """
    Reset all controls.
    """

    # Remove all items
    while len(self.simulationViewer.items) > 0:
      self.simulationViewer.removeItem(self.simulationViewer.items[0])

    # Draw a sphere only to initialize simulation.
    # If we don't do this, viewer crashes. Probably a PYQtGraph bug
    fooMd = gl.MeshData.sphere(rows=10, cols=10)
    self.fooItem = gl.GLMeshItem(meshdata=fooMd, smooth=False, shader='shaded', glOptions='opaque')
    self.fooItem.translate(0, 0, 0)
    self.simulationViewer.addItem(self.fooItem)
    self.simulationViewer.setCameraPosition(distance = 10000)

  def initializeControls(self):
    """
    Refresh controls for each time step.
    """

    # Remove initial sphere
    self.simulationViewer.removeItem(self.fooItem)

    # Arrange the tree once to see how big it is.
    self.treeWidth = 0
    self.treeHeight = 0
    minX = 0
    minZ = 0
    minX, minZ = self.__arrangeNode(self.topRegion, minX, minZ)

    # Rearrange the tree again to center it horizontally.
    offsetX = self.topRegion.tree3d_x
    self.__centerNode(self.topRegion, offsetX)

    # Rearrange the tree again to invert it vertically.
    offsetZ = 50
    self.__invertNode(self.topRegion, offsetZ)

    # Once we have the final position of the regions, we can calculate the position of every column and cell.
    self.__calculateNodeElementsPosition(self.topRegion)

    # Draw the tree recursively from top region.
    self.__drawNode(self.topRegion, True)

    # Adjust camera
    self.__updateCamera(None)

  def refreshControls(self):
    """
    Refresh controls for each time step.
    """

    if Global.simulationInitialized:
      # Draw the tree recursively from top region.
      self.__drawNode(self.topRegion, False)

  def __centerNode(self, node, offsetX):
    """
    Rearrange the node in order to tree is in the center (0, 0, 0) of the scene.
    """

    node.tree3d_x -= offsetX
    for feeder in Global.project.network.getFeederNodes(node):
      self.__centerNode(feeder, offsetX)

  def __invertNode(self, node, offsetZ):
    """
    Rearrange the node in order to tree is inverted from top to bottom.
    """

    node.tree3d_z = offsetZ - node.tree3d_z
    for feeder in Global.project.network.getFeederNodes(node):
      self.__invertNode(feeder, offsetZ)

  def __calculateNodeElementsPosition(self, node):
    """
    Calculate the position of columns and cells of this node.
    """

    # Calculate the relative position of the first column (0, 0)
    # The purpose is we have symmetrical positions. If a node has 30 columns in X axis, then the relative X of the first column is -15 while the last is 15.
    x0 = (node.width / 2) * (-1)
    y0 = (node.height / 2) * (-1)

    # Calculate the absolute position of each column
    for y in range(node.height):
      for x in range(node.width):
        # The absolute X is calculated by multiply its relative position with offset
        xCol = node.tree3d_x + ((x0 + x) * self.offsetColumns)

        # The absolute Y is calculated by multiply its relative position with offset
        yCol = node.tree3d_y + ((y0 + y) * self.offsetColumns)

        # Calculate positions of the columns of cells if node is a region
        # or input bits if node is a sensor
        zCol = node.tree3d_z

        if node.type == NodeType.region:
          column = node.getColumn(x, y)
          column.tree3d_x = xCol
          column.tree3d_y = yCol
          column.tree3d_z = zCol

          # The proximal segment transverse all cells on this column
          column.segment.tree3d_x1 = xCol
          column.segment.tree3d_y1 = yCol
          column.segment.tree3d_z1 = zCol + ((node.numCellsPerColumn - 1) * self.offsetCells)
          column.segment.tree3d_x2 = xCol
          column.segment.tree3d_y2 = yCol
          column.segment.tree3d_z2 = zCol - self.offsetCells # Segment down towards to feeder nodes

          # Calculate the absolute position of each cell
          for z in range(len(column.cells)):
            # The absolute Z is calculated by multiply its relative position with offset
            cell = column.getCell(z)
            cell.tree3d_x = xCol
            cell.tree3d_y = yCol
            cell.tree3d_z = zCol + (z * self.offsetCells)
        else:
          bit = node.getBit(x, y)
          bit.tree3d_x = xCol
          bit.tree3d_y = yCol
          bit.tree3d_z = zCol

    # Perform the same actions for the lower nodes that feed this node
    for feeder in Global.project.network.getFeederNodes(node):
      self.__calculateNodeElementsPosition(feeder)

  def __arrangeNode(self, node, minX, minZ):
    """
    Arrange the node and the lower nodes that feed it in the allowed area.
    Set minX to indicate the right edge of our subtree.
    Set minZ to indicate the bottom edge of our subtree.
    """

    # See how big this node is.
    width = node.width * self.offsetColumns
    height = node.height
    if node.type == NodeType.region:
      depth = node.numCellsPerColumn * self.offsetCells
    else:
      depth = self.offsetCells

    # Recursively arrange the lower nodes that feed this node,
    # allowing room for this node.
    x = minX
    biggestMinZ = minZ + depth
    subtreeMinZ = minZ + depth + self.offsetVerticalNodes
    numFeeders = 0
    for feeder in Global.project.network.getFeederNodes(node):
      # Arrange this feeder's subtree.
      feederMinZ = subtreeMinZ
      x, feederMinZ = self.__arrangeNode(feeder, x, feederMinZ)

      # See if this increases the biggest minZ value.
      if biggestMinZ < feederMinZ:
        biggestMinZ = feederMinZ

      # Allow room before the next sibling.
      x += self.offsetHorizontalNodes

      numFeeders += 1

    # Remove the spacing after the last feeder.
    if numFeeders > 0:
      x -= self.offsetHorizontalNodes

    # See if this node is wider than the subtree under it.
    subtreeWidth = x - minX
    if width > subtreeWidth:
      # Center the subtree under this node.
      # Make the lower nodes that feed this node rearrange themselves
      # moved to center their subtrees.
      x = minX + (width - subtreeWidth) / 2
      for feeder in Global.project.network.getFeederNodes(node):
        # Arrange this feeder's subtree.
        x, subtreeMinZ = self.__arrangeNode(feeder, x, subtreeMinZ)

        # Allow room before the next sibling.
        x += self.offsetHorizontalNodes

      # The subtree's width is this node's width.
      subtreeWidth = width

    # Set this node's center position.
    node.tree3d_x = minX + (subtreeWidth / 2)
    node.tree3d_y = 0
    node.tree3d_z = minZ + (depth / 2)

    # Increase minX to allow room for the subtree before returning.
    minX += subtreeWidth

    if subtreeWidth > self.treeWidth:
      self.treeWidth = subtreeWidth

    if height > self.treeHeight:
      self.treeHeight = height

    # Set the return value for minZ.
    minZ = biggestMinZ

    return minX, minZ

  def __drawNode(self, node, initialize):
    """
    Draw the nodes for the subtree rooted at this node.
    """

    # Recursively make the node draw its feeders.
    for feeder in Global.project.network.getFeederNodes(node):
      self.__drawNode(feeder, initialize)

    # Draw a column of cells if node is a region
    # or an input bit if node is a sensor
    if node.type == NodeType.region:
      for column in node.columns:
        if initialize:
          for cell in column.cells:
            cell.tree3d_initialized = False
        self.__drawColumn(column)
    else:
      for bit in node.bits:
        if initialize:
          bit.tree3d_initialized = False
        self.__drawBit(bit)

  def __drawBit(self, bit):

    # Update properties according to state
    isVisible = True
    if self.menuShowBitsNone.isChecked():
      isVisible = False
    elif bit.isFalselyPredicted.atGivenStepAgo(Global.selStep) and self.menuShowBitsFalselyPredicted.isChecked():
      color = self.colorBitFalselyPredicted
    elif bit.isPredicted.atGivenStepAgo(Global.selStep) and self.menuShowBitsPredicted.isChecked():
      color = self.colorBitPredicted
    elif bit.isActive.atGivenStepAgo(Global.selStep) and self.menuShowBitsActive.isChecked():
      color = self.colorBitActive
    else:
      color = self.colorInactive

    if isVisible:
      # Draw the input bit
      if not bit.tree3d_initialized:
        # TODO: Use cube instead of sphere
        bitMd = gl.MeshData.sphere(rows=2, cols=4)
        bit.tree3d_item = gl.GLMeshItem(meshdata=bitMd, shader='shaded', smooth=False, glOptions='opaque')
        bit.tree3d_item.translate(bit.tree3d_x, bit.tree3d_y, bit.tree3d_z)
        bit.tree3d_initialized = True
        self.simulationViewer.addItem(bit.tree3d_item)

      # Update the color
      if bit.tree3d_selected:
        color = self.colorSelected
      bit.tree3d_item.setColor(color)

    if bit.tree3d_item != None:
      bit.tree3d_item.setVisible(isVisible)

  def __drawColumn(self, column):

    # Update proximal segment
    self.__drawSegment(column.segment)
    for cell in column.cells:
      self.__drawCell(cell)

  def __drawCell(self, cell):

    # Update properties according to state
    isVisible = True
    if self.menuShowCellsNone.isChecked():
      isVisible = False
    elif cell.isFalselyPredicted.atGivenStepAgo(Global.selStep) and self.menuShowCellsFalselyPredicted.isChecked():
      color = self.colorCellFalselyPredicted
    elif cell.isPredicted.atGivenStepAgo(Global.selStep) and self.menuShowCellsPredicted.isChecked():
      color = self.colorCellPredicted
    elif cell.isLearning.atGivenStepAgo(Global.selStep) and self.menuShowCellsLearning.isChecked():
      color = self.colorCellLearning
    elif cell.isActive.atGivenStepAgo(Global.selStep) and self.menuShowCellsActive.isChecked():
      color = self.colorCellActive
    elif self.menuShowCellsInactive.isChecked():
      color = self.colorInactive
    else:
      isVisible = False

    if isVisible:
      # Draw the cell
      if not cell.tree3d_initialized:
        cellMd = gl.MeshData.sphere(rows=10, cols=10)
        cell.tree3d_item = gl.GLMeshItem(meshdata=cellMd, shader='shaded', smooth=False, glOptions='opaque')
        cell.tree3d_item.translate(cell.tree3d_x, cell.tree3d_y, cell.tree3d_z)
        cell.tree3d_initialized = True
        self.simulationViewer.addItem(cell.tree3d_item)

      # Update the color
      if cell.tree3d_selected:
        color = self.colorSelected
      cell.tree3d_item.setColor(color)

    if cell.tree3d_item != None:
      cell.tree3d_item.setVisible(isVisible)

    # Draw/update all distal segments
    for segment in cell.segments:
      segment.tree3d_x1 = cell.tree3d_x
      segment.tree3d_y1 = cell.tree3d_y
      segment.tree3d_z1 = cell.tree3d_z
      segment.tree3d_x2, segment.tree3d_y2, segment.tree3d_z2 = self.__calculateSegmentEndPos(segment, segment.tree3d_x1, segment.tree3d_y1, segment.tree3d_z1)
      self.__drawSegment(segment)

  def __calculateSegmentEndPos(self, segment, xSeg1, ySeg1, zSeg1):
    """
    Calculates an average position of the segment's end through their synapses' end positions.
    """

    sumK = 0.
    numXBelow = 0
    numXAbove = 0
    for synapse in segment.synapses:
      xSyn = synapse.inputElem.tree3d_x
      ySyn = synapse.inputElem.tree3d_y

      # Calculate 'k' (slope) of the straight line representing this synapse
      deltaY = ySyn - ySeg1
      deltaX = xSyn - xSeg1
      if deltaX != 0:
        k = float(deltaY / deltaX)
      else:
        k = 3
      sumK += k

      if xSyn >= xSeg1:
        numXAbove += 1
      else:
        numXBelow += 1

    # Calculate direction of the straight line with base on the number of synapses X's below or above the segment X's
    if numXAbove >= numXBelow:
      direction = 1
    else:
      direction = -1

    # Calculate the 'k' (slope) of the new straight line representing this segment
    # It is an average value among the 'k' of the synapses
    k = 0
    if len(segment.synapses) > 0:
      k = int(sumK / len(segment.synapses))

    # Find the 'b' of the straight line equation using 'k' and segment's start position:
    #   y = ax + b (where 'a' = 'k')
    b = ySeg1 - (k * xSeg1)

    # Calculate the segment's end position
    # TODO: Optimize this routine, i.e. discard loop to find max value
    maxX = xSeg1 + ((self.offsetColumns / 3) * direction)
    maxY = ySeg1 + ((self.offsetColumns / 3) * direction)
    incX = (self.offsetColumns / 10) * direction
    xSeg2 = xSeg1
    while True:
      ySeg2 = (xSeg2 * k) + b
      if ((xSeg2 <= maxX or ySeg2 <= maxY) and direction < 0) or ((xSeg2 >= maxX or ySeg2 >= maxY) and direction > 0):
        break
      xSeg2 += incX
    zSeg2 = zSeg1

    return int(xSeg2), int(ySeg2), zSeg2

  def __drawSegment(self, segment):

    # Update properties according to state
    isVisible = True
    if segment.isRemoved.atGivenStepAgo(Global.selStep) or (segment.type == SegmentType.proximal and self.menuShowProximalSegmentsNone.isChecked()) or (segment.type == SegmentType.distal and self.menuShowDistalSegmentsNone.isChecked()):
      isVisible = False
    else:
      if segment.isFalselyPredicted.atGivenStepAgo(Global.selStep):
        if segment.type == SegmentType.proximal and self.menuShowProximalSegmentsFalselyPredicted.isChecked():
          color = self.colorSegmentFalselyPredicted
        else:
          isVisible = False
      elif segment.isPredicted.atGivenStepAgo(Global.selStep):
        if segment.type == SegmentType.proximal and self.menuShowProximalSegmentsPredicted.isChecked():
          color = self.colorSegmentPredicted
        else:
          isVisible = False
      elif segment.isActive.atGivenStepAgo(Global.selStep):
        if (segment.type == SegmentType.proximal and self.menuShowProximalSegmentsActive.isChecked()) or (segment.type == SegmentType.distal and self.menuShowDistalSegmentsActive.isChecked()):
          color = self.colorSegmentActive
        else:
          isVisible = False
      else:
        if segment.type == SegmentType.proximal:
          color = self.colorInactive
        else:
          isVisible = False

    if isVisible:
      # Draw the segment
      if not segment.tree3d_initialized:
        pts = numpy.array([[segment.tree3d_x1, segment.tree3d_y1, segment.tree3d_z1], [segment.tree3d_x2, segment.tree3d_y2, segment.tree3d_z2]])
        segment.tree3d_item = gl.GLLinePlotItem(pos=pts, width=1, antialias=False)
        segment.tree3d_initialized = True
        self.simulationViewer.addItem(segment.tree3d_item)

      # Update the color
      if segment.tree3d_selected:
        color = self.colorSelected
      segment.tree3d_item.color = pg.glColor(color)
    else:
      segment.tree3d_initialized = False
      if segment.tree3d_item in self.simulationViewer.items:
        self.simulationViewer.removeItem(segment.tree3d_item)

    # Draw/update all synapses of this segment
    for synapse in segment.synapses:
      self.__drawSynapse(segment, synapse, isVisible)

  def __drawSynapse(self, segment, synapse, segmentIsVisible):

    # Update properties according to state
    isVisible = True
    if synapse.isRemoved.atGivenStepAgo(Global.selStep) or (not segment.isActive.atGivenStepAgo(Global.selStep) and not segment.isPredicted.atGivenStepAgo(Global.selStep) and not segment.isFalselyPredicted.atGivenStepAgo(Global.selStep)) or (segment.type == SegmentType.proximal and self.menuShowProximalSynapsesNone.isChecked()) or (segment.type == SegmentType.distal and self.menuShowDistalSynapsesNone.isChecked()):
      isVisible = False
    else:
      if synapse.isFalselyPredicted.atGivenStepAgo(Global.selStep):
        if (segment.type == SegmentType.proximal and self.menuShowProximalSynapsesFalselyPredicted.isChecked()):
          color = self.colorSynapseFalselyPredicted
        else:
          isVisible = False
      elif synapse.isPredicted.atGivenStepAgo(Global.selStep):
        if (segment.type == SegmentType.proximal and self.menuShowProximalSynapsesPredicted.isChecked()):
          color = self.colorSynapsePredicted
        else:
          isVisible = False
      elif synapse.isConnected.atGivenStepAgo(Global.selStep):
        if (segment.type == SegmentType.proximal and self.menuShowProximalSynapsesConnected.isChecked()) or (segment.type == SegmentType.distal and self.menuShowDistalSynapsesConnected.isChecked()):
          color = self.colorSynapseConnected
        else:
          isVisible = False
      else:
        if (segment.type == SegmentType.proximal and self.menuShowProximalSynapsesActive.isChecked()) or (segment.type == SegmentType.distal and self.menuShowDistalSynapsesActive.isChecked()):
          color = self.colorInactive
        else:
          isVisible = False

    if isVisible and segmentIsVisible:
      # Draw the synapse
      if not synapse.tree3d_initialized:
        pts = numpy.array([[segment.tree3d_x2, segment.tree3d_y2, segment.tree3d_z2], [synapse.inputElem.tree3d_x, synapse.inputElem.tree3d_y, synapse.inputElem.tree3d_z]])
        synapse.tree3d_item = gl.GLLinePlotItem(pos=pts, width=1, antialias=False)
        synapse.tree3d_initialized = True
        self.simulationViewer.addItem(synapse.tree3d_item)

      # Update the color
      if synapse.tree3d_selected:
        color = self.colorSelected
      synapse.tree3d_item.color = pg.glColor(color)
    else:
      synapse.tree3d_initialized = False
      if synapse.tree3d_item in self.simulationViewer.items:
        self.simulationViewer.removeItem(synapse.tree3d_item)

  def selectView(self, viewMenu):
    """
    Load a pre-defined view and refresh controls.
    """

    if self.selectedViewMenu != None:
      self.selectedViewMenu.setChecked(False)
    self.selectedViewMenu = viewMenu
    self.selectedViewMenu.setChecked(True)

    # Find the specified view in the views list
    for view in Global.views:
      if view.menu == viewMenu:

        # Update menus
        self.menuShowBitsNone.setChecked(view.showBitsNone)
        self.menuShowBitsActive.setChecked(view.showBitsActive)
        self.menuShowBitsPredicted.setChecked(view.showBitsPredicted)
        self.menuShowBitsFalselyPredicted.setChecked(view.showBitsFalselyPredicted)
        self.menuShowCellsNone.setChecked(view.showCellsNone)
        self.menuShowCellsLearning.setChecked(view.showCellsLearning)
        self.menuShowCellsActive.setChecked(view.showCellsActive)
        self.menuShowCellsPredicted.setChecked(view.showCellsPredicted)
        self.menuShowCellsFalselyPredicted.setChecked(view.showCellsFalselyPredicted)
        self.menuShowCellsInactive.setChecked(view.showCellsInactive)
        self.menuShowProximalSegmentsNone.setChecked(view.showProximalSegmentsNone)
        self.menuShowProximalSegmentsActive.setChecked(view.showProximalSegmentsActive)
        self.menuShowProximalSegmentsPredicted.setChecked(view.showProximalSegmentsPredicted)
        self.menuShowProximalSegmentsFalselyPredicted.setChecked(view.showProximalSegmentsFalselyPredicted)
        self.menuShowProximalSynapsesNone.setChecked(view.showProximalSynapsesNone)
        self.menuShowProximalSynapsesConnected.setChecked(view.showProximalSynapsesConnected)
        self.menuShowProximalSynapsesActive.setChecked(view.showProximalSynapsesActive)
        self.menuShowProximalSynapsesPredicted.setChecked(view.showProximalSynapsesPredicted)
        self.menuShowProximalSynapsesFalselyPredicted.setChecked(view.showProximalSynapsesFalselyPredicted)
        self.menuShowDistalSegmentsNone.setChecked(view.showDistalSegmentsNone)
        self.menuShowDistalSegmentsActive.setChecked(view.showDistalSegmentsActive)
        self.menuShowDistalSynapsesNone.setChecked(view.showDistalSynapsesNone)
        self.menuShowDistalSynapsesConnected.setChecked(view.showDistalSynapsesConnected)
        self.menuShowDistalSynapsesActive.setChecked(view.showDistalSynapsesActive)

        # Update simulation
        self.refreshControls()

        break

    # Disable change options for the 'Default' view
    defaultViewSelected = False
    if self.selectedViewMenu == self.defaultViewMenu:
      defaultViewSelected = True
    self.menuViewsSave.setEnabled(not defaultViewSelected)
    self.menuViewsDelete.setEnabled(not defaultViewSelected)

  #endregion

  #region Events

  def menuLegend_Click(self, event):
    simulationLegendForm = SimulationLegendForm()
    simulationLegendForm.exec_()

  def menuShowBits_Click(self, event):
    menuClicked = self.sender()

    if menuClicked == self.menuShowBitsNone:
      if self.menuShowBitsNone.isChecked():
        self.menuShowBitsActive.setChecked(False)
        self.menuShowBitsPredicted.setChecked(False)
        self.menuShowBitsFalselyPredicted.setChecked(False)
    else:
      self.menuShowBitsNone.setChecked(False)

    self.refreshControls()

  def menuShowCells_Click(self, event):
    menuClicked = self.sender()

    if menuClicked == self.menuShowCellsNone:
      if self.menuShowCellsNone.isChecked():
        self.menuShowCellsLearning.setChecked(False)
        self.menuShowCellsActive.setChecked(False)
        self.menuShowCellsPredicted.setChecked(False)
        self.menuShowCellsFalselyPredicted.setChecked(False)
        self.menuShowCellsInactive.setChecked(False)
    else:
      self.menuShowCellsNone.setChecked(False)

    self.refreshControls()

  def menuShowProximalSegments_Click(self, event):
    menuClicked = self.sender()

    if menuClicked == self.menuShowProximalSegmentsNone:
      if self.menuShowProximalSegmentsNone.isChecked():
        self.menuShowProximalSegmentsActive.setChecked(False)
        self.menuShowProximalSegmentsPredicted.setChecked(False)
        self.menuShowProximalSegmentsFalselyPredicted.setChecked(False)
    else:
      self.menuShowProximalSegmentsNone.setChecked(False)

    self.refreshControls()

  def menuShowProximalSynapses_Click(self, event):
    menuClicked = self.sender()

    if menuClicked == self.menuShowProximalSynapsesNone:
      if self.menuShowProximalSynapsesNone.isChecked():
        self.menuShowProximalSynapsesConnected.setChecked(False)
        self.menuShowProximalSynapsesActive.setChecked(False)
        self.menuShowProximalSynapsesPredicted.setChecked(False)
        self.menuShowProximalSynapsesFalselyPredicted.setChecked(False)
    else:
      self.menuShowProximalSynapsesNone.setChecked(False)

    self.refreshControls()

  def menuShowDistalSegments_Click(self, event):
    menuClicked = self.sender()

    if menuClicked == self.menuShowDistalSegmentsNone:
      if self.menuShowDistalSegmentsNone.isChecked():
        self.menuShowDistalSegmentsActive.setChecked(False)
    else:
      self.menuShowDistalSegmentsNone.setChecked(False)

    self.refreshControls()

  def menuShowDistalSynapses_Click(self, event):
    menuClicked = self.sender()

    if menuClicked == self.menuShowDistalSynapsesNone:
      if self.menuShowDistalSynapsesNone.isChecked():
        self.menuShowDistalSynapsesConnected.setChecked(False)
        self.menuShowDistalSynapsesActive.setChecked(False)
    else:
      self.menuShowDistalSynapsesNone.setChecked(False)

    self.refreshControls()

  def menuView_Click(self, event):
    menuClicked = self.sender()
    self.selectView(menuClicked)

  def menuViewsNew_Click(self, event):

    # Ask for views's name
    enteredText, ok = QtGui.QInputDialog.getText(self, "Input Dialog", "Enter views' name:")
    if ok:
      view = View()
      view.name = enteredText
      view.menu = QtGui.QAction(self)
      view.menu.setText(view.name)
      view.menu.setCheckable(True)
      view.menu.triggered.connect(self.menuView_Click)

      Global.views.append(view)
      self.menuViews.addAction(view.menu)

      self.selectView(view.menu)

  def menuViewsSave_Click(self, event):

    # Find the specified view in the views list
    for view in Global.views:
      if view.menu == self.selectedViewMenu:
        view.showBitsNone = self.menuShowBitsNone.isChecked()
        view.showBitsActive = self.menuShowBitsActive.isChecked()
        view.showBitsPredicted = self.menuShowBitsPredicted.isChecked()
        view.showBitsFalselyPredicted = self.menuShowBitsFalselyPredicted.isChecked()
        view.showCellsNone = self.menuShowCellsNone.isChecked()
        view.showCellsLearning = self.menuShowCellsLearning.isChecked()
        view.showCellsActive = self.menuShowCellsActive.isChecked()
        view.showCellsPredicted = self.menuShowCellsPredicted.isChecked()
        view.showCellsFalselyPredicted = self.menuShowCellsFalselyPredicted.isChecked()
        view.showCellsInactive = self.menuShowCellsInactive.isChecked()
        view.showProximalSegmentsNone = self.menuShowProximalSegmentsNone.isChecked()
        view.showProximalSegmentsActive = self.menuShowProximalSegmentsActive.isChecked()
        view.showProximalSegmentsPredicted = self.menuShowProximalSegmentsPredicted.isChecked()
        view.showProximalSegmentsFalselyPredicted = self.menuShowProximalSegmentsFalselyPredicted.isChecked()
        view.showProximalSynapsesNone = self.menuShowProximalSynapsesNone.isChecked()
        view.showProximalSynapsesConnected = self.menuShowProximalSynapsesConnected.isChecked()
        view.showProximalSynapsesActive = self.menuShowProximalSynapsesActive.isChecked()
        view.showProximalSynapsesPredicted = self.menuShowProximalSynapsesPredicted.isChecked()
        view.showProximalSynapsesFalselyPredicted = self.menuShowProximalSynapsesFalselyPredicted.isChecked()
        view.showDistalSegmentsNone = self.menuShowDistalSegmentsNone.isChecked()
        view.showDistalSegmentsActive = self.menuShowDistalSegmentsActive.isChecked()
        view.showDistalSynapsesNone = self.menuShowDistalSynapsesNone.isChecked()
        view.showDistalSynapsesConnected = self.menuShowDistalSynapsesConnected.isChecked()
        view.showDistalSynapsesActive = self.menuShowDistalSynapsesActive.isChecked()

        Global.saveConfig()

        break

  def menuViewsDelete_Click(self, event):

    # Find the specified view in the views list
    for view in Global.views:
      if view.menu == self.selectedViewMenu:
        Global.views.remove(view)
        self.menuViews.removeAction(view.menu)
        break

    # Set 'Default' view as initial view
    self.selectView(self.defaultViewMenu)

  #endregion
