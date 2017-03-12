from random import randint
from BaseAI import BaseAI
import sys
import itertools
import time
import heuristics

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
        w1 = 40 # 50 percent weightage to max tile in corner
        w2 = 50 + 20# 50 percent weightage to number of free spaces
        w3 = -60 # penalty weightage if there are any non-monotonic rows/columns
        w4 = 10 # 20 percent weightage to having merge pairs

        # h2 : Number of free tiles: Normalize against max free Tiles

        h1 = heuristics.h1(grid)
        h2 = heuristics.h2(grid)
        h3 = heuristics.h3(grid)
        h4 = heuristics.h4(grid)
        score = ((h1*w1) + (h2*w2) + (h3*w3) + (h4*w4)) / (w1 + w2 + w3 + w4 - 20)
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


        move_val_pairs = itertools.product(possible_cells,(2,))
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
