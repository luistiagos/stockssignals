from matplotlib.pyplot import plot, winter
import numpy as np
import pandas as pd
import candlestick_patterns as cp


def bullish(df, index=-1):
    return  df.iloc[index-1]['close'] < df.iloc[index]['open']

def bearish(df, index=-1):
    return  df.iloc[index-1]['close'] > df.iloc[index]['open']


def is_bullish_pattern(df, index=-1):
    patterns = cp.patterns_names()
    for p in patterns:
        if df.iloc[index][p] > 0:
            return True
    return False

def is_bearish_pattern(df, index=-1):
    patterns = cp.patterns_names()
    for p in patterns:
        if df.iloc[index][p] < 0:
            return True
    return False

def is_volume_greather_than_mean(df, vlr=21, index=-1):
    return df.iloc[index]['volume'] > df.iloc[index]['MA_volume_' + str(vlr)]

def is_volume_less_than_mean(df, vlr=21, index=-1):
    return df.iloc[index]['volume'] < df.iloc[index]['MA_volume_' + str(vlr)]

def is_volume_greather_than_mean_or_equal(df, vlr=21, index=-1):
    return df.iloc[index]['volume'] >= df.iloc[index]['MA_volume_' + str(vlr)]

def is_volume_less_than_mean_or_equal(df, vlr=21, index=-1):
    return df.iloc[index]['volume'] <= df.iloc[index]['MA_volume_' + str(vlr)]

def is_stochastic_down(df, low=20, period=14, index=-1):
    if df.iloc[index]['K_' + str(period)] < low and df.iloc[index]['D_' + str(period)] < low:
        return True
    return False

def is_stochastic_up(df, high=80, period=14, index=-1):
    if df.iloc[index]['K_' + str(period)] > high and df.iloc[index]['D_' + str(period)] > high:
        return True
    return False

def is_ma_down(df, mavalue=21, attr='close', index=-1):
    ma='MA_' + attr + '_' + str(mavalue)
    if df.iloc[index][ma] > df.iloc[index][attr]:
        return True
    return False

def is_ma_up(df, mavalue=21, attr='close', index=-1):
    ma='MA_' + attr + '_' + str(mavalue)
    if df.iloc[index][ma] < df.iloc[index][attr]:
        return True
    return False

def is_ema_down(df, mavalue=21, attr='close', index=-1):
    ma='EMA_' + attr + '_' + str(mavalue)
    if df.iloc[index][ma] > df.iloc[index][attr]:
        return True
    return False

def is_ema_up(df, mavalue=21, attr='close', index=-1):
    ma='EMA_' + attr + '_' + str(mavalue)
    if df.iloc[index][ma] < df.iloc[index][attr]:
        return True
    return False

def is_price_up_chance_diverg(df, dfh, index=-1):
    if dfh.iloc[index]['change24p'] < 0 and df.iloc[index]['change7p'] > 0 and df.iloc[index]['change30p'] > 0:
        return True
    return False

def is_price_down_chance_diverg(df, dfh, index=-1):
    if dfh.iloc[index]['change24p'] > 0 and df.iloc[index]['change7p'] < 0 and df.iloc[index]['change30p'] < 0:
        return True
    return False

def is_bband_overprice(df, value=20, attr='close', index=-1):
    return df.iloc[index][attr] >= df.iloc[index]['UPPER_BAND_' + attr + '_' + str(value)]

def is_bband_underprice(df, value=20, attr='close', index=-1):
    return df.iloc[index][attr] <= df.iloc[index]['LOWER_BAND_' + attr + '_' + str(value)]

def is_overprice_close_in_band(df, value=20, attr='close', index=-1):
    exp = df.iloc[-2]['close'] > df.iloc[index-1]['UPPER_BAND_' + attr + '_' + str(value)]
    exp2 = df.iloc[-1]['close'] <= df.iloc[index]['UPPER_BAND_' + attr + '_' + str(value)]
    return exp and exp2

def is_underprice_close_in_band(df, value=20, attr='close', index=-1):
    exp = df.iloc[index-1]['close'] > df.iloc[index-1]['UPPER_BAND_' + attr + '_' + str(value)]
    exp2 = df.iloc[index]['close'] <= df.iloc[index]['UPPER_BAND_' + attr + '_' + str(value)]
    return exp and exp2

def is_cross_ma_up(df, ma_l=9, ma_h=21, index=-1):
    position_cross = 'PositionCrossMA_' + ma_l + '_' + ma_h
    if df.iloc[index][position_cross] == 1:
        return True
    return False

def is_cross_ma_dow(df, size=1, ma_l=9, ma_h=21, index=-1):
    position_cross = 'PositionCrossMA_' + ma_l + '_' + ma_h
    if df.iloc[index][position_cross] == -1:
        return True
    return False

def is_cross_ma_up_near(df, ma_l=9, ma_h=21, index=-1, nearv=3):
    for i in range(0, nearv):
        if is_cross_ma_up(df, ma_l, ma_h, index - i):
            return True
    return False

def is_cross_ma_dow_near(df, ma_l=9, ma_h=21, index=-1, nearv=3):
    for i in range(0, nearv):
        if is_cross_ma_dow(df, ma_l, ma_h, index - i):
            return True
    return False
