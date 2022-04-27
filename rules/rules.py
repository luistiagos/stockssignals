import candlestick_patterns as cp
import algorithms


def macd_invert_hist_bull(df, index=-1, size=1, attr='close', fastperiod=12, slowperiod=26, signalperiod=9):
    for i in range(0, size):
        if df.iloc[index-1]['MACDHIST'] < 0 and df.iloc[index]['MACDHIST'] > 0:
            return True
        index = index - 1
    return False

def macd_invert_hist_bear(df, index=-1, size=1, attr='close', fastperiod=12, slowperiod=26, signalperiod=9):
    for i in range(0, size):
        if df.iloc[index-1]['MACDHIST'] > 0 and df.iloc[index]['MACDHIST'] < 0:
            return True
        index = index - 1
    return False

def macd_hist_compare(df, index=-1, indexCompare=-2):
    if abs(df.iloc[index]['MACDHIST']) > abs(df.iloc[indexCompare]['MACDHIST']):
        return 1
    elif abs(df.iloc[index]['MACDHIST']) < abs(df.iloc[indexCompare]['MACDHIST']):
        return -1
    return 0

def stocastic_rsi_invert_up(df, period=14, low=20, index=-1, size=5):
    for i in range(0, size):
        if df.iloc[index-1]['K_' + str(period)] < low and df.iloc[index-1]['D_' + str(period)] < low:
            if df.iloc[index]['K_' + str(period)] > low and df.iloc[index]['D_' + str(period)] > low:
                return True
        index = index - 1
    return False

def stocastic_rsi_invert_down(df, period=14, high=80, index=-1, size=5):
    for i in range(0, size):
        if df.iloc[index-1]['K_' + str(period)] > high and df.iloc[index-1]['D_' + str(period)] > high:
            if df.iloc[index]['K_' + str(period)] < high and df.iloc[index]['D_' + str(period)] < high:
                return True
        index = index - 1
    return False

def rsi_invert_up(df, index=-1, size=1, period=14, value=50):
    for i in range(0,size):
        if is_rsi_up(df, index=index, size=1, period=period, value=value):
            if is_rsi_down(df, index=index-1, size=1, period=period, value=value):
                return True
        index = index - 1
    return False

def rsi_invert_down(df, index=-1, size=1, period=14, value=50):
    for i in range(0,size):
        if is_rsi_down(df, index=index, size=1, period=period, value=value):
            if is_rsi_up(df, index=index-1, size=1, period=period, value=value):
                return True
        index = index - 1
    return False

def compare_ema(df, ema1, ema2, index=-1, attr='close'):
    sema1 = 'EMA_' + attr + '_' + str(ema1)
    sema2 = 'EMA_' + attr + '_' + str(ema2)
    if sema1 not in df or sema2 not in df:
        algorithms.exponential_move_averanges(df, [ema1,ema2], attr)
    return df.iloc[index][sema1] > df.iloc[index-1][sema2]

def ema_compare(df, ema1, ema2, index=-1, attr='close'):
    sema1 = 'EMA_' + attr + '_' + str(ema1)
    sema2 = 'EMA_' + attr + '_' + str(ema2)
    if df.iloc[index][sema2] - df.iloc[index-1][sema1] > 0:
        return 1
    elif df.iloc[index][sema2] - df.iloc[index-1][sema1] < 0:
        return -1
    return 0

def align_emas_up(df, emas=[], index=-1, attr='close'):
    for i in range(1, len(emas)):
        sema1 = 'EMA_' + attr + '_' + emas[i-1]
        sema2 = 'EMA_' + attr + '_' + emas[i]
        if df.iloc[index][sema1] < df.iloc[index][sema2]: 
            return False
    return True

def align_emas_down(df, emas=[], index=-1, attr='close'):
    for i in range(1, len(emas)):
        sema1 = 'EMA_' + attr + '_' + emas[i-1]
        sema2 = 'EMA_' + attr + '_' + emas[i]
        if df.iloc[index][sema1] > df.iloc[index][sema2]:
            return False
    return True

def adx_up(df, period=14, index=-1, adx_length=25):
    adx = 'ADX_' + str(period)
    return df.iloc[index][adx] > adx_length;

def adx_down(df, period=14, index=-1, adx_length=25):
    adx = 'ADX_' + str(period)
    return df.iloc[index][adx] < adx_length;

def heiken_ashi_volume_adx_strategy_up(df, adx_length=25, adx_p=14, index=-1, o='open_ha', c='close_ha', ema1=50, ema2=200, ema_trend=100):
    avd = adx_up(df, adx_p, index-1, adx_length) #df.iloc[index-1]['ADX_14'] > adx_length;
    volume = df.iloc[index-1]['volume'] < df.iloc[index]['volume']
    up = compare_ema(df, ema1, ema2, index=index-1) #df.iloc[index-1]['EMA_close_50'] > df.iloc[index-1]['EMA_close_200'] 
    up2 = red(df, index - 1, o, c) and green(df, index, o, c)
    maup = is_ema_up(df, ema_trend, 'close', index=-1)
    return avd and volume and up and up2 and maup

def heiken_ashi_volume_adx_strategy_down(df, adx_length=25, adx_p=14, index=-1, o='open_ha', c='close_ha', ema1=50, ema2=200, ema_trend=100):
    avd = adx_up(df, adx_p, index-1, adx_length) #df.iloc[index-1]['ADX_14'] > avd_length;
    volume = df.iloc[index-1]['volume'] < df.iloc[index]['volume']
    down = compare_ema(df, ema2, ema1, index=index-1) 
    down2 = bearish(df, index, o, c) and green(df, index - 1, o, c) and red(df, index, o, c)
    madown = is_ema_down(df, ema_trend, 'close', index=-1)
    return avd and volume and down and down2 and madown

def holy_grail_strategy_bull(df, adx_p=14, adx_length=30, index=-1, ema=20, ema_trend=100, size=5):
    sema = 'EMA_close_' + str(ema)
    if green(df) and bullish(df) and adx_up(df, adx_p, index, adx_length) and is_ema_up(df, ema_trend, 'close', index=index):
        for i in range(0,size):
            index = index - 1
            if df.iloc[index]['close'] > df.iloc[index][sema] and df.iloc[index]['low'] <= df.iloc[index][sema]:
                return True
    return False

def holy_grail_strategy_bear(df, adx_p=14, adx_length=30, index=-1, ema=20, ema_trend=100, size=5):
    sema = 'EMA_close_' + str(ema)
    if red(df) and bearish(df) and adx_up(df, adx_p, index, adx_length) and is_ema_down(df, ema_trend, 'close', index=index):
        for i in range(0,size):
            index = index - 1
            if df.iloc[index]['close'] < df.iloc[index][sema] and df.iloc[index]['high'] >= df.iloc[index][sema]:
                return True
    return False

def rsi_macd_stochastic_pro_bullish(df, index=-1, size=4):
    rsi = rsi_invert_down(df, index, size)
    stochrsi = stocastic_rsi_invert_up(df, index=index, size=size)
    macd = macd_invert_hist_bull(df, index-1, size=5)
    return rsi and stochrsi and macd

def rsi_macd_stochastic_pro_bearish(df, index=-1, size=4):
    rsi = rsi_invert_up(df, index, size)
    stochrsi = stocastic_rsi_invert_down(df, index=index, size=size)
    macd = macd_invert_hist_bear(df, index-1, size=5)
    return rsi and stochrsi and macd

def is_rsi_down(df, index=-1, size=1, period=14, value=50):
    rsi = 'RSI_' + str(period)
    if rsi not in df:
        algorithms.rsi(df, [period])
    for i in range(0, size):
        if df.iloc[index][rsi] <= value:
            return True
        index = index - 1
    return False

def is_rsi_up(df, index=-1, size=1, period=14, value=50):
    rsi = 'RSI_' + str(period)
    for i in range(0, size):
        if df.iloc[index][rsi] > value:
            return True
        index = index - 1
    return False

def bullish(df, index=-1, index2=-2, o='open', c='close'):
    return df.iloc[index2][c] < df.iloc[index][c] and df.iloc[index2][o] < df.iloc[index][c]

def bearish(df, index=-1, index2=-2, o='open', c='close'):
    return df.iloc[index2][c] > df.iloc[index][c] and df.iloc[index2][o] > df.iloc[index][c]

def green(df, index=-1, o='open', c='close'):
    return  df.iloc[index][c] > df.iloc[index][o]

def red(df, index=-1, o='open', c='close'):
    return  df.iloc[index][c] < df.iloc[index][o]

def is_bullish_pattern(df, index=-1):
    patterns = cp.patterns_names()
    for p in patterns:
        if p not in df:
            cp.candle_patterns(df)
        if df.iloc[index][p] > 0:
            df.iloc[index]['pattern'] = p
            return True
    return False

def is_bearish_pattern(df, index=-1):
    patterns = cp.patterns_names()
    for p in patterns:
        if p not in df:
            cp.candle_patterns(df)
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

def is_volume_up(df, index=-1):
    return df.iloc[index]['volume'] > df.iloc[index-1]['volume']

def is_volume_down(df, index=-1):
    return df.iloc[index]['volume'] < df.iloc[index-1]['volume']

def is_stochasticrsi_down(df, low=20, period=14, index=-1, size=1):
    for i in range(0, size):
        if df.iloc[index]['K_' + str(period)] < low and df.iloc[index]['D_' + str(period)] < low:
            return True
        index = index - 1
    return False

def is_stochasticrsi_up(df, high=80, period=14, index=-1, size=1):
    for i in range(0, size):
        if df.iloc[index]['K_' + str(period)] > high and df.iloc[index]['D_' + str(period)] > high:
            return True
        index = index - i
    return False

def is_ma_down(df, mavalue=21, maattr='close', attr='close', index=-1):
    ma='MA_' + maattr + '_' + str(mavalue)
    if df.iloc[index][ma] > df.iloc[index][attr]:
        return True
    return False

def is_ma_up(df, mavalue=21, maattr='close', attr='close', index=-1):
    ma='MA_' + maattr + '_' + str(mavalue)
    if df.iloc[index][ma] < df.iloc[index][attr]:
        return True
    return False

def is_ema_down(df, mavalue=21, maattr='close', attr='close', index=-1):
    ma='EMA_' + maattr + '_' + str(mavalue)
    if df.iloc[index][ma] > df.iloc[index][attr]:
        return True
    return False

def is_ema_up(df, mavalue=21, maattr='close', attr='close', index=-1):
    ma='EMA_' + maattr + '_' + str(mavalue)
    if df.iloc[index][ma] < df.iloc[index][attr]:
        return True
    return False

def is_hma_down(df, mavalue=55, maattr='close', attr='close', index=-1):
    ma='HMA_' + maattr + '_' + str(mavalue)
    if df.iloc[index][ma] > df.iloc[index][attr]:
        return True
    return False

def is_hma_up(df, mavalue=55, maattr='close', attr='close', index=-1):
    ma='HMA_' + maattr + '_' + str(mavalue)
    if df.iloc[index][ma] < df.iloc[index][attr]:
        return True
    return False

def hma_invert_up(df, mavalue=55, maattr='close', attr='close', index=-1, size=1):
    if is_hma_up(df, mavalue, maattr, attr, index):
        for i in range(0,size):
            index = index - 1
            if is_hma_down(df, mavalue, maattr, attr, index):
                return True
    return False

def hma_invert_down(df, mavalue=55, maattr='close', attr='close', index=-1, size=1):
    if is_hma_down(df, mavalue, maattr, attr, index):
        for i in range(0,size):
            index = index - 1
            if is_hma_up(df, mavalue, maattr, attr, index):
                return True
    return False

#def is_price_up_chance_diverg(df, dfh, periods, index=-1):
#    change = 'change' + str(periods[0])
#    if change not in df:
#        algorithms.change_pct(df, periods)
#    if change not in dfh:
#        algorithms.change_pct(dfh, periods)
#    if dfh.iloc[index]['change24p'] < 0 and df.iloc[index]['change7p'] > 0 and df.iloc[index]['change30p'] > 0:
#        return True
#    return False

#def is_price_down_chance_diverg(df, dfh, index=-1):
#    if dfh.iloc[index]['change24p'] > 0 and df.iloc[index]['change7p'] < 0 and df.iloc[index]['change30p'] < 0:
#        return True
#    return False

def is_bband_overprice(df, value=20, battr='close', attr='close', index=-1):
    bband = 'UPPER_BAND_' + battr + '_' + str(value)
    return df.iloc[index][attr] >= df.iloc[index][bband]

def is_bband_underprice(df, value=20, battr='close', attr='close', index=-1):
    bband = 'LOWER_BAND_' + battr + '_' + str(value)
    return df.iloc[index][attr] <= df.iloc[index][bband]

def is_overprice_close_in_band(df, value=21, battr='close', attr='close', index=-1, size=5):
    if not is_bband_overprice(df, value=value, battr=battr, attr=attr, index=index):
        for i in range(0,size):
            index = index-1
            if is_bband_overprice(df, value=value, battr=battr, attr=attr, index=index):
                return True
    return False

def is_underprice_close_in_band(df, value=21, battr='close', attr='close', index=-1, size=5):
    if not is_bband_underprice(df, value=value, battr=battr, attr=attr, index=index):
        for i in range(0,size):
            index = index-1
            if is_bband_underprice(df, value=value, battr=battr, attr=attr, index=index):
                return True
    return False

def is_cross_ma_up(df, l=9, h=21,  attr='close', index=-1, size=1):
    position_cross = 'PositionCrossMA_' + attr + '_' + str(l) + '_' + str(h)
    for i in range(0,size):
        if df.iloc[index][position_cross] == 1:
            return True
        index = index-1
    return False

def is_cross_ma_dow(df, l=9, h=21, attr='close', index=-1, size=1):
    position_cross = 'PositionCrossMA_' + attr + '_' + str(l) + '_' + str(h)
    for i in range(0,size):
        if df.iloc[index][position_cross] == -1:
            return True
        index = index-1
    return False

def is_cross_ema_down(df, l=9, h=21, index=-1, size=1, attr='close'):
    position_cross = 'PositionCrossEMA_' + attr + '_' + str(l) + '_' + str(h)
    for i in range(0,size):
        if df.iloc[index][position_cross] == -1:
            return True
        index = index-1
    return False

def is_cross_ema_up(df, l=9, h=21, index=-1, size=1, attr='close'):
    position_cross = 'PositionCrossEMA_' + attr + '_' + str(l) + '_' + str(h)
    for i in range(0,size):
        if df.iloc[index][position_cross] == 1:
            return True
        index = index-1
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

def up_force(df, index=-1):
    return green(df, index=index) and bullish(df,  index=index) and is_volume_up(df, index=index)

def down_force(df, index=-1):
    return red(df, index=index) and bearish(df, index=index) and is_volume_up(df, index=index)

def supertrend_bull(df, index=-1):
    return (df.iloc[index]['Supertrend'] == False)

def supertrend_bear(df, index=-1):
    return (df.iloc[index]['Supertrend'] == True)

def supertrend_invert_bull(df, index, size=1):
    if supertrend_bull(df, index):
        for i in range(0,size):
            index = index - 1
            if supertrend_bear(df, index):
                return True
    return False

def supertrend_invert_bear(df, index, size=1):
    if supertrend_bear(df, index):
        for i in range(0,size):
            index = index - 1
            if supertrend_bull(df, index):
                return True
    return False

#def supertrend(df, bbandvalue=20, index=-1):
#    for i in range(0, len(df)):
#        if is_bband_overprice(df, value=bbandvalue, index=index):
#             return 1
#        elif is_bband_underprice(df, value=bbandvalue, index=index):
#                return -1
#        index = index - 1
#    return 0
