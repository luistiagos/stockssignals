from matplotlib.pyplot import plot, winter
import numpy as np
import pandas as pd
import indicators
import plots
import datetime

#Data Source
import yfinance as yf

def is_123_up(df):
    if len(df) > 5:
        exp1 = df.iloc[-2]['low'] < df.iloc[-1]['low']
        exp2 = df.iloc[-2]['low'] < df.iloc[-3]['low']

        if exp1 and exp2:
            return True
    return False

def is_stochastic_down(df, low=20):
    if df.iloc[-1]['K'] < low and df.iloc[-1]['D'] < low:
        return True
    return False

def is_stochastic_up(df, high=80):
    if df.iloc[-1]['K'] > high and df.iloc[-1]['D'] > high:
        return True
    return False

def is_ma_down(df, ma='MA21'):
    if df.iloc[-1][ma] > df.iloc[-1]['close']:
        return True
    return False

def is_ma_up(df, ma='MA21'):
    if df.iloc[-1][ma] < df.iloc[-1]['close']:
        return True
    return False

def is_price_down_chance_diverg(df, dfh):
    if dfh.iloc[-1]['change24p'] > 0 and df.iloc[-1]['change7p'] < 0 and df.iloc[-1]['change30p'] < 0:
        return True 
    return False

def is_last_candle_great(df):
    return df.iloc[-1]['close'] > df.iloc[-2]['close']

def is_triangle_down(df):
    return df.iloc[-3]['high'] < df.iloc[-2]['high'] and df.iloc[-2]['high'] > df.iloc[-1]['high']

def is_bband_overprice(df):
    return df.iloc[-1]['close'] >= df.iloc[-1]['UPPER_BAND_20']

def is_bband_underprice(df):
    return df.iloc[-1]['close'] <= df.iloc[-1]['LOWER_BAND_20']

def is_bband_underprice_diverg(df, size=5):
    underprice = df.iloc[-1]['close'] <= df.iloc[-1]['LOWER_BAND_20']
    if underprice:
        for i in range(1,size):
            index = i * -1
            if df.iloc[-1]['close'] > df.iloc[index]['MA20']:
                return True
    return False 

def is_overprice_close_in_band(df):
    exp = df.iloc[-2]['close'] >= df.iloc[-2]['UPPER_BAND_20']
    exp2 = df.iloc[-1]['close'] <= df.iloc[-1]['UPPER_BAND_20']
    return exp and exp2

def is_hammer(df):
    if is_last_candle_great(df):
        body = abs(df.iloc[-2]['close'] - df.iloc[-2]['open']) * 2
        cabecera = abs(df.iloc[-2]['high'] - df.iloc[-2]['close'])
        cabo = abs(df.iloc[-2]['low'] - df.iloc[-2]['close'])
        if cabo > cabecera and cabo > body:
            return True
    return False

def is_cross_ma_up(df, size=1):
    is_cross = False
    for i in range(0,size):
        i = i * -1
        if df.iloc[i]['PositionCrossMA'] == 1:
            is_cross = True
            break
    return is_cross

def is_cross_ma_dow(df, size=1):
    is_cross = False
    for i in range(0,size):
        i = i * -1
        if df.iloc[i]['PositionCrossMA'] == -1:
            is_cross = True
            break
    return is_cross

#def is_cross_ma_dow(df, size=1):
#    return df.iloc[size]['PositionCrossMA'] == -1

def get_coins(tick='ETC-USD', period='1000h', interval='1h', period_stocifr=21):
    #df = yf.download(tickers=tick, period = period, interval = interval)
    dt = datetime.datetime.today() + datetime.timedelta(hours=4)
    fromDate = str((dt - datetime.timedelta(hours=200)).strftime('%Y-%m-%d'))
    toDate = str(dt.strftime('%Y-%m-%d'))
    df = yf.download([tick], start=fromDate, end=toDate, interval = "1h")
    df = df.rename(columns={"Open":"open", "Close":"close", "Adj Close":"adj close", "Low":"low", "High":"high"})
    df['change'] = df['close'].pct_change() * 100
    df['change7p'] = df['close'].pct_change(periods=7) * 100
    df['change24p'] = df['close'].pct_change(periods=24) * 100
    df['change30p'] = df['close'].pct_change(periods=30) * 100
    df['RSI'] = indicators.computeRSI(df['adj close'], 14)
    df['MA21'] = indicators.MA(df, 21)
    df['MA9'] = indicators.MA(df, 9)
    df['MA100'] = indicators.MA(df, 100)
    df['MA72'] = indicators.MA(df, 72)
    df['K'], df['D'] = indicators.stochastic(df['RSI'], 3, 3, period_stocifr)

    dfbband = indicators.MA_BBANDS(df, 20)
    df['UPPER_BAND_20'] = dfbband['UPPER_BAND_20']
    df['LOWER_BAND_20'] = dfbband['LOWER_BAND_20']
    df['MA20'] = dfbband['MA_20']

    df['SignalCrossMA'] = 0.0
    df['SignalCrossMA'] = np.where(df['MA9'] > df['MA21'], 1.0, 0.0)
    df['PositionCrossMA'] = df['SignalCrossMA'].diff()

    df = df.dropna()
    return df


df = get_coins('BTC-USD', '1000h', '1h')
print(len(df))
print(df.iloc[-2]['close'])
#print(is_triangle_up(df, 'PI-USD'))
#plots.plot_cross_ma(df)
#print(df.iloc[-1]['open'])
#print(is_stochastic_up(df))
#plots.plot_price(df, 'MA20')
#print(is_ma_down(df, low=5, high=95))
#df = get_coins('BTC-USD', '100d', '1d')
#plots.plot_price(df, 'UPPER_BAND_20')
#print(is_down(df))
#df = get_coins('ETC-USD', '1000m', '15m')
#print(is_down(df))

