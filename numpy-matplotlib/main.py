import argparse
from matplotlib import pyplot as plt
import numpy as np
from scipy import stats


# mu - mean value
# sig - variance
def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))


def draw_gauss_chart(mu, sig, min_range, max_range):
    num_probes = int(abs(max_range - min_range) / 0.05)
    x_values = np.linspace(min_range, max_range, num_probes)

    plt.plot(x_values, gaussian(x_values, mu, sig), label="μ={}, σ²={}".format(mu, sig))
    plt.title("Gaussian function without libraries")
    plt.legend()


def draw_gauss_scipy_chart(mu, sig, min_range, max_range):
    num_probes = int(abs(max_range - min_range) / 0.05)
    x_values = np.linspace(min_range, max_range, num_probes)

    gaussian_scipy = stats.norm(loc=mu, scale=sig)
    y_values = gaussian_scipy.pdf(x_values)
    plt.plot(x_values, y_values, label="μ={}, σ²={}".format(mu, sig))
    plt.title("Gaussian function using scipy")
    plt.legend()


# 🥉 task
def first_task():
    params = get_values_from_input()
    draw_gauss_chart(params["mu"], params["sig"], params["min"], params["max"])
    plt.show()


# 🥈 task
def second_task():
    params = get_values_from_input()
    plt.subplot(1, 2, 1)
    draw_gauss_chart(params["mu"], params["sig"], params["min"], params["max"])

    plt.subplot(1, 2, 2)
    draw_gauss_scipy_chart(params["mu"], params["sig"], params["min"], params["max"])

    plt.show()


# 🥇 task
def third_task():
    params = get_values_argparse()

    # if arguments from standard deviation/variance are smaller than length of sigma's arguments, we must extend the
    # list to equal width of parameters
    # for example:
    # for -s 1.5 2 and -u 3 4 5
    # we extend the -s to 1.5 2 1.5 because number of arguments are smaller than -u
    first_grow, second_grow = 1, 1
    if len(params["mu"]) < len(params["sig"]):
        first_grow = len(params["sig"])
    else:
        second_grow = len(params["mu"])

    for mu, sig in zip(params["mu"] * first_grow, params["sig"] * second_grow):
        draw_gauss_chart(mu, sig, params["min"], params["max"])

    plt.show()


# get values from user using argparse
def get_values_argparse():
    min_range, max_range = 0., 0.
    sig, mu = [], []

    parser = argparse.ArgumentParser()
    parser.add_argument('-s', help='Standard deviation ', type=float, nargs='+')
    parser.add_argument('-u', help='Mean value', type=float, nargs='+')
    parser.add_argument('-w', help='Variance (overrides standard deviation)', type=float, nargs='+')
    parser.add_argument('-r', help='Range of calculations', type=float, nargs=2,
                        default=[-10, 10])
    parser.add_argument('--min', help='Min value of the range (overrides -r)', type=float)
    parser.add_argument('--max', help='Max value of the range (overrides -r)', type=float)
    args = parser.parse_args()

    if args.s:
        sig = args.s
    elif args.w:
        sig = list(map(lambda el: el ** 2, args.w))

    if args.u:
        mu = args.u
    else:
        exit("You must provide the average of the distribution")

    if args.min and args.max:
        min_range = args.min
        max_range = args.max
    elif args.r[0] and args.r[1]:
        min_range = args.r[0]
        max_range = args.r[1]

    if min_range > max_range:
        exit("Min must be less than max!")

    if min_range == 0 and max_range == 0:
        exit("You must provide the range")

    return {"sig": sig, "mu": mu, "min": min_range, "max": max_range}


# get values from user using input()
def get_values_from_input():
    try:
        while True:
            variance = float(input("Type variation: "))
            if variance == 0:
                sig = float(input("Type standard deviation: "))
                sig = sig ** 2
            else:
                sig = variance

            if variance != 0 or sig != 0:
                break
            else:
                print("Variance or standard deviation cannot be equal to 0!")

        mu = float(input("Type average: "))

        while True:
            min_range = float(input("Type min value of the range: "))
            max_range = float(input("Type max value of the range: "))

            if min_range < max_range:
                break
            else:
                print("Min value must be less than max!")
    except ValueError:
        exit("Invalid number! Program aborted!")

    return {"sig": sig, "mu": mu, "min": min_range, "max": max_range}


# first_task()
# second_task()
third_task()
