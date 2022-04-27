import binanceprovider
import pandas as pd
from strategies.InvertTrendSupertrend import InvertTrendSupertrend
from strategies.Supertrendrsihma import Supertrendrsihma
from strategies.LinregReversionHL import LinregReversionHL
from strategies.LinregReversion import LinregReversion
from strategies.LinregReversion2 import LinregReversion2
from strategies.BollingBandsRSIReversion import BollingBandsRSIReversion
from strategies.Reversions import Reversions
from strategies.HollyGrallMACD import HollyGrall
from strategies.HollyGrall import HollyGrall2
from strategies.BollingBandsNoTrend import BollingBandsNoTrend
from strategies.CrossEmaMacd import CrossEmaMacd
from strategies.InvertTrend import InvertTrend
from strategies.HullMA import HullMA
from strategies.TripleEMA import TripleEMA
from strategies.TripleEMA_MACD import TripleEMA_MACD
from datetime import datetime
import threading
import repository
import utils.timeutils as timeutils
import sys

sys.setrecursionlimit(1000000)

def results():
    df = pd.read_csv('sumaryresult.csv', sep=';', index_col=False, 
                 names=['coin', 'percent', 'stopgain', 'stoploss'])
    print(df['percent'].sum())
    print((df['stopgain'].sum() / (df['stopgain'].sum() + df['stoploss'].sum())) * 100)


def savefile(item, file='result.csv'):
    trend = ''
    if item['trend']:
        trend = 'bull'
    else:
        trend = 'bear'
    stored_item = [item['coin'], item['interval'], item['startdate'], item['starttime'], item['date'], item['time'], trend, item['strategy'], item['close'], item['result'], item['profit']]
    repository.store_analysis([stored_item], file)

def saveSumaryfile(sumary, file='sumaryresult.csv'):
    repository.store_analysis([sumary], file)

def backtest(item, strategy, tries=0, stopgain=0, stoploss=0, percent=0):
    coin = item['coin']
    time = item['time']
    interval = item['interval']

    df = binanceprovider.get_candles_by_time(coin, interval, time)
    df['coin'] = coin
    strategy.setDf(df)
    index = strategy.getSize()
    trade = False
    size = len(df) - strategy.getSize()

    while index < size:
        item['date'] = df.iloc[index]['date']
        item['time'] = df.iloc[index]['time']
        if trade:
            if strategy.hitStopGain(index):
                item['result'] = 'Win'
                item['profit'] = strategy.getProfit()
                stopgain = stopgain + 1
                percent = percent + strategy.getProfit()
                trade = False
            elif strategy.hitStopLoss(index):
                item['result'] = 'Loss'
                item['profit'] = strategy.getLoss()
                stoploss= stoploss + 1
                percent = percent + strategy.getLoss()
                trade = False
            elif index == (size - 1):
                p = strategy.getCurrProfitLoss(index)
                if p > 0:
                    item['result'] = 'Win'
                    item['profit'] = strategy.getProfit()
                    stopgain = stopgain + 1
                else:
                    item['result'] = 'Loss'
                    item['profit'] = strategy.getLoss()
                    stoploss = stoploss + 1

            if trade == False:
                item['trend'] = strategy.getTrend()
                item['startdate'] = strategy.getStartDate()
                item['starttime'] = strategy.getStartTime()
                item['close'] = df.iloc[index]['close']
                savefile(item)
        else:
            if strategy.buy(index) or strategy.sell(index):
                trade = True
                tries = tries + 1

        index = index + 1

    if len(df) > 0 and tries < 10:
        item['time'] = timeutils.strdatetime_to_date(df.iloc[0]['date'], df.iloc[0]['time'])
        return backtest(item=item, strategy=strategy, tries=tries, stopgain=stopgain, stoploss=stoploss, percent=percent)

    return (coin, percent, stopgain, stoploss)

def test(coin, interval, strategy, time):
    item = {}
    item['coin'] = coin
    item['strategy'] = strategy.getName()
    item['time'] = time
    item['interval'] = interval

    backt = backtest(strategy=strategy, item=item)
    print(backt)
    saveSumaryfile(backt, file='sumaryresult.csv')

def run():
    threads = set()
    strategy=LinregReversion2()
    time = timeutils.new_utc_date_hours()
    interval='15min'
    coins = repository.load_coins('bcoins.csv')
    for c in coins:
        test(c, interval, strategy, time)
        #t = threading.Thread(target=test, args=(c, interval, strategy, time))
        #t.start()
        #threads.add(t)

    #[t.join() for t in threads]

run()
#results()
