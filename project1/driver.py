import math

class board:
    """ Representation of the physical tiles.
            vals: The board values, in a list form.
            dim : The dimension of the board.
    """

    def __init__(self,input_vals):
        """
            input_str = The state of the board, in string form
        """
        self.vals = input_vals
        self.dim = int(math.sqrt(len(input_vals)))

    def __swap_indices(self, temp_vals, cur_index, new_index):
        temp_vals[cur_index], temp_vals[new_index] = temp_vals[new_index], temp_vals[cur_index]

    def move(self, direction):
        """
            direction : Direction in which the empty slot has to move.

            Returns   : Result board object if board is valid,
                        None otherwise.
        """
        blank_index = self.vals.index(0)
        if direction == "Up":
            new_index = blank_index - self.dim
            if new_index < 0:
                print ("Up move not allowed")
                return None
        elif direction == "Down":
            new_index = blank_index + self.dim
            if new_index >= len(self.vals):
                print ("Down move not allowed")
                return None
        elif direction == "Left":
            if blank_index % self.dim == 0:
                print("Left move not allowed")
                return None
            new_index = blank_index - 1
        elif direction == "Right":
            if (blank_index % self.dim) == self.dim - 1:
                print("Right move not allowed")
                return None
            new_index = blank_index + 1

        # Now that we have calculated the new location we swap and return the
        # new board state
        temp_vals = self.vals[:]
        self.__swap_indices(temp_vals, new_index, blank_index)
        return board(temp_vals)


if __name__ == "__main__":
    print "Hello World"
    root = board([0,2,5,3,4,1,6,7,8])
    print root.vals
    new_board = root.move("Right")
    if new_board is not None: print new_board.vals
