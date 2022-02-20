from os import name
import talib as ta

def bearish_123(df):
    exp1 = df.iloc[-2]['low'] < df.iloc[-1]['low']
    exp2 = df.iloc[-2]['low'] < df.iloc[-3]['low']
    if exp1 and exp2:
        return 1
    return 0

def bullish_123(df):
    exp1 = df.iloc[-2]['high'] > df.iloc[-1]['high']
    exp2 = df.iloc[-2]['high'] > df.iloc[-3]['high']
    if exp1 and exp2:
        return -1
    return 0

def get_talib_candlestick_patterns():
    candles = []
    with open("talib_candlestick_patterns.txt", 'r') as data_file:
        for line in data_file:
            candles.append(line.split()[0])
    return candles

def patterns_names():
    names = get_talib_candlestick_patterns()
    names.append('BEARISH_123')
    names.append('BULLISH_123')

def candle_patterns(df):
    patterns = get_talib_candlestick_patterns()
    for p in patterns:
        df[p] = getattr(ta, p)(df['open'], df['high'], df['low'], df['close'])

    df['BEARISH_123'] = bearish_123(df)
    df['BULLISH_123'] = bullish_123(df)