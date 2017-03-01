from random import randint
from BaseAI import BaseAI
import sys
import itertools
import time

class PlayerAI(BaseAI):

    MAX_DEPTH = 4

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
        """ Initially, let's keep the eval function as purely the max value
        tile. We can iterate later.
        """
        return grid.getMaxTile()

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
            if max_utility >= alpha:
                alpha = max_utility

        return max_child, max_utility

    def generateSpawnLocations(self, grid):
        """ The spawning of locations seems to be important.
        This function returns a list of available locations,
        After implementing certain heuristics to make the opponent
        adversarial.
        """
        return grid.getAvailableCells()

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
            _, utility = self.maximize(x, alpha, beta, depth + 1)

            if utility < min_utility:
                min_child = x
                min_utility = utility

            if min_utility <= alpha:
                break
            if min_utility <= beta:
                beta = min_utility

        return min_child, min_utility
