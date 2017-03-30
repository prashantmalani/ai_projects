# Tiny helper routine to convert Sudoku input string into a dict.

ROW_ARR = ['1','2','3', '4', '5', '6', '7', '8', '9', 'J', 'K']

def convert(inputstr, row_size):
    """ Takes an input_string, and size, and returns a dict.
    """
    lookup = {}
    col = 1
    row = 0

    for c in inputstr:
        if not c.isdigit():
            break
        lookup[ROW_ARR[row] + str(col)] = int(c)
        col += 1
        if (col > row_size):
            col = 1
            row = row + 1

    return lookup

if __name__ == "__main__":
    # Some test code.
    result = convert("12344321", 4)
    print result
