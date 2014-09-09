from nustudio.htm import maxStoredSteps
from nustudio.ui import Global

class Bit:
	"""
	A class only to group properties related to input bits of sensors.
	"""

	#region Constructor

	def __init__(self):
		"""
		Initializes a new instance of this class.
		"""

		self.initialize()

	#endregion

	#region Methods

	def initialize(self):
		"""
		Initialize this bit.
		"""

		self.x = -1
		"""Position on X axis"""

		self.y = -1
		"""Position on Y axis"""

		# States of this element
		self.isActive = [False] * maxStoredSteps
		self.isPredicted = [False] * maxStoredSteps

		#region Statistics properties

		self.statsActivationCount = 0
		self.statsActivationRate = 0.
		self.statsPreditionCount = 0
		self.statsPrecisionRate = 0.

		#endregion

		#region 3d-tree properties (simulation form)

		self.tree3d_initialized = False
		self.tree3d_x = 0
		self.tree3d_y = 0
		self.tree3d_z = 0
		self.tree3d_item = None
		self.tree3d_selected = False

		#endregion

	def nextStep(self):
		"""
		Perfoms actions related to time step progression.
		"""

		# Update states machine by remove the first element and add a new element in the end
		if len(self.isActive) > maxStoredSteps:
			self.isActive.remove(self.isActive[0])
			self.isPredicted.remove(self.isPredicted[0])
		self.isActive.append(False)
		self.isPredicted.append(False)

		# Calculate statistics
		if self.isActive[maxStoredSteps - 1]:
			self.statsActivationCount += 1
		if self.isPredicted[maxStoredSteps - 1]:
			self.statsPreditionCount += 1
		if Global.currStep > 0:
			self.statsActivationRate = self.statsActivationCount / Global.currStep
		if self.statsActivationCount > 0:
			self.statsPrecisionRate = self.statsPreditionCount / self.statsActivationCount

	#endregion
