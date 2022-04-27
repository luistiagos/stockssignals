import rules.rules as rules


def is_hit_uptrend(df, attr='high', index=-1, size=1):
    for i in range(0,size):
        if df.iloc[index][attr] >= df.iloc[index]['UPTREND']:
            return True
        index = index - 1
    return False

def is_hit_downtrend(df, attr='low', index=-1, size=1):
    for i in range(0,size):
        if df.iloc[index][attr] <= df.iloc[index]['DOWNTREND']:
            return True
        index = index - 1
    return False

def linetrend_reversion_hl_bull(df, index=-1, size=1):
    if df.iloc[index]['low'] > df.iloc[index]['DOWNTREND']:
        if df.iloc[index]['high'] < df.iloc[index]['UPTREND']:
            for i in range(0,size):
                index = index - 1
                if df.iloc[index]['low'] <= df.iloc[index]['DOWNTREND']:
                    return True
    return False

def linetrend_reversion_hl_bear(df, index=-1, size=1):
    if df.iloc[index]['high'] < df.iloc[index]['UPTREND']:
        if df.iloc[index]['low'] > df.iloc[index]['DOWNTREND']:
            for i in range(0,size):
                index = index - 1
                if df.iloc[index]['high'] >= df.iloc[index]['UPTREND']:
                    return True
    return False

def linetrend_reversion_bull(df, index=-1, size=1):
    if df.iloc[index]['close'] > df.iloc[index]['DOWNTREND']:
        if df.iloc[index]['high'] < df.iloc[index]['UPTREND']:
            for i in range(0,size):
                index = index - 1
                if df.iloc[index]['close'] <= df.iloc[index]['DOWNTREND']:
                    return True
    return False

def linetrend_reversion_bear(df, index=-1, size=1):
    if df.iloc[index]['close'] < df.iloc[index]['UPTREND']:
        if df.iloc[index]['low'] > df.iloc[index]['UPTREND']:
            for i in range(0,size):
                index = index - 1
                if df.iloc[index]['close'] >= df.iloc[index]['UPTREND']:
                    return True
    return False