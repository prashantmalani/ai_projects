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

# Mergeability: If adjacent tiles are mergeable, it counts towards a positive score
# Normalized to a 100 (out of the total number of mergeable pairs)
# Note that we don't count 0s
# Hanging values (i.e 8,0,0,0) counts towards an umergeable pair
def h4(grid):
    total_pairs = 0
    merge_pairs = 0

    # First check the rows
    i = 0
    while  i < grid.size:
        j = 0
        while j < grid.size:
            if j == 0:
                cur_val = grid.map[i][j]
                j += 1
                continue
            new_val = grid.map[i][j]
            if new_val == 0:
                j += 1
                continue
            else:
                if cur_val != 0:
                    if cur_val == new_val:
                        # Matching pair
                        total_pairs += 1
                        merge_pairs += 1
                        j += 1
                        continue
                    else:
                        # Non-matching pair
                        total_pairs += 1
                        j += 1
                        if j >= grid.size:
                            continue
                        cur_val = new_val

                        continue
                else:
                    cur_val = new_val
                    j += 1
                    continue
        # We've reached the end. If the cur_val is 0 means it's all 0's
        # If the cur_val is non-zero, then it's a hanging number
        if cur_val == 0 and new_val !=0:
            total_pairs += 1
        if cur_val !=0 and new_val == 0:
            total_pairs += 1
        i += 1

    # First check the rows
    i = 0
    while  i < grid.size:
        j = 0
        while j < grid.size:
            if j == 0:
                cur_val = grid.map[j][i]
                j += 1
                continue
            new_val = grid.map[j][i]
            if new_val == 0:
                j += 1
                continue
            else:
                if cur_val != 0:
                    if cur_val == new_val:
                        # Matching pair
                        total_pairs += 1
                        merge_pairs += 1
                        j += 1
                        continue
                    else:
                        # Non-matching pair
                        total_pairs += 1
                        j += 1
                        if j >= grid.size:
                            continue
                        cur_val = new_val

                        continue
                else:
                    cur_val = new_val
                    j += 1
                    continue
        # We've reached the end. If the cur_val is 0 means it's all 0's
        # If the cur_val is non-zero, then it's a hanging number
        if cur_val == 0 and new_val !=0:
            total_pairs += 1
        if cur_val !=0 and new_val == 0:
            total_pairs += 1
        i += 1

    h4 = (merge_pairs * 100) / total_pairs
    return h4


if __name__ == "__main__":
    sampleGrid = Grid(4);
    print "Testing h4 - 1"
    sampleGrid.map = [[512,256,16,2],[64,32,8,4],[0,32,2,4],[0,8,0,8]]
    h4_1 = h4(sampleGrid)
    assert(h4_1 == 15)
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
