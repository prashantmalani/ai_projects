# Class implementation of A* solver for P1
import Queue
from solver import solver
from node import node
import time

class astar_solver(solver):
    """ Represents specific implementation of the solver, for A-Star
    """
    def __init__(self, root_node, dimension):
        self.board_dim = dimension
        solver.__init__(self, root_node, dimension)

    def solve(self):
        start_time = time.time()
        frontier = Queue.PriorityQueue(maxsize = 0)
        frontier_set = set()

        explored = set()

        # The explored / set should only hold board values, since we don't
        # care about the depth/parents/children etc.
        # Initialize the frontier queue with the root node.
        # We keep a set alongside the queue, since it's difficult to check whether
        # an element is present in the queue or not.
        #
        # Also : Calculate the manhattan number
        frontier.put((self.calcManhattan(self.root.board.vals), self.root))
        frontier_set.add(tuple(self.root.board.vals))

        while not frontier.empty():
            #Remove the node from queue, and to explored set
            cur_node_tuple = frontier.get();
            cur_node = cur_node_tuple[1]
            frontier_set.remove(tuple(cur_node.board.vals))
            explored.add(tuple(cur_node.board.vals))

            # Check if we are at the goal position
            if cur_node.board.vals == self.goal_state:
                end_time = time.time()
                self.print_result_path(cur_node, len(frontier_set),
                    end_time - start_time)
                return

            been_expanded = False
            # Expand in lexicographical order
            for cur_move in self.MOVES:
                new_board = cur_node.board.move(cur_move)
                if new_board is None:
                    continue
                new_board_tuple = tuple(new_board.vals)
                if (    new_board_tuple not in explored
                    and new_board_tuple not in frontier_set):
                    frontier.put((self.calcManhattan(new_board.vals),
                        node(cur_node, new_board, cur_node.depth + 1,
                        cur_move)))
                    frontier_set.add(tuple(new_board.vals))
                    # Update expanded node count
                    been_expanded = True

            # Update max fringe values, and nodes_expanded counts, max search depth
            # The example suggests that even if a node hasn't been explored,
            # as long as it is in the frontier set, it contributes to the depth
            # calculation.
            cur_frontier = len(frontier_set)
            if cur_frontier > self.max_fringe:
                self.max_fringe = cur_frontier
            self.nodes_expanded += 1
            if been_expanded is True:
                # Update max depth bookeeping
                if cur_node.depth + 1 > self.max_depth:
                    self.max_depth = cur_node.depth + 1

        print "Failure: Couldn't find a valid path"
        return

    def calcManhattan(self, board_orig):
        """ Calculate the manhattan number of the board.
        """
        val = 0
        board = board_orig[:]
        # Replace 0-tile with it's own index
        zero_index = board.index(0)
        board[zero_index] = zero_index
        for i, cur_tile in enumerate(board):
            cur_row = i / self.board_dim
            cur_col = i % self.board_dim

            desired_row = cur_tile / self.board_dim
            desired_col = cur_tile % self.board_dim
            val += abs(desired_row - cur_row) + abs(desired_col - cur_col)
        return val
