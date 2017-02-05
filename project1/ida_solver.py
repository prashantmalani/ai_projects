# Class implementation of A* solver for P1
import Queue
from solver import solver
from node import node
import time

class ida_solver(solver):
    """ Represents specific implementation of the solver, for A-Star
    """
    def __init__(self, root_node, dimension):
        self.board_dim = dimension
        solver.__init__(self, root_node, dimension)

    def solve(self):
        start_time = time.time()
        # Calculate the manhattan number and set that as the initial
        # threshold.
        cutoff = self.calcManhattan(self.root.board.vals)

        # We start off the search, and keep the limit as what the manhattan
        # value is (as the limit).

        # We don't add elements which have a cost function greater than
        # cutoff. If at the end of the iteration, we don't have a larger cutoff
        # That means there is nothing more to explore.

        while True:
            # The explored / set should only hold board values, since we don't
            # care about the depth/parents/children etc.
            # Initialize the frontier stack with the root node.
            # We keep a set alongside the stack, since it's difficult to check
            # whether an element is present in the stack or not.
            frontier = []
            frontier_set = set()
            explored = set()

            frontier.append(self.root)
            frontier_set.add(tuple(self.root.board.vals))
            new_cost = -1 # Init new_cost to some value, so it doesn't go out of scope
            while len(frontier) != 0:
                #Remove the node from queue, and to explored set
                cur_node = frontier.pop();
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
                for cur_move in self.MOVES[::-1]:
                    new_board = cur_node.board.move(cur_move)
                    if new_board is None:
                        continue
                    new_board_tuple = tuple(new_board.vals)
                    new_cost = cur_node.depth + 1 + self.calcManhattan(new_board.vals)
                    if new_cost > cutoff:
                        continue
                    if (    new_board_tuple not in explored
                        and new_board_tuple not in frontier_set):
                        frontier.append(node(cur_node, new_board, cur_node.depth + 1,
                            cur_move))
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
            # This is the outer for loop
            # If we have reached here, that means the inner loop failed to find
            # the correct node. If it does this, and the new_cost value is not
            # greater than new cutoff, then we have failed, else Update
            if new_cost > cutoff:
                cutoff = new_cost
            else:
                break
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
