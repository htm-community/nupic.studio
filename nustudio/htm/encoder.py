
class Encoder:
	"""
	This is a super class which every derived encoder should inherits.
	Raw data should be encoded to map of bits which are readable for HTM's
	"""

	def __init__(self):
		"""
		Constructor.
		"""

		pass

	def encodeToHtm(self, rawData):
		"""
		Transform raw data to a map of bits and return this.
		"""

		pass

	def decodeFromHtm(self, htmData):
		"""
		Transform a map of bits to raw data and return this.
		"""

		pass
