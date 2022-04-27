from rules import rules
from rules import linetrend
from rules import linreg
from utils import utils
from rules import linreg
from strategies.Strategy import Strategy

class HollyGrall(Strategy):
    def __init__(self, adx_p=14, adx_length=30, size=10, ema=20):
        Strategy.__init__(self, 1)
        self.adx_p = adx_p
        self.adx_length = adx_length
        self.intercept = None
        self.size = size
        self.ema = ema

    def getName(self):
        return 'HollyGrallMACD'
    
    def is_candles_follow_ma(self, df, index=-1, size=5, bull=True):
        for i in range(0, size):
            index = index - 1
            if bull:
                if rules.is_ema_down(df, self.ema, attr='low', index=index):
                    return False
            else:
                if rules.is_ema_up(df, self.ema, attr='high', index=index):
                    return False
        return True

    def getIndexMAIntercept(self, df, index=-1, size=1, bull=True):
        for i in range(0,size):
            index = index-1
            if bull:
                if rules.is_ema_down(df, self.ema, attr='low', index=index) and rules.is_ema_up(df, self.ema, attr='open', index=index) and rules.is_ema_up(df, self.ema, attr='close', index=index):
                    return index
            else:
                if rules.is_ema_up(df, self.ema, attr='high', index=index) and rules.is_ema_down(df, self.ema, attr='open', index=index) and rules.is_ema_down(df, self.ema, attr='close', index=index):
                    return index
        return None
    
    def getHighestTopOrBottonIndex(self, df, index=-1, size=5, bull=True):
        value = None
        hl = None
        if bull:
            value = df.iloc[index-size:index]['high'].max()
            hl = 'high'
        else:
            value = df.iloc[index-size:index]['low'].min()
            hl = 'low'
        return df.index.get_loc(df[df[hl] == value].iloc[-1].name)

    def bull(self, df, index=-1):
        macdhist = rules.macd_hist_compare(self.df, index=index-1, indexCompare=index)
        if macdhist > -1:
            self.intercept = self.getIndexMAIntercept(df, index=index, size=1, bull=True)
            if self.intercept != None:
                if rules.adx_up(df, period=self.adx_p, index=index, adx_length=self.adx_length):
                    if self.is_candles_follow_ma(df, index=self.intercept, size=3, bull=True):
                        highest = self.getHighestTopOrBottonIndex(df, index=self.intercept-1, size=3, bull=True)
                        if df.iloc[index]['high'] > df.iloc[highest]['high']:
                            return True
        return False

    def bear(self, df, index=-1):
        macdhist = rules.macd_hist_compare(self.df, index=index-1, indexCompare=index)
        if macdhist > -1:
            self.intercept = self.getIndexMAIntercept(df, index=index, size=1, bull=False)
            if self.intercept != None:
                if rules.adx_up(df, period=self.adx_p, index=index, adx_length=self.adx_length):
                    if self.is_candles_follow_ma(df, index=self.intercept, size=3, bull=False):
                        lowest = self.getHighestTopOrBottonIndex(df, index=self.intercept-1, size=3, bull=False)
                        if df.iloc[index]['low'] < df.iloc[lowest]['low']:
                            return True
        return False

    def hitStopGain(self, index=-1):
        macdhist = rules.macd_hist_compare(self.df, index=index-1, indexCompare=index)
        if self.trend:
            if self.df.iloc[index]['close'] > self.startprice and macdhist < 0:
                self.stopgain = self.df.iloc[index]['close'] 
                return True
        else:
            if self.df.iloc[index]['close'] < self.startprice and macdhist < 0:
                self.stopgain = self.df.iloc[index]['close']
                return True
        return False

    def buyStopLoss(self, index):
        return self.df.iloc[self.intercept]['EMA_close_30']

    def buyStopGain(self, index):
        return self.stopgain

    def sellStopGain(self, index):
        return self.stopgain

    def sellStopLoss(self, index):
        return self.df.iloc[self.intercept]['EMA_close_30']

    #def hitStopGain(self, index=-1):
    #    if self.trend:
    #        if self.df.iloc[index]['close'] < self.df.iloc[index]['EMA_close_21']:
    #            self.stopgain = self.df.iloc[index]['close']
    #            return True
    #    else:
    #        if self.df.iloc[index]['close'] > self.df.iloc[index]['EMA_close_21']:
    #            self.stopgain = self.df.iloc[index]['close']
    #            return True
    #    return False

    #def buyStopLoss(self, index):
    #    return self.df.iloc[index-1]['low']

    #def buyStopGain(self, index):
    #    return 0

    #def sellStopGain(self, index):
    #    return 0

    #def sellStopLoss(self, index):
    #    return self.df.iloc[index-1]['high']