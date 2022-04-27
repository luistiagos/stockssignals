from rules import rules
from rules import linetrend
from rules import linreg
from utils import utils
from rules import linreg
from strategies.Strategy import Strategy

class TripleEMA_MACD(Strategy):
    def __init__(self, size=1, ema1=8, ema2=14, ema3=50):
        Strategy.__init__(self, 1)
        self.size = size
        self.ema1 = str(ema1)
        self.ema2 = str(ema2)
        self.ema3 = str(ema3)

    def getName(self):
        return 'TripleEMA_MACD_' + self.ema1 + '_' + self.ema2 + '_' + self.ema3

    def bull(self, df, index=-1):
        #self.addConditional(rules.adx_up(df, period=14, index=index, adx_length=30))
        self.addConditional(rules.macd_invert_hist_bull(df, index=index))
        self.addConditional(rules.align_emas_up(df, emas=[self.ema1,self.ema2, self.ema3], index=index, attr='close'))
        self.addConditional(rules.is_ema_up(df, attr='close', mavalue=self.ema1, index=index))
        if self.checkConditionals():
            return True
        return False

    def bear(self, df, index=-1):
        #self.addConditional(rules.adx_up(df, period=14, index=index, adx_length=30))
        self.addConditional(rules.macd_invert_hist_bear(df, index=index))
        self.addConditional(rules.align_emas_down(df, emas=[self.ema1,self.ema2, self.ema3], index=index, attr='close'))
        self.addConditional(rules.is_ema_down(df, attr='close', mavalue=self.ema1, index=index))
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

    def buyStopLoss(self, index=-1):
        return self.df.iloc[index]['low'] - self.df.iloc[index]['ATR'] * 3

    def sellStopLoss(self, index=-1):
        return self.df.iloc[index]['high'] + self.df.iloc[index]['ATR'] * 3
