from driver import csp
import converter
import math

def get_square_neighbors(key, size):
    row = int(key[0])
    col = int(key[1])

    neighbors  = []
    sq_rt = int(math.sqrt(size))
    # The row limit calculations work better with base 0 indexing.
    row = row - 1
    col = col - 1
    min_row = row - (row % sq_rt)
    min_col = col - (col % sq_rt)
    for x in range(min_row, min_row + sq_rt):
        for y in range(min_col, min_col + sq_rt):
            neighbors.append(str(x + 1) + str(y + 1))

    return neighbors

def get_neighbors(key, size):
    row = key[0]
    col = key[1]
    neighbors = []
    # Add all other elements in row_size
    for i in range(1, size + 1):
        if i != int(col):
            neighbors.append(row + str(i))
    # Add all other elements in the column.
    for cur_row in converter.ROW_ARR[:size]:
        if cur_row != row:
            neighbors.append(cur_row + col)

    # Add square specific constraints (if they don't already exist).
    neighbors_square = get_square_neighbors(key, size)
    neighbors_square.remove(key)
    for x in neighbors_square:
        neighbors.append(x)

    return neighbors
