
class Link:
    """
    A class only to group properties related to links among nodes in hierarchy.
    """

    def __init__(self):
        """
        Initializes a new instance of this class.
        """

        # Node which its output will be used as input to the second node.
        self.out_node = None

        # Target region to receive the input.
        self.in_node = None
