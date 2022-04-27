from rules import rules
from rules import linetrend
from rules import linreg
from utils import utils
from rules import linreg
from strategies.Strategy import Strategy

class BollingBandsNoTrend(Strategy):
    def __init__(self, size=1):
        Strategy.__init__(self, size)
        self.adx_length = 20

    def getName(self):
        return 'BollingBandsNoTrend'

    def bull(self, df, index=-1):
        if rules.is_underprice_close_in_band(df, index=index, size=self.size):
            if rules.adx_down(df, index=index, adx_length=self.adx_length):
                return True
        return False


    def bear(self, df, index=-1):
        if rules.is_overprice_close_in_band(df, index=index, size=self.size):
            if rules.adx_down(df, index=index, adx_length=self.adx_length):
                return True
        return False

    def buyStopLoss(self, index):
        return self.df.iloc[index-1]['low']

    def buyStopGain(self, index):
        return self.df.iloc[index]['MA_close_21']

    def sellStopLoss(self, index):
        return self.df.iloc[index-1]['high']

    def sellStopGain(self, index=-1):
        return self.df.iloc[index-1]['MA_close_21']