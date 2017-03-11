from Grid import Grid
import itertools

# placement of the max tile. corners get 100, along the edges gets 50, central
# tile get 25
def h1(grid):
    max_val = grid.getMaxTile()
    #  print "Max tile value is:" + str(max_val)

    # h1 : Position of max tile: Corners scored highest, mid scored lowest
    locs = [(x,y) for (x,y) in itertools.product(range(4), range(4)) if grid.map[x][y] == max_val]
    # Pic any max val tile, in case there are many

    one_max_loc = locs[0]
    score = 4
    if (one_max_loc[0] % (grid.size - 1) > 0) :
        score /= 2
    if (one_max_loc[1] % (grid.size - 1) > 0) :
        score /= 2
    h1 = (score * 25 )# normalize to 100 ; h1 = (score * 100) / 4
    return h1

# % of free tiles
def h2(grid):
    num_free_tiles = len(grid.getAvailableCells())
    h2 = (num_free_tiles * 100) / 16
    return h2

# % of NON-monotonic rows/columns
def h3(grid):
    # calculate number of non-monotonic rows / columns out of 8.
    # First check the rows
    non_monot = 0;
    for i in range(4):
        old_diff = 0
        new_diff = 0
        for j in range(1,4):
            new_diff = grid.map[i][j] - grid.map[i][j-1]
            # If there is no change, continue looking at the next value
            if new_diff == 0:
                continue

            if new_diff > 0:
                new_diff = 1
            else:
                new_diff = -1

            # The logic here is as follows
            # old_diff tracks the current trend; if it is +ve, we've seen at
            # least one increase in value. if it is -ve, we've seen at least
            # one decrease.
            # so as long as old_diff * new_diff is >= 0 , this means there
            # hasn't been any sign inversion.
            if (new_diff * old_diff) < 0:
                non_monot += 1
                break
            if new_diff != 0 and old_diff == 0:
                old_diff = new_diff

    for i in range(4):
        old_diff = 0
        new_diff = 0
        for j in range(1,4):
            new_diff = grid.map[j][i] - grid.map[j-1][i]
            # If there is no change, continue looking at the next value
            if new_diff == 0:
                continue
            if new_diff > 0:
                new_diff = 1
            else:
                new_diff = -1

            if (new_diff * old_diff) < 0:
                non_monot += 1
                break
            if new_diff != 0 and old_diff == 0:
                old_diff = new_diff

    h3 = (non_monot * 100) / 8
    return h3

if __name__ == "__main__":
    sampleGrid = Grid(4);
    sampleGrid.map = [[2,4,6,8],[4,6,8,10],[4,6,6,4],[2,4,4,10]]
    print "Testing h3"
    h3 = h3(sampleGrid)
    assert(h3 == 62)
    sampleGrid.map = [[0,2,2,0],[0,0,4,10],[4,0,0,4],[4,0,0,0]]
    print "Testing h2"
    h2 = h2(sampleGrid)
    assert(h2 == 56)
    sampleGrid.map = [[2,4,6,8],[8,16,0,0],[4,0,0,4],[4,0,0,0]]
    print "Testing h1- 25"
    h1_25 = h1(sampleGrid)
    assert(h1_25 == 25)
    print "Testing h1- 50"
    sampleGrid.map = [[2,16,6,8],[8,8,0,0],[4,0,0,4],[4,0,0,0]]
    h1_50 = h1(sampleGrid)
    assert(h1_50 == 50)
    print "Testing h1- 100 "
    sampleGrid.map = [[16,2,6,8],[8,8,0,0],[4,0,0,4],[4,0,0,0]]
    h1_100 = h1(sampleGrid)
    assert(h1_100 == 100)
