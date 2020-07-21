
class Link:
    """
    A class only to group properties related to links among nodes in hierarchy.
    """

    def __init__(self):
        """
        Initializes a new instance of this class.
        """

        self.outNode = None
        """Node which its output will be used as input to the second node."""

        self.inNode = None
        """Target region to receive the input."""
