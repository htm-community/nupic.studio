
class Link:
  """
  A class only to group properties related to links among nodes in hierarchy.
  """

  #region Constructor

  def __init__(self):
    """
    Initializes a new instance of this class.
    """

    #region Instance fields

    self.outNode = None
    """Node which its output will be used as input to the second node."""

    self.inNode = None
    """Target region to receive the input."""

    #endregion

  #endregion
