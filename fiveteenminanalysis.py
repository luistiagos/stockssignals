import repository
from datetime import datetime
from os.path import exists
import csv
import houranalysis
import binanceprovider
import rules.rules as rules
import threading
import multiprocessing as mp

def avaliable(coin):
    df = binanceprovider.get_candles_15min(coin)
    #x = len(df) > 0 and (rules.heiken_ashi_volume_adx_strategy_up(df))
    if len(df) == 0:
        return False

    x = True #rules.holy_grail_strategy_bull(df) #rules.heiken_ashi_volume_adx_strategy_up(df)
    y = rules.heiken_ashi_volume_adx_strategy_up(df) #rules.macd_invert_hist(df, -2) #rules.is_stochastic_down(df, 20)
    if x and y:
        print(coin + ' ' + str(df.iloc[-2]['time']) + ' ' + str(df.iloc[-2]['close_ha']))
        return True
    return False
    #and (rules.holy_grail_strategy_bull(df) or rules.holy_grail_strategy_bear(df))
    #return len(df) > 0 and (rules.is_bullish_pattern(df) or rules.is_bearish_pattern(df))

def check_coin(coin, filtered_coins):
    if avaliable(coin):
        filtered_coins.add(coin)

def analysis(coins):
    filtered_coins = set()
    threads = set()
    for c in coins:
        #check_coin(c, filtered_coins)
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
    time = datetime.now()
    analysis(coins)
    print(datetime.now() - time)