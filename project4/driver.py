import sys
import converter
import ac_helper
from sets import Set
import math

COLUMN_SIZE = 9

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

class csp():
    def __init__(self, input_dict):
        """ Set up the domain for each variable. This will also be a dict, but
        be a list or dict of all elements
        """
        self.X = input_dict
        self.D = {}
        self.arcs = []
        for key, value in self.X.items():
            if value == 0:
                self.D[key] = range(1, COLUMN_SIZE + 1)
            else:
                self.D[key] = [value]

            # Add all the arcs for the problem.
            # In this case, we can just iterate over each element and add the constraints
            # For every element
            row = key[0]
            col = int(key[1])

            # Add all other elements in row_size
            for i in range(1, COLUMN_SIZE + 1):
                if i != col:
                    self.arcs.append((key, row + str(i)))
            # Add all other elements in the column.
            for cur_row in converter.ROW_ARR[:COLUMN_SIZE]:
                if cur_row != row:
                    self.arcs.append((key, cur_row + str(col)))

            # Add square specific constraints (if they don't already exist).
            neighbors = get_square_neighbors(key, COLUMN_SIZE)
            neighbors.remove(key)
            for xj in neighbors:
                if not (key, xj) in self.arcs:
                    self.arcs.append((key, xj))


def solveSudoku(input_str):
    sudoku = converter.convert(input_str, COLUMN_SIZE)
    print "Initializing the csp"
    cur_csp = csp(sudoku)
    print ac_helper.ac3(cur_csp, COLUMN_SIZE)
    for key, value in cur_csp.X.items():
        if len(cur_csp.D[key]) > 1:
            print "Cannot be completely solved"
            return
    print "Completely solvable"


def main():
    # Go through each input of sudoku, and perform solve it
    with open(sys.argv[1], 'r') as f:
        for line in f:
            print line
            solveSudoku(line)
            raw_input('...')

if __name__ == "__main__":
    main()
