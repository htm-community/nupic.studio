import collections
import json
import pkg_resources

__version__ = "1.1.3"


def versionList(versionString):
  """
  Transform a version from string to integer list in order to make possible versions comparison.

  :param versionString: a string containing the version in the format '9.9.9.xxx'
  :return: a integer list containing the version in the format ['9', '9', '9']. Alphanumerics are ignored.
  """

  versionInt = []
  versionSplit = versionString.split(".")
  for v in versionSplit:
    if v.isdigit():
      versionInt.append(v)
    else:
      break
  return versionInt

try:
  import nupic
except ImportError:
  raise ImportError("NuPIC library not found! Access https://github.com/numenta/nupic/ for get help on how install it.")
foundNupic = pkg_resources.get_distribution("nupic")
versionRequiredMin = "0.2.2"
versionRequiredMax = "99.99.99"
if not (versionList(versionRequiredMin) <= versionList(foundNupic.version) <= versionList(versionRequiredMax)):
  raise Exception("Unexpected version of NuPIC Library! Expected between %s and %s, but detected %s in %s." % (versionRequiredMin, versionRequiredMax, foundNupic.version, foundNupic.location))

try:
  from PyQt4 import Qt, QtCore, QtGui, QtOpenGL
except ImportError:
  msg = "PyQt4 library not found! Access http://pyqt.sourceforge.net/Docs/PyQt4/installation.html for get help on how install it" \
    "...or use a package manager like apt, yum, or brew:\n" \
    "  apt-get install python-qt4 python-qt4-gl\n" \
    "  yum install PyQt4\n" \
    "  brew install pyqt"
  raise ImportError(msg)

class MachineState(object):
  """
  This class consists of a queue with max length to store states for each time step.
  """

  def __init__(self, defaultValue, maxLen):
    self.defaultValue = defaultValue
    self.maxLen = maxLen
    self.list = [defaultValue] * maxLen

  def getList(self):
    """
    Get list with stored states machine.
    """

    return self.list

  def rotate(self):
    """
    Update states machine by remove the first element and add a new element in the end.
    """

    self.list.remove(self.list[0])
    self.list.append(self.defaultValue)

  def atGivenStepAgo(self, timeStep):
    """
    Get the state for a given time step.
    """

    return self.list[len(self.list) - timeStep - 1]

  def setForCurrStep(self, value):
    """
    Set the state for the current time step.
    """

    self.list[len(self.list) - 1] = value

  def atCurrStep(self):
    """
    Get the state of the current time step.
    """

    return self.list[len(self.list) - 1]

  def atPreviousStep(self):
    """
    Get the state of the previous time step.
    """

    return self.list[len(self.list) - 2]

  def atFirstStep(self):
    """
    Get the state of the firt time step.
    """

    return self.list[0]

def getInstantiatedClass(moduleName, className, classParams):
  """
  Return an instantiated class given a module, class, and constructor params
  """

  # Remove single quote from parameter values
  #   foo: 'bar' => foo: bar
  classParams = classParams.replace(": '", ": ")
  classParams = classParams.replace("', ", ", ")
  classParams = classParams.replace("'}", "}")
  classParams = classParams.replace("'", "\"")

  module = __import__(moduleName, fromlist=[className])
  class_ = getattr(module, className)
  params = json.loads(classParams, object_pairs_hook=collections.OrderedDict)
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
    self.dataChanged.emit(index, index)
    return True

  def data(self, index, role=None):
    column, row = index.column(), index.row()
    if role == QtCore.Qt.TextAlignmentRole:
      return QtCore.Qt.AlignRight
    elif role == QtCore.Qt.DisplayRole:
      return self.data[row][column]
    return

  def columnCount(self, parent=None, **kwargs):
    return len(self.header)

  def rowCount(self, parent=None, **kwargs):
    return len(self.data)

  def flags(self, index):
    return self.flags
