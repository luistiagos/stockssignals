import csv
import os
from os.path import exists

def store_coins(filename, coins):
    with open(filename, 'a', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        for item in coins:
            writer.writerow([item])

def load_coins(filename):
    if exists(filename) == False:
        store_coins()
    coins = set()
    with open(filename, 'r', newline='', encoding='UTF8') as f:
        reader = csv.reader(f)
        for item in reader:
            coins.add(item[0])
    return coins

def remove_file(filename):
    if os.path.exists(filename):
        os.remove(filename)

def store_analysis(data, filename):
    with open(filename, 'a', newline='', encoding='UTF8') as f:
        writer = csv.writer(f,  delimiter=';')
        for item in data:
            arr = item
            writer.writerow(arr)

