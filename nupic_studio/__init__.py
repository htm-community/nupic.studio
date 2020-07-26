import pkg_resources
from pathlib import Path
from PyQt5 import QtGui, QtCore, QtWidgets

__version__ = "1.1.3"
REPO_DIR = str(Path(__file__).parent)


def versionList(versionString):
    """
    Transform a version from string to integer list in order to make possible versions comparison.
    :param versionString: a string containing the version in the format '9.9.9.xxx'
    :return: a integer list containing the version in the format ['9', '9', '9']. Alphanumerics are ignored.
    """
    version_int = []
    version_split = versionString.split(".")
    for v in version_split:
        if v.isdigit():
            version_int.append(v)
        else:
            break
    return version_int


try:
    import nupic
except ImportError:
    raise ImportError("NuPIC library not found! Access https://github.com/numenta/nupic/ for get help on how install it.")
found_nupic = pkg_resources.get_distribution("nupic")
version_required_min = "0.2.2"
version_required_max = "99.99.99"
if not (versionList(version_required_min) <= versionList(found_nupic.version) <= versionList(version_required_max)):
    raise Exception("Unexpected version of NuPIC Library! Expected between %s and %s, but detected %s in %s." % (version_required_min, version_required_max, found_nupic.version, found_nupic.location))


class MachineState(object):
    """
    This class consists of a queue with max length to store states for each time step.
    """

    def __init__(self, default_value, max_len):
        self.default_value = default_value
        self.max_len = max_len
        self.list = [default_value] * max_len

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
        self.list.append(self.default_value)

    def atGivenStepAgo(self, time_step):
        """
        Get the state for a given time step.
        """
        return self.list[len(self.list) - time_step - 1]

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


def getInstantiatedClass(module_name, class_name, class_params):
    """
    Return an instantiated class given a module, class, and constructor params
    """
    module = __import__(module_name, fromlist=[class_name])
    class_ = getattr(module, class_name)
    instance = class_(**class_params)
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

        num_cols = len(self.header)
        self.setColumnCount(num_cols)
        num_rows = len(self.data)
        self.setRowCount(num_rows)

        for col in range(num_cols):
            self.setHeaderData(col, QtCore.Qt.Horizontal, self.header[col])

        for row in range(num_rows):
            for col in range(num_cols):
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
