import numpy
import os
from PIL import Image
from PyQt5 import QtGui, QtCore, QtWidgets
from nupic_studio.htm.node import Node, NodeType
from nupic_studio.htm.segment import SegmentType
from nupic_studio.ui import Global, State, View
from nupic_studio.ui.simulation_legend_form import SimulationLegendForm
from nupic_studio.util import Texture3D


class SimulationForm(QtWidgets.QWidget):

    def __init__(self):
        """
        Initializes a new instance of this class.
        """
        QtWidgets.QWidget.__init__(self)
        self.initUI()

    def initUI(self):

        # viewer_3d
        self.viewer_3d = Viewer3D()
        self.viewer_3d.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        # layout
        layout = QtWidgets.QGridLayout()
        layout.addWidget(self.viewer_3d)

        # Form
        self.setLayout(layout)
        self.setWindowTitle("Simulation")
        self.setWindowIcon(QtGui.QIcon(Global.appPath + '/images/logo.ico'))
        self.setMinimumSize(300, 300)
        self.setToolTip("Left-Button-Pressed: Rotate\r\nLeft-Button-DoubleClick: Reset observer camera\r\nRight-Button-Pressed: Shows menu\r\nMiddle-Button-Pressed: Pan\r\nWheel: Zoom in/out")

    def clearControls(self):
        """
        Reset all controls.
        """
        self.viewer_3d.clear()

    def update(self):
            """
            Refresh controls for each time step.
            """
            self.viewer_3d.update()

    def refreshControls(self):
        """
        Refresh controls for each time step.
        """
        self.viewer_3d.updateElements3d()

class Viewer3D(QtWidgets.QLabel):

    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        self.mouse_working_area = None

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

        self.initUI()

        # Create views menus
        for view in Global.views:
            view.menu = QtWidgets.QAction(self)
            view.menu.setText(view.name)
            view.menu.setCheckable(True)
            view.menu.triggered.connect(self.menuView_click)
            self.menuViews.addAction(view.menu)

            # If this is the first menu, set it as default
            if self.defaultViewMenu == None:
                self.defaultViewMenu = view.menu

        # Load default view
        self.selectView(self.defaultViewMenu)

    def initUI(self):

        # menuViewsNew
        self.menuViewsNew = QtWidgets.QAction(self)
        self.menuViewsNew.setText("Create new view")
        self.menuViewsNew.triggered.connect(self.menuViewsNew_click)

        # menuViewsSave
        self.menuViewsSave = QtWidgets.QAction(self)
        self.menuViewsSave.setText("Save selected view")
        self.menuViewsSave.triggered.connect(self.menuViewsSave_click)

        # menuViewsDelete
        self.menuViewsDelete = QtWidgets.QAction(self)
        self.menuViewsDelete.setText("Delete selected view")
        self.menuViewsDelete.triggered.connect(self.menuViewsDelete_click)

        # menuViews
        self.menuViews = QtWidgets.QMenu()
        self.menuViews.addAction(self.menuViewsNew)
        self.menuViews.addAction(self.menuViewsSave)
        self.menuViews.addAction(self.menuViewsDelete)
        self.menuViews.addSeparator()
        self.menuViews.setTitle("&View")

        # menuShowBitsNone
        self.menuShowBitsNone = QtWidgets.QAction(self)
        self.menuShowBitsNone.setText("&None")
        self.menuShowBitsNone.setCheckable(True)
        self.menuShowBitsNone.triggered.connect(self.menuShowBits_click)

        # menuShowBitsActive
        self.menuShowBitsActive = QtWidgets.QAction(self)
        self.menuShowBitsActive.setText("&Active")
        self.menuShowBitsActive.setCheckable(True)
        self.menuShowBitsActive.triggered.connect(self.menuShowBits_click)

        # menuShowBitsPredicted
        self.menuShowBitsPredicted = QtWidgets.QAction(self)
        self.menuShowBitsPredicted.setText("&Predicted")
        self.menuShowBitsPredicted.setCheckable(True)
        self.menuShowBitsPredicted.triggered.connect(self.menuShowBits_click)

        # menuShowBitsFalselyPredicted
        self.menuShowBitsFalselyPredicted = QtWidgets.QAction(self)
        self.menuShowBitsFalselyPredicted.setText("&Falsely Predicted")
        self.menuShowBitsFalselyPredicted.setCheckable(True)
        self.menuShowBitsFalselyPredicted.triggered.connect(self.menuShowBits_click)

        # menuShowBits
        self.menuShowBits = QtWidgets.QMenu()
        self.menuShowBits.addAction(self.menuShowBitsNone)
        self.menuShowBits.addAction(self.menuShowBitsActive)
        self.menuShowBits.addAction(self.menuShowBitsPredicted)
        self.menuShowBits.addAction(self.menuShowBitsFalselyPredicted)
        self.menuShowBits.setTitle("&Sensor bits")

        # menuShowCellsNone
        self.menuShowCellsNone = QtWidgets.QAction(self)
        self.menuShowCellsNone.setText("&None")
        self.menuShowCellsNone.setCheckable(True)
        self.menuShowCellsNone.triggered.connect(self.menuShowCells_click)

        # menuShowCellsLearning
        self.menuShowCellsLearning = QtWidgets.QAction(self)
        self.menuShowCellsLearning.setText("&Learning")
        self.menuShowCellsLearning.setCheckable(True)
        self.menuShowCellsLearning.triggered.connect(self.menuShowCells_click)

        # menuShowCellsActive
        self.menuShowCellsActive = QtWidgets.QAction(self)
        self.menuShowCellsActive.setText("&Active")
        self.menuShowCellsActive.setCheckable(True)
        self.menuShowCellsActive.triggered.connect(self.menuShowCells_click)

        # menuShowCellsInactive
        self.menuShowCellsInactive = QtWidgets.QAction(self)
        self.menuShowCellsInactive.setText("&Inactive")
        self.menuShowCellsInactive.setCheckable(True)
        self.menuShowCellsInactive.triggered.connect(self.menuShowCells_click)

        # menuShowCellsPredicted
        self.menuShowCellsPredicted = QtWidgets.QAction(self)
        self.menuShowCellsPredicted.setText("&Predicted")
        self.menuShowCellsPredicted.setCheckable(True)
        self.menuShowCellsPredicted.triggered.connect(self.menuShowCells_click)

        # menuShowCellsFalselyPredicted
        self.menuShowCellsFalselyPredicted = QtWidgets.QAction(self)
        self.menuShowCellsFalselyPredicted.setText("&Falsely Predicted")
        self.menuShowCellsFalselyPredicted.setCheckable(True)
        self.menuShowCellsFalselyPredicted.triggered.connect(self.menuShowCells_click)

        # menuShowCells
        self.menuShowCells = QtWidgets.QMenu()
        self.menuShowCells.addAction(self.menuShowCellsNone)
        self.menuShowCells.addAction(self.menuShowCellsLearning)
        self.menuShowCells.addAction(self.menuShowCellsActive)
        self.menuShowCells.addAction(self.menuShowCellsPredicted)
        self.menuShowCells.addAction(self.menuShowCellsFalselyPredicted)
        self.menuShowCells.addAction(self.menuShowCellsInactive)
        self.menuShowCells.setTitle("C&ells")

        # menuShowProximalSegmentsNone
        self.menuShowProximalSegmentsNone = QtWidgets.QAction(self)
        self.menuShowProximalSegmentsNone.setText("&None")
        self.menuShowProximalSegmentsNone.setCheckable(True)
        self.menuShowProximalSegmentsNone.triggered.connect(self.menuShowProximalSegments_click)

        # menuShowProximalSegmentsActive
        self.menuShowProximalSegmentsActive = QtWidgets.QAction(self)
        self.menuShowProximalSegmentsActive.setText("&Active")
        self.menuShowProximalSegmentsActive.setCheckable(True)
        self.menuShowProximalSegmentsActive.triggered.connect(self.menuShowProximalSegments_click)

        # menuShowProximalSegmentsPredicted
        self.menuShowProximalSegmentsPredicted = QtWidgets.QAction(self)
        self.menuShowProximalSegmentsPredicted.setText("&Predicted")
        self.menuShowProximalSegmentsPredicted.setCheckable(True)
        self.menuShowProximalSegmentsPredicted.triggered.connect(self.menuShowProximalSegments_click)

        # menuShowProximalSegmentsFalselyPredicted
        self.menuShowProximalSegmentsFalselyPredicted = QtWidgets.QAction(self)
        self.menuShowProximalSegmentsFalselyPredicted.setText("&Falsely Predicted")
        self.menuShowProximalSegmentsFalselyPredicted.setCheckable(True)
        self.menuShowProximalSegmentsFalselyPredicted.triggered.connect(self.menuShowProximalSegments_click)

        # menuShowProximalSegments
        self.menuShowProximalSegments = QtWidgets.QMenu()
        self.menuShowProximalSegments.addAction(self.menuShowProximalSegmentsNone)
        self.menuShowProximalSegments.addAction(self.menuShowProximalSegmentsActive)
        self.menuShowProximalSegments.addAction(self.menuShowProximalSegmentsPredicted)
        self.menuShowProximalSegments.addAction(self.menuShowProximalSegmentsFalselyPredicted)
        self.menuShowProximalSegments.setTitle("&Segments")

        # menuShowProximalSynapsesNone
        self.menuShowProximalSynapsesNone = QtWidgets.QAction(self)
        self.menuShowProximalSynapsesNone.setText("&None")
        self.menuShowProximalSynapsesNone.setCheckable(True)
        self.menuShowProximalSynapsesNone.triggered.connect(self.menuShowProximalSynapses_click)

        # menuShowProximalSynapsesConnected
        self.menuShowProximalSynapsesConnected = QtWidgets.QAction(self)
        self.menuShowProximalSynapsesConnected.setText("&Connected")
        self.menuShowProximalSynapsesConnected.setCheckable(True)
        self.menuShowProximalSynapsesConnected.triggered.connect(self.menuShowProximalSynapses_click)

        # menuShowProximalSynapsesActive
        self.menuShowProximalSynapsesActive = QtWidgets.QAction(self)
        self.menuShowProximalSynapsesActive.setText("&Active")
        self.menuShowProximalSynapsesActive.setCheckable(True)
        self.menuShowProximalSynapsesActive.triggered.connect(self.menuShowProximalSynapses_click)

        # menuShowProximalSynapsesPredicted
        self.menuShowProximalSynapsesPredicted = QtWidgets.QAction(self)
        self.menuShowProximalSynapsesPredicted.setText("&Predicted")
        self.menuShowProximalSynapsesPredicted.setCheckable(True)
        self.menuShowProximalSynapsesPredicted.triggered.connect(self.menuShowProximalSynapses_click)

        # menuShowProximalSynapsesFalselyPredicted
        self.menuShowProximalSynapsesFalselyPredicted = QtWidgets.QAction(self)
        self.menuShowProximalSynapsesFalselyPredicted.setText("&Falsely Predicted")
        self.menuShowProximalSynapsesFalselyPredicted.setCheckable(True)
        self.menuShowProximalSynapsesFalselyPredicted.triggered.connect(self.menuShowProximalSynapses_click)

        # menuShowProximalSynapses
        self.menuShowProximalSynapses = QtWidgets.QMenu()
        self.menuShowProximalSynapses.addAction(self.menuShowProximalSynapsesNone)
        self.menuShowProximalSynapses.addAction(self.menuShowProximalSynapsesConnected)
        self.menuShowProximalSynapses.addAction(self.menuShowProximalSynapsesActive)
        self.menuShowProximalSynapses.addAction(self.menuShowProximalSynapsesPredicted)
        self.menuShowProximalSynapses.addAction(self.menuShowProximalSynapsesFalselyPredicted)
        self.menuShowProximalSynapses.setTitle("&Synapses")

        # menuShowProximal
        self.menuShowProximal = QtWidgets.QMenu()
        self.menuShowProximal.addMenu(self.menuShowProximalSegments)
        self.menuShowProximal.addMenu(self.menuShowProximalSynapses)
        self.menuShowProximal.setTitle("&Proximal")

        # menuShowDistalSegmentsNone
        self.menuShowDistalSegmentsNone = QtWidgets.QAction(self)
        self.menuShowDistalSegmentsNone.setText("&None")
        self.menuShowDistalSegmentsNone.setCheckable(True)
        self.menuShowDistalSegmentsNone.triggered.connect(self.menuShowDistalSegments_click)

        # menuShowDistalSegmentsActive
        self.menuShowDistalSegmentsActive = QtWidgets.QAction(self)
        self.menuShowDistalSegmentsActive.setText("&Active")
        self.menuShowDistalSegmentsActive.setCheckable(True)
        self.menuShowDistalSegmentsActive.triggered.connect(self.menuShowDistalSegments_click)

        # menuShowDistalSegments
        self.menuShowDistalSegments = QtWidgets.QMenu()
        self.menuShowDistalSegments.addAction(self.menuShowDistalSegmentsNone)
        self.menuShowDistalSegments.addAction(self.menuShowDistalSegmentsActive)
        self.menuShowDistalSegments.setTitle("&Segments")

        # menuShowDistalSynapsesNone
        self.menuShowDistalSynapsesNone = QtWidgets.QAction(self)
        self.menuShowDistalSynapsesNone.setText("&None")
        self.menuShowDistalSynapsesNone.setCheckable(True)
        self.menuShowDistalSynapsesNone.triggered.connect(self.menuShowDistalSynapses_click)

        # menuShowDistalSynapsesConnected
        self.menuShowDistalSynapsesConnected = QtWidgets.QAction(self)
        self.menuShowDistalSynapsesConnected.setText("&Connected")
        self.menuShowDistalSynapsesConnected.setCheckable(True)
        self.menuShowDistalSynapsesConnected.triggered.connect(self.menuShowDistalSynapses_click)

        # menuShowDistalSynapsesActive
        self.menuShowDistalSynapsesActive = QtWidgets.QAction(self)
        self.menuShowDistalSynapsesActive.setText("&Active")
        self.menuShowDistalSynapsesActive.setCheckable(True)
        self.menuShowDistalSynapsesActive.triggered.connect(self.menuShowDistalSynapses_click)

        # menuShowDistalSynapses
        self.menuShowDistalSynapses = QtWidgets.QMenu()
        self.menuShowDistalSynapses.addAction(self.menuShowDistalSynapsesNone)
        self.menuShowDistalSynapses.addAction(self.menuShowDistalSynapsesConnected)
        self.menuShowDistalSynapses.addAction(self.menuShowDistalSynapsesActive)
        self.menuShowDistalSynapses.setTitle("&Synapses")

        # menuShowDistal
        self.menuShowDistal = QtWidgets.QMenu()
        self.menuShowDistal.addMenu(self.menuShowDistalSegments)
        self.menuShowDistal.addMenu(self.menuShowDistalSynapses)
        self.menuShowDistal.setTitle("&Distal")

        # menuShow
        self.menuShow = QtWidgets.QMenu()
        self.menuShow.addMenu(self.menuShowBits)
        self.menuShow.addMenu(self.menuShowCells)
        self.menuShow.addMenu(self.menuShowProximal)
        self.menuShow.addMenu(self.menuShowDistal)
        self.menuShow.setTitle("&Show")

        # menuLegend
        self.menuLegend = QtWidgets.QAction(self)
        self.menuLegend.setText("&Legend")
        self.menuLegend.triggered.connect(self.menuLegend_click)

        # menuSimulation
        self.menuSimulation = QtWidgets.QMenu()
        self.menuSimulation.addMenu(self.menuViews)
        self.menuSimulation.addMenu(self.menuShow)
        self.menuSimulation.addAction(self.menuLegend)
        self.menuSimulation.setTitle("&Simulation")

        # image
        self.pivot_image = QtGui.QImage(os.path.join(Global.appPath + '/images', 'cross.png'))

        # pivot
        self.pivot = QtWidgets.QLabel(self)
        self.pivot.setPixmap(QtGui.QPixmap.fromImage(self.pivot_image))
        self.pivot.setVisible(False)

        # Change background color
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QtCore.Qt.black)

        # self
        self.setPalette(palette)
        self.setMouseTracking(True)
        self.setAutoFillBackground(True)

    def initializeControls(self, top_region):
        """
        Refresh controls for each time step.
        """
        self.topRegion = top_region

        # Set the colors of the states.
        self.ColorInactive = Texture3D.Gray
        self.ColorSelected = Texture3D.Blue
        self.ColorBitActive = Texture3D.Green
        self.ColorBitPredicted = Texture3D.Yellow
        self.ColorBitFalselyPredicted = Texture3D.Red
        self.ColorCellLearning = Texture3D.GreenYellow
        self.ColorCellActive = Texture3D.Green
        self.ColorCellPredicted = Texture3D.Yellow
        self.ColorCellFalselyPredicted = Texture3D.Red
        self.ColorSegmentActive = Texture3D.Green
        self.ColorSegmentPredicted = Texture3D.Yellow
        self.ColorSegmentFalselyPredicted = Texture3D.Red
        self.ColorSynapseConnected = Texture3D.Green
        self.ColorSynapsePredicted = Texture3D.Yellow
        self.ColorSynapseFalselyPredicted = Texture3D.Red

        # Arrange the tree once to see how big it is.
        self.treeWidth = 0
        self.treeHeight = 0
        minX = 0
        minZ = 0
        minX, minZ = self.__arrangeNode(self.topRegion, minX, minZ)

        x, y, z = self.topRegion.tree3d_pos

        # Rearrange the tree again to center it horizontally.
        offsetX = x
        self.__centerNode(self.topRegion, offsetX)

        # Rearrange the tree again to invert it vertically.
        offsetZ = 50
        self.__invertNode(self.topRegion, offsetZ)

        # Once we have the final position of the regions, we can calculate the position of every column and cell.
        self.__calculateNodeElementsPosition(self.topRegion)

        # Draw the tree recursively from top region.
        self.__drawNode(self.topRegion, True)

    def clear(self):
        """
        Reset all controls.
        """
        self.mouse_working_area = None

    def update(self):
        """
        Refresh controls for each time step.
        """
        if Global.mainForm.isRunning():

            # Get the image to be draw on this viewer.
            image = None
            if Global.mainForm.state == State.Simulating:
                texture = Global.mainForm.simulation.screen_texture
                size = (texture.getXSize(), texture.getYSize())
                format = "RGBA"
                if texture.mightHaveRamImage():
                    image = Image.frombuffer(format, size, texture.getRamImageAs(format), "raw", format, 0, 0)
                else:
                    image = Image.new(format, size)
            elif Global.mainForm.state == State.Playbacking:
                playback_file = os.path.join(Global.mainForm.getRecordPath(), "main_camera_" + "{:08d}".format(Global.mainForm.get_step()) + ".png")
                if os.path.isfile(playback_file):
                    image = Image.open(playback_file)

            # Draw the image.
            _image = image.toqimage()
            self.pixel_map = QtGui.QPixmap.fromImage(_image)
            self.adjustMouseWorkingArea()

    def showContextMenu(self, pos):
        """
        Event handling right-click contextMenu
        """

        if Global.simulationInitialized:
            self.menuSimulation.exec_(self.mapToGlobal(pos))
        else:
            QtWidgets.QMessageBox.information(self, "Information", "Context menu available only during the simulation.")

    def adjustMouseWorkingArea(self):
        viewer_size = self.size()
        self.setPixmap(self.pixel_map.scaled(viewer_size, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        image_size = self.pixmap().size()
        horizontal_margin = (viewer_size.width() - image_size.width()) / 2
        vertical_margin = (viewer_size.height() - image_size.height()) / 2
        self.mouse_working_area = (
        horizontal_margin, vertical_margin, horizontal_margin + image_size.width(), vertical_margin + image_size.height())

    def resizeEvent(self, event):
        if self.mouse_working_area is not None:
            self.adjustMouseWorkingArea()

    def handleKeyEvent(self, event, event_state):
        # Inform Panda to start (or continue) the action associated with the key pressed
        # or stop it if key is released
        key_pressed = event.key()

        # Check if key is in the user's key map an then call associated function
        for k, value in Global.mainForm.simulation.key_map.items():
            if "-" in k:
                [key_ascii, key_state] = k.split("-")
            else:
                key_ascii = k
                key_state = ""
            if key_state == event_state and QtGui.QKeySequence(key_ascii) == key_pressed and not event.isAutoRepeat():
                (func, args) = value
                func(*args)
                break

    def isSimulating(self):
        return (Global.mainForm.state == State.Simulating and not Global.mainForm.paused) and Global.mainForm.simulation is not None

    def keyPressEvent(self, event):
        if self.isSimulating():
            self.handleKeyEvent(event, "")

    def keyReleaseEvent(self, event):
        if self.isSimulating():
            self.handleKeyEvent(event, "up")

    def createStartMouseWorkFn(self, x, y):
        def fn():
            width = self.pivot_image.width()
            height = self.pivot_image.height()
            self.pivot.setGeometry(x - (width / 2), y - (height / 2), width, height)
            self.pivot.setVisible(True)
        return fn

    def createStopMouseWorkFn(self):
        def fn():
            self.pivot.setVisible(False)
        return fn

    def mouseDoubleClickEvent(self, event):
        if self.isSimulating() and self.mouse_working_area is not None and event.buttons() == QtCore.Qt.LeftButton:
            Global.mainForm.simulation.resetCamera()

    def mouseMoveEvent(self, event):
        if self.isSimulating() and self.mouse_working_area is not None:
            def pyqtToPanda(val, max):
                mid = max / 2
                return (val - mid) / float(mid)

            # Check if mouse is on the image
            mouse_pos = event.pos()
            x, y = mouse_pos.x(), mouse_pos.y()
            x0, y0, xn, yn = self.mouse_working_area
            if self.mouse_working_area is not None and x >= x0 and x <= xn and y >= y0 and y <= yn:
                self.mouse_inside_working_area = True
            else:
                self.mouse_inside_working_area = False

            # Fix coordinates by removing margins of PyQT screen
            x -= x0
            y -= y0
            width = xn - x0
            height = yn - y0

            # Transform coordinates from PyQt (0, n) to Panda (-1, 1)
            Global.mainForm.simulation.mouse_x = pyqtToPanda(x, width)
            Global.mainForm.simulation.mouse_y = pyqtToPanda(y, height) * (-1)

            # Pass the movement commands to Panda
            if self.mouse_inside_working_area and Global.mainForm.simulation.mouse_feature == "":
                feature = ""
                if event.buttons() == QtCore.Qt.LeftButton:
                    feature = "rotate"
                elif event.buttons() == QtCore.Qt.MiddleButton:
                    feature = "pan"
                if feature != "":
                    start_fn = self.createStartMouseWorkFn(self.width() / 2, self.height() / 2)
                    stop_fn = self.createStopMouseWorkFn()
                    Global.mainForm.simulation.startMouseWork(feature, start_fn, stop_fn)

    def mousePressEvent(self, event):
        if self.isSimulating() and self.mouse_working_area is not None and event.buttons() == QtCore.Qt.RightButton:
            self.showContextMenu(event.pos())

    def mouseReleaseEvent(self, event):
        if self.isSimulating() and Global.mainForm.simulation.mouse_feature != "":
            Global.mainForm.simulation.stopMouseWork()

    def wheelEvent(self, event):
        if self.isSimulating()and self.mouse_inside_working_area:
            mouse_pos = event.pos()
            start_fn = self.createStartMouseWorkFn(mouse_pos.x(), mouse_pos.y())
            stop_fn = self.createStopMouseWorkFn()
            Global.mainForm.simulation.startMouseWork("zoom", start_fn, stop_fn)
            Global.mainForm.simulation.mouse_steps = event.angleDelta().y()

    def updateElements3d(self):
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

        x, y, z = node.tree3d_pos
        node.tree3d_pos = (x - offsetX, y, z)
        for feeder in Global.project.network.getFeederNodes(node):
            self.__centerNode(feeder, offsetX)

    def __invertNode(self, node, offsetZ):
        """
        Rearrange the node in order to tree is inverted from top to bottom.
        """
        x, y, z = node.tree3d_pos
        node.tree3d_pos = (x, y, offsetZ - z)
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

        xNode, yNode, zNode = node.tree3d_pos

        # Calculate the absolute position of each column
        for y in range(node.height):
            for x in range(node.width):
                # The absolute X is calculated by multiply its relative position with offset
                xCol = xNode + ((x0 + x) * self.offsetColumns)

                # The absolute Y is calculated by multiply its relative position with offset
                yCol = yNode + ((y0 + y) * self.offsetColumns)

                # Calculate positions of the columns of cells if node is a region
                # or input bits if node is a sensor
                zCol = zNode

                if node.type == NodeType.region:
                    column = node.getColumn(x, y)
                    column.tree3d_pos = (xCol, yCol, zCol)

                    # The proximal segment transverse all cells on this column
                    column.segment.tree3d_start_pos = (xCol, yCol, zCol + ((node.numCellsPerColumn - 1) * self.offsetCells))
                    column.segment.tree3d_end_pos = (xCol, yCol, zCol - self.offsetCells)    # Segment down towards to feeder nodes

                    # Calculate the absolute position of each cell
                    for z in range(len(column.cells)):
                        # The absolute Z is calculated by multiply its relative position with offset
                        cell = column.getCell(z)
                        cell.tree3d_pos = (xCol, yCol, zCol + (z * self.offsetCells))
                else:
                    bit = node.getBit(x, y)
                    bit.tree3d_pos = (xCol, yCol, zCol)

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
        node.tree3d_pos = (minX + (subtreeWidth / 2), 0, minZ + (depth / 2))

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
            color = self.ColorBitFalselyPredicted
        elif bit.isPredicted.atGivenStepAgo(Global.selStep) and self.menuShowBitsPredicted.isChecked():
            color = self.ColorBitPredicted
        elif bit.isActive.atGivenStepAgo(Global.selStep) and self.menuShowBitsActive.isChecked():
            color = self.ColorBitActive
        else:
            color = self.ColorInactive

        if isVisible:
            # Draw the input bit
            if not bit.tree3d_initialized:
                bit.tree3d_item_np = Global.mainForm.simulation.createBit(bit.tree3d_pos)
                bit.tree3d_initialized = True

            # Update the color
            if bit.tree3d_selected:
                color = self.ColorSelected
            bit.tree3d_item_np.setTexture(color)

        if bit.tree3d_item_np != None:
            bit.tree3d_item_np.show() if isVisible else bit.tree3d_item_np.hide()

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
            color = self.ColorCellFalselyPredicted
        elif cell.isPredicted.atGivenStepAgo(Global.selStep) and self.menuShowCellsPredicted.isChecked():
            color = self.ColorCellPredicted
        elif cell.isLearning.atGivenStepAgo(Global.selStep) and self.menuShowCellsLearning.isChecked():
            color = self.ColorCellLearning
        elif cell.isActive.atGivenStepAgo(Global.selStep) and self.menuShowCellsActive.isChecked():
            color = self.ColorCellActive
        elif self.menuShowCellsInactive.isChecked():
            color = self.ColorInactive
        else:
            isVisible = False

        if isVisible:
            # Draw the cell
            if not cell.tree3d_initialized:
                cell.tree3d_item_np = Global.mainForm.simulation.createCell(cell.tree3d_pos)
                cell.tree3d_initialized = True

            # Update the color
            if cell.tree3d_selected:
                color = self.ColorSelected
            cell.tree3d_item_np.setTexture(color)

        if cell.tree3d_item_np != None:
            cell.tree3d_item_np.show() if isVisible else cell.tree3d_item_np.hide()

        # Draw/update all distal segments
        for segment in cell.segments:
            segment.tree3d_start_pos = cell.tree3d_pos
            segment.tree3d_end_pos = self.__calculateSegmentEndPos(segment, segment.tree3d_start_pos)
            self.__drawSegment(segment)

    def __calculateSegmentEndPos(self, segment, start_pos):
        """
        Calculates an average position of the segment's end through their synapses' end positions.
        """
        xSeg1, ySeg1, zSeg1 = start_pos

        sumK = 0.
        numXBelow = 0
        numXAbove = 0
        for synapse in segment.synapses:
            xSyn, ySyn, zSyn = synapse.inputElem.tree3d_pos

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
        #    y = ax + b (where 'a' = 'k')
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
                    color = self.ColorSegmentFalselyPredicted
                else:
                    isVisible = False
            elif segment.isPredicted.atGivenStepAgo(Global.selStep):
                if segment.type == SegmentType.proximal and self.menuShowProximalSegmentsPredicted.isChecked():
                    color = self.ColorSegmentPredicted
                else:
                    isVisible = False
            elif segment.isActive.atGivenStepAgo(Global.selStep):
                if (segment.type == SegmentType.proximal and self.menuShowProximalSegmentsActive.isChecked()) or (segment.type == SegmentType.distal and self.menuShowDistalSegmentsActive.isChecked()):
                    color = self.ColorSegmentActive
                else:
                    isVisible = False
            else:
                if segment.type == SegmentType.proximal:
                    color = self.ColorInactive
                else:
                    isVisible = False

        if isVisible:
            # Draw the segment
            if not segment.tree3d_initialized:
                segment.tree3d_item_np = Global.mainForm.simulation.createSegment(segment.tree3d_start_pos, segment.tree3d_end_pos)
                segment.tree3d_initialized = True

            # Update the color
            if segment.tree3d_selected:
                color = self.ColorSelected
            segment.tree3d_item_np.setTexture(color)
        else:
            segment.tree3d_initialized = False
            if segment.tree3d_item_np is not None:
                Global.mainForm.simulation.removeElement(segment.tree3d_item_np)

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
                    color = self.ColorSynapseFalselyPredicted
                else:
                    isVisible = False
            elif synapse.isPredicted.atGivenStepAgo(Global.selStep):
                if (segment.type == SegmentType.proximal and self.menuShowProximalSynapsesPredicted.isChecked()):
                    color = self.ColorSynapsePredicted
                else:
                    isVisible = False
            elif synapse.isConnected.atGivenStepAgo(Global.selStep):
                if (segment.type == SegmentType.proximal and self.menuShowProximalSynapsesConnected.isChecked()) or (segment.type == SegmentType.distal and self.menuShowDistalSynapsesConnected.isChecked()):
                    color = self.ColorSynapseConnected
                else:
                    isVisible = False
            else:
                if (segment.type == SegmentType.proximal and self.menuShowProximalSynapsesActive.isChecked()) or (segment.type == SegmentType.distal and self.menuShowDistalSynapsesActive.isChecked()):
                    color = self.ColorInactive
                else:
                    isVisible = False

        if isVisible and segmentIsVisible:
            # Draw the synapse
            if not synapse.tree3d_initialized:
                synapse.tree3d_item_np = Global.mainForm.simulation.createSynapse(segment.tree3d_end_pos, synapse.inputElem.tree3d_pos)
                synapse.tree3d_initialized = True

            # Update the color
            if synapse.tree3d_selected:
                color = self.ColorSelected
            synapse.tree3d_item_np.setTexture(color)
        else:
            synapse.tree3d_initialized = False
            if synapse.tree3d_item_np is not None:
                Global.mainForm.simulation.removeElement(synapse.tree3d_item_np)

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
                self.updateElements3d()

                break

        # Disable change options for the 'Default' view
        defaultViewSelected = False
        if self.selectedViewMenu == self.defaultViewMenu:
            defaultViewSelected = True
        self.menuViewsSave.setEnabled(not defaultViewSelected)
        self.menuViewsDelete.setEnabled(not defaultViewSelected)

    def menuLegend_click(self, event):
        simulationLegendForm = SimulationLegendForm()
        simulationLegendForm.exec_()

    def menuShowBits_click(self, event):
        menuClicked = self.sender()

        if menuClicked == self.menuShowBitsNone:
            if self.menuShowBitsNone.isChecked():
                self.menuShowBitsActive.setChecked(False)
                self.menuShowBitsPredicted.setChecked(False)
                self.menuShowBitsFalselyPredicted.setChecked(False)
        else:
            self.menuShowBitsNone.setChecked(False)

        self.updateElements3d()

    def menuShowCells_click(self, event):
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

        self.updateElements3d()

    def menuShowProximalSegments_click(self, event):
        menuClicked = self.sender()

        if menuClicked == self.menuShowProximalSegmentsNone:
            if self.menuShowProximalSegmentsNone.isChecked():
                self.menuShowProximalSegmentsActive.setChecked(False)
                self.menuShowProximalSegmentsPredicted.setChecked(False)
                self.menuShowProximalSegmentsFalselyPredicted.setChecked(False)
        else:
            self.menuShowProximalSegmentsNone.setChecked(False)

        self.updateElements3d()

    def menuShowProximalSynapses_click(self, event):
        menuClicked = self.sender()

        if menuClicked == self.menuShowProximalSynapsesNone:
            if self.menuShowProximalSynapsesNone.isChecked():
                self.menuShowProximalSynapsesConnected.setChecked(False)
                self.menuShowProximalSynapsesActive.setChecked(False)
                self.menuShowProximalSynapsesPredicted.setChecked(False)
                self.menuShowProximalSynapsesFalselyPredicted.setChecked(False)
        else:
            self.menuShowProximalSynapsesNone.setChecked(False)

        self.updateElements3d()

    def menuShowDistalSegments_click(self, event):
        menuClicked = self.sender()

        if menuClicked == self.menuShowDistalSegmentsNone:
            if self.menuShowDistalSegmentsNone.isChecked():
                self.menuShowDistalSegmentsActive.setChecked(False)
        else:
            self.menuShowDistalSegmentsNone.setChecked(False)

        self.updateElements3d()

    def menuShowDistalSynapses_click(self, event):
        menuClicked = self.sender()

        if menuClicked == self.menuShowDistalSynapsesNone:
            if self.menuShowDistalSynapsesNone.isChecked():
                self.menuShowDistalSynapsesConnected.setChecked(False)
                self.menuShowDistalSynapsesActive.setChecked(False)
        else:
            self.menuShowDistalSynapsesNone.setChecked(False)

        self.updateElements3d()

    def menuView_click(self, event):
        menuClicked = self.sender()
        self.selectView(menuClicked)

    def menuViewsNew_click(self, event):

        # Ask for views's name
        enteredText, ok = QtWidgets.QInputDialog.getText(self, "Input Dialog", "Enter views' name:")
        if ok:
            view = View()
            view.name = enteredText
            view.menu = QtWidgets.QAction(self)
            view.menu.setText(view.name)
            view.menu.setCheckable(True)
            view.menu.triggered.connect(self.menuView_click)

            Global.views.append(view)
            self.menuViews.addAction(view.menu)

            self.selectView(view.menu)

    def menuViewsSave_click(self, event):

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

    def menuViewsDelete_click(self, event):

        # Find the specified view in the views list
        for view in Global.views:
            if view.menu == self.selectedViewMenu:
                Global.views.remove(view)
                self.menuViews.removeAction(view.menu)
                break

        # Set 'Default' view as initial view
        self.selectView(self.defaultViewMenu)
