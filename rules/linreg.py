from rules import rules

def get_keys(period, attr, dev):
    suffix = str(period) + '_' + attr + '_' + str(dev)
    above = 'LNC_ABOVE_' + suffix
    middle = 'LNC_MIDDLE_' + suffix
    bellow = 'LNC_BELLOW_' + suffix
    return (above, middle, bellow)

def lin_reg_down_region(df, index=-1, attr='high', period=100, lattr='close', dev=2):
    middle = get_keys(period, lattr, dev)[1]
    return df.iloc[index][attr] <= df.iloc[index][middle]

def lin_reg_hit_down(df, index=-1, attr='low', period=100, lattr='close', dev=2):
    bellow = get_keys(period, lattr, dev)[2]
    return df.iloc[index][attr] < df.iloc[index][bellow]

def lin_reg_hit_up(df, index=-1, attr='high', period=100, lattr='close', dev=2):
    above = get_keys(period, lattr, dev)[0]
    return df.iloc[index][attr] > df.iloc[index][above]

def lin_reg_hit_prev_down(df, index=-1, attr='low', period=100, lattr='close', dev=2):
    bellow = get_keys(period, lattr, dev)[2]
    return df.iloc[index][attr] < df.iloc[index-1][bellow]

def lin_reg_hit_prev_up(df, index=-1, attr='high', period=100, lattr='close', dev=2):
    above = get_keys(period, lattr, dev)[0]
    return df.iloc[index][attr] > df.iloc[index-1][above]

def lin_reg_up_region(df, index=-1, attr='low', period=100, lattr='close', dev=2):
    middle = get_keys(period, lattr, dev)[1]
    return df.iloc[index][attr] >= df.iloc[index][middle]

def lin_reg_reversion_bull(df, index=-1, size=5, period=100, linregattr='close', dev=2):
    above, middle, bellow = get_keys(period, linregattr, dev)
    if df.iloc[index]['low'] >= df.iloc[index][bellow]:
        if df.iloc[index]['high'] <= df.iloc[index][middle]:
            for i in range(0,size):
                index = index - 1
                if df.iloc[index]['high'] <= df.iloc[index][bellow]:
                    return True
    return False

def lin_reg_reversion_2deviations_bull(df, index=-1, size=5, period=100, linregattr='close', lattr='low', dev=2, dev2=3):
    above, middle, bellow = get_keys(period, linregattr, dev)
    above2, middle2, bellow2 = get_keys(period, linregattr, dev2)
    if df.iloc[index][lattr] >= df.iloc[index][bellow]:
        if df.iloc[index]['high'] <= df.iloc[index][middle]:
            for i in range(0,size):
                index = index - 1
                if df.iloc[index][lattr] <= df.iloc[index][bellow2] and df.iloc[index]['high'] < df.iloc[index][middle]:
                    return True
    return False

def lin_reg_reversion_2deviations_bear(df, index=-1, size=5, period=100, linregattr='close', lattr='high', dev=2, dev2=3):
    above, middle, bellow = get_keys(period, linregattr, dev)
    above2, middle2, bellow2 = get_keys(period, linregattr, dev2)
    if df.iloc[index][lattr] <= df.iloc[index][above]:
        if df.iloc[index]['low'] >= df.iloc[index][middle]:
            for i in range(0,size):
                index = index - 1
                if df.iloc[index][lattr] >= df.iloc[index][above2] and df.iloc[index]['low'] > df.iloc[index][middle]:
                    return True
    return False

def lin_reg_reversion_bear(df, index=-1, size=5, period=100, linregattr='close', dev=2):
    above, middle, bellow = get_keys(period, linregattr, dev)
    if df.iloc[index]['high'] <= df.iloc[index][above]:
        if df.iloc[index]['low'] >= df.iloc[index][middle]:
            for i in range(0,size):
                index = index - 1
                if df.iloc[index]['low'] >= df.iloc[index][above]:
                    return True
    return False

def lin_reg_reversion_hl_bull(df, index=-1, size=5, period=100, lattr='close', dev=2):
    above, middle, bellow = get_keys(period, lattr, dev)
    if df.iloc[index]['low'] >= df.iloc[index][bellow]:
        if df.iloc[index]['high'] <= df.iloc[index][middle]:
            for i in range(0,size):
                index = index - 1
                if df.iloc[index]['low'] <= df.iloc[index][bellow]:
                    return True
    return False

def lin_reg_reversion_hl_bear(df, index=-1, size=5, period=100, lattr='close', dev=2):
    above, middle, bellow = get_keys(period, lattr, dev)
    if df.iloc[index]['high'] < df.iloc[index][above]:
        if df.iloc[index]['low'] > df.iloc[index][middle]:
            for i in range(0,size):
                index = index - 1
                if df.iloc[index]['high'] >= df.iloc[index][above]:
                    return True
    return False