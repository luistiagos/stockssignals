import pandas as pd
import numpy as np
import indicators
import repository
import talib as ta
import candlestick_patterns as cp
import functions as fn
import algorithms
from scipy.stats import linregress
from sklearn.linear_model import LinearRegression


def get_coins(df):
    df = df.dropna()
    if len(df) > 0:
        df['id'] = np.arange(len(df))+1
        algorithms.heikin_ashi(df)
        algorithms.hl2(df)
        #cp.candle_patterns(df)
        #price_transform(df)
        algorithms.rsi(df, [14, 2])
        #algorithms.stochastic_rsi(df, [14])
        #algorithms.macd(df)
        algorithms.macd(df, fastperiod=12, slowperiod=26, signalperiod=9)
        #change_pct(df, [1,5,7,24,30,100])
        #avd(df, [5,10,20])
        algorithms.move_averanges(df, values=[9,21,50,99,100,200])
        df = df.dropna()
        algorithms.exponential_move_averanges(df, [8,15,14,9,20,30,21,50,99,100,200])
        df = df.dropna()
        algorithms.hma_move_averanges(df,[55, 20, 21, 10])
        df = df.dropna()
        algorithms.adx(df)
        algorithms.true_range(df)
        algorithms.atr(df)
        #algorithms.hl2atrbands(df)
        #algorithms.move_averanges(df, values=[5,10,21], attr='volume')
        algorithms.bbands(df, [21])
        algorithms.supertrend(df)
        #algorithms.bbands(df, [20], attr='close_ha')
        algorithms.cross_ema(df, low=12, high=26)
        df = df.dropna()
        df = df.iloc[len(df)-100:]
        algorithms.linear_reg_channel(df, dev=2, period=100)
        algorithms.linear_reg_channel(df, dev=3, period=100)
        #algorithms.trends_lines(df)
        algorithms.linear_reg_channel(df, dev=2, period=50)
        algorithms.linear_reg_channel(df, dev=3, period=50)
        algorithms.linear_reg_channel(df, dev=2, period=10)
        algorithms.linear_reg_channel(df, dev=3, period=10)
        #algorithms.linear_reg_channel(df, dev=2, period=20)
        #algorithms.linear_reg_channel(df, dev=3, period=20)
        #algorithms.trends_lines(df)
    return df