import pandas as pd
import numpy as np
import indicators
import talib as ta
import candlestick_patterns as cp
import functions as fn
from scipy.stats import linregress
from sklearn.linear_model import LinearRegression

def move_averanges(df, values, attr='close'):
    for v in values:
        ma = 'MA_' + attr + '_' + str(v)
        df[ma] = ta.MA(df[attr], timeperiod=v) #indicators.MA(df, v)#ta.MA(df[attr], v)

def exponential_move_averanges(df, values, attr='close'):
    for v in values:
        ma = 'EMA_' + attr + '_' + str(v)
        df[ma] = ta.EMA(df[attr], v)

def change_pct(df, periods):
    for p in periods:
        change = 'change' + str(p) + 'p'
        df[change] = df['close'].pct_change(periods=p) * 100

def avd(df, periods):
    for p in periods:
        df['ADV' + str(p)] = df['volume'].rolling(window=p).mean().shift(1)

def rsi(df, periods):
    for p in periods:
        df['RSI_' + str(p)] = indicators.computeRSI(df['close'], p)

def stochastic_rsi(df, periods, k_window=3, d_window=3, period_stocifr=21):
    for p in periods:
        rsi = 'RSI_' + str(p)
        if rsi not in df.columns:
            rsi(df, [p])
        df['K_' + str(p)], df['D_' + str(p)] = indicators.stochastic(df[rsi], k_window, d_window, period_stocifr)

def bbands(df, values, attr='close'):
    for v in values:
        dfbband = indicators.MA_BBANDS(df, v, attr)
        upperband = 'UPPER_BAND_' + attr + '_' + str(v)
        lowerband = 'LOWER_BAND_' + attr + '_' + str(v)
        df[upperband] = dfbband['UPPER_BAND_' + str(v)]
        df[lowerband] = dfbband['LOWER_BAND_' + str(v)]
        df['MA_' + attr + '_' + str(v)] = dfbband['MA_' + str(v)]

def cross_ma(df, low=9, high=21, attr='close'):
    ma_l = 'MA_' + attr + '_' + str(low)
    ma_h = 'MA_' + attr + '_' + str(high)
    if ma_l not in df.columns:
        df[ma_l] = ta.MA(df[attr], low)
    if ma_h not in df.columns:
        df[ma_h] = ta.MA(df[attr], high)

    signal_cross = 'SignalCrossMA_' + attr + '_' + ma_l + '_' + ma_h
    position_cross = 'PositionCrossMA_' + attr + '_' + ma_l + '_' + ma_h
    df[signal_cross] = 0.0
    df[signal_cross] = np.where(df[ma_l] > df[ma_h], 1.0, 0.0)
    df[position_cross] = df[signal_cross].diff()

def price_transform(df):
    df['AVGPRICE'] = ta.AVGPRICE(df['open'], df['high'], df['low'], df['close'])

def linear_reg_channel(df, period=100, attr='close', dev=2):
    df['LNC_ABOVE'] = np.zeros(len(df))
    df['LNC_MIDDLE'] = np.zeros(len(df))
    df['LNC_BELLOW'] = np.zeros(len(df))

    ln = indicators.linear_regression_channel(df[-period:], attr, dev)
    df[-period:]['LNC_ABOVE'] = ln['above']
    df[-period:]['LNC_MIDDLE'] = ln['middle']
    df[-period:]['LNC_BELLOW'] = ln['bellow']

def trends_lines(df, period=100):
    df['UPTREND'] = np.zeros(len(df))
    df['DOWNTREND'] = np.zeros(len(df))

    df_high = df.copy()
    df_low = df.copy()

    while len(df_high)>2:
        slope, intercept, r_value, p_value, std_err = linregress(x=df_high[-period:]['id'], y=df_high[-period:]['high'])
        df_high_res = df_high[-period:].loc[df_high[-period:]['high'] > slope * df_high[-period:]['id'] + intercept]
        if len(df_high_res) < 2:
            break
        df_high = df_high_res

    while len(df_low)>2:
        slope, intercept, r_value, p_value, std_err = linregress(x=df_low[-period:]['id'], y=df_low[-period:]['low'])
        df_low_res = df_low[-period:].loc[df_low[-period:]['low'] < slope * df_low[-period:]['id'] + intercept]
        if len(df_low_res) < 2:
            break
        df_low = df_low_res

    slope, intercept, r_value, p_value, std_err = linregress(x=df_high[-period:]['id'], y=df_high[-period:]['high'])
    df['UPTREND'] = (slope * df[-period:]['id'] + intercept)
    slope, intercept, r_value, p_value, std_err = linregress(x=df_low[-period:]['id'], y=df_low[-period:]['low'])
    df['DOWNTREND'] = (slope * df[-period:]['id'] + intercept)

def get_coins(df):
    df = df.dropna()
    if len(df) > 0:
        df['id'] = np.arange(len(df))+1
        #cp.candle_patterns(df)
        #price_transform(df)
        #rsi(df, [14])
        #stochastic_rsi(df, [14])
        #change_pct(df, [1,5,7,24,30,100])
        #avd(df, [5,10,20])
        #move_averanges(df, values=[9,21,50,99,100,200])
        #exponential_move_averanges(df, [9,21,50,99,100,200])
        #move_averanges(df, values=[5,10,21], attr='volume')
        #bbands(df, [20])
        #cross_ma(df)
        #linear_reg_channel(df)
        trends_lines(df)
        df = df.dropna()
    return df