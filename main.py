import dayanalysis
import houranalysis
import fiveteenminanalysis
import binanceprovider
import repository
import rules.rules as rules
import talib as ta
import provider
import plots

if __name__ == "__main__":
    #coins = binanceprovider.get_all_binance_coins()
    #repository.store_coins('bcoins.csv', coins)
    #df = binanceprovider.get_candles_day('BTCUSDT')
    #plots.plot_clandlestics(df[-100:])
    #df = provider.candle_patterns(df)
    #print(ta.RSI(df["close"].values, [timeperiod=14))
    #dayanalysis.run()
    #houranalysis.run()
    #fiveteenminanalysis.run()