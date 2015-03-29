from PyQt4 import QtGui, QtCore
from nupic_studio.ui import Global
from nupic_studio.htm.node import NodeType, Node
from nupic_studio.htm.node_region import Region
from nupic_studio.htm.node_sensor import Sensor
from nupic_studio.ui.node_region_form import RegionForm
from nupic_studio.ui.node_sensor_form import SensorForm

class ArchitectureForm(QtGui.QWidget):

  #region Constructor

  def __init__(self):
    """
    Initializes a new instance of this class.
    """

    QtGui.QWidget.__init__(self)

    self.initUI()

  #endregion

  #region Methods

  def initUI(self):

    # DesignPanel
    self.designPanel = DesignPanel()

    # tabPageDesignLayout
    tabPageDesignLayout = QtGui.QHBoxLayout()
    tabPageDesignLayout.addWidget(self.designPanel)

    # tabPageDesign
    self.tabPageDesign = QtGui.QWidget()
    self.tabPageDesign.setLayout(tabPageDesignLayout)

    # textBoxCode
    self.textBoxCode = QtGui.QTextEdit()
    self.textBoxCode.setReadOnly(True)
    self.textBoxCode.setAlignment(QtCore.Qt.AlignLeft)
    self.textBoxCode.setWordWrapMode(QtGui.QTextOption.NoWrap)
    self.textBoxCode.setFont(QtGui.QFont("Courier New", 9))

    # tabPageCodeLayout
    tabPageCodeLayout = QtGui.QHBoxLayout()
    tabPageCodeLayout.addWidget(self.textBoxCode)

    # tabPageCode
    self.tabPageCode = QtGui.QWidget()
    self.tabPageCode.setLayout(tabPageCodeLayout)

    # tabControlMain
    self.tabControlMain = QtGui.QTabWidget()
    self.tabControlMain.addTab(self.tabPageDesign, "Design")
    self.tabControlMain.addTab(self.tabPageCode, "Code")

    # layout
    layout = QtGui.QHBoxLayout()
    layout.addWidget(self.tabControlMain)

    # ArchitectureForm
    self.setLayout(layout)
    self.setMinimumWidth(300)
    self.setMinimumHeight(300)
    self.setWindowTitle("Network Architecture")
    self.setWindowIcon(QtGui.QIcon(Global.appPath + '/images/logo.ico'))

  def updateCode(self):
    """
    Update the source code of the network.
    """

    code = Global.project.network.getSourceCode()
    self.textBoxCode.setText(code)

  #endregion

class DesignPanel(QtGui.QWidget):

  #region Constructor

  def __init__(self):
    """
    Initializes a new instance of this class.
    """

    QtGui.QWidget.__init__(self)

    #region Instance fields

    self.topRegion = Region("TopRegion")
    """Node that is on top of the hierarchy."""

    self.selectedNode = None
    """Node that is selected for visualization of its details."""

    self.underMouseNode = None
    """Node that is highlighted due to mouse is on it."""

    # Space to skip horizontally between siblings
    # and vertically between generations
    self._offsetHorizontal = 15
    self._offsetVertical = 30

    #endregion

    self.initUI()

  #endregion

  #region Methods

  def initUI(self):

    # menuNodeProperties
    self.menuNodeProperties = QtGui.QAction(self)
    self.menuNodeProperties.setText("&Properties")
    self.menuNodeProperties.triggered.connect(self.__menuNodeProperties_Click)

    # menuNodeAddRegion
    self.menuNodeAddRegion = QtGui.QAction(self)
    self.menuNodeAddRegion.setText("&Add region under this node...")
    self.menuNodeAddRegion.triggered.connect(self.__menuNodeAddRegion_Click)

    # menuNodeAddSensor
    self.menuNodeAddSensor = QtGui.QAction(self)
    self.menuNodeAddSensor.setText("&Add sensor under this node...")
    self.menuNodeAddSensor.triggered.connect(self.__menuNodeAddSensor_Click)

    # menuNodeDelete
    self.menuNodeDelete = QtGui.QAction(self)
    self.menuNodeDelete.setText("&Delete this node...")
    self.menuNodeDelete.triggered.connect(self.__menuNodeDelete_Click)

    # menuNode
    self.menuNode = QtGui.QMenu()
    self.menuNode.addAction(self.menuNodeProperties)
    self.menuNode.addAction(self.menuNodeAddRegion)
    self.menuNode.addAction(self.menuNodeAddSensor)
    self.menuNode.addAction(self.menuNodeDelete)

    # layout
    layout = QtGui.QHBoxLayout()

    # DesignPanel
    self.setLayout(layout)
    self.setToolTip("Left button click: Select region.\r\nRight button click: Show options for region or sensor.")

    # Set center position of the top region
    self.topRegion.tree2d_x = self.minimumWidth() / 2
    self.topRegion.tree2d_y = 30

    # Painter to draw the tree
    self.painter = QtGui.QPainter()

  def __arrangeNode(self, node, minX, minY):
    """
    Arrange the node and the lower nodes that feed it in the allowed area.
    Set minX to indicate the right edge of our subtree.
    Set minY to indicate the bottom edge of our subtree.
    """

    # See how big this node is.
    size = self.__getNodeSize(node)

    # Recursively arrange the lower nodes that feed this node,
    # allowing room for this node.
    x = minX
    width = size.width()
    height = size.height()
    biggestMinY = minY + height
    subtreeMinY = minY + height + self._offsetVertical
    numFeeders = 0
    for feeder in Global.project.network.getFeederNodes(node):

      # Arrange this feeder's subtree.
      feederMinY = subtreeMinY
      x, feederMinY = self.__arrangeNode(feeder, x, feederMinY)

      # See if this increases the biggest minY value.
      if biggestMinY < feederMinY:
        biggestMinY = feederMinY

      # Allow room before the next sibling.
      x += self._offsetHorizontal

      numFeeders += 1

    # Remove the spacing after the last feeder.
    if numFeeders > 0:
      x -= self._offsetHorizontal

    # See if this node is wider than the subtree under it.
    subtreeWidth = x - minX
    if width > subtreeWidth:
      # Center the subtree under this node.
      # Make the lower nodes that feed this node rearrange themselves
      # moved to center their subtrees.
      x = minX + (width - subtreeWidth) / 2
      for feeder in Global.project.network.getFeederNodes(node):
        # Arrange this feeder's subtree.
        x, subtreeMinY = self.__arrangeNode(feeder, x, subtreeMinY)

        # Allow room before the next sibling.
        x += self._offsetHorizontal

      # The subtree's width is this node's width.
      subtreeWidth = width

    # Set this node's center position.
    node.tree2d_x = minX + subtreeWidth / 2
    node.tree2d_y = minY + height / 2

    # Increase minX to allow room for the subtree before returning.
    minX += subtreeWidth

    # Set the return value for minY.
    minY = biggestMinY

    return minX, minY

  def __getNodeSize(self, node):
    """
    Return the size of the string plus a 10 pixel margin.
    """

    fontMetrics = self.painter.fontMetrics()
    width = fontMetrics.width(QtCore.QString(node.name))

    return QtCore.QSizeF(30 + width, 30)

  def __drawNode(self, node):
    """
    Draw the nodes for the subtree rooted at this node.
    """

    # Recursively make the node draw its feeders.
    for feeder in Global.project.network.getFeederNodes(node):
      # Draw the link between this node and this feeder.
      self.painter.drawLine(node.tree2d_x, node.tree2d_y, feeder.tree2d_x, feeder.tree2d_y)

      # Recursively make the node draw its feeders.
      self.__drawNode(feeder)

    # Draw this node centered at (x, y).
    brush = QtGui.QBrush()
    if node == self.selectedNode:
      brush = QtGui.QColor(0, 200, 250)
    else:
      brush = QtGui.QColor(0, 150, 200)

    # Fill and draw a polygon at our location.
    size = self.__getNodeSize(node)
    x = node.tree2d_x
    y = node.tree2d_y
    width = size.width()
    height = size.height()
    if node.type == NodeType.region:
      point1 = QtCore.QPoint((x - width / 2) + 10, (y - height / 2))
      point2 = QtCore.QPoint((x + width / 2) - 10, (y - height / 2))
    elif (node.type == NodeType.sensor):
      point1 = QtCore.QPoint((x - width / 2), (y - height / 2))
      point2 = QtCore.QPoint((x + width / 2), (y - height / 2))
    point3 = QtCore.QPoint((x + width / 2), (y + height / 2))
    point4 = QtCore.QPoint((x - width / 2), (y + height / 2))
    polygon = QtGui.QPolygon([point1, point2, point3, point4])
    self.painter.setBrush(brush)
    self.painter.drawPolygon(polygon)
    node.tree2d_polygon = polygon

    # Draw the text.
    self.painter.drawText(polygon.boundingRect(), QtCore.Qt.AlignCenter, node.name)

  def __nodeAtPoint(self, node, mousePoint):
    """
    Return the node at this point (or None if there isn't one there).
    """

    # See if the point is under this node.
    if node.tree2d_polygon.boundingRect().contains(mousePoint):
      return node

    # See if the point is under a node in the subtree.
    for feeder in Global.project.network.getFeederNodes(node):
      hitNode = self.__nodeAtPoint(feeder, mousePoint)
      if hitNode != None:
        return hitNode

    return None

  #endregion

  #region Events

  def paintEvent(self, event):
    """
    Draw and center the tree on the form.
    """

    # Initialize painter
    self.painter.begin(self)
    self.painter.setFont(QtGui.QFont("Arial", 8))
    self.painter.fillRect(self.rect(), QtCore.Qt.white)

    # Arrange the tree once to see how big it is.
    minX = 0
    minY = 0
    minX, minY = self.__arrangeNode(self.topRegion, minX, minY)

    # Rearrange the tree again to center it horizontally.
    minX = (self.width() - minX) / 2
    minY = 10
    minX, minY = self.__arrangeNode(self.topRegion, minX, minY)

    # Draw the tree recursively from top region.
    self.__drawNode(self.topRegion)

    # End painter
    self.painter.end()

  def mousePressEvent(self, event):
    """
    If this is a right button down and the mouse is over a node, display a context menu.
    """

    if event.buttons() == QtCore.Qt.LeftButton:
      self.underMouseNode = self.__nodeAtPoint(self.topRegion, event.pos())
      if self.underMouseNode != None:
        # Select the node and updates any related information.
        self.selectedNode = self.underMouseNode

        # Redraw the tree to show the updates.
        self.repaint()

        # Refresh dependents tools
        Global.simulationForm.refreshControls()
        Global.nodeInformationForm.refreshControls()
    elif event.buttons() == QtCore.Qt.RightButton:
      self.underMouseNode = self.__nodeAtPoint(self.topRegion, event.pos())
      if self.underMouseNode != None:
        # Don't let the user delete the top node.
        self.menuNodeAddRegion.setEnabled(not Global.simulationInitialized and self.underMouseNode.type != NodeType.sensor)
        self.menuNodeAddSensor.setEnabled(not Global.simulationInitialized and self.underMouseNode.type != NodeType.sensor)
        self.menuNodeDelete.setEnabled(not Global.simulationInitialized and self.underMouseNode != self.topRegion)

        # Display the context menu.
        self.menuNode.exec_(self.mapToGlobal(event.pos()))

  def __menuNodeProperties_Click(self, event):
    """
    View node propeerties.
    """

    if self.underMouseNode.type == NodeType.region:
      regionForm = RegionForm()
      regionForm.setControlsValues()
      dialogResult = regionForm.exec_()

      # Update controls with the new changes
      if dialogResult == QtGui.QDialog.Accepted:
        Global.mainForm.markProjectChanges(True)
        Global.architectureForm.updateCode()
    elif self.underMouseNode.type == NodeType.sensor:
      sensorForm = SensorForm()
      sensorForm.setControlsValues()
      dialogResult = sensorForm.exec_()

      # Update controls with the new changes
      if dialogResult == QtGui.QDialog.Accepted:
        Global.mainForm.markProjectChanges(True)
        Global.architectureForm.updateCode()

  def __menuNodeAddRegion_Click(self, event):
    """
    Add a feeder region to the selected region.
    """

    # Ask for region's name
    enteredText, ok = QtGui.QInputDialog.getText(self, "Input Dialog", "Enter region's name:")
    if ok:
      validExpr = QtCore.QRegExp('[a-zA-Z0-9_]+')
      if not validExpr.exactMatch(enteredText):
        QtGui.QMessageBox.warning(self, "Warning", "'" + enteredText + "' is not a valid name. Only characters, numbers and _ are accepted.")
        return

      Global.mainForm.markProjectChanges(True)

      # Add new region below highlighted region
      newRegion = Region(enteredText)
      Global.project.network.addFeederNode(newRegion, self.underMouseNode)

      # Redraw the tree to show the updates.
      self.repaint()
      Global.architectureForm.updateCode()

  def __menuNodeAddSensor_Click(self, event):
    """
    Add a feeder sensor to the selected region.
    """

    # Ask for sensor's name
    enteredText, ok = QtGui.QInputDialog.getText(self, "Input Dialog", "Enter sensor's name:")
    if ok:
      validExpr = QtCore.QRegExp('[a-zA-Z0-9_]+')
      if not validExpr.exactMatch(enteredText):
        QtGui.QMessageBox.warning(self, "Warning", "'" + enteredText + "' is not a valid name. Only characters, numbers and _ are accepted.")
        return

      Global.mainForm.markProjectChanges(True)

      # Add new sensor below highlighted region
      newSensor = Sensor(enteredText)
      Global.project.network.addFeederNode(newSensor, self.underMouseNode)

      # Redraw the tree to show the updates.
      self.repaint()
      Global.architectureForm.updateCode()

  def __menuNodeDelete_Click(self, event):
    """
    Delete this node from the tree.
    """

    if QtGui.QMessageBox.question(self, "Question", "Are you sure you want to delete this node?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No) == QtGui.QMessageBox.Yes:
      Global.mainForm.markProjectChanges(True)

      # Delete the node and its subtree.
      Global.project.network.deleteFeederNode(self.underMouseNode)

      # Redraw the tree to show the updates.
      self.repaint()
      Global.architectureForm.updateCode()

  #endregion
