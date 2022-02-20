import repository
import binanceprovider
import rules
from datetime import datetime

def avaliable(coin):
    #df = binanceprovider.get_candles_day(coin)
    return True #len(df) > 0 and rules.is_bullish_pattern(df)

def analysis(coins):
    filtered_coins = set()
    for coin in coins:
        if avaliable(coin):
            filtered_coins.add(coin)
    if len(filtered_coins) > 0:
        repository.store_analysis(filtered_coins, 'daycoins.csv')


def run():
    coins = repository.load_coins('bcoins.csv')
    time = datetime.now()
    analysis(coins)
    print(datetime.now() - time)