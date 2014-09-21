import ast
from PyQt4 import QtGui, QtCore

__version__ = "1.0.0"

def getInstantiatedClass(moduleName, className, classParams):
	"""
	Return an instantiated class given a module, class, and constructor params
	"""

	module = __import__(moduleName, fromlist=[className])
	class_ = getattr(module, className)
	params = ast.literal_eval(classParams)
	instance = class_(**params)

	return instance

class ArrayTableModel(QtGui.QStandardItemModel):

	def __init__(self, flags):
		QtGui.QStandardItemModel.__init__(self)

		self.flags = flags
		self.header = []
		self.data = []

	def update(self, header, data):
		self.header = header
		self.data = data

		numCols = len(self.header)
		self.setColumnCount(numCols)
		numRows = len(self.data)
		self.setRowCount(numRows)

		for col in range(numCols):
			self.setHeaderData(col, QtCore.Qt.Horizontal, self.header[col])

		for row in range(numRows):
			for col in range(numCols):
				value = self.data[row][col]
				self.setData(self.index(row, col, QtCore.QModelIndex()), value)

	def setData(self, index, value, role=None):
		self.data[index.row()][index.column()] = value
		return True

	def data(self, index, role=None):
		column, row = index.column(), index.row()
		if role == QtCore.Qt.TextAlignmentRole:
			return QtCore.Qt.AlignRight
		elif role == QtCore.Qt.DisplayRole:
			return self.data[row][column]
		return

	def columnCount(self, parent=QtCore.QModelIndex(), **kwargs):
		return len(self.header)

	def rowCount(self, parent=QtCore.QModelIndex(), **kwargs):
		return len(self.data)

	def flags(self, index):
		return self.flags
