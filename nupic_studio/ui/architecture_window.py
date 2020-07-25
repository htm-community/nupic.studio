from PyQt5 import QtGui, QtCore, QtWidgets
from nupic_studio.ui import Global
from nupic_studio.htm.node import NodeType, Node
from nupic_studio.htm.node_region import Region
from nupic_studio.htm.node_sensor import Sensor
from nupic_studio.ui.node_region_window import RegionWindow
from nupic_studio.ui.node_sensor_window import SensorWindow


class ArchitectureWindow(QtWidgets.QWidget):

    def __init__(self):
        """
        Initializes a new instance of this class.
        """
        QtWidgets.QWidget.__init__(self)
        self.initUI()

    def initUI(self):

        # design_panel
        self.design_panel = DesignPanel()

        # tab_page_design_layout
        tab_page_design_layout = QtWidgets.QHBoxLayout()
        tab_page_design_layout.addWidget(self.design_panel)

        # tab_page_design
        self.tab_page_design = QtWidgets.QWidget()
        self.tab_page_design.setLayout(tab_page_design_layout)

        # textbox_code
        self.textbox_code = QtWidgets.QTextEdit()
        self.textbox_code.setReadOnly(True)
        self.textbox_code.setAlignment(QtCore.Qt.AlignLeft)
        self.textbox_code.setWordWrapMode(QtGui.QTextOption.NoWrap)
        self.textbox_code.setFont(QtGui.QFont("Courier New", 9))

        # tab_page_code_layout
        tab_page_code_layout = QtWidgets.QHBoxLayout()
        tab_page_code_layout.addWidget(self.textbox_code)

        # tab_page_code
        self.tab_page_code = QtWidgets.QWidget()
        self.tab_page_code.setLayout(tab_page_code_layout)

        # tab_control_main
        self.tab_control_main = QtWidgets.QTabWidget()
        self.tab_control_main.addTab(self.tab_page_design, "Design")
        self.tab_control_main.addTab(self.tab_page_code, "Code")

        # layout
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.tab_control_main)

        # self
        self.setLayout(layout)
        self.setMinimumWidth(300)
        self.setMinimumHeight(300)
        self.setWindowTitle("Network Architecture")
        self.setWindowIcon(QtGui.QIcon(Global.app_path + '/images/logo.ico'))

    def updateCode(self):
        """
        Update the source code of the network.
        """
        code = Global.project.network.getSourceCode()
        self.textbox_code.setText(code)


class DesignPanel(QtWidgets.QWidget):

    def __init__(self):
        """
        Initializes a new instance of this class.
        """
        QtWidgets.QWidget.__init__(self)

        # Node that is on top of the hierarchy.
        self.top_region = Region("TopRegion")

        # Node that is selected for visualization of its details.
        self.selected_node = None

        # Node that is highlighted due to mouse is on it.
        self.under_mouse_node = None

        # Space to skip horizontally between siblings
        # and vertically between generations
        self.offset_horizontal = 15
        self.offset_vertical = 30

        self.initUI()

    def initUI(self):

        # menu_node_properties
        self.menu_node_properties = QtWidgets.QAction(self)
        self.menu_node_properties.setText("&Properties")
        self.menu_node_properties.triggered.connect(self.menuNodeProperties_click)

        # menu_node_add_region
        self.menu_node_add_region = QtWidgets.QAction(self)
        self.menu_node_add_region.setText("&Add region under this node...")
        self.menu_node_add_region.triggered.connect(self.menuNodeAddRegion_click)

        # menu_node_add_sensor
        self.menu_node_add_sensor = QtWidgets.QAction(self)
        self.menu_node_add_sensor.setText("&Add sensor under this node...")
        self.menu_node_add_sensor.triggered.connect(self.menuNodeAddSensor_click)

        # menu_node_delete
        self.menu_node_delete = QtWidgets.QAction(self)
        self.menu_node_delete.setText("&Delete this node...")
        self.menu_node_delete.triggered.connect(self.menuNodeDelete_click)

        # menu_node
        self.menu_node = QtWidgets.QMenu()
        self.menu_node.addAction(self.menu_node_properties)
        self.menu_node.addAction(self.menu_node_add_region)
        self.menu_node.addAction(self.menu_node_add_sensor)
        self.menu_node.addAction(self.menu_node_delete)

        # layout
        layout = QtWidgets.QHBoxLayout()

        # DesignPanel
        self.setLayout(layout)
        self.setToolTip("Left button click: Select region.\r\nRight button click: Show options for region or sensor.")

        # Set center position of the top region
        self.top_region.tree2d_x = self.minimumWidth() / 2
        self.top_region.tree2d_y = 30

        # Painter to draw the tree
        self.painter = QtGui.QPainter()

    def arrangeNode(self, node, min_x, minY):
        """
        Arrange the node and the lower nodes that feed it in the allowed area.
        Set min_x to indicate the right edge of our subtree.
        Set minY to indicate the bottom edge of our subtree.
        """

        # See how big this node is.
        size = self.getNodeSize(node)

        # Recursively arrange the lower nodes that feed this node,
        # allowing room for this node.
        x = min_x
        width = size.width()
        height = size.height()
        biggest_min_y = minY + height
        subtree_min_y = minY + height + self.offset_vertical
        feeders_count = 0
        for feeder in Global.project.network.getFeederNodes(node):

            # Arrange this feeder's subtree.
            feeder_min_y = subtree_min_y
            x, feeder_min_y = self.arrangeNode(feeder, x, feeder_min_y)

            # See if this increases the biggest minY value.
            if biggest_min_y < feeder_min_y:
                biggest_min_y = feeder_min_y

            # Allow room before the next sibling.
            x += self.offset_horizontal

            feeders_count += 1

        # Remove the spacing after the last feeder.
        if feeders_count > 0:
            x -= self.offset_horizontal

        # See if this node is wider than the subtree under it.
        subtree_width = x - min_x
        if width > subtree_width:
            # Center the subtree under this node.
            # Make the lower nodes that feed this node rearrange themselves
            # moved to center their subtrees.
            x = min_x + (width - subtree_width) / 2
            for feeder in Global.project.network.getFeederNodes(node):
                # Arrange this feeder's subtree.
                x, subtree_min_y = self.arrangeNode(feeder, x, subtree_min_y)

                # Allow room before the next sibling.
                x += self.offset_horizontal

            # The subtree's width is this node's width.
            subtree_width = width

        # Set this node's center position.
        node.tree2d_x = min_x + subtree_width / 2
        node.tree2d_y = minY + height / 2

        # Increase min_x to allow room for the subtree before returning.
        min_x += subtree_width

        # Set the return value for minY.
        minY = biggest_min_y

        return min_x, minY

    def getNodeSize(self, node):
        """
        Return the size of the string plus a 10 pixel margin.
        """
        font_metrics = self.painter.fontMetrics()
        width = font_metrics.width(node.name)
        return QtCore.QSizeF(30 + width, 30)

    def drawNode(self, node):
        """
        Draw the nodes for the subtree rooted at this node.
        """

        # Recursively make the node draw its feeders.
        for feeder in Global.project.network.getFeederNodes(node):
            # Draw the link between this node and this feeder.
            self.painter.drawLine(node.tree2d_x, node.tree2d_y, feeder.tree2d_x, feeder.tree2d_y)

            # Recursively make the node draw its feeders.
            self.drawNode(feeder)

        # Draw this node centered at (x, y).
        brush = QtGui.QBrush()
        if node == self.selected_node:
            brush = QtGui.QColor(0, 200, 250)
        else:
            brush = QtGui.QColor(0, 150, 200)

        # Fill and draw a polygon at our location.
        size = self.getNodeSize(node)
        x = node.tree2d_x
        y = node.tree2d_y
        width = size.width()
        height = size.height()
        if node.type == NodeType.REGION:
            point1 = QtCore.QPoint((x - width / 2) + 10, (y - height / 2))
            point2 = QtCore.QPoint((x + width / 2) - 10, (y - height / 2))
        elif (node.type == NodeType.SENSOR):
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

    def nodeAtPoint(self, node, mouse_point):
        """
        Return the node at this point (or None if there isn't one there).
        """

        # See if the point is under this node.
        if node.tree2d_polygon.boundingRect().contains(mouse_point):
            return node

        # See if the point is under a node in the subtree.
        for feeder in Global.project.network.getFeederNodes(node):
            hit_node = self.nodeAtPoint(feeder, mouse_point)
            if hit_node != None:
                return hit_node

        return None

    def paintEvent(self, event):
        """
        Draw and center the tree on the window.
        """

        # Initialize painter
        self.painter.begin(self)
        self.painter.setFont(QtGui.QFont("Arial", 8))
        self.painter.fillRect(self.rect(), QtCore.Qt.white)

        # Arrange the tree once to see how big it is.
        min_x = 0
        min_y = 0
        min_x, min_y = self.arrangeNode(self.top_region, min_x, min_y)

        # Rearrange the tree again to center it horizontally.
        min_x = (self.width() - min_x) / 2
        min_y = 10
        min_x, min_y = self.arrangeNode(self.top_region, min_x, min_y)

        # Draw the tree recursively from top region.
        self.drawNode(self.top_region)

        # End painter
        self.painter.end()

    def mousePressEvent(self, event):
        """
        If this is a right button down and the mouse is over a node, display a context menu.
        """
        if event.buttons() == QtCore.Qt.LeftButton:
            self.under_mouse_node = self.nodeAtPoint(self.top_region, event.pos())
            if self.under_mouse_node != None:
                # Select the node and updates any related information.
                self.selected_node = self.under_mouse_node

                # Redraw the tree to show the updates.
                self.repaint()

                # Refresh dependents tools
                Global.simulation_window.refreshControls()
                Global.node_information_window.refreshControls()
        elif event.buttons() == QtCore.Qt.RightButton:
            self.under_mouse_node = self.nodeAtPoint(self.top_region, event.pos())
            if self.under_mouse_node != None:
                # Don't let the user delete the top node.
                self.menu_node_add_region.setEnabled(not Global.simulation_initialized and self.under_mouse_node.type != NodeType.SENSOR)
                self.menu_node_add_sensor.setEnabled(not Global.simulation_initialized and self.under_mouse_node.type != NodeType.SENSOR)
                self.menu_node_delete.setEnabled(not Global.simulation_initialized and self.under_mouse_node != self.top_region)

                # Display the context menu.
                self.menu_node.exec_(self.mapToGlobal(event.pos()))

    def menuNodeProperties_click(self, event):
        """
        View node propeerties.
        """
        if self.under_mouse_node.type == NodeType.REGION:
            region_window = RegionWindow()
            region_window.setControlsValues()
            dialog_result = region_window.exec_()

            # Update controls with the new changes
            if dialog_result == QtWidgets.QDialog.Accepted:
                Global.main_window.markProjectChanges(True)
                Global.architecture_window.updateCode()
        elif self.under_mouse_node.type == NodeType.SENSOR:
            sensor_window = SensorWindow()
            sensor_window.setControlsValues()
            dialog_result = sensor_window.exec_()

            # Update controls with the new changes
            if dialog_result == QtWidgets.QDialog.Accepted:
                Global.main_window.markProjectChanges(True)
                Global.architecture_window.updateCode()

    def menuNodeAddRegion_click(self, event):
        """
        Add a feeder region to the selected region.
        """

        # Ask for region's name
        entered_text, ok = QtWidgets.QInputDialog.getText(self, "Input Dialog", "Enter region's name:")
        if ok:
            valid_expr = QtCore.QRegExp('[a-zA-Z0-9_]+')
            if not valid_expr.exactMatch(entered_text):
                QtWidgets.QMessageBox.warning(self, "Warning", "'" + entered_text + "' is not a valid name. Only characters, numbers and _ are accepted.")
                return

            Global.main_window.markProjectChanges(True)

            # Add new region below highlighted region
            new_region = Region(entered_text)
            Global.project.network.addFeederNode(new_region, self.under_mouse_node)

            # Redraw the tree to show the updates.
            self.repaint()
            Global.architecture_window.updateCode()

    def menuNodeAddSensor_click(self, event):
        """
        Add a feeder sensor to the selected region.
        """

        # Ask for sensor's name
        entered_text, ok = QtWidgets.QInputDialog.getText(self, "Input Dialog", "Enter sensor's name:")
        if ok:
            valid_expr = QtCore.QRegExp('[a-zA-Z0-9_]+')
            if not valid_expr.exactMatch(entered_text):
                QtWidgets.QMessageBox.warning(self, "Warning", "'" + entered_text + "' is not a valid name. Only characters, numbers and _ are accepted.")
                return

            Global.main_window.markProjectChanges(True)

            # Add new sensor below highlighted region
            new_sensor = Sensor(entered_text)
            Global.project.network.addFeederNode(new_sensor, self.under_mouse_node)

            # Redraw the tree to show the updates.
            self.repaint()
            Global.architecture_window.updateCode()

    def menuNodeDelete_click(self, event):
        """
        Delete this node from the tree.
        """
        if QtWidgets.QMessageBox.question(self, "Question", "Are you sure you want to delete this node?", QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.Yes:
            Global.main_window.markProjectChanges(True)

            # Delete the node and its subtree.
            Global.project.network.deleteFeederNode(self.under_mouse_node)

            # Redraw the tree to show the updates.
            self.repaint()
            Global.architecture_window.updateCode()
