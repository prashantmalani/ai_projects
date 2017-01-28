# Class implementation of BFS solver for P1
from solver import solver
from node import node
import time

class dfs_solver(solver):
    """ Represents specific implementation of the solver, for DFS
    """
    def __init__(self, root_node, dimension):
        solver.__init__(self, root_node, dimension)

    def solve(self):
        start_time = time.time()
        frontier = []
        frontier_set = set()

        explored = set()

        # The explored / set should only hold board values, since we don't
        # care about the depth/parents/children etc.
        # Initialize the frontier stack with the root node.
        # We keep a set alongside the stack, since it's difficult to check whether
        # an element is present in the stack or not.
        frontier.append(self.root)
        frontier_set.add(tuple(self.root.board.vals))

        while len(frontier) != 0:
            #Remove the node from stack, and to explored set
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
            # Expand in reverse lexicographical order
            for cur_move in self.MOVES[::-1]:
                new_board = cur_node.board.move(cur_move)
                if new_board is None:
                    continue
                new_board_tuple = tuple(new_board.vals)
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

        print "Failure: Couldn't find a valid path"
        return
