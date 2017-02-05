from board import board
from node import node
from bfs_solver import bfs_solver
from dfs_solver import dfs_solver
from astar_solver import astar_solver
from ida_solver import ida_solver
import Queue
import sys
import math


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print "Invalid number of arguments"
        sys.exit(0)
    algo = sys.argv[1]
    init_str = sys.argv[2]
    init_list = [int(x) for x in init_str.split(',')]

    if (math.sqrt(len(init_list)) ** 2) != len(init_list):
        print "Not a square list"
        sys.exit(0)

    # Check whether all the numbers are there in the board
    for i in range(len(init_list)):
        if i not in init_list:
            print "We found a missing number in the list"
            sys.exit(0)
    init_vals = board(init_list)
    # Create the root node
    start_node = node(None, init_vals, 0, None)
    if algo == 'bfs':
        solver = bfs_solver(start_node, init_vals.dim)
    elif algo == "ast":
        solver = astar_solver(start_node, init_vals.dim)
    elif algo == "ida":
        solver = ida_solver(start_node, init_vals.dim)
    else:
        solver = dfs_solver(start_node, init_vals.dim)
    solver.solve()
