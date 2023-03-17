import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from config import *
import json
import file
import requests

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

def draw_chart_from_file_config():
    draw_gauss_chart(mu, sig, min_range, max_range)
    plt.show()

def draw_chart_from_json():
    file = open('config.json')
    params = json.load(file)
    draw_gauss_chart(params['mu'], params['sig'], params['min_range'], params['max_range'])
    plt.show()


# File URL: sqrt.pl/data.csv
# File URL: sqrt.pl/init.csv
def convert_csv_to_json(file_to_load):
    data = file.csv_load_data(file_to_load)
    keys = list(data[0].keys())
    series = {}

    for key in keys:
        series[key] = []

    for row in data:
        for key in keys:
            series[key] += row[key]

    return series


# df = pd.read_csv('data.csv')
# print(df['ax'])
# print(list(df['ax']))

# json load
# json save

# json_file = file.json_load('sig.json')
#
# output = {}
# for row in json_file:
#     output[row] = json_file[row]['name']
#
# file.json_save(output, 'output.json')


x = requests.get('https://api.exchangerate.host/latest', params = {"base": "PLN"})

for name, rate in x.json()['rates'].items():
    print(name, rate)