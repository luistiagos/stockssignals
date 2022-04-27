from rules import rules
from rules import linetrend
from rules import linreg
from utils import utils
from rules import linreg
from strategies.Strategy import Strategy

class InvertTrend(Strategy):
    def __init__(self, size=1, isfollowtendency=True):
        Strategy.__init__(self, size)
        self.isfollowtendency = isfollowtendency

    def getName(self):
        return 'InvertTrend'

    def bull(self, df, index=-1):
        self.addConditional(linetrend.linetrend_reversion_bull(df, index=index, size=self.size))
        if self.isfollowtendency:
            self.addConditional(rules.is_ema_up(df, mavalue=100, index=index))
        return self.checkConditionals()


    def bear(self, df, index=-1):
        self.addConditional(linetrend.linetrend_reversion_bear(df, index=index, size=self.size))
        if self.isfollowtendency:
            self.addConditional(rules.is_ema_down(df, mavalue=100, index=index))
        return self.checkConditionals()

    def buyStopLoss(self, index):
        return self.df.iloc[index]['DOWNTREND']

    def buyStopGain(self, index):
        return self.df.iloc[index]['UPTREND']

    def sellStopLoss(self, index):
        return self.df.iloc[index]['UPTREND']

    def sellStopGain(self, index):
        return self.df.iloc[index]['DOWNTREND']