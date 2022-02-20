import repository
from datetime import datetime
from os.path import exists
import csv
import houranalysis
import binanceprovider
import rules
import threading
import multiprocessing as mp

def avaliable(coin):
    df = binanceprovider.get_candles_hour(coin)
    return len(df) > 0 and (rules.is_bullish_pattern(df) or rules.is_bearish_pattern(df)) #and rules.is_cross_ma_dows(df, 6)

def check_coin(coin, filtered_coins):
    if avaliable(coin):
        filtered_coins.add(coin)

def analysis(coins):
    filtered_coins = set()
    threads = set()
    for c in coins:
        t = threading.Thread(target=check_coin, args=(c, filtered_coins))
        t.start()
        threads.add(t)

    [t.join() for t in threads]

    if len(filtered_coins) > 0:
        repository.store_analysis(filtered_coins, '15manalysis.csv')

def load_hour_coins():
    if exists('hourcoins.csv') == False:
        houranalysis.run()

    coins = set()
    with open('hourcoins.csv', 'r', newline='', encoding='UTF8') as f:
        reader = csv.reader(f)
        for item in reader:
            coins.add(item[0])
    return coins

def run():
    coins = load_hour_coins()
    #coins = []
    #count = 0
    #for c in coinsx:
    #    if count <= 10:
    #        coins.append(c)
    #    count = count + 1
    time = datetime.now()
    analysis(coins)
    print(datetime.now() - time)