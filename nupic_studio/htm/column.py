from nupic_studio.htm.segment import Segment, SegmentType

class Column:
    """
    A class only to group properties related to columns.
    """

    def __init__(self):
        """
        Initializes a new instance of this class.
        """

        # Position on X axis
        self.x = -1

        # Position on Y axis
        self.y = -1

        # Proximal segment of this column
        self.segment = Segment(SegmentType.proximal)

        # List of cells that compose this column.
        self.cells = []

        self.tree3d_pos = (0, 0, 0)

    def getCell(self, z):
        """
        Return the cell located at given position
        """

        for cell in self.cells:
            if cell.z == z:
                return cell

    def nextStep(self):
        """
        Perfoms actions related to time step progression.
        """

        self.segment.nextStep()
        for cell in self.cells:
            cell.nextStep()

    def calculateStatistics(self):
        """
        Calculate statistics after an iteration.
        """

        self.segment.calculateStatistics()
        for cell in self.cells:
            cell.calculateStatistics()
