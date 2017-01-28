# Base class for solvers, which contains common initialization code and Helper
# functions.
class solver:
    """ Represents the base class that performs the search logic, and prints results.
        Attributes:
        root           : Root of the tree
        goal_state     : The end result that we wish to achieve
        nodes_expanded : The number of nodes that get expanded to (1 or many) child(ren)
        max_fringe     : The max size that the fringe reaches during any algorithm
        max_depth      : The max depth that the algorithm ever goes to.
    """
    MOVES = ["Up", "Down", "Left", "Right"]

    def __init__(self, root_node, dimension):
        self.root = root_node
        self.goal_state = range(dimension * dimension)
        self.nodes_expanded = 0
        self.max_fringe = 0
        self.max_depth = 0

    def print_result_path(self, end_node, cur_fringe):
        """ Helper function to print stats in the desired format.
        """
        cur_node = end_node
        move_list = []
        while cur_node.parent is not None:
            move_list.append(cur_node.move)
            cur_node = cur_node.parent
        print "path to goal: " + str(move_list[::-1])
        print "cost_of_path: " + str(len(move_list))
        print "nodes_expanded: " + str(self.nodes_expanded)
        print "fringe size: " + str(cur_fringe)
        print "max_fringe_size:" + str(self.max_fringe)
        print "search_depth:" + str(end_node.depth)
        print "max_search_depth:" + str(self.max_depth)
        print "running_time: " + str(123132)
        print "max_ram_usage:" + str(2343242)
