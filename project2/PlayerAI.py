from random import randint
from BaseAI import BaseAI
import sys
import itertools
import time

class PlayerAI(BaseAI):

    MAX_DEPTH = 5

    def getMove(self, grid):
        #moves = grid.getAvailableMoves()
        #return moves[randint(0, len(moves) - 1)] if moves else None
        start = time.clock()
        alpha = -sys.maxint - 1
        beta = sys.maxint
        child, _ = self.maximize(grid, alpha, beta, 0)
        end = time.clock()
        print "Time taken for move:" + str(end - start)
        return child

    def eval_func(self, grid):
        """ Evaluation function of the current grid.
        """
        # Each heuristic is scored on 100, and we give each one weights.
        w1 = 50 # 50 percent weightage to max tile in corner
        w2 = 50 # 50 percent weightage to number of free spaces
        w3 = -30 # penalty weightage if there are any non-monotonic rows/columns

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

        # h2 : Number of free tiles: Normalize against max free Tiles
        num_free_tiles = len(grid.getAvailableCells())
        h2 = (num_free_tiles * 100) / 16

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

        score = (h1*w1 + h2*w2 + h3*w3) / (w1 + w2 + w3)
        return score



    def maximize(self, grid, alpha, beta, depth):
        # Terminal state
        # For the time being basically cap of the search at a particular dept
        if len(grid.getAvailableMoves()) == 0 or depth >= self.MAX_DEPTH:
            return (None, self.eval_func(grid))

        max_child = None
        max_utility = -sys.maxint - 1 # Set to - inf

        for cur_move in grid.getAvailableMoves():
            x = grid.clone()
            # Call maximize on the child
            if x.move(cur_move) is False:
                continue
            _, utility = self.minimize(x, alpha, beta, depth + 1)
            if utility > max_utility:
                max_child = cur_move
                max_utility = utility
            if max_utility >= beta:
                break
            if max_utility > alpha:
                #print ('ALPHA updated:%f' % max_utility)
                alpha = max_utility

        return max_child, max_utility

    def generateSpawnLocations(self, grid):
        """ The spawning of locations seems to be important.
        This function returns a list of available locations,
        After implementing certain heuristics to make the opponent
        adversarial.
        """
        orig_list = grid.getAvailableCells()
        loc_list = [(x,y) for x,y in orig_list if (x is 0 or x is 3) and (y is 0 or y is 3)]
        if len(loc_list) is 0:
            return orig_list
        return loc_list


    def minimize(self, grid, alpha, beta, depth):
        # Terminal state
        # For the time being basically cap of the search at a particular dept
        if len(grid.getAvailableCells()) == 0 or depth >= self.MAX_DEPTH:
            return (None, self.eval_func(grid))

        min_child = None
        min_utility = sys.maxint
        possible_cells = self.generateSpawnLocations(grid)


        move_val_pairs = itertools.product(possible_cells,(2,4))
        # Shall we assume that 2's are always drawn ?
        # Is that better adversarial wise?
        for cur_location,cur_val in move_val_pairs:
            x = grid.clone()
            x.insertTile(cur_location, cur_val)
            # print "Tile inserted:" + str(cur_val) + ", location:" + str(cur_location)
            _, utility = self.maximize(x, alpha, beta, depth + 1)

            if utility < min_utility:
                min_child = x
                min_utility = utility
            if min_utility <= alpha:
                break
            if min_utility < beta:
                #print ('BETA updated:%f' % min_utility)
                beta = min_utility
        #print('MIN: depth=%d, min_util=%f' % (depth, min_utility))
        return min_child, min_utility
