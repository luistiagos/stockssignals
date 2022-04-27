from unicodedata import name
import repository
from datetime import datetime
from binance.exceptions import BinanceAPIException 
import binanceprovider
import rules as rules
import threading
import multiprocessing as mp
import strategies.strategies as strategies
from inspect import getmembers, isfunction

functions = {}

def init_function():
    members = getmembers(strategies, isfunction)
    for m in members:
        functions[m[0]] = m[1]

def exec_function(name, df):
    return functions[name](df)

def populate_candle(item, df, index=-1):
    item['date'] = df.iloc[index]['date']
    item['time'] = df.iloc[index]['time']
    item['open'] = df.iloc[index]['open']
    item['close'] = df.iloc[index]['close']
    item['pattern'] = ''
    if 'pattern' in df.iloc[index]:
        item['pattern'] = df.iloc[index]['pattern']

def sub_exec_strategies(df, functionname, item):
    check, stoploss, stopgain = exec_function(functionname, df)
    if  check:
        index = -1
        item['check'] = True
        if 'bear' in functionname:
            item['trend'] = 'bear'
        else:
            item['trend'] = 'bull'
        item['strategy'] = functionname
        populate_candle(item, df, index)
        stored_item = [item['coin'], item['intervel'], item['date'], item['time'], item['trend'], item['strategy'], item['pattern'], item['close'], stoploss, stopgain]
        repository.store_analysis([stored_item], 'stockanalysis.csv')

def exec_strategies(df, item):
    threads = set()
    names = []
    #names.append('lin_reg_reversion_bull')
    #names.append('lin_reg_reversion_bear')
    #names.append('lin_reg_reversion_period_50_bull')
    #names.append('lin_reg_reversion_period_50_bear')
    #names.append('lin_reg_reversion_period_hl_50_bull')
    #names.append('lin_reg_reversion_period_hl_50_bear')
    names.append('triple_ema_macd_bull')
    names.append('triple_ema_macd_bear')
    names.append('lin_reg_reversion2_bull')
    names.append('lin_reg_reversion2_bear')

    for funcname in names:
        t = threading.Thread(target=sub_exec_strategies, args=(df,funcname,item))
        t.start()
        threads.add(t)
    [t.join() for t in threads]

def avalible(coin, interval='hour'):
    item = {'coin': coin, 'check':False, 'intervel': interval}
    df = binanceprovider.get_candles_by_time(coin, interval)
    if len(df) > 0:
        exec_strategies(df, item)


def check_coin(coin, interval):
    coin = coin.strip()
    avalible(coin, interval)

def analysis(coins, interval):
    threads = set()
    for c in coins:
        #check_coin(c, interval)
        t = threading.Thread(target=check_coin, args=(c,interval))
        t.start()
        threads.add(t)

    [t.join() for t in threads]

    #if len(itens) > 0:
    #    repository.store_analysis(itens, 'stockanalysis.csv')

def execute(coins, intervals):
    for interval in intervals:
        analysis(coins, interval)

def run():
    init_function()
    repository.remove_file('stockanalysis.csv')
    coins = repository.load_coins('bcoins.csv')
    time = datetime.now()
    execute(coins, ['15min', '30min', 'hour', '2hours', '4hours', 'day'])
    print(datetime.now() - time)


run()