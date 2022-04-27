import numpy

def max_high(df, size=1, index=-1):
    lst = []
    for i in range(0,size):
        lst.append(df.iloc[index]['high'])
        index = index + 1
    return numpy.max(lst)

def min_low(df, size=1, index=-1):
    lst = []
    for i in range(0,size):
        lst.append(df.iloc[index]['low'])
        index = index - 1
    return numpy.min(lst)

def get_change(current, previous):
    if current == previous:
        return 0
    try:
        return (abs(current - previous) / previous) * 100.0
    except ZeroDivisionError:
        return float('inf')