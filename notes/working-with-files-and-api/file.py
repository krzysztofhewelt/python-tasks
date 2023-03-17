import codecs
import csv
import json


def csv_load_data(path, sep = ','):
    raw = list(csv.DictReader(codecs.open(path, 'r', 'utf-8')))
    return raw


def json_load(path):
    file = open(path)
    raw = json.load(file)
    return raw

def json_save(data, filename):
    file = open(filename, 'w')
    json.dump(data, file)