import sys
import converter

COLUMN_SIZE = 9

def solveSudoku(input_str):
    sudoku = converter.convert(input_str, COLUMN_SIZE)

def main():
    # Go through each input of sudoku, and perform solve it
    with open(sys.argv[1], 'r') as f:
        for line in f:
            print line
            solveSudoku(line)

if __name__ == "__main__":
    main()
