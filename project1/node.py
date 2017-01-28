# Class representing a node in the tree 
class node:
    """ Represents the equivalent of a node in the tree
        Attributes:
        parent :  Reference to the parent of the node
        val    :  Board state for the current board
        depth  :  Depth at which the current node resides.
    """
    def __init__(self, parent, board, depth, move):
        self.parent = parent
        self.board = board
        self.depth = depth
        self.move = move
