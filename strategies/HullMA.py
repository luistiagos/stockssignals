from rules import rules
from rules import linetrend
from rules import linreg
from utils import utils
from rules import linreg
from strategies.Strategy import Strategy

class HullMA(Strategy):
    def __init__(self, size=1, hullema=55):
        Strategy.__init__(self, 1)
        self.size = size
        self.hullema = hullema

    def getName(self):
        return 'HullMA'

    def bull(self, df, index=-1):
        self.addConditional(rules.adx_up(df, period=14, index=index, adx_length=30))
        self.addConditional(rules.macd_invert_hist_bull(df, index=index))
        self.addConditional(rules.is_hma_up(df, attr='low', index=index))
        self.addConditional(rules.is_hma_down(df, attr='open', index=index-1))
        self.addConditional(rules.is_hma_down(df, attr='high', index=index-2))
        if self.checkConditionals():
            return True
        return False

    def bear(self, df, index=-1):
        self.addConditional(rules.adx_up(df, period=14, index=index, adx_length=30))
        self.addConditional(rules.macd_invert_hist_bear(df, index=index))
        self.addConditional(rules.is_hma_down(df, attr='high', index=index))
        self.addConditional(rules.is_hma_up(df, attr='open', index=index-1))
        self.addConditional(rules.is_hma_up(df, attr='low', index=index-2))
        if self.checkConditionals():
            return True
        return False

    def hitStopGain(self, index=-1):
        if self.trend:
            if self.df.iloc[index]['close'] > self.startprice:
                if rules.macd_hist_compare(self.df, index=index-1, indexCompare=index) > 0:
                    return True
        else:
            if self.df.iloc[index]['close'] < self.startprice:
                if rules.macd_hist_compare(self.df, index=index-1, indexCompare=index) > 0:
                    return True
        return False
    
    #def hitStopLoss(self, index=-1):
    #    if self.stoploss != None:
    #        if self.trend:
    #            if rules.macd_hist_compare(self.df, index=index-1, indexCompare=index) > 0:
    #                self.stoploss = self.df.iloc[index]['close']
    #                return True
    #        else:
    #            if rules.macd_hist_compare(self.df, index=index-1, indexCompare=index) > 0:
    #                self.stoploss = self.df.iloc[index]['close']
    #                return True
    #    return False

    #def getStopLoss(self):
    #   return super(HullMA, self).getStopLoss() * 2
    
    def buyStopLoss(self, index=-1):
        return self.df.iloc[index]['low'] - self.df.iloc[index]['ATR'] * 3
    
    def sellStopLoss(self, index=-1):
        return self.df.iloc[index]['high'] + self.df.iloc[index]['ATR'] * 3
    
    #def buyStopGain(self, index=-1):
    #    return self.df.iloc[index]['high'] + self.df.iloc[index]['ATR'] * 2
    
    #def sellStopGain(self, index=-1):
    #    return self.df.iloc[index]['low'] - self.df.iloc[index]['ATR'] * 2
