from rules import rules
from rules import linetrend
from rules import linreg
from utils import utils
from rules import linreg
from strategies.Strategy import Strategy

class LinregReversion(Strategy):
    def __init__(self, size=1, period=100, attr='close', dev=2, devstop=3,
                 stopgainmiddle=True, isfollowtendency=True):
        Strategy.__init__(self, size)
        suffix = str(period) + '_' + attr + '_' + str(dev)
        suffixstop = str(period) + '_' + attr + '_' + str(devstop)
        self.above = 'LNC_ABOVE_' + suffix
        self.middle = 'LNC_MIDDLE_' + suffix
        self.bellow = 'LNC_BELLOW_' + suffix
        self.above_stop = 'LNC_ABOVE_' + suffixstop
        self.bellow_stop = 'LNC_BELLOW_' + suffixstop
        self.stopgainmiddle = stopgainmiddle
        self.isfollowtendency = isfollowtendency
        self.period = period
        
    def getName(self):
        return 'LinregReversion'

    def bull(self, df, index=-1):
        self.addConditional(linreg.lin_reg_reversion_bull(df, period=self.period, index=index-1, size=self.size))
        if self.isfollowtendency:
            self.addConditional(rules.is_ema_up(df, mavalue=100, index=index))
        return self.checkConditionals()


    def bear(self, df, index=-1):
        self.addConditional(linreg.lin_reg_reversion_bear(df, period=self.period, index=index-1, size=self.size))
        if self.isfollowtendency:
            self.addConditional(rules.is_ema_down(df, mavalue=100, index=index))
        return self.checkConditionals()

    def buyStopLoss(self, index):
        return self.df.iloc[index][self.bellow_stop]

    def buyStopGain(self, index):
        stop = self.middle
        if not self.stopgainmiddle:
            stop = self.bellow
        return self.df.iloc[index][stop]

    def sellStopLoss(self, index):
        return self.df.iloc[index][self.above_stop]

    def sellStopGain(self, index):
        stop = self.middle
        if not self.stopgainmiddle:
            stop = self.above
        return self.df.iloc[index][stop]