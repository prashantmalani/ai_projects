import sys
import converter
import ac_helper
from sets import Set
import copy

COLUMN_SIZE = 9

class csp():
    def __init__(self, input_dict):
        """Set up the domain for each variable. This will also be a dict, but
        be a list or dict of all elements.
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
            # In this case, we can just iterate over each element and add the
            # constraints.
            neighbors = ac_helper.get_neighbors(key, COLUMN_SIZE)
            for xj in neighbors:
                if not (key, xj) in self.arcs:
                    self.arcs.append((key, xj))

    def revise(self, xi, xj):
        """Perform revision step of AC-3 algorithm. """
        revised = False
        for x in self.D[xi]:
            d_xj = self.D[xj][:]
            if x in d_xj:
                d_xj.remove(x)
            # If there is no value of xj in Dj such that x != xj, then remove.
            # x from Di
            if len(d_xj) == 0:
                self.D[xi].remove(x)
                revised = True
        return revised

    def ac3(self, size):
        """The AC-3 algorithm main body, which loops through the queue of arcs
        and updates it based on whether a revision was performed.
        """
        while len(self.arcs) > 0:
            (xi, xj) = self.arcs.pop(0)
            if self.revise(xi, xj) is True:
                if len(self.D[xi]) == 0:
                    return False
                neighbors = ac_helper.get_neighbors(xi, size)
                neighbors.remove(xj)
                for xk in neighbors:
                    if not (xk, xi) in self.arcs:
                        self.arcs.append((xk,xi))
        return True


def update_vals_csp(cur_csp, key, val, neighb_list):
    """Helper function to update the CSP if the forward checking check
    succeeds.
    """
    cur_csp.X[key] = val
    cur_csp.D[key] = [val]

    neighbors = ac_helper.get_neighbors(key, COLUMN_SIZE)
    for cur_key in neighbors:
        # Only remove val from the domains of undecided entries.
        if val in cur_csp.D[cur_key] and cur_csp.X[cur_key] == 0:
            neighb_list.append(cur_key)
            cur_csp.D[cur_key].remove(val)

def undo_update_vals_csp(cur_csp, key, val, orig_domain, neighb_list):
    """Helper function to undo whatever changes were made to the CSP, in case
    this particular attempt at back-tracking didn't succeed.
    """
    cur_csp.X[key] = 0
    cur_csp.D[key] = orig_domain[:]
    for cur_key in neighb_list:
        cur_csp.D[cur_key].append(val)

def back_tracking(orig_csp):
    """ Back tracking algorithm main body."""
    # Loop through the unassigned variables and select value's in its domain.
    # We have to use Minimum remaining values heuristic.
    unassigned_inds = []
    for ind, value in orig_csp.X.items():
        if value == 0:
            unassigned_inds.append((ind, orig_csp.D[ind]))

    # Sort these according to length of domains.
    unassigned_inds.sort(key=lambda x: len(x[1]))

    # Termination condition for the recursive backtracking algorithm.
    if len(unassigned_inds) == 0:
        return True

    for cur_ind, domain in unassigned_inds:
        for cand_val in domain:
            ret = perform_forward_checking(orig_csp, cur_ind, cand_val)
            if ret is False:
                continue
            else:
                neighbor_list = []
                update_vals_csp(orig_csp, cur_ind, cand_val, neighbor_list)
                ret = back_tracking(orig_csp)
                if (ret == True):
                    return True
                else:
                    undo_update_vals_csp(orig_csp, cur_ind, cand_val, domain,
                                         neighbor_list)
                    continue
        # If we reached here, that means no value of the domain could satisfy
        # the Sudoku.
        return False


def print_sudoku(cur_csp):
    """ Helper function to print the sudoku board in the the CSP."""
    for i in range(1, COLUMN_SIZE + 1):
        for j in range(1, COLUMN_SIZE + 1):
            print '{:4}'.format(cur_csp.X[(str(i) + str(j))]),
        print

def perform_forward_checking(cur_csp, key, val):
    """ Perform consistency checking with all the neighbors of the key.
        If any domain size of a neighbor goes down to 0, then this is an invalid
        configuration, and we should return False.

        Otherwise, we should remove the element xi from each of the other
        domains so that it can be used in the next step of back tracking.
    """
    xi_val = val
    neighbors = ac_helper.get_neighbors(key, COLUMN_SIZE)
    for xj in neighbors:
        cur_domain_xj = cur_csp.D[xj][:]
        if xi_val in cur_domain_xj:
            cur_domain_xj.remove(xi_val)
            if len(cur_domain_xj) < 1:
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
            solved = False
            break

    # Update all the key values that you can, & their corresponding domains.
    for key, value in cur_csp.X.items():
       if len(cur_csp.D[key]) == 1:
           cur_csp.X[key] = cur_csp.D[key][0]
           cur_csp.D[key] = [cur_csp.X[key]]

    if solved != True:
        back_tracking(cur_csp)

    with open('output.txt', 'w') as f:
        for i in range(1, COLUMN_SIZE + 1):
            for j in range(1, COLUMN_SIZE + 1):
                f.write('%d' % cur_csp.X[str(i) + str(j)])
        f.write('\n')

def main():
    if len(sys.argv) != 2:
        print "Invalid input!"
        sys.exit(-1)
    solveSudoku(sys.argv[1])

if __name__ == "__main__":
    main()
