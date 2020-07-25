import numpy
import os
from PIL import Image
from PyQt5 import QtGui, QtCore, QtWidgets
from nupic_studio.htm.node import Node, NodeType
from nupic_studio.htm.segment import SegmentType
from nupic_studio.ui import Global, State, NEW_VIEW
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
        self.setWindowIcon(QtGui.QIcon(Global.app_path + '/images/logo.ico'))
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
        self.default_view = None
        self.selected_view = None

        # Tree
        self.top_region = None
        self.tree_width = 0
        self.tree_height = 0

        # Space to skip horizontally between siblings and vertically between generations
        self.offset_horizontal_nodes = 20
        self.offset_vertical_nodes = 25

        # Horizontal space between two columns
        self.offset_columns = 10

        # Vertical space between two cells
        self.offset_cells = 5

        self.initUI()

        # Create views menus
        for view in Global.views:
            menu = QtWidgets.QAction(self)
            menu.setText(view['name'])
            menu.setCheckable(True)
            menu.triggered.connect(self.menuView_click)
            self.menu_views.addAction(menu)
            view['menu'] = menu

            # If this is the first menu, set it as default
            if self.default_view is None:
                self.default_view = view

        # Load default view
        self.selectView(self.default_view)

    def initUI(self):

        # menu_views_new
        self.menu_views_new = QtWidgets.QAction(self)
        self.menu_views_new.setText("Create new view")
        self.menu_views_new.triggered.connect(self.menuViewsNew_click)

        # menu_views_save
        self.menu_views_save = QtWidgets.QAction(self)
        self.menu_views_save.setText("Save selected view")
        self.menu_views_save.triggered.connect(self.menuViewsSave_click)

        # menu_views_delete
        self.menu_views_delete = QtWidgets.QAction(self)
        self.menu_views_delete.setText("Delete selected view")
        self.menu_views_delete.triggered.connect(self.menuViewsDelete_click)

        # menu_views
        self.menu_views = QtWidgets.QMenu()
        self.menu_views.addAction(self.menu_views_new)
        self.menu_views.addAction(self.menu_views_save)
        self.menu_views.addAction(self.menu_views_delete)
        self.menu_views.addSeparator()
        self.menu_views.setTitle("&View")

        # menu_show_bits_none
        self.menu_show_bits_none = QtWidgets.QAction(self)
        self.menu_show_bits_none.setText("&None")
        self.menu_show_bits_none.setCheckable(True)
        self.menu_show_bits_none.triggered.connect(self.menuShowBits_click)

        # menu_show_bits_active
        self.menu_show_bits_active = QtWidgets.QAction(self)
        self.menu_show_bits_active.setText("&Active")
        self.menu_show_bits_active.setCheckable(True)
        self.menu_show_bits_active.triggered.connect(self.menuShowBits_click)

        # menu_show_bits_predicted
        self.menu_show_bits_predicted = QtWidgets.QAction(self)
        self.menu_show_bits_predicted.setText("&Predicted")
        self.menu_show_bits_predicted.setCheckable(True)
        self.menu_show_bits_predicted.triggered.connect(self.menuShowBits_click)

        # menu_show_bits_falsely_predicted
        self.menu_show_bits_falsely_predicted = QtWidgets.QAction(self)
        self.menu_show_bits_falsely_predicted.setText("&Falsely Predicted")
        self.menu_show_bits_falsely_predicted.setCheckable(True)
        self.menu_show_bits_falsely_predicted.triggered.connect(self.menuShowBits_click)

        # menu_show_bits
        self.menu_show_bits = QtWidgets.QMenu()
        self.menu_show_bits.addAction(self.menu_show_bits_none)
        self.menu_show_bits.addAction(self.menu_show_bits_active)
        self.menu_show_bits.addAction(self.menu_show_bits_predicted)
        self.menu_show_bits.addAction(self.menu_show_bits_falsely_predicted)
        self.menu_show_bits.setTitle("&Sensor bits")

        # menu_show_cells_none
        self.menu_show_cells_none = QtWidgets.QAction(self)
        self.menu_show_cells_none.setText("&None")
        self.menu_show_cells_none.setCheckable(True)
        self.menu_show_cells_none.triggered.connect(self.menuShowCells_click)

        # menu_show_cells_learning
        self.menu_show_cells_learning = QtWidgets.QAction(self)
        self.menu_show_cells_learning.setText("&Learning")
        self.menu_show_cells_learning.setCheckable(True)
        self.menu_show_cells_learning.triggered.connect(self.menuShowCells_click)

        # menu_show_cells_active
        self.menu_show_cells_active = QtWidgets.QAction(self)
        self.menu_show_cells_active.setText("&Active")
        self.menu_show_cells_active.setCheckable(True)
        self.menu_show_cells_active.triggered.connect(self.menuShowCells_click)

        # menu_show_cells_inactive
        self.menu_show_cells_inactive = QtWidgets.QAction(self)
        self.menu_show_cells_inactive.setText("&Inactive")
        self.menu_show_cells_inactive.setCheckable(True)
        self.menu_show_cells_inactive.triggered.connect(self.menuShowCells_click)

        # menu_show_cells_predicted
        self.menu_show_cells_predicted = QtWidgets.QAction(self)
        self.menu_show_cells_predicted.setText("&Predicted")
        self.menu_show_cells_predicted.setCheckable(True)
        self.menu_show_cells_predicted.triggered.connect(self.menuShowCells_click)

        # menu_show_cells_falsely_predicted
        self.menu_show_cells_falsely_predicted = QtWidgets.QAction(self)
        self.menu_show_cells_falsely_predicted.setText("&Falsely Predicted")
        self.menu_show_cells_falsely_predicted.setCheckable(True)
        self.menu_show_cells_falsely_predicted.triggered.connect(self.menuShowCells_click)

        # menu_show_cells
        self.menu_show_cells = QtWidgets.QMenu()
        self.menu_show_cells.addAction(self.menu_show_cells_none)
        self.menu_show_cells.addAction(self.menu_show_cells_learning)
        self.menu_show_cells.addAction(self.menu_show_cells_active)
        self.menu_show_cells.addAction(self.menu_show_cells_predicted)
        self.menu_show_cells.addAction(self.menu_show_cells_falsely_predicted)
        self.menu_show_cells.addAction(self.menu_show_cells_inactive)
        self.menu_show_cells.setTitle("C&ells")

        # menu_show_proximal_segments_none
        self.menu_show_proximal_segments_none = QtWidgets.QAction(self)
        self.menu_show_proximal_segments_none.setText("&None")
        self.menu_show_proximal_segments_none.setCheckable(True)
        self.menu_show_proximal_segments_none.triggered.connect(self.menuShowProximalSegments_click)

        # menu_show_proximal_segments_active
        self.menu_show_proximal_segments_active = QtWidgets.QAction(self)
        self.menu_show_proximal_segments_active.setText("&Active")
        self.menu_show_proximal_segments_active.setCheckable(True)
        self.menu_show_proximal_segments_active.triggered.connect(self.menuShowProximalSegments_click)

        # menu_show_proximal_segments_predicted
        self.menu_show_proximal_segments_predicted = QtWidgets.QAction(self)
        self.menu_show_proximal_segments_predicted.setText("&Predicted")
        self.menu_show_proximal_segments_predicted.setCheckable(True)
        self.menu_show_proximal_segments_predicted.triggered.connect(self.menuShowProximalSegments_click)

        # menu_show_proximal_segments_falsely_predicted
        self.menu_show_proximal_segments_falsely_predicted = QtWidgets.QAction(self)
        self.menu_show_proximal_segments_falsely_predicted.setText("&Falsely Predicted")
        self.menu_show_proximal_segments_falsely_predicted.setCheckable(True)
        self.menu_show_proximal_segments_falsely_predicted.triggered.connect(self.menuShowProximalSegments_click)

        # menu_show_proximal_segments
        self.menu_show_proximal_segments = QtWidgets.QMenu()
        self.menu_show_proximal_segments.addAction(self.menu_show_proximal_segments_none)
        self.menu_show_proximal_segments.addAction(self.menu_show_proximal_segments_active)
        self.menu_show_proximal_segments.addAction(self.menu_show_proximal_segments_predicted)
        self.menu_show_proximal_segments.addAction(self.menu_show_proximal_segments_falsely_predicted)
        self.menu_show_proximal_segments.setTitle("&Segments")

        # menu_show_proximal_synapses_none
        self.menu_show_proximal_synapses_none = QtWidgets.QAction(self)
        self.menu_show_proximal_synapses_none.setText("&None")
        self.menu_show_proximal_synapses_none.setCheckable(True)
        self.menu_show_proximal_synapses_none.triggered.connect(self.menuShowProximalSynapses_click)

        # menu_show_proximal_synapses_connected
        self.menu_show_proximal_synapses_connected = QtWidgets.QAction(self)
        self.menu_show_proximal_synapses_connected.setText("&Connected")
        self.menu_show_proximal_synapses_connected.setCheckable(True)
        self.menu_show_proximal_synapses_connected.triggered.connect(self.menuShowProximalSynapses_click)

        # menu_show_proximal_synapses_active
        self.menu_show_proximal_synapses_active = QtWidgets.QAction(self)
        self.menu_show_proximal_synapses_active.setText("&Active")
        self.menu_show_proximal_synapses_active.setCheckable(True)
        self.menu_show_proximal_synapses_active.triggered.connect(self.menuShowProximalSynapses_click)

        # menu_show_proximal_synapses_predicted
        self.menu_show_proximal_synapses_predicted = QtWidgets.QAction(self)
        self.menu_show_proximal_synapses_predicted.setText("&Predicted")
        self.menu_show_proximal_synapses_predicted.setCheckable(True)
        self.menu_show_proximal_synapses_predicted.triggered.connect(self.menuShowProximalSynapses_click)

        # menu_show_proximal_synapses_falsely_predicted
        self.menu_show_proximal_synapses_falsely_predicted = QtWidgets.QAction(self)
        self.menu_show_proximal_synapses_falsely_predicted.setText("&Falsely Predicted")
        self.menu_show_proximal_synapses_falsely_predicted.setCheckable(True)
        self.menu_show_proximal_synapses_falsely_predicted.triggered.connect(self.menuShowProximalSynapses_click)

        # menu_show_proximal_synapses
        self.menu_show_proximal_synapses = QtWidgets.QMenu()
        self.menu_show_proximal_synapses.addAction(self.menu_show_proximal_synapses_none)
        self.menu_show_proximal_synapses.addAction(self.menu_show_proximal_synapses_connected)
        self.menu_show_proximal_synapses.addAction(self.menu_show_proximal_synapses_active)
        self.menu_show_proximal_synapses.addAction(self.menu_show_proximal_synapses_predicted)
        self.menu_show_proximal_synapses.addAction(self.menu_show_proximal_synapses_falsely_predicted)
        self.menu_show_proximal_synapses.setTitle("&Synapses")

        # menu_show_proximal
        self.menu_show_proximal = QtWidgets.QMenu()
        self.menu_show_proximal.addMenu(self.menu_show_proximal_segments)
        self.menu_show_proximal.addMenu(self.menu_show_proximal_synapses)
        self.menu_show_proximal.setTitle("&Proximal")

        # menu_show_distal_segments_none
        self.menu_show_distal_segments_none = QtWidgets.QAction(self)
        self.menu_show_distal_segments_none.setText("&None")
        self.menu_show_distal_segments_none.setCheckable(True)
        self.menu_show_distal_segments_none.triggered.connect(self.menuShowDistalSegments_click)

        # menu_show_distal_segments_active
        self.menu_show_distal_segments_active = QtWidgets.QAction(self)
        self.menu_show_distal_segments_active.setText("&Active")
        self.menu_show_distal_segments_active.setCheckable(True)
        self.menu_show_distal_segments_active.triggered.connect(self.menuShowDistalSegments_click)

        # menu_show_distal_segments
        self.menu_show_distal_segments = QtWidgets.QMenu()
        self.menu_show_distal_segments.addAction(self.menu_show_distal_segments_none)
        self.menu_show_distal_segments.addAction(self.menu_show_distal_segments_active)
        self.menu_show_distal_segments.setTitle("&Segments")

        # menu_show_distal_synapses_none
        self.menu_show_distal_synapses_none = QtWidgets.QAction(self)
        self.menu_show_distal_synapses_none.setText("&None")
        self.menu_show_distal_synapses_none.setCheckable(True)
        self.menu_show_distal_synapses_none.triggered.connect(self.menuShowDistalSynapses_click)

        # menu_show_distal_synapses_connected
        self.menu_show_distal_synapses_connected = QtWidgets.QAction(self)
        self.menu_show_distal_synapses_connected.setText("&Connected")
        self.menu_show_distal_synapses_connected.setCheckable(True)
        self.menu_show_distal_synapses_connected.triggered.connect(self.menuShowDistalSynapses_click)

        # menu_show_distal_synapses_active
        self.menu_show_distal_synapses_active = QtWidgets.QAction(self)
        self.menu_show_distal_synapses_active.setText("&Active")
        self.menu_show_distal_synapses_active.setCheckable(True)
        self.menu_show_distal_synapses_active.triggered.connect(self.menuShowDistalSynapses_click)

        # menu_show_distal_synapses
        self.menu_show_distal_synapses = QtWidgets.QMenu()
        self.menu_show_distal_synapses.addAction(self.menu_show_distal_synapses_none)
        self.menu_show_distal_synapses.addAction(self.menu_show_distal_synapses_connected)
        self.menu_show_distal_synapses.addAction(self.menu_show_distal_synapses_active)
        self.menu_show_distal_synapses.setTitle("&Synapses")

        # menu_show_distal
        self.menu_show_distal = QtWidgets.QMenu()
        self.menu_show_distal.addMenu(self.menu_show_distal_segments)
        self.menu_show_distal.addMenu(self.menu_show_distal_synapses)
        self.menu_show_distal.setTitle("&Distal")

        # menu_show
        self.menu_show = QtWidgets.QMenu()
        self.menu_show.addMenu(self.menu_show_bits)
        self.menu_show.addMenu(self.menu_show_cells)
        self.menu_show.addMenu(self.menu_show_proximal)
        self.menu_show.addMenu(self.menu_show_distal)
        self.menu_show.setTitle("&Show")

        # menu_legend
        self.menu_legend = QtWidgets.QAction(self)
        self.menu_legend.setText("&Legend")
        self.menu_legend.triggered.connect(self.menuLegend_click)

        # menu_simulation
        self.menu_simulation = QtWidgets.QMenu()
        self.menu_simulation.addMenu(self.menu_views)
        self.menu_simulation.addMenu(self.menu_show)
        self.menu_simulation.addAction(self.menu_legend)
        self.menu_simulation.setTitle("&Simulation")

        # image
        self.pivot_image = QtGui.QImage(os.path.join(Global.app_path + '/images', 'cross.png'))

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
        self.top_region = top_region

        # Set the colors of the states.
        self.COLOR_INACTIVE = Texture3D.GRAY
        self.COLOR_SELECTED = Texture3D.BLUE
        self.COLOR_BIT_ACTIVE = Texture3D.Green
        self.COLOR_BIT_PREDICTED = Texture3D.YELLOW
        self.COLOR_BIT_FALSELY_PREDICTED = Texture3D.RED
        self.COLOR_CELL_LEARNING = Texture3D.GREEN_YELLOW
        self.COLOR_CELL_ACTIVE = Texture3D.Green
        self.COLOR_CELL_PREDICTED = Texture3D.YELLOW
        self.COLOR_CELL_FALSELY_PREDICTED = Texture3D.RED
        self.COLOR_SEGMENT_ACTIVE = Texture3D.Green
        self.COLOR_SEGMENT_PREDICTED = Texture3D.YELLOW
        self.COLOR_SEGMENT_FALSELY_PREDICTED = Texture3D.RED
        self.COLOR_SYNAPSE_CONNECTED = Texture3D.Green
        self.COLOR_SYNAPSE_PREDICTED = Texture3D.YELLOW
        self.COLOR_SYNAPSE_FALSELY_PREDICTED = Texture3D.RED

        # Arrange the tree once to see how big it is.
        self.tree_width = 0
        self.tree_height = 0
        self.arrangeNode(self.top_region, 0, 0)

        x, _, _ = self.top_region.tree3d_pos

        # Rearrange the tree again to center it horizontally.
        self.centerNode(self.top_region, x)

        # Rearrange the tree again to invert it vertically.
        self.invertNode(self.top_region, 50)

        # Once we have the final position of the regions, we can calculate the position of every column and cell.
        self.calculateNodeElementsPosition(self.top_region)

        # Draw the tree recursively from top region.
        self.drawNode(self.top_region, True)

    def clear(self):
        """
        Reset all controls.
        """
        self.mouse_working_area = None

    def update(self):
        """
        Refresh controls for each time step.
        """
        if Global.main_form.isRunning():

            # Get the image to be draw on this viewer.
            image = None
            if Global.main_form.state == State.SIMULATING:
                texture = Global.main_form.simulation.screen_texture
                size = (texture.getXSize(), texture.getYSize())
                format = "RGBA"
                if texture.mightHaveRamImage():
                    image = Image.frombuffer(format, size, texture.getRamImageAs(format), "raw", format, 0, 0)
                else:
                    image = Image.new(format, size)
            elif Global.main_form.state == State.PLAYBACKING:
                playback_file = os.path.join(Global.main_form.getRecordPath(), "main_camera_" + "{:08d}".format(Global.main_form.get_step()) + ".png")
                if os.path.isfile(playback_file):
                    image = Image.open(playback_file)

            # Draw the image.
            image = image.toqimage()
            self.pixel_map = QtGui.QPixmap.fromImage(image)
            self.adjustMouseWorkingArea()

    def showContextMenu(self, pos):
        """
        Event handling right-click contextMenu
        """
        if Global.simulation_initialized:
            self.menu_simulation.exec_(self.mapToGlobal(pos))
        else:
            QtWidgets.QMessageBox.information(self, "Information", "Context menu available only during the simulation.")

    def adjustMouseWorkingArea(self):
        viewer_size = self.size()
        self.setPixmap(self.pixel_map.scaled(viewer_size, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        image_size = self.pixmap().size()
        horizontal_margin = (viewer_size.width() - image_size.width()) / 2
        vertical_margin = (viewer_size.height() - image_size.height()) / 2
        self.mouse_working_area = (horizontal_margin, vertical_margin, horizontal_margin + image_size.width(), vertical_margin + image_size.height())

    def resizeEvent(self, event):
        if self.mouse_working_area is not None:
            self.adjustMouseWorkingArea()

    def handleKeyEvent(self, event, event_state):
        # Inform Panda to start (or continue) the action associated with the key pressed
        # or stop it if key is released
        key_pressed = event.key()

        # Check if key is in the user's key map an then call associated function
        for k, value in Global.main_form.simulation.key_map.items():
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
        return (Global.main_form.state == State.SIMULATING and not Global.main_form.paused) and Global.main_form.simulation is not None

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
            Global.main_form.simulation.resetCamera()

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
            Global.main_form.simulation.mouse_x = pyqtToPanda(x, width)
            Global.main_form.simulation.mouse_y = pyqtToPanda(y, height) * (-1)

            # Pass the movement commands to Panda
            if self.mouse_inside_working_area and Global.main_form.simulation.mouse_feature == "":
                feature = ""
                if event.buttons() == QtCore.Qt.LeftButton:
                    feature = "rotate"
                elif event.buttons() == QtCore.Qt.MiddleButton:
                    feature = "pan"
                if feature != "":
                    start_fn = self.createStartMouseWorkFn(self.width() / 2, self.height() / 2)
                    stop_fn = self.createStopMouseWorkFn()
                    Global.main_form.simulation.startMouseWork(feature, start_fn, stop_fn)

    def mousePressEvent(self, event):
        if self.isSimulating() and self.mouse_working_area is not None and event.buttons() == QtCore.Qt.RightButton:
            self.showContextMenu(event.pos())

    def mouseReleaseEvent(self, event):
        if self.isSimulating() and Global.main_form.simulation.mouse_feature != "":
            Global.main_form.simulation.stopMouseWork()

    def wheelEvent(self, event):
        if self.isSimulating()and self.mouse_inside_working_area:
            mouse_pos = event.pos()
            start_fn = self.createStartMouseWorkFn(mouse_pos.x(), mouse_pos.y())
            stop_fn = self.createStopMouseWorkFn()
            Global.main_form.simulation.startMouseWork("zoom", start_fn, stop_fn)
            Global.main_form.simulation.mouse_steps = event.angleDelta().y()

    def updateElements3d(self):
        """
        Refresh controls for each time step.
        """
        if Global.simulation_initialized:
            # Draw the tree recursively from top region.
            self.drawNode(self.top_region, False)

    def centerNode(self, node, offset_x):
        """
        Rearrange the node in order to tree is in the center (0, 0, 0) of the scene.
        """
        x, y, z = node.tree3d_pos
        node.tree3d_pos = (x - offset_x, y, z)
        for feeder in Global.project.network.getFeederNodes(node):
            self.centerNode(feeder, offset_x)

    def invertNode(self, node, offset_z):
        """
        Rearrange the node in order to tree is inverted from top to bottom.
        """
        x, y, z = node.tree3d_pos
        node.tree3d_pos = (x, y, offset_z - z)
        for feeder in Global.project.network.getFeederNodes(node):
            self.invertNode(feeder, offset_z)

    def calculateNodeElementsPosition(self, node):
        """
        Calculate the position of columns and cells of this node.
        """

        # Calculate the relative position of the first column (0, 0)
        # The purpose is we have symmetrical positions. If a node has 30 columns in X axis, then the relative X of the first column is -15 while the last is 15.
        x0 = (node.width / 2) * (-1)
        y0 = (node.height / 2) * (-1)

        x_node, y_node, z_node = node.tree3d_pos

        # Calculate the absolute position of each column
        for y in range(node.height):
            for x in range(node.width):
                # The absolute X is calculated by multiply its relative position with offset
                x_col = x_node + ((x0 + x) * self.offset_columns)

                # The absolute Y is calculated by multiply its relative position with offset
                y_col = y_node + ((y0 + y) * self.offset_columns)

                # Calculate positions of the columns of cells if node is a region
                # or input bits if node is a sensor
                z_col = z_node

                if node.type == NodeType.REGION:
                    column = node.getColumn(x, y)
                    column.tree3d_pos = (x_col, y_col, z_col)

                    # The proximal segment transverse all cells on this column
                    column.segment.tree3d_start_pos = (x_col, y_col, z_col + ((node.cells_per_column - 1) * self.offset_cells))
                    column.segment.tree3d_end_pos = (x_col, y_col, z_col - self.offset_cells)    # Segment down towards to feeder nodes

                    # Calculate the absolute position of each cell
                    for z in range(len(column.cells)):
                        # The absolute Z is calculated by multiply its relative position with offset
                        cell = column.getCell(z)
                        cell.tree3d_pos = (x_col, y_col, z_col + (z * self.offset_cells))
                else:
                    bit = node.getBit(x, y)
                    bit.tree3d_pos = (x_col, y_col, z_col)

        # Perform the same actions for the lower nodes that feed this node
        for feeder in Global.project.network.getFeederNodes(node):
            self.calculateNodeElementsPosition(feeder)

    def arrangeNode(self, node, min_x, min_z):
        """
        Arrange the node and the lower nodes that feed it in the allowed area.
        Set min_x to indicate the right edge of our subtree.
        Set min_z to indicate the bottom edge of our subtree.
        """

        # See how big this node is.
        width = node.width * self.offset_columns
        height = node.height
        if node.type == NodeType.REGION:
            depth = node.cells_per_column * self.offset_cells
        else:
            depth = self.offset_cells

        # Recursively arrange the lower nodes that feed this node,
        # allowing room for this node.
        x = min_x
        biggest_min_z = min_z + depth
        subtree_min_z = min_z + depth + self.offset_vertical_nodes
        feeders_count = 0
        for feeder in Global.project.network.getFeederNodes(node):
            # Arrange this feeder's subtree.
            feeder_min_z = subtree_min_z
            x, feeder_min_z = self.arrangeNode(feeder, x, feeder_min_z)

            # See if this increases the biggest min_z value.
            if biggest_min_z < feeder_min_z:
                biggest_min_z = feeder_min_z

            # Allow room before the next sibling.
            x += self.offset_horizontal_nodes

            feeders_count += 1

        # Remove the spacing after the last feeder.
        if feeders_count > 0:
            x -= self.offset_horizontal_nodes

        # See if this node is wider than the subtree under it.
        subtree_width = x - min_x
        if width > subtree_width:
            # Center the subtree under this node.
            # Make the lower nodes that feed this node rearrange themselves
            # moved to center their subtrees.
            x = min_x + (width - subtree_width) / 2
            for feeder in Global.project.network.getFeederNodes(node):
                # Arrange this feeder's subtree.
                x, subtree_min_z = self.arrangeNode(feeder, x, subtree_min_z)

                # Allow room before the next sibling.
                x += self.offset_horizontal_nodes

            # The subtree's width is this node's width.
            subtree_width = width

        # Set this node's center position.
        node.tree3d_pos = (min_x + (subtree_width / 2), 0, min_z + (depth / 2))

        # Increase min_x to allow room for the subtree before returning.
        min_x += subtree_width

        if subtree_width > self.tree_width:
            self.tree_width = subtree_width

        if height > self.tree_height:
            self.tree_height = height

        # Set the return value for min_z.
        min_z = biggest_min_z

        return min_x, min_z

    def drawNode(self, node, initialize):
        """
        Draw the nodes for the subtree rooted at this node.
        """

        # Recursively make the node draw its feeders.
        for feeder in Global.project.network.getFeederNodes(node):
            self.drawNode(feeder, initialize)

        # Draw a column of cells if node is a region
        # or an input bit if node is a sensor
        if node.type == NodeType.REGION:
            for column in node.columns:
                if initialize:
                    for cell in column.cells:
                        cell.tree3d_initialized = False
                self.drawColumn(column)
        else:
            for bit in node.bits:
                if initialize:
                    bit.tree3d_initialized = False
                self.drawBit(bit)

    def drawBit(self, bit):

        # Update properties according to state
        is_visible = True
        if self.menu_show_bits_none.isChecked():
            is_visible = False
        elif bit.is_falsely_predicted.atGivenStepAgo(Global.sel_step) and self.menu_show_bits_falsely_predicted.isChecked():
            color = self.COLOR_BIT_FALSELY_PREDICTED
        elif bit.is_predicted.atGivenStepAgo(Global.sel_step) and self.menu_show_bits_predicted.isChecked():
            color = self.COLOR_BIT_PREDICTED
        elif bit.is_active.atGivenStepAgo(Global.sel_step) and self.menu_show_bits_active.isChecked():
            color = self.COLOR_BIT_ACTIVE
        else:
            color = self.COLOR_INACTIVE

        if is_visible:
            # Draw the input bit
            if not bit.tree3d_initialized:
                bit.tree3d_item_np = Global.main_form.simulation.createBit(bit.tree3d_pos)
                bit.tree3d_initialized = True

            # Update the color
            if bit.tree3d_selected:
                color = self.COLOR_SELECTED
            bit.tree3d_item_np.setTexture(color)

        if bit.tree3d_item_np != None:
            bit.tree3d_item_np.show() if is_visible else bit.tree3d_item_np.hide()

    def drawColumn(self, column):

        # Update proximal segment
        self.drawSegment(column.segment)
        for cell in column.cells:
            self.drawCell(cell)

    def drawCell(self, cell):

        # Update properties according to state
        is_visible = True
        if self.menu_show_cells_none.isChecked():
            is_visible = False
        elif cell.is_falsely_predicted.atGivenStepAgo(Global.sel_step) and self.menu_show_cells_falsely_predicted.isChecked():
            color = self.COLOR_CELL_FALSELY_PREDICTED
        elif cell.is_predicted.atGivenStepAgo(Global.sel_step) and self.menu_show_cells_predicted.isChecked():
            color = self.COLOR_CELL_PREDICTED
        elif cell.is_learning.atGivenStepAgo(Global.sel_step) and self.menu_show_cells_learning.isChecked():
            color = self.COLOR_CELL_LEARNING
        elif cell.is_active.atGivenStepAgo(Global.sel_step) and self.menu_show_cells_active.isChecked():
            color = self.COLOR_CELL_ACTIVE
        elif self.menu_show_cells_inactive.isChecked():
            color = self.COLOR_INACTIVE
        else:
            is_visible = False

        if is_visible:
            # Draw the cell
            if not cell.tree3d_initialized:
                cell.tree3d_item_np = Global.main_form.simulation.createCell(cell.tree3d_pos)
                cell.tree3d_initialized = True

            # Update the color
            if cell.tree3d_selected:
                color = self.COLOR_SELECTED
            cell.tree3d_item_np.setTexture(color)

        if cell.tree3d_item_np != None:
            cell.tree3d_item_np.show() if is_visible else cell.tree3d_item_np.hide()

        # Draw/update all distal segments
        for segment in cell.segments:
            segment.tree3d_start_pos = cell.tree3d_pos
            segment.tree3d_end_pos = self.calculateSegmentEndPos(segment, segment.tree3d_start_pos)
            self.drawSegment(segment)

    def calculateSegmentEndPos(self, segment, start_pos):
        """
        Calculates an average position of the segment's end through their synapses' end positions.
        """
        x_seg1, y_seg1, z_seg1 = start_pos

        sum_k = 0.0
        num_x_below = 0
        num_x_above = 0
        for synapse in segment.synapses:
            x_syn, y_syn, z_syn = synapse.input_elem.tree3d_pos

            # Calculate 'k' (slope) of the straight line representing this synapse
            delta_y = y_syn - y_seg1
            delta_x = x_syn - x_seg1
            if delta_x != 0:
                k = float(delta_y / delta_x)
            else:
                k = 3
            sum_k += k

            if x_syn >= x_seg1:
                num_x_above += 1
            else:
                num_x_below += 1

        # Calculate direction of the straight line with base on the number of synapses X's below or above the segment X's
        if num_x_above >= num_x_below:
            direction = 1
        else:
            direction = -1

        # Calculate the 'k' (slope) of the new straight line representing this segment
        # It is an average value among the 'k' of the synapses
        k = 0
        if len(segment.synapses) > 0:
            k = int(sum_k / len(segment.synapses))

        # Find the 'b' of the straight line equation using 'k' and segment's start position:
        #    y = ax + b (where 'a' = 'k')
        b = y_seg1 - (k * x_seg1)

        # Calculate the segment's end position
        # TODO: Optimize this routine, i.e. discard loop to find max value
        max_x = x_seg1 + ((self.offset_columns / 3) * direction)
        max_y = y_seg1 + ((self.offset_columns / 3) * direction)
        inc_x = (self.offset_columns / 10) * direction
        x_seg2 = x_seg1
        while True:
            y_seg2 = (x_seg2 * k) + b
            if ((x_seg2 <= max_x or y_seg2 <= max_y) and direction < 0) or ((x_seg2 >= max_x or y_seg2 >= max_y) and direction > 0):
                break
            x_seg2 += inc_x
        z_seg2 = z_seg1

        return int(x_seg2), int(y_seg2), z_seg2

    def drawSegment(self, segment):

        # Update properties according to state
        is_visible = True
        if segment.is_removed.atGivenStepAgo(Global.sel_step) or (segment.type == SegmentType.PROXIMAL and self.menu_show_proximal_segments_none.isChecked()) or (segment.type == SegmentType.DISTAL and self.menu_show_distal_segments_none.isChecked()):
            is_visible = False
        else:
            if segment.is_falsely_predicted.atGivenStepAgo(Global.sel_step):
                if segment.type == SegmentType.PROXIMAL and self.menu_show_proximal_segments_falsely_predicted.isChecked():
                    color = self.COLOR_SEGMENT_FALSELY_PREDICTED
                else:
                    is_visible = False
            elif segment.is_predicted.atGivenStepAgo(Global.sel_step):
                if segment.type == SegmentType.PROXIMAL and self.menu_show_proximal_segments_predicted.isChecked():
                    color = self.COLOR_SEGMENT_PREDICTED
                else:
                    is_visible = False
            elif segment.is_active.atGivenStepAgo(Global.sel_step):
                if (segment.type == SegmentType.PROXIMAL and self.menu_show_proximal_segments_active.isChecked()) or (segment.type == SegmentType.DISTAL and self.menu_show_distal_segments_active.isChecked()):
                    color = self.COLOR_SEGMENT_ACTIVE
                else:
                    is_visible = False
            else:
                if segment.type == SegmentType.PROXIMAL:
                    color = self.COLOR_INACTIVE
                else:
                    is_visible = False

        if is_visible:
            # Draw the segment
            if not segment.tree3d_initialized:
                segment.tree3d_item_np = Global.main_form.simulation.createSegment(segment.tree3d_start_pos, segment.tree3d_end_pos)
                segment.tree3d_initialized = True

            # Update the color
            if segment.tree3d_selected:
                color = self.COLOR_SELECTED
            segment.tree3d_item_np.setTexture(color)
        else:
            segment.tree3d_initialized = False
            if segment.tree3d_item_np is not None:
                Global.main_form.simulation.removeElement(segment.tree3d_item_np)

        # Draw/update all synapses of this segment
        for synapse in segment.synapses:
            self.drawSynapse(segment, synapse, is_visible)

    def drawSynapse(self, segment, synapse, segment_is_visible):

        # Update properties according to state
        is_visible = True
        if synapse.is_removed.atGivenStepAgo(Global.sel_step) or (not segment.is_active.atGivenStepAgo(Global.sel_step) and not segment.is_predicted.atGivenStepAgo(Global.sel_step) and not segment.is_falsely_predicted.atGivenStepAgo(Global.sel_step)) or (segment.type == SegmentType.PROXIMAL and self.menu_show_proximal_synapses_none.isChecked()) or (segment.type == SegmentType.DISTAL and self.menu_show_distal_synapses_none.isChecked()):
            is_visible = False
        else:
            if synapse.is_falsely_predicted.atGivenStepAgo(Global.sel_step):
                if (segment.type == SegmentType.PROXIMAL and self.menu_show_proximal_synapses_falsely_predicted.isChecked()):
                    color = self.COLOR_SYNAPSE_FALSELY_PREDICTED
                else:
                    is_visible = False
            elif synapse.is_predicted.atGivenStepAgo(Global.sel_step):
                if (segment.type == SegmentType.PROXIMAL and self.menu_show_proximal_synapses_predicted.isChecked()):
                    color = self.COLOR_SYNAPSE_PREDICTED
                else:
                    is_visible = False
            elif synapse.is_connected.atGivenStepAgo(Global.sel_step):
                if (segment.type == SegmentType.PROXIMAL and self.menu_show_proximal_synapses_connected.isChecked()) or (segment.type == SegmentType.DISTAL and self.menu_show_distal_synapses_connected.isChecked()):
                    color = self.COLOR_SYNAPSE_CONNECTED
                else:
                    is_visible = False
            else:
                if (segment.type == SegmentType.PROXIMAL and self.menu_show_proximal_synapses_active.isChecked()) or (segment.type == SegmentType.DISTAL and self.menu_show_distal_synapses_active.isChecked()):
                    color = self.COLOR_INACTIVE
                else:
                    is_visible = False

        if is_visible and segment_is_visible:
            # Draw the synapse
            if not synapse.tree3d_initialized:
                synapse.tree3d_item_np = Global.main_form.simulation.createSynapse(segment.tree3d_end_pos, synapse.input_elem.tree3d_pos)
                synapse.tree3d_initialized = True

            # Update the color
            if synapse.tree3d_selected:
                color = self.COLOR_SELECTED
            synapse.tree3d_item_np.setTexture(color)
        else:
            synapse.tree3d_initialized = False
            if synapse.tree3d_item_np is not None:
                Global.main_form.simulation.removeElement(synapse.tree3d_item_np)

    def selectView(self, view):
        """
        Load a pre-defined view and refresh controls.
        """

        if self.selected_view != None:
            self.selected_view['menu'].setChecked(False)
        self.selected_view = view
        self.selected_view['menu'].setChecked(True)

        # Update menus
        self.menu_show_bits_none.setChecked(view['show_bits_none'])
        self.menu_show_bits_active.setChecked(view['show_bits_active'])
        self.menu_show_bits_predicted.setChecked(view['show_bits_predicted'])
        self.menu_show_bits_falsely_predicted.setChecked(view['show_bits_falsely_predicted'])
        self.menu_show_cells_none.setChecked(view['show_cells_none'])
        self.menu_show_cells_learning.setChecked(view['show_cells_learning'])
        self.menu_show_cells_active.setChecked(view['show_cells_active'])
        self.menu_show_cells_predicted.setChecked(view['show_cells_predicted'])
        self.menu_show_cells_falsely_predicted.setChecked(view['show_cells_falsely_predicted'])
        self.menu_show_cells_inactive.setChecked(view['show_cells_inactive'])
        self.menu_show_proximal_segments_none.setChecked(view['show_proximal_segments_none'])
        self.menu_show_proximal_segments_active.setChecked(view['show_proximal_segments_active'])
        self.menu_show_proximal_segments_predicted.setChecked(view['show_proximal_segments_predicted'])
        self.menu_show_proximal_segments_falsely_predicted.setChecked(view['show_proximal_segments_falsely_predicted'])
        self.menu_show_proximal_synapses_none.setChecked(view['show_proximal_synapses_none'])
        self.menu_show_proximal_synapses_connected.setChecked(view['show_proximal_synapses_connected'])
        self.menu_show_proximal_synapses_active.setChecked(view['show_proximal_synapses_active'])
        self.menu_show_proximal_synapses_predicted.setChecked(view['show_proximal_synapses_predicted'])
        self.menu_show_proximal_synapses_falsely_predicted.setChecked(view['show_proximal_synapses_falsely_predicted'])
        self.menu_show_distal_segments_none.setChecked(view['show_distal_segments_none'])
        self.menu_show_distal_segments_active.setChecked(view['show_distal_segments_active'])
        self.menu_show_distal_synapses_none.setChecked(view['show_distal_synapses_none'])
        self.menu_show_distal_synapses_connected.setChecked(view['show_distal_synapses_connected'])
        self.menu_show_distal_synapses_active.setChecked(view['show_distal_synapses_active'])

        # Update simulation
        self.updateElements3d()

        # Disable change options for the 'Default' view
        default_view_selected = False
        if self.selected_view == self.default_view:
            default_view_selected = True
        self.menu_views_save.setEnabled(not default_view_selected)
        self.menu_views_delete.setEnabled(not default_view_selected)

    def menuLegend_click(self, event):
        simulation_legend_form = SimulationLegendForm()
        simulation_legend_form.exec_()

    def menuShowBits_click(self, event):
        menu_clicked = self.sender()
        if menu_clicked == self.menu_show_bits_none:
            if self.menu_show_bits_none.isChecked():
                self.menu_show_bits_active.setChecked(False)
                self.menu_show_bits_predicted.setChecked(False)
                self.menu_show_bits_falsely_predicted.setChecked(False)
        else:
            self.menu_show_bits_none.setChecked(False)
        self.updateElements3d()

    def menuShowCells_click(self, event):
        menu_clicked = self.sender()
        if menu_clicked == self.menu_show_cells_none:
            if self.menu_show_cells_none.isChecked():
                self.menu_show_cells_learning.setChecked(False)
                self.menu_show_cells_active.setChecked(False)
                self.menu_show_cells_predicted.setChecked(False)
                self.menu_show_cells_falsely_predicted.setChecked(False)
                self.menu_show_cells_inactive.setChecked(False)
        else:
            self.menu_show_cells_none.setChecked(False)
        self.updateElements3d()

    def menuShowProximalSegments_click(self, event):
        menu_clicked = self.sender()
        if menu_clicked == self.menu_show_proximal_segments_none:
            if self.menu_show_proximal_segments_none.isChecked():
                self.menu_show_proximal_segments_active.setChecked(False)
                self.menu_show_proximal_segments_predicted.setChecked(False)
                self.menu_show_proximal_segments_falsely_predicted.setChecked(False)
        else:
            self.menu_show_proximal_segments_none.setChecked(False)
        self.updateElements3d()

    def menuShowProximalSynapses_click(self, event):
        menu_clicked = self.sender()
        if menu_clicked == self.menu_show_proximal_synapses_none:
            if self.menu_show_proximal_synapses_none.isChecked():
                self.menu_show_proximal_synapses_connected.setChecked(False)
                self.menu_show_proximal_synapses_active.setChecked(False)
                self.menu_show_proximal_synapses_predicted.setChecked(False)
                self.menu_show_proximal_synapses_falsely_predicted.setChecked(False)
        else:
            self.menu_show_proximal_synapses_none.setChecked(False)
        self.updateElements3d()

    def menuShowDistalSegments_click(self, event):
        menu_clicked = self.sender()
        if menu_clicked == self.menu_show_distal_segments_none:
            if self.menu_show_distal_segments_none.isChecked():
                self.menu_show_distal_segments_active.setChecked(False)
        else:
            self.menu_show_distal_segments_none.setChecked(False)
        self.updateElements3d()

    def menuShowDistalSynapses_click(self, event):
        menu_clicked = self.sender()
        if menu_clicked == self.menu_show_distal_synapses_none:
            if self.menu_show_distal_synapses_none.isChecked():
                self.menu_show_distal_synapses_connected.setChecked(False)
                self.menu_show_distal_synapses_active.setChecked(False)
        else:
            self.menu_show_distal_synapses_none.setChecked(False)
        self.updateElements3d()

    def menuView_click(self, event):
        menu_clicked = self.sender()
        for view in Global.views:
            if view['menu'] == menu_clicked:
                self.selectView(view)
                break

    def menuViewsNew_click(self, event):

        # Ask for views's name
        entered_text, ok = QtWidgets.QInputDialog.getText(self, "Input Dialog", "Enter views' name:")
        if ok:
            menu = QtWidgets.QAction(self)
            menu.setText(entered_text)
            menu.setCheckable(True)
            menu.triggered.connect(self.menuView_click)

            view = NEW_VIEW
            view['name'] = entered_text
            view['menu'] = menu
            Global.views.append(view)
            self.menu_views.addAction(menu)

            self.selectView(view)

    def menuViewsSave_click(self, event):
        self.selected_view['show_bits_none'] = self.menu_show_bits_none.isChecked()
        self.selected_view['show_bits_active'] = self.menu_show_bits_active.isChecked()
        self.selected_view['show_bits_predicted'] = self.menu_show_bits_predicted.isChecked()
        self.selected_view['show_bits_falsely_predicted'] = self.menu_show_bits_falsely_predicted.isChecked()
        self.selected_view['show_cells_none'] = self.menu_show_cells_none.isChecked()
        self.selected_view['show_cells_learning'] = self.menu_show_cells_learning.isChecked()
        self.selected_view['show_cells_active'] = self.menu_show_cells_active.isChecked()
        self.selected_view['show_cells_predicted'] = self.menu_show_cells_predicted.isChecked()
        self.selected_view['show_cells_falsely_predicted'] = self.menu_show_cells_falsely_predicted.isChecked()
        self.selected_view['show_cells_inactive'] = self.menu_show_cells_inactive.isChecked()
        self.selected_view['show_proximal_segments_none'] = self.menu_show_proximal_segments_none.isChecked()
        self.selected_view['show_proximal_segments_active'] = self.menu_show_proximal_segments_active.isChecked()
        self.selected_view['show_proximal_segments_predicted'] = self.menu_show_proximal_segments_predicted.isChecked()
        self.selected_view['show_proximal_segments_falsely_predicted'] = self.menu_show_proximal_segments_falsely_predicted.isChecked()
        self.selected_view['show_proximal_synapses_none'] = self.menu_show_proximal_synapses_none.isChecked()
        self.selected_view['show_proximal_synapses_connected'] = self.menu_show_proximal_synapses_connected.isChecked()
        self.selected_view['show_proximal_synapses_active'] = self.menu_show_proximal_synapses_active.isChecked()
        self.selected_view['show_proximal_synapses_predicted'] = self.menu_show_proximal_synapses_predicted.isChecked()
        self.selected_view['show_proximal_synapses_falsely_predicted'] = self.menu_show_proximal_synapses_falsely_predicted.isChecked()
        self.selected_view['show_distal_segments_none'] = self.menu_show_distal_segments_none.isChecked()
        self.selected_view['show_distal_segments_active'] = self.menu_show_distal_segments_active.isChecked()
        self.selected_view['show_distal_synapses_none'] = self.menu_show_distal_synapses_none.isChecked()
        self.selected_view['show_distal_synapses_connected'] = self.menu_show_distal_synapses_connected.isChecked()
        self.selected_view['show_distal_synapses_active'] = self.menu_show_distal_synapses_active.isChecked()
        Global.saveConfig()

    def menuViewsDelete_click(self, event):
        self.menu_views.removeAction(self.selected_view['menu'])
        Global.views.remove(self.selected_view)

        # Set 'Default' view as initial view
        self.selectView(self.default_view)
