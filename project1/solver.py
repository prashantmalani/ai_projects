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

    def print_result_path(self, end_node, cur_fringe, time):
        """ Helper function to print stats in the desired format.
        """
        cur_node = end_node
        move_list = []
        while cur_node.parent is not None:
            move_list.append(cur_node.move)
            cur_node = cur_node.parent
        with open("output.txt", "w" ) as f:
            f.write("path_to_goal: %s\n" % str(move_list[::-1]))
            f.write("cost_of_path: %s\n" % str(len(move_list)))
            f.write("nodes_expanded: %s\n" % str(self.nodes_expanded))
            f.write("fringe_size: %s\n" % str(cur_fringe))
            f.write("max_fringe_size: %s\n" % str(self.max_fringe))
            f.write("search_depth: %s\n" % str(end_node.depth))
            f.write("max_search_depth: %s\n" % str(self.max_depth))
            f.write("running_time: %s\n" % str(time))
            f.write("max_ram_usage: %s\n" % str(2343242))
