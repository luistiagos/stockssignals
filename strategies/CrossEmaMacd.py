from rules import rules
from rules import linetrend
from rules import linreg
from utils import utils
from rules import linreg
from strategies.Strategy import Strategy

class CrossEmaMacd(Strategy):
    def __init__(self, size=5):
        Strategy.__init__(self, size)
        self.crossmacdbull = None
        self.crossmacdbear = None

    def getName(self):
        return 'CrossEmaMacd'

    def bull(self, df, index):
        if rules.is_cross_ema_up(df, index=index-1, size=1, l=12, h=26):
            if rules.macd_invert_hist_bull(df, index=index-1, size=1):
                if rules.adx_up(df, period=14, index=index-1, adx_length=25):
                    return True
        return False

    def bear(self, df, index=-1):
        if rules.is_cross_ema_down(df, index=index-1, size=1, l=12, h=26):
            if rules.macd_invert_hist_bear(df, index=index-1, size=1):
                if rules.adx_down(df, period=14, index=index-1, adx_length=25):
                    return True
        return False

    def buyStopLoss(self, index):
        return self.df.iloc[index-1]['low']

    def buyStopGain(self, index):
        return self.df.iloc[index-1]['close'] + (abs(self.df.iloc[index-1]['close'] - self.df.iloc[index-1]['low']) * 2)

    def sellStopLoss(self, index):
        return self.df.iloc[index-1]['high']

    def sellStopGain(self, index=-1):
        return self.df.iloc[index-1]['close'] - (abs(self.df.iloc[index-1]['high'] - self.df.iloc[index-1]['close']) * 2)