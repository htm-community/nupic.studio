from PyQt4 import QtGui, QtCore
from nupic_studio.ui import Global

class RegionForm(QtGui.QDialog):

  #region Constructor

  def __init__(self):
    """
    Initializes a new instance of this class.
    """

    QtGui.QDialog.__init__(self)

    self.initUI()

  #endregion

  #region Methods

  def initUI(self):

    # labelWidth
    self.labelWidth = QtGui.QLabel()
    self.labelWidth.setText("Width")
    self.labelWidth.setAlignment(QtCore.Qt.AlignRight)

    # spinnerWidth
    self.spinnerWidth = QtGui.QSpinBox()
    self.spinnerWidth.setAlignment(QtCore.Qt.AlignRight)
    self.spinnerWidth.setMinimum(3)
    self.spinnerWidth.setEnabled(not Global.simulationInitialized)
    self.spinnerWidth.setToolTip("")

    # labelHeight
    self.labelHeight = QtGui.QLabel()
    self.labelHeight.setText("Height")
    self.labelHeight.setAlignment(QtCore.Qt.AlignRight)

    # spinnerHeight
    self.spinnerHeight = QtGui.QSpinBox()
    self.spinnerHeight.setAlignment(QtCore.Qt.AlignRight)
    self.spinnerHeight.setMinimum(3)
    self.spinnerHeight.setEnabled(not Global.simulationInitialized)
    self.spinnerHeight.setToolTip("")

    # mainLayout
    mainLayout = QtGui.QGridLayout()
    mainLayout.addWidget(self.labelWidth, 0, 0)
    mainLayout.addWidget(self.spinnerWidth, 0, 1)
    mainLayout.addWidget(self.labelHeight, 1, 0)
    mainLayout.addWidget(self.spinnerHeight, 1, 1)

    # labelPotentialRadius
    self.labelPotentialRadius = QtGui.QLabel()
    self.labelPotentialRadius.setText("Potential Radius")
    self.labelPotentialRadius.setAlignment(QtCore.Qt.AlignRight)

    # spinnerPotentialRadius
    self.spinnerPotentialRadius = QtGui.QSpinBox()
    self.spinnerPotentialRadius.setAlignment(QtCore.Qt.AlignRight)
    self.spinnerPotentialRadius.setEnabled(not Global.simulationInitialized)
    self.spinnerPotentialRadius.setToolTip("This parameter determines the extent of the input that each column can potentially be connected to. This can be thought of as the input bits that are visible to each column, or a 'receptiveField' of the field of vision. A large enough value will result in 'global coverage', meaning that each column can potentially be connected to every input bit. This parameter defines a square (or hyper square) area: a column will have a max square potential pool with sides of length 2 * potentialRadius + 1.")

    # labelPotentialPct
    self.labelPotentialPct = QtGui.QLabel()
    self.labelPotentialPct.setText("Potential (%)")
    self.labelPotentialPct.setAlignment(QtCore.Qt.AlignRight)

    # spinnerPotentialPct
    self.spinnerPotentialPct = QtGui.QDoubleSpinBox()
    self.spinnerPotentialPct.setAlignment(QtCore.Qt.AlignRight)
    self.spinnerPotentialPct.setMaximum(1)
    self.spinnerPotentialPct.setDecimals(2)
    self.spinnerPotentialPct.setSingleStep(0.01)
    self.spinnerPotentialPct.setEnabled(not Global.simulationInitialized)
    self.spinnerPotentialPct.setToolTip("The percent of the inputs, within a column's potential radius, that a column can be connected to. If set to 1, the column will be connected to every input within its potential radius. This parameter is used to give each column a unique potential pool when a large potentialRadius causes overlap between the columns. At initialization time we choose ((2*potentialRadius + 1)^(# inputDimensions) * potentialPct) input bits to comprise the column's potential pool.")

    # checkBoxGlobalInhibition
    self.checkBoxGlobalInhibition = QtGui.QCheckBox()
    self.checkBoxGlobalInhibition.setText("Global Inhibition")
    self.checkBoxGlobalInhibition.setEnabled(not Global.simulationInitialized)
    self.checkBoxGlobalInhibition.setToolTip("If true, then during inhibition phase the winning columns are selected as the most active columns from the region as a whole. Otherwise, the winning columns are selected with respect to their local neighborhoods. Using global inhibition boosts performance x60.")

    # labelLocalAreaDensity
    self.labelLocalAreaDensity = QtGui.QLabel()
    self.labelLocalAreaDensity.setText("Local Area Density")
    self.labelLocalAreaDensity.setAlignment(QtCore.Qt.AlignRight)

    # spinnerLocalAreaDensity
    self.spinnerLocalAreaDensity = QtGui.QDoubleSpinBox()
    self.spinnerLocalAreaDensity.setAlignment(QtCore.Qt.AlignRight)
    self.spinnerLocalAreaDensity.setMinimum(-1.0)
    self.spinnerLocalAreaDensity.setDecimals(2)
    self.spinnerLocalAreaDensity.setSingleStep(0.01)
    self.spinnerLocalAreaDensity.setEnabled(not Global.simulationInitialized)
    self.spinnerLocalAreaDensity.setToolTip("The desired density of active columns within a local inhibition area (the size of which is set by the internally calculated inhibitionRadius, which is in turn determined from the average size of the connected potential pools of all columns). The inhibition logic will insure that at most N columns remain ON within a local inhibition area, where N = localAreaDensity * (total number of columns in inhibition area).")

    # labelNumActiveColumnsPerInhArea
    self.labelNumActiveColumnsPerInhArea = QtGui.QLabel()
    self.labelNumActiveColumnsPerInhArea.setText("Num. Active Columns Per Inh. Area")
    self.labelNumActiveColumnsPerInhArea.setAlignment(QtCore.Qt.AlignRight)

    # spinnerNumActiveColumnsPerInhArea
    self.spinnerNumActiveColumnsPerInhArea = QtGui.QSpinBox()
    self.spinnerNumActiveColumnsPerInhArea.setAlignment(QtCore.Qt.AlignRight)
    self.spinnerNumActiveColumnsPerInhArea.setEnabled(not Global.simulationInitialized)
    self.spinnerNumActiveColumnsPerInhArea.setToolTip("An alternate way to control the density of the active columns. If numActiveColumnsPerInhArea is specified then localAreaDensity must be less than 0, and vice versa. When using numActiveColumnsPerInhArea, the inhibition logic will insure that at most 'numActiveColumnsPerInhArea' columns remain ON within a local inhibition area (the size of which is set by the internally calculated inhibitionRadius, which is in turn determined from the average size of the connected receptive fields of all columns). When using this method, as columns learn and grow their effective receptive fields, the inhibitionRadius will grow, and hence the net density of the active columns will *decrease*. This is in contrast to the localAreaDensity method, which keeps the density of active columns the same regardless of the size of their receptive fields.")

    # labelStimulusThreshold
    self.labelStimulusThreshold = QtGui.QLabel()
    self.labelStimulusThreshold.setText("Stimulus Threshold")
    self.labelStimulusThreshold.setAlignment(QtCore.Qt.AlignRight)

    # spinnerStimulusThreshold
    self.spinnerStimulusThreshold = QtGui.QSpinBox()
    self.spinnerStimulusThreshold.setAlignment(QtCore.Qt.AlignRight)
    self.spinnerStimulusThreshold.setEnabled(not Global.simulationInitialized)
    self.spinnerStimulusThreshold.setToolTip("This is a number specifying the minimum number of synapses that must be on in order for a columns to turn ON. The purpose of this is to prevent noise input from activating columns. Specified as a percent of a fully grown synapse.")

    # labelProximalSynConnectedPerm
    self.labelProximalSynConnectedPerm = QtGui.QLabel()
    self.labelProximalSynConnectedPerm.setText("Connected")
    self.labelProximalSynConnectedPerm.setAlignment(QtCore.Qt.AlignRight)

    # spinnerProximalSynConnectedPerm
    self.spinnerProximalSynConnectedPerm = QtGui.QDoubleSpinBox()
    self.spinnerProximalSynConnectedPerm.setAlignment(QtCore.Qt.AlignRight)
    self.spinnerProximalSynConnectedPerm.setDecimals(4)
    self.spinnerProximalSynConnectedPerm.setSingleStep(0.0001)
    self.spinnerProximalSynConnectedPerm.setEnabled(not Global.simulationInitialized)
    self.spinnerProximalSynConnectedPerm.setToolTip("The default connected threshold. Any synapse whose permanence value is above the connected threshold is a 'connected synapse', meaning it can contribute to the cell's firing.")

    # labelProximalSynPermIncrement
    self.labelProximalSynPermIncrement = QtGui.QLabel()
    self.labelProximalSynPermIncrement.setText("Increment")
    self.labelProximalSynPermIncrement.setAlignment(QtCore.Qt.AlignRight)

    # spinnerProximalSynPermIncrement
    self.spinnerProximalSynPermIncrement = QtGui.QDoubleSpinBox()
    self.spinnerProximalSynPermIncrement.setAlignment(QtCore.Qt.AlignRight)
    self.spinnerProximalSynPermIncrement.setDecimals(4)
    self.spinnerProximalSynPermIncrement.setSingleStep(0.0001)
    self.spinnerProximalSynPermIncrement.setEnabled(not Global.simulationInitialized)
    self.spinnerProximalSynPermIncrement.setToolTip("The amount by which an active synapse is incremented in each round. Specified as a percent of a fully grown synapse.")

    # labelProximalSynPermDecrement
    self.labelProximalSynPermDecrement = QtGui.QLabel()
    self.labelProximalSynPermDecrement.setText("Decrement")
    self.labelProximalSynPermDecrement.setAlignment(QtCore.Qt.AlignRight)

    # spinnerProximalSynPermDecrement
    self.spinnerProximalSynPermDecrement = QtGui.QDoubleSpinBox()
    self.spinnerProximalSynPermDecrement.setAlignment(QtCore.Qt.AlignRight)
    self.spinnerProximalSynPermDecrement.setDecimals(4)
    self.spinnerProximalSynPermDecrement.setSingleStep(0.0001)
    self.spinnerProximalSynPermDecrement.setEnabled(not Global.simulationInitialized)
    self.spinnerProximalSynPermDecrement.setToolTip("The amount by which an inactive synapse is decremented in each round. Specified as a percent of a fully grown synapse.")

    # groupBoxProximalSynPerm
    groupBoxProximalSynPermLayout = QtGui.QGridLayout()
    groupBoxProximalSynPermLayout.addWidget(self.labelProximalSynConnectedPerm, 0, 0)
    groupBoxProximalSynPermLayout.addWidget(self.spinnerProximalSynConnectedPerm, 0, 1)
    groupBoxProximalSynPermLayout.addWidget(self.labelProximalSynPermIncrement, 1, 0)
    groupBoxProximalSynPermLayout.addWidget(self.spinnerProximalSynPermIncrement, 1, 1)
    groupBoxProximalSynPermLayout.addWidget(self.labelProximalSynPermDecrement, 2, 0)
    groupBoxProximalSynPermLayout.addWidget(self.spinnerProximalSynPermDecrement, 2, 1)

    # groupBoxProximalSynPerm
    self.groupBoxProximalSynPerm = QtGui.QGroupBox()
    self.groupBoxProximalSynPerm.setLayout(groupBoxProximalSynPermLayout)
    self.groupBoxProximalSynPerm.setTitle("Proximal Synapses Permanence")

    # labelMinPctOverlapDutyCycle
    self.labelMinPctOverlapDutyCycle = QtGui.QLabel()
    self.labelMinPctOverlapDutyCycle.setText("Min. Overlap Duty Cycle (%)")
    self.labelMinPctOverlapDutyCycle.setAlignment(QtCore.Qt.AlignRight)

    # spinnerMinPctOverlapDutyCycle
    self.spinnerMinPctOverlapDutyCycle = QtGui.QDoubleSpinBox()
    self.spinnerMinPctOverlapDutyCycle.setAlignment(QtCore.Qt.AlignRight)
    self.spinnerMinPctOverlapDutyCycle.setMaximum(100)
    self.spinnerMinPctOverlapDutyCycle.setDecimals(3)
    self.spinnerMinPctOverlapDutyCycle.setSingleStep(0.001)
    self.spinnerMinPctOverlapDutyCycle.setEnabled(not Global.simulationInitialized)
    self.spinnerMinPctOverlapDutyCycle.setToolTip("A number between 0 and 1.0, used to set a floor on how often a column should have at least stimulusThreshold active inputs. Periodically, each column looks at the overlap duty cycle of all other columns within its inhibition radius and sets its own internal minimal acceptable duty cycle to:\
      minPctDutyCycleBeforeInh * max(other columns' duty cycles).\
    On each iteration, any column whose overlap duty cycle falls below this computed value will get all of its permanence values boosted up by synPermActiveInc. Raising all permanences in response to a sub-par duty cycle before inhibition allows a cell to search for new inputs when either its previously learned inputs are no longer ever active, or when the vast majority of them have been 'hijacked' by other columns.")

    # labelMinPctActiveDutyCycle
    self.labelMinPctActiveDutyCycle = QtGui.QLabel()
    self.labelMinPctActiveDutyCycle.setText("Min. Active Duty Cycle (%)")
    self.labelMinPctActiveDutyCycle.setAlignment(QtCore.Qt.AlignRight)

    # spinnerMinPctActiveDutyCycle
    self.spinnerMinPctActiveDutyCycle = QtGui.QDoubleSpinBox()
    self.spinnerMinPctActiveDutyCycle.setAlignment(QtCore.Qt.AlignRight)
    self.spinnerMinPctActiveDutyCycle.setMaximum(100)
    self.spinnerMinPctActiveDutyCycle.setDecimals(3)
    self.spinnerMinPctActiveDutyCycle.setSingleStep(0.001)
    self.spinnerMinPctActiveDutyCycle.setEnabled(not Global.simulationInitialized)
    self.spinnerMinPctActiveDutyCycle.setToolTip("A number between 0 and 1.0, used to set a floor on how often a column should be activate. Periodically, each column looks at the activity duty cycle of all other columns within its inhibition radius and sets its own internal minimal acceptable duty cycle to:\
      minPctDutyCycleAfterInh * max(other columns' duty cycles).\
    On each iteration, any column whose duty cycle after inhibition falls below this computed value will get its internal boost factor increased.")

    # labelDutyCyclePeriod
    self.labelDutyCyclePeriod = QtGui.QLabel()
    self.labelDutyCyclePeriod.setText("Duty Cycle Period")
    self.labelDutyCyclePeriod.setAlignment(QtCore.Qt.AlignRight)

    # spinnerDutyCyclePeriod
    self.spinnerDutyCyclePeriod = QtGui.QSpinBox()
    self.spinnerDutyCyclePeriod.setAlignment(QtCore.Qt.AlignRight)
    self.spinnerDutyCyclePeriod.setMaximum(1000)
    self.spinnerDutyCyclePeriod.setEnabled(not Global.simulationInitialized)
    self.spinnerDutyCyclePeriod.setToolTip("The period used to calculate duty cycles. Higher values make it take longer to respond to changes in boost or synPerConnectedCell. Shorter values make it more unstable and likely to oscillate.")

    # labelMaxBoost
    self.labelMaxBoost = QtGui.QLabel()
    self.labelMaxBoost.setText("Max Boost")
    self.labelMaxBoost.setAlignment(QtCore.Qt.AlignRight)

    # spinnerMaxBoost
    self.spinnerMaxBoost = QtGui.QDoubleSpinBox()
    self.spinnerMaxBoost.setAlignment(QtCore.Qt.AlignRight)
    self.spinnerMaxBoost.setDecimals(2)
    self.spinnerMaxBoost.setSingleStep(0.01)
    self.spinnerMaxBoost.setEnabled(not Global.simulationInitialized)
    self.spinnerMaxBoost.setToolTip("The maximum overlap boost factor. Each column's overlap gets multiplied by a boost factor before it gets considered for inhibition. The actual boost factor for a column is number between 1.0 and maxBoost. A boost factor of 1.0 is used if the duty cycle is >= minOverlapDutyCycle, maxBoost is used if the duty cycle is 0, and any duty cycle in between is linearly extrapolated from these 2 endpoints.")

    # labelSpSeed
    self.labelSpSeed = QtGui.QLabel()
    self.labelSpSeed.setText("Seed")
    self.labelSpSeed.setAlignment(QtCore.Qt.AlignRight)

    # spinnerSpSeed
    self.spinnerSpSeed = QtGui.QSpinBox()
    self.spinnerSpSeed.setAlignment(QtCore.Qt.AlignRight)
    self.spinnerSpSeed.setMinimum(-1)
    self.spinnerSpSeed.setMaximum(5000)
    self.spinnerSpSeed.setEnabled(not Global.simulationInitialized)
    self.spinnerSpSeed.setToolTip("Seed for random values.")

    # tabPageSpatialLayout
    tabPageSpatialLayout = QtGui.QGridLayout()
    tabPageSpatialLayout.addWidget(self.labelPotentialRadius, 0, 0)
    tabPageSpatialLayout.addWidget(self.spinnerPotentialRadius, 0, 1)
    tabPageSpatialLayout.addWidget(self.labelPotentialPct, 1, 0)
    tabPageSpatialLayout.addWidget(self.spinnerPotentialPct, 1, 1)
    tabPageSpatialLayout.addWidget(self.checkBoxGlobalInhibition, 2, 0)
    tabPageSpatialLayout.addWidget(self.labelLocalAreaDensity, 3, 0)
    tabPageSpatialLayout.addWidget(self.spinnerLocalAreaDensity, 3, 1)
    tabPageSpatialLayout.addWidget(self.labelNumActiveColumnsPerInhArea, 4, 0)
    tabPageSpatialLayout.addWidget(self.spinnerNumActiveColumnsPerInhArea, 4, 1)
    tabPageSpatialLayout.addWidget(self.labelStimulusThreshold, 5, 0)
    tabPageSpatialLayout.addWidget(self.spinnerStimulusThreshold, 5, 1)
    tabPageSpatialLayout.addWidget(self.groupBoxProximalSynPerm, 6, 1)
    tabPageSpatialLayout.addWidget(self.labelMinPctOverlapDutyCycle, 7, 0)
    tabPageSpatialLayout.addWidget(self.spinnerMinPctOverlapDutyCycle, 7, 1)
    tabPageSpatialLayout.addWidget(self.labelMinPctActiveDutyCycle, 8, 0)
    tabPageSpatialLayout.addWidget(self.spinnerMinPctActiveDutyCycle, 8, 1)
    tabPageSpatialLayout.addWidget(self.labelDutyCyclePeriod, 9, 0)
    tabPageSpatialLayout.addWidget(self.spinnerDutyCyclePeriod, 9, 1)
    tabPageSpatialLayout.addWidget(self.labelMaxBoost, 10, 0)
    tabPageSpatialLayout.addWidget(self.spinnerMaxBoost, 10, 1)
    tabPageSpatialLayout.addWidget(self.labelSpSeed, 11, 0)
    tabPageSpatialLayout.addWidget(self.spinnerSpSeed, 11, 1)

    # tabPageSpatial
    self.tabPageSpatial = QtGui.QWidget()
    self.tabPageSpatial.setLayout(tabPageSpatialLayout)

    # labelNumCellsPerColumn
    self.labelNumCellsPerColumn = QtGui.QLabel()
    self.labelNumCellsPerColumn.setText("Num. Cells Per Column")
    self.labelNumCellsPerColumn.setAlignment(QtCore.Qt.AlignRight)

    # spinnerNumCellsPerColumn
    self.spinnerNumCellsPerColumn = QtGui.QSpinBox()
    self.spinnerNumCellsPerColumn.setAlignment(QtCore.Qt.AlignRight)
    self.spinnerNumCellsPerColumn.setMinimum(1)
    self.spinnerNumCellsPerColumn.setEnabled(not Global.simulationInitialized)
    self.spinnerNumCellsPerColumn.setToolTip("Number of cells per column. More cells, more contextual information")

    # labelLearningRadius
    self.labelLearningRadius = QtGui.QLabel()
    self.labelLearningRadius.setText("Learning Radius")
    self.labelLearningRadius.setAlignment(QtCore.Qt.AlignRight)

    # spinnerLearningRadius
    self.spinnerLearningRadius = QtGui.QSpinBox()
    self.spinnerLearningRadius.setAlignment(QtCore.Qt.AlignRight)
    self.spinnerLearningRadius.setMinimum(1)
    self.spinnerLearningRadius.setMaximum(10000)
    self.spinnerLearningRadius.setEnabled(not Global.simulationInitialized)
    self.spinnerLearningRadius.setToolTip("Radius around cell from which it can sample to form distal dendrite connections")

    # labelDistalSynInitialPerm
    self.labelDistalSynInitialPerm = QtGui.QLabel()
    self.labelDistalSynInitialPerm.setText("Initial")
    self.labelDistalSynInitialPerm.setAlignment(QtCore.Qt.AlignRight)

    # spinnerDistalSynInitialPerm
    self.spinnerDistalSynInitialPerm = QtGui.QDoubleSpinBox()
    self.spinnerDistalSynInitialPerm.setAlignment(QtCore.Qt.AlignRight)
    self.spinnerDistalSynInitialPerm.setDecimals(4)
    self.spinnerDistalSynInitialPerm.setSingleStep(0.0001)
    self.spinnerDistalSynInitialPerm.setEnabled(not Global.simulationInitialized)
    self.spinnerDistalSynInitialPerm.setToolTip("The initial permanence of an distal synapse.")

    # labelDistalSynConnectedPerm
    self.labelDistalSynConnectedPerm = QtGui.QLabel()
    self.labelDistalSynConnectedPerm.setText("Connected")
    self.labelDistalSynConnectedPerm.setAlignment(QtCore.Qt.AlignRight)

    # spinnerDistalSynConnectedPerm
    self.spinnerDistalSynConnectedPerm = QtGui.QDoubleSpinBox()
    self.spinnerDistalSynConnectedPerm.setAlignment(QtCore.Qt.AlignRight)
    self.spinnerDistalSynConnectedPerm.setDecimals(4)
    self.spinnerDistalSynConnectedPerm.setSingleStep(0.0001)
    self.spinnerDistalSynConnectedPerm.setEnabled(not Global.simulationInitialized)
    self.spinnerDistalSynConnectedPerm.setToolTip("The default connected threshold. Any synapse whose permanence value is above the connected threshold is a 'connected synapse', meaning it can contribute to the cell's firing.")

    # labelDistalSynPermIncrement
    self.labelDistalSynPermIncrement = QtGui.QLabel()
    self.labelDistalSynPermIncrement.setText("Increment")
    self.labelDistalSynPermIncrement.setAlignment(QtCore.Qt.AlignRight)

    # spinnerDistalSynPermIncrement
    self.spinnerDistalSynPermIncrement = QtGui.QDoubleSpinBox()
    self.spinnerDistalSynPermIncrement.setAlignment(QtCore.Qt.AlignRight)
    self.spinnerDistalSynPermIncrement.setDecimals(4)
    self.spinnerDistalSynPermIncrement.setSingleStep(0.0001)
    self.spinnerDistalSynPermIncrement.setEnabled(not Global.simulationInitialized)
    self.spinnerDistalSynPermIncrement.setToolTip("The amount by which an active synapse is incremented in each round. Specified as a percent of a fully grown synapse.")

    # labelDistalSynPermDecrement
    self.labelDistalSynPermDecrement = QtGui.QLabel()
    self.labelDistalSynPermDecrement.setText("Decrement")
    self.labelDistalSynPermDecrement.setAlignment(QtCore.Qt.AlignRight)

    # spinnerDistalSynPermDecrement
    self.spinnerDistalSynPermDecrement = QtGui.QDoubleSpinBox()
    self.spinnerDistalSynPermDecrement.setAlignment(QtCore.Qt.AlignRight)
    self.spinnerDistalSynPermDecrement.setDecimals(4)
    self.spinnerDistalSynPermDecrement.setSingleStep(0.0001)
    self.spinnerDistalSynPermDecrement.setEnabled(not Global.simulationInitialized)
    self.spinnerDistalSynPermDecrement.setToolTip("The amount by which an inactive synapse is decremented in each round. Specified as a percent of a fully grown synapse.")

    # groupBoxDistalSynPermLayout
    groupBoxDistalSynPermLayout = QtGui.QGridLayout()
    groupBoxDistalSynPermLayout.addWidget(self.labelDistalSynInitialPerm, 0, 0)
    groupBoxDistalSynPermLayout.addWidget(self.spinnerDistalSynInitialPerm, 0, 1)
    groupBoxDistalSynPermLayout.addWidget(self.labelDistalSynConnectedPerm, 1, 0)
    groupBoxDistalSynPermLayout.addWidget(self.spinnerDistalSynConnectedPerm, 1, 1)
    groupBoxDistalSynPermLayout.addWidget(self.labelDistalSynPermIncrement, 2, 0)
    groupBoxDistalSynPermLayout.addWidget(self.spinnerDistalSynPermIncrement, 2, 1)
    groupBoxDistalSynPermLayout.addWidget(self.labelDistalSynPermDecrement, 3, 0)
    groupBoxDistalSynPermLayout.addWidget(self.spinnerDistalSynPermDecrement, 3, 1)

    # groupBoxDistalSynPerm
    self.groupBoxDistalSynPerm = QtGui.QGroupBox()
    self.groupBoxDistalSynPerm.setLayout(groupBoxDistalSynPermLayout)
    self.groupBoxDistalSynPerm.setTitle("Distal Synapses Permanence")

    # labelMinThreshold
    self.labelMinThreshold = QtGui.QLabel()
    self.labelMinThreshold.setText("Min. Threshold")
    self.labelMinThreshold.setAlignment(QtCore.Qt.AlignRight)
    self.labelMinThreshold.setToolTip("If the number of synapses active on a segment is at least this threshold, it is selected as the best matching cell in a bursing column")

    # spinnerMinThreshold
    self.spinnerMinThreshold = QtGui.QSpinBox()
    self.spinnerMinThreshold.setAlignment(QtCore.Qt.AlignRight)
    self.spinnerMinThreshold.setEnabled(not Global.simulationInitialized)
    self.spinnerMinThreshold.setToolTip("")

    # labelActivationThreshold
    self.labelActivationThreshold = QtGui.QLabel()
    self.labelActivationThreshold.setText("Activation Threshold")
    self.labelActivationThreshold.setAlignment(QtCore.Qt.AlignRight)

    # spinnerActivationThreshold
    self.spinnerActivationThreshold = QtGui.QSpinBox()
    self.spinnerActivationThreshold.setAlignment(QtCore.Qt.AlignRight)
    self.spinnerActivationThreshold.setEnabled(not Global.simulationInitialized)
    self.spinnerActivationThreshold.setToolTip("If the number of active connected synapses on a segment is at least this threshold, the segment is said to be active")

    # labelMaxNumNewSynapses
    self.labelMaxNumNewSynapses = QtGui.QLabel()
    self.labelMaxNumNewSynapses.setText("Max. Num. New Synapses")
    self.labelMaxNumNewSynapses.setAlignment(QtCore.Qt.AlignRight)

    # spinnerMaxNumNewSynapses
    self.spinnerMaxNumNewSynapses = QtGui.QSpinBox()
    self.spinnerMaxNumNewSynapses.setAlignment(QtCore.Qt.AlignRight)
    self.spinnerMaxNumNewSynapses.setEnabled(not Global.simulationInitialized)
    self.spinnerMaxNumNewSynapses.setToolTip("The maximum number of synapses added to a segment during learning")

    # labelTpSeed
    self.labelTpSeed = QtGui.QLabel()
    self.labelTpSeed.setText("Seed")
    self.labelTpSeed.setAlignment(QtCore.Qt.AlignRight)

    # spinnerTpSeed
    self.spinnerTpSeed = QtGui.QSpinBox()
    self.spinnerTpSeed.setAlignment(QtCore.Qt.AlignRight)
    self.spinnerTpSeed.setMinimum(-1)
    self.spinnerTpSeed.setMaximum(5000)
    self.spinnerTpSeed.setEnabled(not Global.simulationInitialized)
    self.spinnerTpSeed.setToolTip("Seed for random values.")

    # tabPageTemporalLayout
    tabPageTemporalLayout = QtGui.QGridLayout()
    tabPageTemporalLayout.addWidget(self.labelNumCellsPerColumn, 0, 0)
    tabPageTemporalLayout.addWidget(self.spinnerNumCellsPerColumn, 0, 1)
    tabPageTemporalLayout.addWidget(self.labelLearningRadius, 1, 0)
    tabPageTemporalLayout.addWidget(self.spinnerLearningRadius, 1, 1)
    tabPageTemporalLayout.addWidget(self.groupBoxDistalSynPerm, 2, 1)
    tabPageTemporalLayout.addWidget(self.labelMinThreshold, 3, 0)
    tabPageTemporalLayout.addWidget(self.spinnerMinThreshold, 3, 1)
    tabPageTemporalLayout.addWidget(self.labelActivationThreshold, 4, 0)
    tabPageTemporalLayout.addWidget(self.spinnerActivationThreshold, 4, 1)
    tabPageTemporalLayout.addWidget(self.labelMaxNumNewSynapses, 5, 0)
    tabPageTemporalLayout.addWidget(self.spinnerMaxNumNewSynapses, 5, 1)
    tabPageTemporalLayout.addWidget(self.labelTpSeed, 6, 0)
    tabPageTemporalLayout.addWidget(self.spinnerTpSeed, 6, 1)
    tabPageTemporalLayout.setRowStretch(7, 100)

    # tabPageTemporal
    self.tabPageTemporal = QtGui.QWidget()
    self.tabPageTemporal.setLayout(tabPageTemporalLayout)

    # tabControlMain
    self.tabControlMain = QtGui.QTabWidget()
    self.tabControlMain.addTab(self.tabPageSpatial, "Spatial Parameters")
    self.tabControlMain.addTab(self.tabPageTemporal, "Temporal Parameters")
    self.tabControlMain.selectedIndex = 1

    # buttonBox
    self.buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel)
    self.buttonBox.button(QtGui.QDialogButtonBox.Ok).clicked.connect(self.__buttonOk_Click)
    self.buttonBox.button(QtGui.QDialogButtonBox.Ok).setEnabled(not Global.simulationInitialized)
    self.buttonBox.button(QtGui.QDialogButtonBox.Cancel).clicked.connect(self.__buttonCancel_Click)

    # layout
    layout = QtGui.QVBoxLayout()
    layout.addLayout(mainLayout)
    layout.addWidget(self.tabControlMain)
    layout.addWidget(self.buttonBox)

    # RegionForm
    self.setLayout(layout)
    self.setModal(True)
    self.setWindowTitle("Region Properties")
    self.setWindowIcon(QtGui.QIcon(Global.appPath + '/images/logo.ico'))

  def setControlsValues(self):
    """
    Set controls values from a class instance.
    """

    # Set controls value with region params
    node = Global.architectureForm.designPanel.underMouseNode
    self.spinnerWidth.setValue(node.width)
    self.spinnerHeight.setValue(node.height)
    self.spinnerPotentialRadius.setValue(node.potentialRadius)
    self.spinnerPotentialPct.setValue(node.potentialPct)
    self.checkBoxGlobalInhibition.setChecked(node.globalInhibition)
    self.spinnerLocalAreaDensity.setValue(node.localAreaDensity)
    self.spinnerNumActiveColumnsPerInhArea.setValue(node.numActiveColumnsPerInhArea)
    self.spinnerStimulusThreshold.setValue(node.stimulusThreshold)
    self.spinnerProximalSynConnectedPerm.setValue(node.proximalSynConnectedPerm)
    self.spinnerProximalSynPermIncrement.setValue(node.proximalSynPermIncrement)
    self.spinnerProximalSynPermDecrement.setValue(node.proximalSynPermDecrement)
    self.spinnerMinPctOverlapDutyCycle.setValue(node.minPctOverlapDutyCycle)
    self.spinnerMinPctActiveDutyCycle.setValue(node.minPctActiveDutyCycle)
    self.spinnerDutyCyclePeriod.setValue(node.dutyCyclePeriod)
    self.spinnerMaxBoost.setValue(node.maxBoost)
    self.spinnerSpSeed.setValue(node.spSeed)
    self.spinnerNumCellsPerColumn.setValue(node.numCellsPerColumn)
    self.spinnerLearningRadius.setValue(node.learningRadius)
    self.spinnerDistalSynInitialPerm.setValue(node.distalSynInitialPerm)
    self.spinnerDistalSynConnectedPerm.setValue(node.distalSynConnectedPerm)
    self.spinnerDistalSynPermIncrement.setValue(node.distalSynPermIncrement)
    self.spinnerDistalSynPermDecrement.setValue(node.distalSynPermDecrement)
    self.spinnerMinThreshold.setValue(node.minThreshold)
    self.spinnerActivationThreshold.setValue(node.activationThreshold)
    self.spinnerMaxNumNewSynapses.setValue(node.maxNumNewSynapses)
    self.spinnerTpSeed.setValue(node.tpSeed)

  #endregion

  #region Events

  def __buttonOk_Click(self, event):
    """
    Check if values changed and save the,.
    """

    width = self.spinnerWidth.value()
    height = self.spinnerHeight.value()
    potentialRadius = self.spinnerPotentialRadius.value()
    potentialPct = self.spinnerPotentialPct.value()
    globalInhibition = self.checkBoxGlobalInhibition.isChecked()
    localAreaDensity = self.spinnerLocalAreaDensity.value()
    numActiveColumnsPerInhArea = self.spinnerNumActiveColumnsPerInhArea.value()
    stimulusThreshold = self.spinnerStimulusThreshold.value()
    proximalSynConnectedPerm = self.spinnerProximalSynConnectedPerm.value()
    proximalSynPermIncrement = self.spinnerProximalSynPermIncrement.value()
    proximalSynPermDecrement = self.spinnerProximalSynPermDecrement.value()
    minPctOverlapDutyCycle = self.spinnerMinPctOverlapDutyCycle.value()
    minPctActiveDutyCycle = self.spinnerMinPctActiveDutyCycle.value()
    dutyCyclePeriod = self.spinnerDutyCyclePeriod.value()
    maxBoost = self.spinnerMaxBoost.value()
    spSeed = self.spinnerSpSeed.value()
    numCellsPerColumn = self.spinnerNumCellsPerColumn.value()
    learningRadius = self.spinnerLearningRadius.value()
    distalSynInitialPerm = self.spinnerDistalSynInitialPerm.value()
    distalSynConnectedPerm = self.spinnerDistalSynConnectedPerm.value()
    distalSynPermIncrement = self.spinnerDistalSynPermIncrement.value()
    distalSynPermDecrement = self.spinnerDistalSynPermDecrement.value()
    minThreshold = self.spinnerMinThreshold.value()
    activationThreshold = self.spinnerActivationThreshold.value()
    maxNumNewSynapses = self.spinnerMaxNumNewSynapses.value()
    tpSeed = self.spinnerTpSeed.value()

    # If anything has changed
    node = Global.architectureForm.designPanel.underMouseNode
    if  node.width != width or node.height != height or node.potentialRadius != potentialRadius or node.potentialPct != potentialPct or node.globalInhibition != globalInhibition or node.localAreaDensity != localAreaDensity or node.numActiveColumnsPerInhArea != numActiveColumnsPerInhArea or node.stimulusThreshold != stimulusThreshold\
      or node.proximalSynConnectedPerm != proximalSynConnectedPerm or node.proximalSynPermIncrement != proximalSynPermIncrement or node.proximalSynPermDecrement != proximalSynPermDecrement or node.minPctOverlapDutyCycle != minPctOverlapDutyCycle or node.minPctActiveDutyCycle != minPctActiveDutyCycle or node.dutyCyclePeriod != dutyCyclePeriod or node.maxBoost != maxBoost or node.spSeed != spSeed\
       or node.numCellsPerColumn != numCellsPerColumn or node.learningRadius != learningRadius or node.distalSynInitialPerm != distalSynInitialPerm or node.distalSynConnectedPerm != distalSynConnectedPerm or node.distalSynPermIncrement != distalSynPermIncrement or node.distalSynPermDecrement != distalSynPermDecrement or node.minThreshold != minThreshold or node.activationThreshold != activationThreshold or node.maxNumNewSynapses != maxNumNewSynapses or node.tpSeed != tpSeed:

      # Set region params with controls values
      node.width = width
      node.height = height
      node.potentialRadius = potentialRadius
      node.potentialPct = potentialPct
      node.globalInhibition = globalInhibition
      node.localAreaDensity = localAreaDensity
      node.numActiveColumnsPerInhArea = numActiveColumnsPerInhArea
      node.stimulusThreshold = stimulusThreshold
      node.proximalSynConnectedPerm = proximalSynConnectedPerm
      node.proximalSynPermIncrement = proximalSynPermIncrement
      node.proximalSynPermDecrement = proximalSynPermDecrement
      node.minPctOverlapDutyCycle = minPctOverlapDutyCycle
      node.minPctActiveDutyCycle = minPctActiveDutyCycle
      node.dutyCyclePeriod = dutyCyclePeriod
      node.maxBoost = maxBoost
      node.spSeed = spSeed
      node.numCellsPerColumn = numCellsPerColumn
      node.learningRadius = learningRadius
      node.distalSynInitialPerm = distalSynInitialPerm
      node.distalSynConnectedPerm = distalSynConnectedPerm
      node.distalSynPermIncrement = distalSynPermIncrement
      node.distalSynPermDecrement = distalSynPermDecrement
      node.minThreshold = minThreshold
      node.activationThreshold = activationThreshold
      node.maxNumNewSynapses = maxNumNewSynapses
      node.tpSeed = tpSeed

      self.accept()

    self.close()

  def __buttonCancel_Click(self, event):
    self.reject()
    self.close()

  #endregion
