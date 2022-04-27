from rules import rules
from rules import linetrend
from rules import linreg
from utils import utils
from rules import linreg
from strategies.Strategy import Strategy

class LinregReversion2(Strategy):
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
        return 'LinregReversion2'

    def bull(self, df, index=-1):
        above, middle, bellow = linreg.get_keys(self.period, 'close', 2)
        self.addConditional(df.iloc[index-1]['open'] < df.iloc[index-1][bellow])
        self.addConditional(df.iloc[index]['low'] > df.iloc[index-1][bellow])
        self.addConditional(df.iloc[index]['high'] < df.iloc[index-1][middle])
        return self.checkConditionals()


    def bear(self, df, index=-1):
        above, middle, bellow = linreg.get_keys(self.period, 'close', 2)
        self.addConditional(df.iloc[index-1]['open'] > df.iloc[index-1][above])
        self.addConditional(df.iloc[index]['low'] < df.iloc[index-1][above])
        self.addConditional(df.iloc[index]['low'] > df.iloc[index-1][middle])
        return self.checkConditionals()