import sys
import csv
import time

def main():
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    input_list = []
    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        input_list = list(reader)
        input_list = [[int(x) for x in rec] for rec in input_list]

    # Parse out the plotting data
    x1_in = [x[0] for x in input_list]
    x2_in = [x[1] for x in input_list]
    x3_in = ['r' if x[2] >0 else 'b' for x in input_list]

    # Initialize the weights
    b = 0
    w1 = 0
    w2 = 0
    i = 0

    with open('output1.csv', 'w') as f:
        # Iterate over all the elements till we get convergence
        while True:
            i += 1
            old_b = b
            old_w1 = w1
            old_w2 = w2
            for entry in input_list:
                f_x1 = b + (w1 * entry[0]) + (w2 * entry[1])
                result = f_x1 * entry[2]
                if result <= 0:
                    w1 += entry[0] * entry[2]
                    w2 += entry[1] * entry[2]
                    b += 1 * entry[2]

            f.write('%d,%d,%d\n' % (w1,w2,b))
            if (old_b == b and old_w1 == w1 and old_w2 == w2):
                break


if __name__ == "__main__":
    main()
