from board import board
from node import node
from bfs_solver import bfs_solver
from dfs_solver import dfs_solver
from astar_solver import astar_solver
import Queue
import sys


if __name__ == "__main__":
    algo = sys.argv[1]
    init_str = sys.argv[2]
    init_list = [int(x) for x in init_str.split(',')]
    init_vals = board(init_list)
    # Create the root node
    start_node = node(None, init_vals, 0, None)
    if algo == 'bfs':
        solver = bfs_solver(start_node, init_vals.dim)
    elif algo == "ast":
        solver = astar_solver(start_node, init_vals.dim)
    else:
        solver = dfs_solver(start_node, init_vals.dim)
    solver.solve()
