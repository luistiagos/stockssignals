from binance import Client
import pandas as pd
import datetime
import provider
import rules

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
    klines = client.get_historical_klines(symbol, interval, fromDate, toDate)
    df = pd.DataFrame(klines, columns=['dateTime', 'open', 'high', 'low', 'close', 'volume', 'closeTime', 'quoteAssetVolume', 'numberOfTrades', 'takerBuyBaseVol', 'takerBuyQuoteVol', 'ignore'])
    df.dateTime = pd.to_datetime(df.dateTime, unit='ms')
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
    return provider.get_coins(df)

def get_candles_day(symbol):
    dt = datetime.datetime.today()
    fromDate = str((dt - datetime.timedelta(weeks=72)).strftime('%d/%m/%Y %H:%M:%S'))
    toDate = str(dt.strftime('%d/%m/%Y %H:%M:%S'))
    return get_candles(symbol, Client.KLINE_INTERVAL_1DAY, fromDate, toDate)

def get_candles_hour(symbol):
    dt = datetime.datetime.today() + datetime.timedelta(hours=4)
    fromDate = str((dt - datetime.timedelta(weeks=4)).strftime('%d/%m/%Y %H:%M:%S'))
    toDate = str(dt.strftime('%d/%m/%Y %H:%M:%S'))
    return get_candles(symbol, Client.KLINE_INTERVAL_1HOUR, fromDate, toDate)

def get_candles_15min(symbol):
    dt = datetime.datetime.today() + datetime.timedelta(hours=4)
    fromDate = str((dt - datetime.timedelta(weeks=1)).strftime('%d/%m/%Y %H:%M:%S'))
    toDate = str(dt.strftime('%d/%m/%Y %H:%M:%S'))
    return get_candles(symbol, Client.KLINE_INTERVAL_15MINUTE, fromDate, toDate)

def get_candles_5min(symbol):
    dt = datetime.datetime.today() + datetime.timedelta(hours=4)
    fromDate = str((dt - datetime.timedelta(days=4)).strftime('%d/%m/%Y %H:%M:%S'))
    toDate = str(dt.strftime('%d/%m/%Y %H:%M:%S'))
    return get_candles(symbol, Client.KLINE_INTERVAL_5MINUTE, fromDate, toDate)

def get_candles_min(symbol):
    dt = datetime.datetime.today() + datetime.timedelta(hours=4)
    fromDate = str((dt - datetime.timedelta(days=1)).strftime('%d/%m/%Y %H:%M:%S'))
    toDate = str(dt.strftime('%d/%m/%Y %H:%M:%S'))
    return get_candles(symbol, Client.KLINE_INTERVAL_1MINUTE, fromDate, toDate)


#coin = get_all_binance_coins()
#fromDate = str(datetime.strptime('19/11/2021', '%d/%m/%Y'))
#toDate = str(datetime.strptime('20/11/2021', '%d/%m/%Y'))
#symbol = "BTCUSDT"
#interval = Client.KLINE_INTERVAL_1MINUTE
#df = get_candles(symbol, interval, fromDate, toDate)
#df

