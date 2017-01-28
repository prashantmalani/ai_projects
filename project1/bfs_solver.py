# Class implementation of BFS solver for P1
import Queue
from solver import solver
from node import node

class bfs_solver(solver):
    """ Represents specific implementation of the solver, for BFS
    """
    def __init__(self, root_node, dimension):
        solver.__init__(self, root_node, dimension)

    def solve(self):
        frontier = Queue.Queue(maxsize = 0)
        frontier_set = set()

        explored = set()

        # The explored / set should only hold board values, since we don't
        # care about the depth/parents/children etc.
        # Initialize the frontier queue with the root node.
        # We keep a set alongside the queue, since it's difficult to check whether
        # an element is present in the queue or not.
        frontier.put(self.root)
        frontier_set.add(tuple(self.root.board.vals))

        while not frontier.empty():
            #Remove the node from queue, and to explored set
            cur_node = frontier.get();
            frontier_set.remove(tuple(cur_node.board.vals))
            explored.add(tuple(cur_node.board.vals))

            # Update max depth bookeeping
            if cur_node.depth > self.max_depth:
                self.max_depth = cur_node.depth

            # Check if we are at the goal position
            if cur_node.board.vals == self.goal_state:
                print "We have reached our goal state"
                self.print_result_path(cur_node, len(frontier_set))
                return

            been_expanded = False
            # Expand in lexicographical order
            for cur_move in self.MOVES:
                new_board = cur_node.board.move(cur_move)
                if (    new_board is not None
                    and tuple(new_board.vals) not in explored.union(frontier_set)):
                    frontier.put(node(cur_node, new_board, cur_node.depth + 1,
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
            if been_expanded is True:
                self.nodes_expanded += 1
                # Update max depth bookeeping
                if cur_node.depth + 1 > self.max_depth:
                    self.max_depth = cur_node.depth + 1

        print "Failure: Couldn't find a valid path"
        return
