from scipy.stats import linregress
import talib as ta
import numpy as np
import indicators
import math
import pandas as pd
import candlestick_patterns as cp

def cross_ma(df, low=9, high=21, attr='close'):
    ma_l = 'MA_' + attr + '_' + str(low)
    ma_h = 'MA_' + attr + '_' + str(high)
    if ma_l not in df.columns:
        df[ma_l] = ta.MA(df[attr], low)
    if ma_h not in df.columns:
        df[ma_h] = ta.MA(df[attr], high)

    signal_cross = 'SignalCrossMA_' + attr + '_' + ma_l + '_' + ma_h
    position_cross = 'PositionCrossMA_' + attr + '_' + str(low) + '_' + str(high)
    df[signal_cross] = 0.0
    df[signal_cross] = np.where(df[ma_l] > df[ma_h], 1.0, 0.0)
    df[position_cross] = df[signal_cross].diff()
    
def cross_ema(df, low=9, high=21, attr='close'):
    ma_l = 'EMA_' + attr + '_' + str(low)
    ma_h = 'EMA_' + attr + '_' + str(high)
    if ma_l not in df.columns:
        df[ma_l] = ta.EMA(df[attr], low)
    if ma_h not in df.columns:
        df[ma_h] = ta.EMA(df[attr], high)

    signal_cross = 'SignalCrossEMA_' + attr + '_' + ma_l + '_' + ma_h
    position_cross = 'PositionCrossEMA_' + attr + '_' + str(low) + '_' + str(high)
    df[signal_cross] = 0.0
    df[signal_cross] = np.where(df[ma_l] > df[ma_h], 1.0, 0.0)
    df[position_cross] = df[signal_cross].diff()

def linear_reg_channel(df, period=100, attr='close', dev=2):
    LNC_ABOVE = 'LNC_ABOVE_' + str(period) + '_' + attr + '_' + str(dev)
    LNC_MIDDLE = 'LNC_MIDDLE_' + str(period) + '_' + attr + '_' + str(dev)
    LNC_BELLOW = 'LNC_BELLOW_' + str(period) + '_' + attr + '_' + str(dev)
    df[LNC_ABOVE] = np.zeros(len(df))
    df[LNC_MIDDLE] = np.zeros(len(df))
    df[LNC_BELLOW] = np.zeros(len(df))

    i = 1
    start = period
    while True:
        if len(df.iloc[-start-1:-i]) == 0:
            break
        linreg_channel(df.iloc[-start-1:-i], period=period, attr=attr, dev=dev,
                    above=LNC_ABOVE, middle=LNC_MIDDLE, bellow=LNC_BELLOW)
        i = i + period
        if i > len(df):
            break
        start = start + period
        if start > len(df):
            start = start - len(df)

def linreg_channel(df, period=100, attr='close', dev=2, above='', middle='', bellow=''):
    ln = indicators.linear_regression_channel(df[-period:], attr, dev)
    df[-period:][above] = ln['above']
    df[-period:][middle] = ln['middle']
    df[-period:][bellow] = ln['bellow']

def macd(df, attr='close', fastperiod=8, slowperiod=21, signalperiod=5):
    macd, macdsignal, macdhist = ta.MACD(df[attr], fastperiod=fastperiod, slowperiod=slowperiod, signalperiod=signalperiod)
    df['MACD'] = macd
    df['MACDSIGNAL'] = macdsignal
    df['MACDHIST'] = macdhist

def stochastic_rsi(df, periods, k_window=3, d_window=3, period_stocifr=21):
    for p in periods:
        rsi = 'RSI_' + str(p)
        if rsi not in df.columns:
            rsi(df, [p])
        df['K_' + str(p)], df['D_' + str(p)] = indicators.stochastic(df[rsi], k_window, d_window, period_stocifr)

def rsi(df, periods):
    for p in periods:
        df['RSI_' + str(p)] = indicators.computeRSI(df['close'], p)

def avd(df, periods):
    for p in periods:
        df['ADV' + str(p)] = df['volume'].rolling(window=p).mean().shift(1)

def change_pct(df, periods):
    for p in periods:
        change = 'change' + str(p) + 'p'
        df[change] = df['close'].pct_change(periods=p) * 100

def move_averanges(df, values, attr='close'):
    for v in values:
        ma = 'MA_' + attr + '_' + str(v)
        df[ma] = ta.MA(df[attr], timeperiod=v)

def exponential_move_averanges(df, values, attr='close'):
    for v in values:
        ma = 'EMA_' + attr + '_' + str(v)
        df[ma] = ta.EMA(df[attr], v)

def wma_move_averanges(df, values, attr='close'):
    for v in values:
        ma = 'WMA_' + attr + '_' + str(v)
        df[ma] = ta.WMA(df[attr], v)

def hma_move_averanges(df, values, attr='close'):
     for v in values:
        try:
            hma = 'HMA_' + attr + '_' + str(v)
            df[hma] = ta.WMA(ta.WMA(df[attr], v // 2).multiply(2).sub(ta.WMA(df[attr], v)), int(np.sqrt(v)))
        except:
            print('error')

def adx(df, period=14):
    df['ADX_' + str(period)] = ta.ADX(df['high'], df['low'], df['close'], timeperiod=period)

def bbands(df, values=[20], attr='close'):
    for v in values:
        dfbband = indicators.MA_BBANDS(df, v, attr)
        upperband = 'UPPER_BAND_' + attr + '_' + str(v)
        lowerband = 'LOWER_BAND_' + attr + '_' + str(v)
        df[upperband] = dfbband['UPPER_BAND_' + str(v)]
        df[lowerband] = dfbband['LOWER_BAND_' + str(v)]
        df['MA_' + attr + '_' + str(v)] = dfbband['MA_' + str(v)]

def trends_lines(df, period=100):
    df['UPTREND'] = np.zeros(len(df))
    df['DOWNTREND'] = np.zeros(len(df))

    i = 1
    start = period
    while True:
        if len(df.iloc[-start-1:-i]) == 0:
            break
        trendslines(df.iloc[-start-1:-i], period=period)
        i = i + period
        if i > len(df):
            break
        start = start + period
        if start > len(df):
            start = start - len(df)


def trendslines(df, period=100):

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


def true_range(df):
    high = df['high']
    low = df['low']
    close = df['close']

    price_diffs = [high - low,
                   high - close.shift(),
                   close.shift() - low]
    true_range = pd.concat(price_diffs, axis=1)
    true_range = true_range.abs().max(axis=1)
    df['TRUERANGE'] = true_range

def atr(df, atr_period=14):
    df['ATR'] = df['TRUERANGE'].ewm(alpha=1/atr_period,min_periods=atr_period).mean()

def hl2(df):
    df['HL2'] = (df['high'] + df['low']) / 2

def supertrend(df, attr='HL2', multiplier=3):
    final_upperband = df[attr] + (multiplier * df['ATR'])
    final_lowerband = df[attr] - (multiplier * df['ATR'])
    close = df['close']
    # initialize Supertrend column to True
    supertrend = [True] * len(df) #len(df)

    for i in range(1, len(df)):
        curr = i * -1
        prev = (i * -1) - 1

        # if current close price crosses above upperband
        if close.iloc[curr] > final_upperband.iloc[prev]:
            supertrend[curr] = True
        # if current close price crosses below lowerband
        elif close.iloc[curr] < final_lowerband.iloc[prev]:
            supertrend[curr] = False
        # else, the trend continues
        else:
            supertrend[curr] = supertrend[prev]

            # adjustment to the final bands
            if supertrend[curr] == True and final_lowerband.iloc[curr] < final_lowerband.iloc[prev]:
                final_lowerband.iloc[curr] = final_lowerband.iloc[prev]
            if supertrend[curr] == False and final_upperband.iloc[curr] > final_upperband.iloc[prev]:
                final_upperband.iloc[curr] = final_upperband.iloc[prev]

        # to remove bands according to the trend direction
        #if supertrend[curr] == True:
        #    final_upperband.iloc[curr] = np.nan
        #else:
        #    final_lowerband.iloc[curr] = np.nan

    df['Supertrend'] = supertrend
    df['Supertrend_FinalLowerband'] = final_lowerband
    df['Supertrend_FinalUpperband'] = final_upperband

def heikin_ashi(df):
    df['close_ha'] = (df['open'] + df['high'] + df['low'] + df['close']) / 4
    df['open_ha'] = ((df['open'] + df['close']) / 2).shift(1)
    df['high_ha'] = df['high']
    df['low_ha'] = df['low']
