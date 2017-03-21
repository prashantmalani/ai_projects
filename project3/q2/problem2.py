import sys
import csv
import numpy

ALPHA = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, .4]

def calc_stats(arr):
    """ Return mean and standard deviation of list.
    """
    std_dev = numpy.std(arr)
    mean = numpy.mean(arr)
    return mean,std_dev

def normalize_data(arr, mean, std):
    res = [ (x - mean) / std for x in arr]
    return res

def single_iter(x0, age, weight, height, b0, b_age, b_wt):
    dim = len(age)
    sum_b0 = 0
    sum_age = 0
    sum_wt = 0

    # Calculate risk portion
    for i in range(0,dim):
        fx = (b0 * x0[i]) + (b_age * age[i]) + (b_wt * weight[i])
        diff = fx - height[i]
        sum_b0 += diff * x0[i]
        sum_age += diff * age[i]
        sum_wt += diff * weight[i]
    return sum_b0, sum_age, sum_wt

def perform_regression(alpha, x0, age, weight, height, iterations,f):
    # Initialize the weights
    b0 = 0
    b_age = 0
    b_wt = 0

    dim = len(age)
    for i in range(0,iterations):
        sum_b0, sum_age, sum_wt = single_iter(x0, age, weight, height, b0, b_age,
        b_wt)
        b0 -= (alpha * sum_b0) / dim
        b_age -= (alpha * sum_age) / dim
        b_wt -= (alpha * sum_wt) / dim
        #print ("i=%d, b_0=%f, b_age=%f, b_wt=%f" % (i, b0, b_age, b_wt))
    f.write('%f,%f,%f,%f,%f\n' % (alpha, iterations, b0, b_age, b_wt))

def main():
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    input_list = []
    with open(input_file, 'r') as f:
        reader = csv.reader(f)
        input_list = list(reader)
        input_list = [[float(x) for x in rec] for rec in input_list]

    # Parse out the plotting data
    age = [x[0] for x in input_list]
    wt = [x[1] for x in input_list]
    ht = [x[2] for x in input_list]

    #normalize the data
    age_mean, age_std = calc_stats(age)
    wt_mean, wt_std = calc_stats(wt)
    age_n = normalize_data(age, age_mean, age_std)
    wt_n = normalize_data(wt, wt_mean, wt_std)
    x_0 = [1] * len(age_n)

    f = open(output_file, 'w')

    for alpha in ALPHA:
        perform_regression(alpha, x_0, age_n, wt_n, ht, 100,f)

    f.close()





if __name__ == "__main__":
    main()
