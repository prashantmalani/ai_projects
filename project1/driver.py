import math
import Queue

MOVES = ["Up", "Down", "Left", "Right"]

class board:
    """ Representation of the physical tiles.
            vals: The board values, in a list form.
            dim : The dimension of the board.
    """

    def __init__(self,input_vals):
        """
            input_str = The state of the board, in string form
        """
        self.vals = input_vals
        self.dim = int(math.sqrt(len(input_vals)))

    def __swap_indices(self, temp_vals, cur_index, new_index):
        temp_vals[cur_index], temp_vals[new_index] = temp_vals[new_index], temp_vals[cur_index]

    def move(self, direction):
        """
            direction : Direction in which the empty slot has to move.

            Returns   : Result board object if board is valid,
                        None otherwise.
        """
        blank_index = self.vals.index(0)
        if direction == "Up":
            new_index = blank_index - self.dim
            if new_index < 0:
                # print ("Up move not allowed")
                return None
        elif direction == "Down":
            new_index = blank_index + self.dim
            if new_index >= len(self.vals):
                # print ("Down move not allowed")
                return None
        elif direction == "Left":
            if blank_index % self.dim == 0:
                # print("Left move not allowed")
                return None
            new_index = blank_index - 1
        elif direction == "Right":
            if (blank_index % self.dim) == self.dim - 1:
                # print("Right move not allowed")
                return None
            new_index = blank_index + 1

        # Now that we have calculated the new location we swap and return the
        # new board state
        temp_vals = self.vals[:]
        self.__swap_indices(temp_vals, new_index, blank_index)
        return board(temp_vals)


class state:
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

class solver:
    def __init__(self, root_node, dimension):
        self.root = root_node
        self.goal_state = range(dimension * dimension)
        self.nodes_expanded = 0
        self.max_fringe = 0
        self.max_depth = 0

    def solve_bfs(self):
        frontier = Queue.Queue(maxsize = 0)

        explored = set()
        # The explored / set should only hold board values, since we don't
        # care about the depth/parents/children etc.
        frontier.put(self.root)
        frontier_set = set()
        frontier_set.add(tuple(self.root.board.vals))
        while not frontier.empty():

            #Remove the node from queue
            cur_state = frontier.get();
            frontier_set.remove(tuple(cur_state.board.vals))
            explored.add(tuple(cur_state.board.vals))

            # Update max depth bookeeping
            if cur_state.depth > self.max_depth:
                self.max_depth = cur_state.depth

            # Check if we are at the goal position
            if cur_state.board.vals ==  self.goal_state:
                print "We have reached our goal state"
                self.__print_result_path(cur_state, frontier.qsize())
                return

            # Expand in lexicographical order
            for cur_move in MOVES:
                new_board = cur_state.board.move(cur_move)
                if (    new_board is not None
                    and tuple(new_board.vals) not in explored.union(frontier_set)):
                    frontier.put(state(cur_state, new_board, cur_state.depth + 1,
                        cur_move))
                    frontier_set.add(tuple(new_board.vals))
                    # Update expanded node count
                    self.nodes_expanded += 1

            # Update max fringe values
            cur_frontier = frontier.qsize()
            if cur_frontier > self.max_fringe:
                self.max_fringe = cur_frontier
        print "Failure: Couldn't find a valid path"
        return

    def __print_result_path(self, end_state, cur_fringe):
        cur_state = end_state
        move_list = []
        while cur_state.parent is not None:
            move_list.append(cur_state.move)
            cur_state = cur_state.parent
        print "path to goal: " + str(move_list[::-1])
        print "cost_of_path: " + str(len(move_list))
        print "nodes_expanded: " + str(self.nodes_expanded)
        print "fringe size: " + str(cur_fringe)
        print "max_fringe_size:" + str(self.max_fringe)
        print "search_depth:" + str(cur_state.depth)
        print "max_search_depth:" + str(self.max_depth)
        print "running_time: " + str(123132)
        print "max_ram_usage:" + str(2343242)

if __name__ == "__main__":
    print "Hello World"
    root = board([1,2,5,3,4,0,6,7,8])
    print root.vals
    new_board = root.move("Right")
    # Create the root node
    start_node = state(None, root, 0, None)
    bfs_solver = solver(start_node, root.dim)
    bfs_solver.solve_bfs()
