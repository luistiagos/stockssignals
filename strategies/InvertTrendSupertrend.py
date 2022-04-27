from rules import rules
from rules import linetrend
from utils import utils

class InvertTrendSupertrend:
    def __init__(self, size=1):
        self.size = size
        self.stoploss = None
        self.stopgain = None
        self.trend = None
        self.startprice = None
        self.df_trade = None

    def setDf(self, df):
        self.df = df
    
    def buy(self, index=-1):
        if rules.green(self.df) and rules.bullish(self.df) and rules.supertrend_bull(self.df, index) and linetrend.linetrend_reversion_hl_bull(self.df, index, self.size):
            self.trend = True
            self.df_trade = self.df.iloc[index]
            self.startprice = self.df.iloc[index]['close']
            self.stoploss = utils.min_low(self.df, size=self.size, index=index)
            self.stopgain = self.stoploss + (self.startprice - self.stoploss) * 1.5
            return True
        return False

    def sell(self, index=-1):
        if rules.red(self.df) and rules.bearish(self.df) and rules.supertrend_bear(self.df) and linetrend.linetrend_reversion_hl_bear(self.df, index, self.size):
            self.trend = False
            self.df_trade = self.df.iloc[index]
            self.startprice = self.df.iloc[index]['close']
            self.stoploss = utils.max_high(self.df, size=self.size, index=index)
            self.stopgain = self.startprice - (self.stoploss - self.startprice) * 1.5
            return True
        return False

    def getDfTrade(self):
        return self.df_trade

    def getStopLoss(self):
        return self.stoploss

    def getStopGain(self):
        return utils.get_change(self.startprice, self.stoploss)

    def getProfit(self):
        return utils.get_change(self.startprice, self.stopgain)
    
    def getProfit(self):
        return utils.get_change(self.startprice, self.stopgain)
    
    def getLoss(self):
        return utils.get_change(self.startprice, self.stoploss)

    def hitStopLoss(self, index=-1):
        if self.stoploss != None:
            if self.trend:
                return self.df.iloc[index]['high'] >= self.stoploss
            else:
                return self.df.iloc[index]['low'] <= self.stoploss
        return False

    def hitStopGain(self, index=-1):
        if self.stopgain != None:
            if self.trend:
                return self.df.iloc[index]['high'] >= self.stopgain
            else:
                return self.df.iloc[index]['low'] <= self.stopgain
        return False

    def getSize(self):
        return self.size