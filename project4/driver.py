import sys
import converter
import ac_helper
from sets import Set

COLUMN_SIZE = 9

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
            neighbors = ac_helper.get_neighbors(key, COLUMN_SIZE)
            for xj in neighbors:
                if not (key, xj) in self.arcs:
                    self.arcs.append((key, xj))

    def revise(self, xi, xj):
        # Perform revision step of AC-3 algorithm
        revised = False
        for x in self.D[xi]:
            d_xj = self.D[xj][:]
            if x in d_xj:
                d_xj.remove(x)
            # If there is no value of xj in Dj such that x != xj, then remove x from Di
            if len(d_xj) == 0:
                self.D[xi].remove(x)
                revised = True
        return revised

    def ac3(self, size):
        while len(self.arcs) > 0:
            (xi, xj) = self.arcs.pop(0)
            if self.revise(xi, xj) is True:
                if len(self.D[xi]) == 0:
                    return False
                neighbors = ac_helper.get_neighbors(xi, size)
                #if xj in neighbors:
                neighbors.remove(xj)
                for xk in neighbors:
                    if not (xk, xi) in self.arcs:
                        self.arcs.append((xk,xi))
        return True

def solveSudoku(input_str):
    sudoku = converter.convert(input_str, COLUMN_SIZE)
    cur_csp = csp(sudoku)
    cur_csp.ac3(COLUMN_SIZE)

    for key, value in cur_csp.X.items():
        if len(cur_csp.D[key]) > 1:
            print "Cannot be completely solved"
            return
    print "Completely solvable"


def main():
    # Go through each input of sudoku, and perform solve it
    with open(sys.argv[1], 'r') as f:
        for line in f:
            #print line
            solveSudoku(line)
            #raw_input('...')

if __name__ == "__main__":
    main()
