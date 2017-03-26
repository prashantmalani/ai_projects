from driver import csp

def revise(csp, xi, xj):
    # Perform revision step of AC-3 algorithm
    revised = False
    for x in csp.D[xi]:
        d_xj = csp.D[xj][:]
        if x in d_xj:
            d_xj.remove(x)
        # If there is no value of xj in Dj such that x != xj, then remove x from Di
        if len(d_xj) == 0:
            csp.D[xi].remove(x)
            revised = True
    return revised

def find_neighbors(xi, size):
    # Find all neighbours of i
    cur_row = int(xi[0])
    cur_col = int(xi[1])
    row_min = cur_row - 1
    if row_min <= 1:
        row_min = 1
    row_max = cur_row + 1
    if row_max > size:
        row_max = size

    col_min = cur_col - 1
    if col_min <= 1:
        col_min = 1
    col_max = cur_col + 1
    if col_max > size:
        col_max = size

    neighbors = []
    for x in range(row_min, row_max + 1):
        for y in range(col_min, col_max +1):
            neighbors.append(str(x) + str(y))

    neighbors.remove(xi)
    return neighbors


def ac3(csp, size):
    while len(csp.arcs) > 0:
        (xi, xj) = csp.arcs.pop(0)
        if revise(csp, xi, xj) is True:
            if len(csp.D[xi]) == 0:
                return False
            neighbors = find_neighbors(xi, size)
            if xj in neighbors:
                neighbors.remove(xj)
            for xk in neighbors:
                 csp.arcs.append((xk,xi))
    return True
