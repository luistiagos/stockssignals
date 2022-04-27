import repository
from datetime import datetime
from os.path import exists
import csv
import dayanalysis
import binanceprovider
import rules.rules as rules

def avaliable(coin):
    #df = binanceprovider.get_candles_hour(coin)
    return True #len(df) > 0 and (rules.is_bearish_pattern(df) or rules.is_bullish_pattern(df))

def analysis(coins):
    filtered_coins = set()
    for coin in coins:
        if avaliable(coin):
            filtered_coins.add(coin)
    if len(filtered_coins) > 0:
        repository.store_analysis(filtered_coins, 'hourcoins.csv')

def load_day_coins():
    if exists('daycoins.csv') == False:
        dayanalysis.run()

    coins = set()
    with open('daycoins.csv', 'r', newline='', encoding='UTF8') as f:
        reader = csv.reader(f)
        for item in reader:
            coins.add(item[0])
    return coins

def run():
    coins = load_day_coins()
    time = datetime.now()
    analysis(coins)
    print(datetime.now() - time)
