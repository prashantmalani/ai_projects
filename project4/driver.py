import sys
import converter
import ac_helper
from sets import Set
import copy

COLUMN_SIZE = 9

counter = 0

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

def back_tracking(orig_csp):
    # Loop through the unassigned variables and select value's in its domain
    # We have to use Minimum remaining values heuristic

    # Find all the keys which have unassigned values
    unassigned_inds = []
    for ind, value in orig_csp.X.items():
        if value == 0:
            unassigned_inds.append((ind, orig_csp.D[ind]))

    # Sort these according to length of domains
    unassigned_inds.sort(key=lambda x: len(x[1]))
    print("Number of unassigned indices=%d" % len(unassigned_inds))
    print_sudoku(orig_csp)
    #print "The unassigned indices are:"
    #for x in unassigned_inds:
    #    print x
    # Make a deep copy of the back tracking , so that the forward checking can be
    # maintained
    for cur_ind, domain in unassigned_inds:
        for cand_val in domain:
            # raw_input()
            #print "Cur index, value:" + cur_ind + "," + str(cand_val)
            temp_csp = copy.deepcopy(orig_csp)
            temp_csp.X[cur_ind] = cand_val
            ret = perform_forward_checking(temp_csp, cur_ind)
            if ret is False:
                #print "Forward checking failed"
                continue
            else:
                # Send the version of the csp updated via forward checking to
                # Use the inferences
                # Perform AC-3 also on it
                ret= temp_csp.ac3(COLUMN_SIZE)
                if ret is True:
                    for key, value in temp_csp.X.items():
                        if len(temp_csp.D[key]) == 1:
                            temp_csp.X[key] = temp_csp.D[key][0]

                #print "Forward checking succeeded"
                ret = back_tracking(temp_csp)
                if (ret == True):
                    # We have found assignments which make sense
                    orig_csp = temp_csp
                    return True
                else:
                    # We just start over and make a new copy of the
                    # unassigned variable.
                    continue
    return False


def print_sudoku(cur_csp):
    for i in range(1, COLUMN_SIZE + 1):
        for j in range(1, COLUMN_SIZE + 1):
            print '{:4}'.format(cur_csp.X[(str(i) + str(j))]),
        print

def perform_forward_checking(cur_csp, key):
    """ Perform consistency checking with all the neighbors of the key.
        If any Domain of a neighbor goes down to 0, then this is an invalid
        configuration, and we should return

        Otherwise, we should remove the element xi from each of the other domains
        so that it can be used in the next step of back tracking.
        """
    xi_val = cur_csp.X[key]
    #print "Sanity check: Forward checking assignment:" + str(xi_val)
    neighbors = ac_helper.get_neighbors(key, COLUMN_SIZE)
    for xj in neighbors:
        if xi_val in cur_csp.D[xj]:
            cur_csp.D[xj].remove(xi_val)
            #print "Removing element from key:" + xj
            if len(cur_csp.D[xj]) < 1:
                return False
    return True

def solveSudoku(input_str):
    global counter
    sudoku = converter.convert(input_str, COLUMN_SIZE)
    cur_csp = csp(sudoku)
    # Pre process using AC-3
    cur_csp.ac3(COLUMN_SIZE)

    solved = True
    for key, value in cur_csp.X.items():
        if len(cur_csp.D[key]) > 1:
            print "Cannot be completely solved"
            solved = False
            break
    if solved ==  True:
        print "Already solved by AC-3"
    else:
         #Update all the values that back AC-3 has been able to resolve.
        for key, value in cur_csp.X.items():
           if len(cur_csp.D[key]) == 1:
               cur_csp.X[key] = cur_csp.D[key][0]
        cur_csp = csp(sudoku)
        back_tracking(cur_csp)


def main():
    # Go through each input of sudoku, and perform solve it
    with open(sys.argv[1], 'r') as f:
        for line in f:
            #print line
            solveSudoku(line)
            raw_input('...')

if __name__ == "__main__":
    main()
