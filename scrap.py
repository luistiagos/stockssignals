# -*- coding: utf-8 -*-
from datetime import datetime
import sandbox
import csv
import repository

def check_signal_down(coin):
    df = sandbox.get_coins(coin, '6M', '1d')
    dfh = sandbox.get_coins(coin, '1M', '1h')
    if len(df) > 0 and len(dfh) > 0:
        ismad = True #sandbox.is_ma_down(df)
        isstochup = sandbox.is_stochastic_down(dfh, 5)
        ischgdivdown = True #sandbox.is_price_down_chance_diverg(df, dfh)
        is_last_green = True #sandbox.is_last_candle_great(df)
        return ischgdivdown and ismad and isstochup and is_last_green
    return False 

def check_signal_down2(coin):
    df = sandbox.get_coins(coin, '200d', '1d')
    dfh = sandbox.get_coins(coin, '200h', '1h')
    if len(df) > 0 and len(dfh):
        istriangledown = True #sandbox.is_triangle_down(dfh)
        ismad = True #sandbox.is_ma_down(df)
        ismauh = True #sandbox.is_ma_up(dfh)
        isstochup = True #sandbox.is_stochastic_up(df, 95)
        ischgdivdown = True #sandbox.is_price_down_chance_diverg(df, dfh)
        is_last_green = True #sandbox.is_last_candle_great(df)
        is_over_price = sandbox.is_overprice_close_in_band(dfh)
        return is_over_price and istriangledown and ismad and isstochup and ismauh
    return False

def check_signal_up(coin):
    dfm = sandbox.get_coins(coin, '10d', '15m')
    dfh = sandbox.get_coins(coin, '10d', '1h')
    if len(dfh) > 0 and len(dfm) > 0:
        return sandbox.is_ma_up(dfh) and sandbox.is_ma_up(dfm) and sandbox.is_stochastic_down(dfm) and sandbox.is_cross_ma_up(dfm)
    #(sandbox.is_ma_up(df) and sandbox.is_triangle_up(df, coin))
    return False

def check_cross_up(coin):
    df = sandbox.get_coins(coin, '200d', '1d')
    if len(df):
        return (sandbox.is_ma_up(df, 'MA72') and sandbox.is_cross_ma_up(df, 5))
    return False

def check_signal(coin):
    df = sandbox.get_coins(coin, '100d', '1d')
    dfh = sandbox.get_coins(coin, '100h', '1h')
    if len(df) > 0 and len(dfh):
        return sandbox.is_hammer(df)
    return False 




def analise_coins(coins):
    with open('cryptos.csv', 'a', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        for item in coins:
            if check_signal_up(item):
                arr = [item, 'https://finance.yahoo.com/quote/' + str(item) + '/chart?p=' + str(item)]
                writer.writerow(arr)




coins = repository.load_coins()
time = datetime.now()
analise_coins(coins)
print(datetime.now() - time)

