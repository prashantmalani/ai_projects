

def convert(inputstr, row_size):
    """ Takes an input_string, and size, and returns a dict.
    """
    lookup = {}
    col = 1
    row = 0
    row_arr = ['A','B','C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']
    for c in inputstr:
        if not c.isdigit():
            break
        lookup[row_arr[row] + str(col)] = int(c)
        col += 1
        if (col > row_size):
            col = 1
            row = row + 1

    return lookup

if __name__ == "__main__":
    # Some test code
    result = convert("12344321", 4)
    print result
