from abc import abstractmethod
from audioop import mul
from utils import utils

class Strategy:
    def __init__(self, size=1, multiplystopgain=2):
        self.size = size
        self.stoploss = None
        self.stopgain = None
        self.trend = None
        self.startprice = None
        self.startdate = None
        self.starttime = None
        self.df_trade = None
        self.multiplystopgain = multiplystopgain
        self.conditionals = []

    def addConditional(self, cond):
        self.conditionals.append(cond)

    def checkConditionals(self):
        if len(self.conditionals) == 0:
            return False
        retr = all(self.conditionals)
        self.conditionals = []
        return retr

    def setDf(self, df):
        self.df = df

    def getTrend(self):
        return self.trend
    
    def setTrend(self, trend):
        self.trend = trend

    def getDfTrade(self):
        return self.df_trade

    @abstractmethod
    def getName(self):
        pass

    @abstractmethod
    def bull(self, df, index=-1):
        pass

    @abstractmethod
    def bear(self, df, index=-1):
        pass

    def buyStopLoss(self, index=-1):
        return self.df.iloc[index-1]['low']

    def buyStopGain(self, index=-1):
        return self.df.iloc[index-1]['close'] + (abs(self.df.iloc[index-1]['close'] - self.stoploss) * self.multiplystopgain)

    def sellStopLoss(self, index=-1):
        return self.df.iloc[index-1]['high']

    def sellStopGain(self, index=-1):
        return self.df.iloc[index-1]['close'] - (abs(self.df.iloc[index-1]['close'] - self.stoploss) * self.multiplystopgain)

    def getStartDate(self):
        return self.startdate
    
    def getStartTime(self):
        return self.starttime
    
    def setTradeInfo(self, index):
        self.df_trade = self.df.iloc[index]
        self.startprice = self.df.iloc[index]['close']
        self.startdate = self.df.iloc[index]['date']
        self.starttime = self.df.iloc[index]['time']
        if self.trend:
            self.stoploss = self.buyStopLoss(index)
            self.stopgain = self.buyStopGain(index)
        else:
            self.stoploss = self.sellStopLoss(index)
            self.stopgain = self.sellStopGain(index)

    def buy(self, index=-1):
        if self.bull(self.df, index):
            self.trend = True
            self.setTradeInfo(index)
            return True
        return False

    def sell(self, index=-1):
        if self.bear(self.df, index):
            self.trend = False
            self.setTradeInfo(index)
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

    def getLoss(self):
        return utils.get_change(self.startprice, self.stoploss) * -1

    def getCurrProfitLoss(self, index=-1):
        dist = utils.get_change(self.startprice, self.df.iloc[index]['close'])
        if self.df.iloc[index]['close'] > self.startprice:
            if self.trend:
                return dist
            return dist * -1
        elif self.df.iloc[index]['close'] > self.startprice:
            if self.trend:
                return dist * -1
        return dist

    def hitStopLoss(self, index=-1):
        if self.stoploss != None:
            if self.trend:
                if self.df.iloc[index]['low'] <= self.stoploss:
                    return True
            else:
                if self.df.iloc[index]['high'] >= self.stoploss:
                    return True
        return False

    def hitStopGain(self, index=-1):
        if self.stopgain != None:
            if self.trend:
                return self.df.iloc[index]['close'] > self.startprice and self.df.iloc[index]['high'] >= self.stopgain
            else:
                return self.df.iloc[index]['close'] < self.startprice and self.df.iloc[index]['low'] <= self.stopgain
        return False

    def getSize(self):
        return self.size
    

