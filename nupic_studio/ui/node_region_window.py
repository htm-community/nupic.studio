from PyQt5 import QtGui, QtCore, QtWidgets
from nupic_studio.ui import ICON, State, Global


class RegionWindow(QtWidgets.QDialog):

    def __init__(self, main_window):
        """
        Initializes a new instance of this class.
        """
        QtWidgets.QDialog.__init__(self)
        self.main_window = main_window
        self.initUI()

    def initUI(self):

        # label_width
        self.label_width = QtWidgets.QLabel()
        self.label_width.setText("Width")
        self.label_width.setAlignment(QtCore.Qt.AlignRight)

        # spinner_width
        self.spinner_width = QtWidgets.QSpinBox()
        self.spinner_width.setAlignment(QtCore.Qt.AlignRight)
        self.spinner_width.setMinimum(3)
        self.spinner_width.setEnabled(not self.main_window.isRunning())
        self.spinner_width.setToolTip("")

        # label_height
        self.label_height = QtWidgets.QLabel()
        self.label_height.setText("Height")
        self.label_height.setAlignment(QtCore.Qt.AlignRight)

        # spinner_height
        self.spinner_height = QtWidgets.QSpinBox()
        self.spinner_height.setAlignment(QtCore.Qt.AlignRight)
        self.spinner_height.setMinimum(3)
        self.spinner_height.setEnabled(not self.main_window.isRunning())
        self.spinner_height.setToolTip("")

        # main_layout
        main_layout = QtWidgets.QGridLayout()
        main_layout.addWidget(self.label_width, 0, 0)
        main_layout.addWidget(self.spinner_width, 0, 1)
        main_layout.addWidget(self.label_height, 1, 0)
        main_layout.addWidget(self.spinner_height, 1, 1)

        # label_potential_radius
        self.label_potential_radius = QtWidgets.QLabel()
        self.label_potential_radius.setText("Potential Radius")
        self.label_potential_radius.setAlignment(QtCore.Qt.AlignRight)

        # spinner_potential_radius
        self.spinner_potential_radius = QtWidgets.QSpinBox()
        self.spinner_potential_radius.setAlignment(QtCore.Qt.AlignRight)
        self.spinner_potential_radius.setEnabled(not self.main_window.isRunning())
        self.spinner_potential_radius.setToolTip("This parameter determines the extent of the input that each column can potentially be connected to. This can be thought of as the input bits that are visible to each column, or a 'receptiveField' of the field of vision. A large enough value will result in 'global coverage', meaning that each column can potentially be connected to every input bit. This parameter defines a square (or hyper square) area: a column will have a max square potential pool with sides of length 2 * potential_radius + 1.")

        # label_potential_pct
        self.label_potential_pct = QtWidgets.QLabel()
        self.label_potential_pct.setText("Potential (%)")
        self.label_potential_pct.setAlignment(QtCore.Qt.AlignRight)

        # spinner_potential_pct
        self.spinner_potential_pct = QtWidgets.QDoubleSpinBox()
        self.spinner_potential_pct.setAlignment(QtCore.Qt.AlignRight)
        self.spinner_potential_pct.setMaximum(1)
        self.spinner_potential_pct.setDecimals(2)
        self.spinner_potential_pct.setSingleStep(0.01)
        self.spinner_potential_pct.setEnabled(not self.main_window.isRunning())
        self.spinner_potential_pct.setToolTip("The percent of the inputs, within a column's potential radius, that a column can be connected to. If set to 1, the column will be connected to every input within its potential radius. This parameter is used to give each column a unique potential pool when a large potential_radius causes overlap between the columns. At initialization time we choose ((2*potential_radius + 1)^(# inputDimensions) * potential_pct) input bits to comprise the column's potential pool.")

        # checkbox_global_inhibition
        self.checkbox_global_inhibition = QtWidgets.QCheckBox()
        self.checkbox_global_inhibition.setText("Global Inhibition")
        self.checkbox_global_inhibition.setEnabled(not self.main_window.isRunning())
        self.checkbox_global_inhibition.setToolTip("If true, then during inhibition phase the winning columns are selected as the most active columns from the region as a whole. Otherwise, the winning columns are selected with respect to their local neighborhoods. Using global inhibition boosts performance x60.")

        # label_local_area_density
        self.label_local_area_density = QtWidgets.QLabel()
        self.label_local_area_density.setText("Local Area Density")
        self.label_local_area_density.setAlignment(QtCore.Qt.AlignRight)

        # spinner_local_area_density
        self.spinner_local_area_density = QtWidgets.QDoubleSpinBox()
        self.spinner_local_area_density.setAlignment(QtCore.Qt.AlignRight)
        self.spinner_local_area_density.setMinimum(-1.0)
        self.spinner_local_area_density.setDecimals(2)
        self.spinner_local_area_density.setSingleStep(0.01)
        self.spinner_local_area_density.setEnabled(not self.main_window.isRunning())
        self.spinner_local_area_density.setToolTip("The desired density of active columns within a local inhibition area (the size of which is set by the internally calculated inhibitionRadius, which is in turn determined from the average size of the connected potential pools of all columns). The inhibition logic will insure that at most N columns remain ON within a local inhibition area, where N = local_area_density * (total number of columns in inhibition area).")

        # label_num_active_columns_per_inh_area
        self.label_num_active_columns_per_inh_area = QtWidgets.QLabel()
        self.label_num_active_columns_per_inh_area.setText("Num. Active Columns Per Inh. Area")
        self.label_num_active_columns_per_inh_area.setAlignment(QtCore.Qt.AlignRight)

        # spinner_num_active_columns_per_inh_area
        self.spinner_num_active_columns_per_inh_area = QtWidgets.QSpinBox()
        self.spinner_num_active_columns_per_inh_area.setAlignment(QtCore.Qt.AlignRight)
        self.spinner_num_active_columns_per_inh_area.setEnabled(not self.main_window.isRunning())
        self.spinner_num_active_columns_per_inh_area.setToolTip("An alternate way to control the density of the active columns. If num_active_columns_per_inh_area is specified then local_area_density must be less than 0, and vice versa. When using num_active_columns_per_inh_area, the inhibition logic will insure that at most 'num_active_columns_per_inh_area' columns remain ON within a local inhibition area (the size of which is set by the internally calculated inhibitionRadius, which is in turn determined from the average size of the connected receptive fields of all columns). When using this method, as columns learn and grow their effective receptive fields, the inhibitionRadius will grow, and hence the net density of the active columns will *decrease*. This is in contrast to the local_area_density method, which keeps the density of active columns the same regardless of the size of their receptive fields.")

        # label_stimulus_threshold
        self.label_stimulus_threshold = QtWidgets.QLabel()
        self.label_stimulus_threshold.setText("Stimulus Threshold")
        self.label_stimulus_threshold.setAlignment(QtCore.Qt.AlignRight)

        # spinner_stimulus_threshold
        self.spinner_stimulus_threshold = QtWidgets.QSpinBox()
        self.spinner_stimulus_threshold.setAlignment(QtCore.Qt.AlignRight)
        self.spinner_stimulus_threshold.setEnabled(not self.main_window.isRunning())
        self.spinner_stimulus_threshold.setToolTip("This is a number specifying the minimum number of synapses that must be on in order for a columns to turn ON. The purpose of this is to prevent noise input from activating columns. Specified as a percent of a fully grown synapse.")

        # label_proximal_syn_connected_perm
        self.label_proximal_syn_connected_perm = QtWidgets.QLabel()
        self.label_proximal_syn_connected_perm.setText("Connected")
        self.label_proximal_syn_connected_perm.setAlignment(QtCore.Qt.AlignRight)

        # spinner_proximal_syn_connected_perm
        self.spinner_proximal_syn_connected_perm = QtWidgets.QDoubleSpinBox()
        self.spinner_proximal_syn_connected_perm.setAlignment(QtCore.Qt.AlignRight)
        self.spinner_proximal_syn_connected_perm.setDecimals(4)
        self.spinner_proximal_syn_connected_perm.setSingleStep(0.0001)
        self.spinner_proximal_syn_connected_perm.setEnabled(not self.main_window.isRunning())
        self.spinner_proximal_syn_connected_perm.setToolTip("The default connected threshold. Any synapse whose permanence value is above the connected threshold is a 'connected synapse', meaning it can contribute to the cell's firing.")

        # label_proximal_syn_perm_increment
        self.label_proximal_syn_perm_increment = QtWidgets.QLabel()
        self.label_proximal_syn_perm_increment.setText("Increment")
        self.label_proximal_syn_perm_increment.setAlignment(QtCore.Qt.AlignRight)

        # spinner_proximal_syn_perm_increment
        self.spinner_proximal_syn_perm_increment = QtWidgets.QDoubleSpinBox()
        self.spinner_proximal_syn_perm_increment.setAlignment(QtCore.Qt.AlignRight)
        self.spinner_proximal_syn_perm_increment.setDecimals(4)
        self.spinner_proximal_syn_perm_increment.setSingleStep(0.0001)
        self.spinner_proximal_syn_perm_increment.setEnabled(not self.main_window.isRunning())
        self.spinner_proximal_syn_perm_increment.setToolTip("The amount by which an active synapse is incremented in each round. Specified as a percent of a fully grown synapse.")

        # label_proximal_syn_perm_decrement
        self.label_proximal_syn_perm_decrement = QtWidgets.QLabel()
        self.label_proximal_syn_perm_decrement.setText("Decrement")
        self.label_proximal_syn_perm_decrement.setAlignment(QtCore.Qt.AlignRight)

        # spinner_proximal_syn_perm_decrement
        self.spinner_proximal_syn_perm_decrement = QtWidgets.QDoubleSpinBox()
        self.spinner_proximal_syn_perm_decrement.setAlignment(QtCore.Qt.AlignRight)
        self.spinner_proximal_syn_perm_decrement.setDecimals(4)
        self.spinner_proximal_syn_perm_decrement.setSingleStep(0.0001)
        self.spinner_proximal_syn_perm_decrement.setEnabled(not self.main_window.isRunning())
        self.spinner_proximal_syn_perm_decrement.setToolTip("The amount by which an inactive synapse is decremented in each round. Specified as a percent of a fully grown synapse.")

        # group_box_proximal_syn_perm
        group_box_proximal_syn_perm_layout = QtWidgets.QGridLayout()
        group_box_proximal_syn_perm_layout.addWidget(self.label_proximal_syn_connected_perm, 0, 0)
        group_box_proximal_syn_perm_layout.addWidget(self.spinner_proximal_syn_connected_perm, 0, 1)
        group_box_proximal_syn_perm_layout.addWidget(self.label_proximal_syn_perm_increment, 1, 0)
        group_box_proximal_syn_perm_layout.addWidget(self.spinner_proximal_syn_perm_increment, 1, 1)
        group_box_proximal_syn_perm_layout.addWidget(self.label_proximal_syn_perm_decrement, 2, 0)
        group_box_proximal_syn_perm_layout.addWidget(self.spinner_proximal_syn_perm_decrement, 2, 1)

        # group_box_proximal_syn_perm
        self.group_box_proximal_syn_perm = QtWidgets.QGroupBox()
        self.group_box_proximal_syn_perm.setLayout(group_box_proximal_syn_perm_layout)
        self.group_box_proximal_syn_perm.setTitle("Proximal Synapses Permanence")

        # label_min_pct_overlap_duty_cycle
        self.label_min_pct_overlap_duty_cycle = QtWidgets.QLabel()
        self.label_min_pct_overlap_duty_cycle.setText("Min. Overlap Duty Cycle (%)")
        self.label_min_pct_overlap_duty_cycle.setAlignment(QtCore.Qt.AlignRight)

        # spinner_min_pct_overlap_duty_cycle
        self.spinner_min_pct_overlap_duty_cycle = QtWidgets.QDoubleSpinBox()
        self.spinner_min_pct_overlap_duty_cycle.setAlignment(QtCore.Qt.AlignRight)
        self.spinner_min_pct_overlap_duty_cycle.setMaximum(100)
        self.spinner_min_pct_overlap_duty_cycle.setDecimals(3)
        self.spinner_min_pct_overlap_duty_cycle.setSingleStep(0.001)
        self.spinner_min_pct_overlap_duty_cycle.setEnabled(not self.main_window.isRunning())
        self.spinner_min_pct_overlap_duty_cycle.setToolTip("A number between 0 and 1.0, used to set a floor on how often a column should have at least stimulus_threshold active inputs. Periodically, each column looks at the overlap duty cycle of all other columns within its inhibition radius and sets its own internal minimal acceptable duty cycle to:\
            min_pct_duty_cycle_before_inh * max(other columns' duty cycles).\
            On each iteration, any column whose overlap duty cycle falls below this computed value will get all of its permanence values boosted up by synPermActiveInc. Raising all permanences in response to a sub-par duty cycle before inhibition allows a cell to search for new inputs when either its previously learned inputs are no longer ever active, or when the vast majority of them have been 'hijacked' by other columns.")

        # label_min_pct_active_duty_cycle
        self.label_min_pct_active_duty_cycle = QtWidgets.QLabel()
        self.label_min_pct_active_duty_cycle.setText("Min. Active Duty Cycle (%)")
        self.label_min_pct_active_duty_cycle.setAlignment(QtCore.Qt.AlignRight)

        # spinner_min_pct_active_duty_cycle
        self.spinner_min_pct_active_duty_cycle = QtWidgets.QDoubleSpinBox()
        self.spinner_min_pct_active_duty_cycle.setAlignment(QtCore.Qt.AlignRight)
        self.spinner_min_pct_active_duty_cycle.setMaximum(100)
        self.spinner_min_pct_active_duty_cycle.setDecimals(3)
        self.spinner_min_pct_active_duty_cycle.setSingleStep(0.001)
        self.spinner_min_pct_active_duty_cycle.setEnabled(not self.main_window.isRunning())
        self.spinner_min_pct_active_duty_cycle.setToolTip("A number between 0 and 1.0, used to set a floor on how often a column should be activate. Periodically, each column looks at the activity duty cycle of all other columns within its inhibition radius and sets its own internal minimal acceptable duty cycle to:\
            min_pct_duty_cycle_after_inh * max(other columns' duty cycles).\
            On each iteration, any column whose duty cycle after inhibition falls below this computed value will get its internal boost factor increased.")

        # label_duty_cycle_period
        self.label_duty_cycle_period = QtWidgets.QLabel()
        self.label_duty_cycle_period.setText("Duty Cycle Period")
        self.label_duty_cycle_period.setAlignment(QtCore.Qt.AlignRight)

        # spinner_duty_cycle_period
        self.spinner_duty_cycle_period = QtWidgets.QSpinBox()
        self.spinner_duty_cycle_period.setAlignment(QtCore.Qt.AlignRight)
        self.spinner_duty_cycle_period.setMaximum(1000)
        self.spinner_duty_cycle_period.setEnabled(not self.main_window.isRunning())
        self.spinner_duty_cycle_period.setToolTip("The period used to calculate duty cycles. Higher values make it take longer to respond to changes in boost or synPerConnectedCell. Shorter values make it more unstable and likely to oscillate.")

        # label_max_boost
        self.label_max_boost = QtWidgets.QLabel()
        self.label_max_boost.setText("Max Boost")
        self.label_max_boost.setAlignment(QtCore.Qt.AlignRight)

        # spinner_max_boost
        self.spinner_max_boost = QtWidgets.QDoubleSpinBox()
        self.spinner_max_boost.setAlignment(QtCore.Qt.AlignRight)
        self.spinner_max_boost.setDecimals(2)
        self.spinner_max_boost.setSingleStep(0.01)
        self.spinner_max_boost.setEnabled(not self.main_window.isRunning())
        self.spinner_max_boost.setToolTip("The maximum overlap boost factor. Each column's overlap gets multiplied by a boost factor before it gets considered for inhibition. The actual boost factor for a column is number between 1.0 and max_boost. A boost factor of 1.0 is used if the duty cycle is >= minOverlapDutyCycle, max_boost is used if the duty cycle is 0, and any duty cycle in between is linearly extrapolated from these 2 endpoints.")

        # label_sp_seed
        self.label_sp_seed = QtWidgets.QLabel()
        self.label_sp_seed.setText("Seed")
        self.label_sp_seed.setAlignment(QtCore.Qt.AlignRight)

        # spinner_sp_seed
        self.spinner_sp_seed = QtWidgets.QSpinBox()
        self.spinner_sp_seed.setAlignment(QtCore.Qt.AlignRight)
        self.spinner_sp_seed.setMinimum(-1)
        self.spinner_sp_seed.setMaximum(5000)
        self.spinner_sp_seed.setEnabled(not self.main_window.isRunning())
        self.spinner_sp_seed.setToolTip("Seed for random values.")

        # tab_page_spatial_layout
        tab_page_spatial_layout = QtWidgets.QGridLayout()
        tab_page_spatial_layout.addWidget(self.label_potential_radius, 0, 0)
        tab_page_spatial_layout.addWidget(self.spinner_potential_radius, 0, 1)
        tab_page_spatial_layout.addWidget(self.label_potential_pct, 1, 0)
        tab_page_spatial_layout.addWidget(self.spinner_potential_pct, 1, 1)
        tab_page_spatial_layout.addWidget(self.checkbox_global_inhibition, 2, 0)
        tab_page_spatial_layout.addWidget(self.label_local_area_density, 3, 0)
        tab_page_spatial_layout.addWidget(self.spinner_local_area_density, 3, 1)
        tab_page_spatial_layout.addWidget(self.label_num_active_columns_per_inh_area, 4, 0)
        tab_page_spatial_layout.addWidget(self.spinner_num_active_columns_per_inh_area, 4, 1)
        tab_page_spatial_layout.addWidget(self.label_stimulus_threshold, 5, 0)
        tab_page_spatial_layout.addWidget(self.spinner_stimulus_threshold, 5, 1)
        tab_page_spatial_layout.addWidget(self.group_box_proximal_syn_perm, 6, 1)
        tab_page_spatial_layout.addWidget(self.label_min_pct_overlap_duty_cycle, 7, 0)
        tab_page_spatial_layout.addWidget(self.spinner_min_pct_overlap_duty_cycle, 7, 1)
        tab_page_spatial_layout.addWidget(self.label_min_pct_active_duty_cycle, 8, 0)
        tab_page_spatial_layout.addWidget(self.spinner_min_pct_active_duty_cycle, 8, 1)
        tab_page_spatial_layout.addWidget(self.label_duty_cycle_period, 9, 0)
        tab_page_spatial_layout.addWidget(self.spinner_duty_cycle_period, 9, 1)
        tab_page_spatial_layout.addWidget(self.label_max_boost, 10, 0)
        tab_page_spatial_layout.addWidget(self.spinner_max_boost, 10, 1)
        tab_page_spatial_layout.addWidget(self.label_sp_seed, 11, 0)
        tab_page_spatial_layout.addWidget(self.spinner_sp_seed, 11, 1)

        # tab_page_spatial
        self.tab_page_spatial = QtWidgets.QWidget()
        self.tab_page_spatial.setLayout(tab_page_spatial_layout)

        # label_cells_per_column
        self.label_cells_per_column = QtWidgets.QLabel()
        self.label_cells_per_column.setText("Num. Cells Per Column")
        self.label_cells_per_column.setAlignment(QtCore.Qt.AlignRight)

        # spinner_cells_per_column
        self.spinner_cells_per_column = QtWidgets.QSpinBox()
        self.spinner_cells_per_column.setAlignment(QtCore.Qt.AlignRight)
        self.spinner_cells_per_column.setMinimum(1)
        self.spinner_cells_per_column.setEnabled(not self.main_window.isRunning())
        self.spinner_cells_per_column.setToolTip("Number of cells per column. More cells, more contextual information")

        # label_distal_syn_initial_perm
        self.label_distal_syn_initial_perm = QtWidgets.QLabel()
        self.label_distal_syn_initial_perm.setText("Initial")
        self.label_distal_syn_initial_perm.setAlignment(QtCore.Qt.AlignRight)

        # spinner_distal_syn_initial_perm
        self.spinner_distal_syn_initial_perm = QtWidgets.QDoubleSpinBox()
        self.spinner_distal_syn_initial_perm.setAlignment(QtCore.Qt.AlignRight)
        self.spinner_distal_syn_initial_perm.setDecimals(4)
        self.spinner_distal_syn_initial_perm.setSingleStep(0.0001)
        self.spinner_distal_syn_initial_perm.setEnabled(not self.main_window.isRunning())
        self.spinner_distal_syn_initial_perm.setToolTip("The initial permanence of an distal synapse.")

        # label_distal_syn_connected_perm
        self.label_distal_syn_connected_perm = QtWidgets.QLabel()
        self.label_distal_syn_connected_perm.setText("Connected")
        self.label_distal_syn_connected_perm.setAlignment(QtCore.Qt.AlignRight)

        # spinner_distal_syn_connected_perm
        self.spinner_distal_syn_connected_perm = QtWidgets.QDoubleSpinBox()
        self.spinner_distal_syn_connected_perm.setAlignment(QtCore.Qt.AlignRight)
        self.spinner_distal_syn_connected_perm.setDecimals(4)
        self.spinner_distal_syn_connected_perm.setSingleStep(0.0001)
        self.spinner_distal_syn_connected_perm.setEnabled(not self.main_window.isRunning())
        self.spinner_distal_syn_connected_perm.setToolTip("The default connected threshold. Any synapse whose permanence value is above the connected threshold is a 'connected synapse', meaning it can contribute to the cell's firing.")

        # label_distal_syn_perm_increment
        self.label_distal_syn_perm_increment = QtWidgets.QLabel()
        self.label_distal_syn_perm_increment.setText("Increment")
        self.label_distal_syn_perm_increment.setAlignment(QtCore.Qt.AlignRight)

        # spinner_distal_syn_perm_increment
        self.spinner_distal_syn_perm_increment = QtWidgets.QDoubleSpinBox()
        self.spinner_distal_syn_perm_increment.setAlignment(QtCore.Qt.AlignRight)
        self.spinner_distal_syn_perm_increment.setDecimals(4)
        self.spinner_distal_syn_perm_increment.setSingleStep(0.0001)
        self.spinner_distal_syn_perm_increment.setEnabled(not self.main_window.isRunning())
        self.spinner_distal_syn_perm_increment.setToolTip("The amount by which an active synapse is incremented in each round. Specified as a percent of a fully grown synapse.")

        # label_distal_syn_perm_decrement
        self.label_distal_syn_perm_decrement = QtWidgets.QLabel()
        self.label_distal_syn_perm_decrement.setText("Decrement")
        self.label_distal_syn_perm_decrement.setAlignment(QtCore.Qt.AlignRight)

        # spinner_distal_syn_perm_decrement
        self.spinner_distal_syn_perm_decrement = QtWidgets.QDoubleSpinBox()
        self.spinner_distal_syn_perm_decrement.setAlignment(QtCore.Qt.AlignRight)
        self.spinner_distal_syn_perm_decrement.setDecimals(4)
        self.spinner_distal_syn_perm_decrement.setSingleStep(0.0001)
        self.spinner_distal_syn_perm_decrement.setEnabled(not self.main_window.isRunning())
        self.spinner_distal_syn_perm_decrement.setToolTip("The amount by which an inactive synapse is decremented in each round. Specified as a percent of a fully grown synapse.")

        # group_box_distal_syn_perm_layout
        group_box_distal_syn_perm_layout = QtWidgets.QGridLayout()
        group_box_distal_syn_perm_layout.addWidget(self.label_distal_syn_initial_perm, 0, 0)
        group_box_distal_syn_perm_layout.addWidget(self.spinner_distal_syn_initial_perm, 0, 1)
        group_box_distal_syn_perm_layout.addWidget(self.label_distal_syn_connected_perm, 1, 0)
        group_box_distal_syn_perm_layout.addWidget(self.spinner_distal_syn_connected_perm, 1, 1)
        group_box_distal_syn_perm_layout.addWidget(self.label_distal_syn_perm_increment, 2, 0)
        group_box_distal_syn_perm_layout.addWidget(self.spinner_distal_syn_perm_increment, 2, 1)
        group_box_distal_syn_perm_layout.addWidget(self.label_distal_syn_perm_decrement, 3, 0)
        group_box_distal_syn_perm_layout.addWidget(self.spinner_distal_syn_perm_decrement, 3, 1)

        # group_box_distal_syn_perm
        self.group_box_distal_syn_perm = QtWidgets.QGroupBox()
        self.group_box_distal_syn_perm.setLayout(group_box_distal_syn_perm_layout)
        self.group_box_distal_syn_perm.setTitle("Distal Synapses Permanence")

        # label_min_threshold
        self.label_min_threshold = QtWidgets.QLabel()
        self.label_min_threshold.setText("Min. Threshold")
        self.label_min_threshold.setAlignment(QtCore.Qt.AlignRight)
        self.label_min_threshold.setToolTip("If the number of synapses active on a segment is at least this threshold, it is selected as the best matching cell in a bursing column")

        # spinner_min_threshold
        self.spinner_min_threshold = QtWidgets.QSpinBox()
        self.spinner_min_threshold.setAlignment(QtCore.Qt.AlignRight)
        self.spinner_min_threshold.setEnabled(not self.main_window.isRunning())
        self.spinner_min_threshold.setToolTip("")

        # label_activation_threshold
        self.label_activation_threshold = QtWidgets.QLabel()
        self.label_activation_threshold.setText("Activation Threshold")
        self.label_activation_threshold.setAlignment(QtCore.Qt.AlignRight)

        # spinner_activation_threshold
        self.spinner_activation_threshold = QtWidgets.QSpinBox()
        self.spinner_activation_threshold.setAlignment(QtCore.Qt.AlignRight)
        self.spinner_activation_threshold.setEnabled(not self.main_window.isRunning())
        self.spinner_activation_threshold.setToolTip("If the number of active connected synapses on a segment is at least this threshold, the segment is said to be active")

        # label_max_new_synapses
        self.label_max_new_synapses = QtWidgets.QLabel()
        self.label_max_new_synapses.setText("Max. Num. New Synapses")
        self.label_max_new_synapses.setAlignment(QtCore.Qt.AlignRight)

        # spinner_max_new_synapses
        self.spinner_max_new_synapses = QtWidgets.QSpinBox()
        self.spinner_max_new_synapses.setAlignment(QtCore.Qt.AlignRight)
        self.spinner_max_new_synapses.setEnabled(not self.main_window.isRunning())
        self.spinner_max_new_synapses.setToolTip("The maximum number of synapses added to a segment during learning")

        # label_tp_seed
        self.label_tp_seed = QtWidgets.QLabel()
        self.label_tp_seed.setText("Seed")
        self.label_tp_seed.setAlignment(QtCore.Qt.AlignRight)

        # spinner_tp_seed
        self.spinner_tp_seed = QtWidgets.QSpinBox()
        self.spinner_tp_seed.setAlignment(QtCore.Qt.AlignRight)
        self.spinner_tp_seed.setMinimum(-1)
        self.spinner_tp_seed.setMaximum(5000)
        self.spinner_tp_seed.setEnabled(not self.main_window.isRunning())
        self.spinner_tp_seed.setToolTip("Seed for random values.")

        # tab_page_temporal_layout
        tab_page_temporal_layout = QtWidgets.QGridLayout()
        tab_page_temporal_layout.addWidget(self.label_cells_per_column, 0, 0)
        tab_page_temporal_layout.addWidget(self.spinner_cells_per_column, 0, 1)
        tab_page_temporal_layout.addWidget(self.group_box_distal_syn_perm, 1, 1)
        tab_page_temporal_layout.addWidget(self.label_min_threshold, 2, 0)
        tab_page_temporal_layout.addWidget(self.spinner_min_threshold, 2, 1)
        tab_page_temporal_layout.addWidget(self.label_activation_threshold, 3, 0)
        tab_page_temporal_layout.addWidget(self.spinner_activation_threshold, 3, 1)
        tab_page_temporal_layout.addWidget(self.label_max_new_synapses, 4, 0)
        tab_page_temporal_layout.addWidget(self.spinner_max_new_synapses, 4, 1)
        tab_page_temporal_layout.addWidget(self.label_tp_seed, 5, 0)
        tab_page_temporal_layout.addWidget(self.spinner_tp_seed, 5, 1)
        tab_page_temporal_layout.setRowStretch(6, 100)

        # tab_page_temporal
        self.tab_page_temporal = QtWidgets.QWidget()
        self.tab_page_temporal.setLayout(tab_page_temporal_layout)

        # tab_control_main
        self.tab_control_main = QtWidgets.QTabWidget()
        self.tab_control_main.addTab(self.tab_page_spatial, "Spatial Parameters")
        self.tab_control_main.addTab(self.tab_page_temporal, "Temporal Parameters")
        self.tab_control_main.selectedIndex = 1

        # button_box
        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.button_box.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self.buttonOk_click)
        self.button_box.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(not self.main_window.isRunning())
        self.button_box.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self.buttonCancel_click)

        # layout
        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(main_layout)
        layout.addWidget(self.tab_control_main)
        layout.addWidget(self.button_box)

        # self
        self.setLayout(layout)
        self.setModal(True)
        self.setWindowTitle("Region Properties")
        self.setWindowIcon(ICON)

    def setControlsValues(self):
        """
        Set controls values from a class instance.
        """

        # Set controls value with region params
        node = self.main_window.architecture_window.design_panel.under_mouse_node
        self.spinner_width.setValue(node.width)
        self.spinner_height.setValue(node.height)
        self.spinner_potential_radius.setValue(node.potential_radius)
        self.spinner_potential_pct.setValue(node.potential_pct)
        self.checkbox_global_inhibition.setChecked(node.global_inhibition)
        self.spinner_local_area_density.setValue(node.local_area_density)
        self.spinner_num_active_columns_per_inh_area.setValue(node.num_active_columns_per_inh_area)
        self.spinner_stimulus_threshold.setValue(node.stimulus_threshold)
        self.spinner_proximal_syn_connected_perm.setValue(node.proximal_syn_connected_perm)
        self.spinner_proximal_syn_perm_increment.setValue(node.proximal_syn_perm_increment)
        self.spinner_proximal_syn_perm_decrement.setValue(node.proximal_syn_perm_decrement)
        self.spinner_min_pct_overlap_duty_cycle.setValue(node.min_pct_overlap_duty_cycle)
        self.spinner_min_pct_active_duty_cycle.setValue(node.min_pct_active_duty_cycle)
        self.spinner_duty_cycle_period.setValue(node.duty_cycle_period)
        self.spinner_max_boost.setValue(node.max_boost)
        self.spinner_sp_seed.setValue(node.sp_seed)
        self.spinner_cells_per_column.setValue(node.cells_per_column)
        self.spinner_distal_syn_initial_perm.setValue(node.distal_syn_initial_perm)
        self.spinner_distal_syn_connected_perm.setValue(node.distal_syn_connected_perm)
        self.spinner_distal_syn_perm_increment.setValue(node.distal_syn_perm_increment)
        self.spinner_distal_syn_perm_decrement.setValue(node.distal_syn_perm_decrement)
        self.spinner_min_threshold.setValue(node.min_threshold)
        self.spinner_activation_threshold.setValue(node.activation_threshold)
        self.spinner_max_new_synapses.setValue(node.max_new_synapses)
        self.spinner_tp_seed.setValue(node.tp_seed)

    def buttonOk_click(self, event):
        """
        Check if values changed and save the,.
        """

        width = self.spinner_width.value()
        height = self.spinner_height.value()
        potential_radius = self.spinner_potential_radius.value()
        potential_pct = self.spinner_potential_pct.value()
        global_inhibition = self.checkbox_global_inhibition.isChecked()
        local_area_density = self.spinner_local_area_density.value()
        num_active_columns_per_inh_area = self.spinner_num_active_columns_per_inh_area.value()
        stimulus_threshold = self.spinner_stimulus_threshold.value()
        proximal_syn_connected_perm = self.spinner_proximal_syn_connected_perm.value()
        proximal_syn_perm_increment = self.spinner_proximal_syn_perm_increment.value()
        proximal_syn_perm_decrement = self.spinner_proximal_syn_perm_decrement.value()
        min_pct_overlap_duty_cycle = self.spinner_min_pct_overlap_duty_cycle.value()
        min_pct_active_duty_cycle = self.spinner_min_pct_active_duty_cycle.value()
        duty_cycle_period = self.spinner_duty_cycle_period.value()
        max_boost = self.spinner_max_boost.value()
        sp_seed = self.spinner_sp_seed.value()
        cells_per_column = self.spinner_cells_per_column.value()
        distal_syn_initial_perm = self.spinner_distal_syn_initial_perm.value()
        distal_syn_connected_perm = self.spinner_distal_syn_connected_perm.value()
        distal_syn_perm_increment = self.spinner_distal_syn_perm_increment.value()
        distal_syn_perm_decrement = self.spinner_distal_syn_perm_decrement.value()
        min_threshold = self.spinner_min_threshold.value()
        activation_threshold = self.spinner_activation_threshold.value()
        max_new_synapses = self.spinner_max_new_synapses.value()
        tp_seed = self.spinner_tp_seed.value()

        # If anything has changed
        node = self.main_window.architecture_window.design_panel.under_mouse_node
        if node.width != width or node.height != height or node.potential_radius != potential_radius or node.potential_pct != potential_pct or node.global_inhibition != global_inhibition or node.local_area_density != local_area_density or node.num_active_columns_per_inh_area != num_active_columns_per_inh_area or node.stimulus_threshold != stimulus_threshold\
            or node.proximal_syn_connected_perm != proximal_syn_connected_perm or node.proximal_syn_perm_increment != proximal_syn_perm_increment or node.proximal_syn_perm_decrement != proximal_syn_perm_decrement or node.min_pct_overlap_duty_cycle != min_pct_overlap_duty_cycle or node.min_pct_active_duty_cycle != min_pct_active_duty_cycle or node.duty_cycle_period != duty_cycle_period or node.max_boost != max_boost or node.sp_seed != sp_seed\
            or node.cells_per_column != cells_per_column or node.distal_syn_initial_perm != distal_syn_initial_perm or node.distal_syn_connected_perm != distal_syn_connected_perm or node.distal_syn_perm_increment != distal_syn_perm_increment or node.distal_syn_perm_decrement != distal_syn_perm_decrement or node.min_threshold != min_threshold or node.activation_threshold != activation_threshold or node.max_new_synapses != max_new_synapses or node.tp_seed != tp_seed:

            # Set region params with controls values
            node.width = width
            node.height = height
            node.potential_radius = potential_radius
            node.potential_pct = potential_pct
            node.global_inhibition = global_inhibition
            node.local_area_density = local_area_density
            node.num_active_columns_per_inh_area = num_active_columns_per_inh_area
            node.stimulus_threshold = stimulus_threshold
            node.proximal_syn_connected_perm = proximal_syn_connected_perm
            node.proximal_syn_perm_increment = proximal_syn_perm_increment
            node.proximal_syn_perm_decrement = proximal_syn_perm_decrement
            node.min_pct_overlap_duty_cycle = min_pct_overlap_duty_cycle
            node.min_pct_active_duty_cycle = min_pct_active_duty_cycle
            node.duty_cycle_period = duty_cycle_period
            node.max_boost = max_boost
            node.sp_seed = sp_seed
            node.cells_per_column = cells_per_column
            node.distal_syn_initial_perm = distal_syn_initial_perm
            node.distal_syn_connected_perm = distal_syn_connected_perm
            node.distal_syn_perm_increment = distal_syn_perm_increment
            node.distal_syn_perm_decrement = distal_syn_perm_decrement
            node.min_threshold = min_threshold
            node.activation_threshold = activation_threshold
            node.max_new_synapses = max_new_synapses
            node.tp_seed = tp_seed

            self.accept()

        self.close()

    def buttonCancel_click(self, event):
        self.reject()
        self.close()
