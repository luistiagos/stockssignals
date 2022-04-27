from rules import rules
from rules import linetrend
from utils import utils
from rules import linreg

class Supertrendrsihma:
    def __init__(self, size=1):
        self.size = size
        self.stoploss = None
        self.stopgain = None
        self.trend = None
        self.startprice = None
        self.df_trade = None

    def setDf(self, df):
        self.df = df
    
    def bull(self, df):
        if linreg.lin_reg_down_region(df) and rules.rsi_invert_up(df, size=3, period=2, value=20): #and rules.supertrend_bull(df):
            if rules.is_hma_up(df, mavalue=10):
                return True
        return False

    def bear(self,df):
        if linreg.lin_reg_up_region(df) and rules.rsi_invert_down(df, size=3, period=2, value=80): #and rules.supertrend_bear(df):
            if rules.is_hma_down(df, mavalue=10):
                return True
        return False
    
    def buy(self, index=-1):
        if self.bull(self.df):
            self.trend = True
            self.df_trade = self.df.iloc[index]
            self.startprice = self.df.iloc[index]['close']
            self.stoploss = utils.min_low(self.df, size=self.size, index=index)
            self.stopgain = self.stoploss + (self.startprice - self.stoploss) * 1.5
            return True
        return False

    def sell(self, index=-1):
        if self.bear(self.df):
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