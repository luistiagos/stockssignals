from binance import Client
import pandas as pd
import datetime
import provider
import rules.rules as rules
from datetime import timezone
import utils.timeutils as timeutils

api_key = "qBMufCjtvHVnJcXtCmiPXAz2ibU5cHf6mUQMw6w7pii1El2ugalduzpZCARhOeunDA"
api_secret = "BvkhLmacjJkc8SKKQ2vD6CNdYIPbtdY8HHH94olMKKY7v4RX8coBnxvMn2PFw4TT"
client = Client(api_key, api_secret)


def get_all_binance_coins():
    exchange_info = client.get_exchange_info()
    coins = set()
    for s in exchange_info['symbols']:
        if s['baseAsset'] != 'USDT' and s['quoteAsset'] == 'USDT':
            coins.add(s['baseAsset'] + 'USDT')
    return coins

def get_candles(symbol, interval, fromDate, toDate):
    #timestamp = client._get_earliest_valid_timestamp(symbol, interval)
    #klines = client.get_klines((symbol=symbol,interval=interval, startTime=fromDate, endTime=toDate))
    klines = client.get_historical_klines(symbol, interval, start_str=str(fromDate), end_str=str(toDate))
    #klines = client.get_historical_klines(symbol, interval, timestamp, limit=1000)
    #klines = client.get_klines(symbol=symbol,interval=interval,limit=500)
    df = pd.DataFrame(klines, columns=['dateTime', 'open', 'high', 'low', 'close', 'volume', 'closeTime', 'quoteAssetVolume', 'numberOfTrades', 'takerBuyBaseVol', 'takerBuyQuoteVol', 'ignore'])
    df.dateTime = timeutils.utc_to_localdate(pd.to_datetime(df.dateTime, unit='ms'))
    df['date'] = df.dateTime.dt.strftime("%d/%m/%Y")
    df['time'] = df.dateTime.dt.strftime("%H:%M:%S")
    df = df.drop(['dateTime', 'closeTime', 'quoteAssetVolume', 'numberOfTrades', 'takerBuyBaseVol','takerBuyQuoteVol', 'ignore'], axis=1)
    column_names = ["date", "time", "open", "high", "low", "close", "volume"]
    df = df.reindex(columns=column_names)
    df['open'] = df['open'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)
    df['close'] = df['close'].astype(float)
    df['volume'] = df['volume'].astype(float)
    #df['open_ha'] = (df['open'].shift(1) + df['close'].shift(1)) / 2
    #df['close_ha'] = (df['open'] + df['close'] + df['low'] + df['high']) / 4

    return provider.get_coins(df)

def get_candles_day(symbol, dt=timeutils.new_utc_date()):
    timestampFromDate = (dt - datetime.timedelta(days=1000)).timestamp()
    timestampToDate = dt.timestamp()
    #fromDate = str((dt - datetime.timedelta(days=1000)).strftime('%d/%m/%Y %H:%M:%S'))
    #toDate = str(dt.strftime('%d/%m/%Y %H:%M:%S'))
    return get_candles(symbol, Client.KLINE_INTERVAL_1DAY, timestampFromDate, timestampToDate)

def get_candles_hour(symbol, dt=timeutils.new_utc_date_hours()):
    timestampFromDate = (dt - datetime.timedelta(hours=1000)).timestamp()
    timestampToDate = dt.timestamp()
    #fromDate = str((dt - datetime.timedelta(hours=200)).strftime('%d/%m/%Y %H:%M:%S'))
    #toDate = str(dt.strftime('%d/%m/%Y %H:%M:%S'))
    return get_candles(symbol, Client.KLINE_INTERVAL_1HOUR, timestampFromDate, timestampToDate)

def get_candles_2hour(symbol, dt=timeutils.new_utc_date_hours()):
    timestampFromDate = (dt - datetime.timedelta(hours=2000)).timestamp()
    timestampToDate = dt.timestamp()
    #fromDate = str((dt - datetime.timedelta(hours=200)).strftime('%d/%m/%Y %H:%M:%S'))
    #toDate = str(dt.strftime('%d/%m/%Y %H:%M:%S'))
    return get_candles(symbol, Client.KLINE_INTERVAL_2HOUR, timestampFromDate, timestampToDate)

def get_candles_4hour(symbol, dt=timeutils.new_utc_date_hours()):
    timestampFromDate = (dt - datetime.timedelta(hours=4000)).timestamp()
    timestampToDate = dt.timestamp()
    #fromDate = str((dt - datetime.timedelta(hours=200)).strftime('%d/%m/%Y %H:%M:%S'))
    #toDate = str(dt.strftime('%d/%m/%Y %H:%M:%S'))
    return get_candles(symbol, Client.KLINE_INTERVAL_4HOUR, timestampFromDate, timestampToDate)

def get_candles_30min(symbol, dt=timeutils.new_utc_date_minutes()):
    timestampFromDate = (dt - datetime.timedelta(hours=500)).timestamp()
    timestampToDate = dt.timestamp()
    #fromDate = str((dt - datetime.timedelta(hours=200)).strftime('%d/%m/%Y %H:%M:%S'))
    #toDate = str(dt.strftime('%d/%m/%Y %H:%M:%S'))
    return get_candles(symbol, Client.KLINE_INTERVAL_30MINUTE, timestampFromDate, timestampToDate)

def get_candles_15min(symbol, dt=timeutils.new_utc_date_minutes()):
    timestampFromDate = (dt - datetime.timedelta(hours=250)).timestamp()
    timestampToDate = dt.timestamp()
    #fromDate = str((dt - datetime.timedelta(hours=200)).strftime('%d/%m/%Y %H:%M:%S'))
    #toDate = str(dt.strftime('%d/%m/%Y %H:%M:%S'))
    return get_candles(symbol, Client.KLINE_INTERVAL_15MINUTE, timestampFromDate, timestampToDate)

def get_candles_5min(symbol, dt=timeutils.new_utc_date_minutes()):
    timestampFromDate = (dt - datetime.timedelta(minutes=5000)).timestamp()
    timestampToDate = dt.timestamp()
    #fromDate = str((dt - datetime.timedelta(hours=200)).strftime('%d/%m/%Y %H:%M:%S'))
    #toDate = str(dt.strftime('%d/%m/%Y %H:%M:%S'))
    return get_candles(symbol, Client.KLINE_INTERVAL_5MINUTE, timestampFromDate, timestampToDate)

def get_candles_3min(symbol, dt=timeutils.new_utc_date_minutes()):
    timestampFromDate = (dt - datetime.timedelta(minutes=3000)).timestamp()
    timestampToDate = dt.timestamp()
    #fromDate = str((dt - datetime.timedelta(hours=200)).strftime('%d/%m/%Y %H:%M:%S'))
    #toDate = str(dt.strftime('%d/%m/%Y %H:%M:%S'))
    return get_candles(symbol, Client.KLINE_INTERVAL_3MINUTE, timestampFromDate, timestampToDate)

def get_candles_min(symbol, dt=timeutils.new_utc_date_minutes()):
    timestampFromDate = (dt - datetime.timedelta(minutes=1000)).timestamp()
    timestampToDate = dt.timestamp()
    #fromDate = str((dt - datetime.timedelta(hours=200)).strftime('%d/%m/%Y %H:%M:%S'))
    #toDate = str(dt.strftime('%d/%m/%Y %H:%M:%S'))
    return get_candles(symbol, Client.KLINE_INTERVAL_1MINUTE, timestampFromDate, timestampToDate)

def get_times_label():
    return ['day', '4hours', '2hours', 'hour', '30min' ,'15min', '5min', '3min', 'min']

def get_candles_by_time(symbol, time='day', dt=timeutils.new_utc_date_minutes()):
    funcs = {}
    funcs['day'] = get_candles_day
    funcs['4hours'] = get_candles_4hour
    funcs['2hours'] = get_candles_2hour
    funcs['hour'] = get_candles_hour
    funcs['30min'] = get_candles_30min
    funcs['15min'] = get_candles_15min
    funcs['5min'] = get_candles_5min
    funcs['3min'] = get_candles_3min
    funcs['min'] = get_candles_min
    return funcs[time](symbol, dt)

#coin = get_all_binance_coins()
#fromDate = str(datetime.strptime('19/11/2021', '%d/%m/%Y'))
#toDate = str(datetime.strptime('20/11/2021', '%d/%m/%Y'))
#symbol = "BTCUSDT"
#interval = Client.KLINE_INTERVAL_1MINUTE
#df = get_candles(symbol, interval, fromDate, toDate)
#df

#timestamp = client._get_earliest_valid_timestamp('BTCUSDT', '1d')
#print(timestamp)
#x = client.get_historical_klines('BTCUSDT', '1d', timestamp, limit=1000)
#print(x)

#dt = datetime.datetime.today()
#fromDate = str((dt - datetime.timedelta(weeks=1)).strftime('%d/%m/%Y %H:%M:%S'))
#toDate = str(dt.strftime('%d/%m/%Y %H:%M:%S'))
#x = get_candles('BTCUSDT', Client.KLINE_INTERVAL_15MINUTE, fromDate, toDate)
#print(x)

#dt = datetime.datetime.today()
#fromDate = str((dt - datetime.timedelta(weeks=1)).strftime('%d/%m/%Y %H:%M:%S'))
#toDate = str(dt.strftime('%d/%m/%Y %H:%M:%S'))
#x = get_candles('BTCUSDT', Client.KLINE_INTERVAL_15MINUTE, fromDate, toDate)
#print(x)

#qtds = []
#for t in get_times_label():
#    x = get_candles_by_time('BTCUSDT', t)
#    qtds.append(t + ' ' + str(len(x)))

#for l in qtds:
#    print(l)

#x = get_candles_by_time('BTCUSDT', 'hour')
#print(len(x))
#print(x.iloc[-2]['date'])
#print(x.iloc[-2]['time'])
#print(x.iloc[-2]['close'])

#print(datetime.datetime.utcnow() - datetime.datetime.now())

