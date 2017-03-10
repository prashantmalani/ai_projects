
grid = [[2,4,6,8],[4,6,8,10],[4,6,6,4],[2,4,4,10]]

non_monot = 0;
for i in range(4):
    old_diff = 0
    new_diff = 0
    for j in range(1,4):
        print('i,j=%d,%d' % (i,j))
        new_diff = grid[i][j] - grid[i][j-1]
        # If there is no change, continue looking at the next value
        if new_diff == 0:
            continue

        if new_diff > 0:
            new_diff = 1
        else:
            new_diff = -1
        print('New_diff=%d, old_diff=%d' % (new_diff, old_diff))
        # The logic here is as follows
        # old_diff tracks the current trend; if it is +ve, we've seen at
        # least one increase in value. if it is -ve, we've seen at least
        # one decrease.
        # so as long as old_diff * new_diff is >= 0 , this means there
        # hasn't been any sign inversion.
        if (new_diff * old_diff) < 0:
            print("Found non-monot")
            non_monot += 1
            break
        if new_diff != 0 and old_diff == 0:
            old_diff = new_diff

for i in range(4):
    old_diff = 0
    new_diff = 0
    for j in range(1,4):
        print('i,j=%d,%d' % (j,i))
        new_diff = grid[j][i] - grid[j-1][i]
        # If there is no change, continue looking at the next value
        if new_diff == 0:
            continue
        if new_diff > 0:
            new_diff = 1
        else:
            new_diff = -1

        print('New_diff=%d, old_diff=%d' % (new_diff, old_diff))
        if (new_diff * old_diff) < 0:
            print("Found non-monot")
            non_monot += 1
            break
        if new_diff != 0 and old_diff == 0:
            old_diff = new_diff

print "Number of non-monoton:" + str(non_monot)
