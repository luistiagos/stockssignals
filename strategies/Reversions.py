from rules import rules
from rules import linetrend
from rules import linreg
from utils import utils
from rules import linreg

class Reversions:
    def __init__(self, size=5):
        self.size = size
        self.stoploss = None
        self.stopgain = None
        self.trend = None
        self.startprice = None
        self.df_trade = None

    def setDf(self, df):
        self.df = df

    def bull(self, df, index=-1):
        if linreg.lin_reg_reversion_bull(df, index=index, size=self.size):
            #if rules.rsi_invert_up(df, index=index, size=self.size):
            if rules.hma_invert_up(df, index=index, size=self.size):
                return True
        return False

    def bear(self, df, index=-1):
        if linreg.lin_reg_reversion_bear(df, index=index, size=self.size):
            #if rules.rsi_invert_down(df, index=index, size=self.size):
            if rules.hma_invert_down(df, index=index, size=self.size):
                return True
        return False

    def buy(self, index=-1):
        if self.bull(self.df):
            self.trend = True
            self.df_trade = self.df.iloc[index]
            self.startprice = self.df.iloc[index]['close']
            self.stoploss = self.df.iloc[index]['LNC_BELLOW']
            self.stopgain = rules.is_hma_down(self.df, index=index) #self.df.iloc[index]['LNC_MIDDLE'] #self.stoploss + (self.startprice - self.stoploss) * 1.5
            return True
        return False

    def sell(self, index=-1):
        if self.bear(self.df):
            self.trend = False
            self.df_trade = self.df.iloc[index]
            self.startprice = self.df.iloc[index]['close']
            self.stoploss = self.df.iloc[index]['LNC_ABOVE']
            self.stopgain = rules.is_hma_up(self.df, index=index) #self.df.iloc[index]['LNC_MIDDLE'] #self.startprice - (self.stoploss - self.startprice) * 1.5
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