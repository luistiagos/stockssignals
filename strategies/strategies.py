import imp
import rules.rules as rules
import rules.linreg as linreg
import rules.linetrend as linetrend
from strategies.Reversions import Reversions
from strategies.HollyGrallMACD import HollyGrall
from strategies.LinregReversion import LinregReversion
from strategies.LinregReversionHL import LinregReversionHL
from strategies.LinregReversion2 import LinregReversion2
from strategies.TripleEMA_MACD import TripleEMA_MACD

#def linear_reg_suport_bull(df):
#    return linreg.lin_reg_hit_down(df) and rules.green(df, o='open_ha', c='close_ha') and rules.bullish(df, o='open_ha', c='close_ha')

#def linear_reg_resist_above_bear(df):
#    return rules.lin_reg_resist_above(df) and rules.red(df, o='open_ha', c='close_ha') and rules.bearish(df, o='open_ha', c='close_ha')

#def linear_reg_resist_middle_bull(df):
#   return rules.lin_reg_resist_middle(df) and rules.green(df, o='open_ha', c='close_ha') and rules.bullish(df, o='open_ha', c='close_ha')

#def linear_reg_support_middle_bear(df):
#    return rules.lin_reg_suport_middle(df) and rules.red(df, o='open_ha', c='close_ha') and rules.bearish(df, o='open_ha', c='close_ha')

def linreg_support(df):
    if rules.bullish(df,-1,'open_ha','close_ha') and rules.bearish(df,-2,'open_ha','close_ha'):
        if rules.green(df, -1, 'open_ha', 'close_ha') and rules.red(df, -2, 'open_ha', 'close_ha'):
            if rules.green(df, -3, 'open_ha', 'close_ha'):
                return linreg.lin_reg_hit_up(df, -2)
    return False

def linreg_resist(df):
    if rules.bearish(df,-1,'open_ha','close_ha') and rules.bullish(df,-2,'open_ha','close_ha'):
        if rules.red(df, -1, 'open_ha', 'close_ha') and rules.green(df, -2, 'open_ha', 'close_ha'):
            if rules.red(df, -3, 'open_ha', 'close_ha'):
                return linreg.lin_reg_hit_down(df, -2)
    return False

def lin_reg_reversion_bull(df):
    linregrev = LinregReversion(isfollowtendency=False, size=3)
    result = linregrev.bull(df, -1)
    if result:
        linregrev.setDf(df)
        linregrev.setTrend(True)
        linregrev.setTradeInfo(-1)
    return (result, linregrev.getStopLoss(), linregrev.getStopGain())

def lin_reg_reversion_bear(df):
    linregrev = LinregReversion(isfollowtendency=False, size=3)
    result = linregrev.bear(df, -1)
    if result:
        linregrev.setDf(df)
        linregrev.setTrend(False)
        linregrev.setTradeInfo(-1)
    return (result, linregrev.getStopLoss(), linregrev.getStopGain())

def lin_reg_reversion_period_50_bull(df):
    linregrev = LinregReversion(size=3, period=50, isfollowtendency=False, stopgainmiddle=False)
    result = linregrev.bull(df, -1)
    if result:
        linregrev.setDf(df)
        linregrev.setTrend(True)
        linregrev.setTradeInfo(-1)
    return (result, linregrev.getStopLoss(), linregrev.getStopGain())

def lin_reg_reversion_period_50_bear(df):
    linregrev = LinregReversion(size=3, period=50, isfollowtendency=False, stopgainmiddle=False)
    result = linregrev.bear(df, -1)
    if result:
        linregrev.setDf(df)
        linregrev.setTrend(False)
        linregrev.setTradeInfo(-1)
    return (result, linregrev.getStopLoss(), linregrev.getStopGain())

def lin_reg_reversion_period_hl_50_bull(df):
    linregrev = LinregReversionHL(size=1, period=10, isfollowtendency=False, stopgainmiddle=False)
    result = linregrev.bull(df, -1)
    if result:
        linregrev.setDf(df)
        linregrev.setTrend(True)
        linregrev.setTradeInfo(-1)
    return (result, linregrev.getStopLoss(), linregrev.getStopGain())

def lin_reg_reversion_period_hl_50_bear(df):
    linregrev = LinregReversionHL(size=1, period=10, isfollowtendency=False, stopgainmiddle=False)
    result = linregrev.bear(df, -1)
    if result:
        linregrev.setDf(df)
        linregrev.setTrend(True)
        linregrev.setTradeInfo(-1)
    return (result, linregrev.getStopLoss(), linregrev.getStopGain())

def lin_reg_reversion2_bear(df):
    linregrev = LinregReversion2()
    result = linregrev.bear(df, -1)
    if result:
        linregrev.setDf(df)
        linregrev.setTrend(True)
        linregrev.setTradeInfo(-1)
    return (result, linregrev.getStopLoss(), linregrev.getStopGain())

def lin_reg_reversion2_bull(df):
    linregrev = LinregReversion2()
    result = linregrev.bull(df, -1)
    if result:
        linregrev.setDf(df)
        linregrev.setTrend(True)
        linregrev.setTradeInfo(-1)
    return (result, linregrev.getStopLoss(), linregrev.getStopGain())



def triple_ema_macd_bull(df):
    tripleema_macd = TripleEMA_MACD()
    return (tripleema_macd.bull(df, -1), tripleema_macd.getStopLoss(), tripleema_macd.getStopGain())

def triple_ema_macd_bear(df):
    tripleema_macd = TripleEMA_MACD()
    return (tripleema_macd.bear(df, -1), tripleema_macd.getStopLoss(), tripleema_macd.getStopGain())

def heiken_ashi_volume_adx_strategy_bull(df):
    return rules.heiken_ashi_volume_adx_strategy_up(df)

def heiken_ashi_volume_adx_strategy_bear(df):
    return rules.heiken_ashi_volume_adx_strategy_down(df)

def heiken_ashi_volume_adx_strategy_resist_middle_bull(df):
    return linreg.lin_reg_up_region(df, attr='close') and heiken_ashi_volume_adx_strategy_bull(df)

def heiken_ashi_volume_adx_strategy_support_middle_bear(df):
    return linreg.lin_reg_down_region(df, attr='close') and heiken_ashi_volume_adx_strategy_bear(df)

def holy_grail_strategy_bull(df):
    holyGrall = HollyGrall()
    return holyGrall.bull(df, -1)

def holy_grail_strategy_bear(df):
    holyGrall = HollyGrall()
    return holyGrall.bear(df, -1)

def macd_invert_bull(df):
    return rules.macd_invert_hist_bull(df)

def macd_invert_bear(df):
    return rules.macd_invert_hist_bear(df)

#def linear_reg_sup_bellow_macd_bull(df):
#    return linear_reg_sup_bellow_bull(df) and macd_invert_bull(df)

#def linear_reg_resist_above_macd_bear(df):
#    return linear_reg_resist_above_bear(df) and macd_invert_bear(df)

def rsi_macd_stochastic_pro_bull(df):
    return rules.rsi_macd_stochastic_pro_bullish(df)

def rsi_macd_stochastic_pro_bear(df):
    return rules.rsi_macd_stochastic_pro_bearish(df)

def highly_profitable_stochastic_RSI_MACD_bull(df):
    return rules.rsi_invert_up(df) and rules.stocastic_rsi_invert_up(df) and rules.macd_invert_hist_bull(df)

def highly_profitable_stochastic_RSI_MACD_bear(df):
    return rules.rsi_invert_down(df) and rules.stocastic_rsi_invert_down(df) and rules.macd_invert_hist_bear(df)

def bbands_invert_bull(df):
    return rules.is_rsi_up(df) and rules.is_ema_up(df, 100) and rules.green(df) and rules.bullish(df) and rules.is_underprice_close_in_band(df, attr='close')

def bbands_invert_bear(df):
    return rules.is_rsi_down(df) and rules.is_ema_down(df, 100) and rules.red(df) and rules.bearish(df) and rules.is_overprice_close_in_band(df, attr='close')

def bbands_stocastic_rsi_invert_bull(df):
    return bbands_invert_bull(df) and rules.stocastic_rsi_invert_up(df, low=5, high=95)

def bbands_stocastic_rsi_invert_bear(df):
    return bbands_invert_bear(df) and rules.stocastic_rsi_invert_down(df, low=5, high=95)

def half_trend_rsi_bull(df):
    return rules.is_rsi_down(df, index=-1, period=2, value=10) and rules.green(df) and rules.bullish(df) and rules.is_ema_up(df, 100, 'close', index=-1)

def half_trend_rsi_bear(df):
    return rules.is_rsi_up(df, index=-2, period=2, value=90) and rules.red(df) and rules.bearish(df) and rules.is_ema_down(df, 100, 'close', index=-1)

def bull_pattern(df):
    return rules.is_bullish_pattern(df)

def bear_pattern(df):
    return rules.is_bearish_pattern(df)

def invert_trend_bear(df):
    return rules.down_force(df) and linetrend.linetrend_reversion_bear(df)

def invert_trend_bull(df):
    return rules.up_force(df) and linetrend.linetrend_reversion_bull(df)

def invert_trend_supertrend_bear(df):
    return rules.supertrend_bear(df) and linetrend.linetrend_reversion_bear(df)

def invert_trend_supertrend_bull(df):
    return rules.supertrend_bull(df) and linetrend.linetrend_reversion_bull(df)

def out_up_linreg_bull(df):
    index = -1
    for i in range(0,5):
        index = index -1
        if linreg.lin_reg_hit_up(df, index, 'open') and linreg.lin_reg_hit_up(df, index, 'close'):
            return True
    return False

def out_up_linreg_bear(df):
    index = -1
    for i in range(0,5):
        index = index -1
        if linreg.lin_reg_hit_down(df, index, 'open') and linreg.lin_reg_hit_down(df, index, 'close'):
            return True
    return False


def invert_trend_stocastic_rsi_volume_bull(df):
    if df.iloc[-1]['volume'] > df.iloc[-2]['volume']:
        if rules.stocastic_rsi_invert_up(df, size=4):
            if invert_trend_bull(df):
                return True
    return False

def invert_trend_stocastic_rsi_volume_bear(df):
    if df.iloc[-1]['volume'] > df.iloc[-2]['volume']:
        if rules.stocastic_rsi_invert_down(df, size=4):
            if invert_trend_bear(df):
                return True
    return False

def cross_ema_bear(df):
    return rules.is_cross_ema_dow(df, size=3)

def cross_ema_bull(df):
    return rules.is_cross_ema_up(df, size=3)

def cross_ema_lin_reg_reversion_stocastic_rsi_invert_bear(df):
    if rules.is_cross_ema_dow(df, size=3) and linreg.lin_reg_reversion_bear(df, size=6):
        if rules.stocastic_rsi_invert_down(df, size=6):
            return True 
    return False

def cross_ema_lin_reg_reversion_stocastic_rsi_invert_bull(df):
    if rules.is_cross_ema_up(df, size=3) and linreg.lin_reg_reversion_bull(df, size=6):
        if rules.stocastic_rsi_invert_up(df, size=6):
            return True 
    return False

def macd_invert_rsi_up_bull(df):
    return rules.is_rsi_up(df) and rules.macd_invert_hist_bull(df, size=1)

def macd_invert_rsi_down_bear(df):
    return rules.is_rsi_down(df) and rules.macd_invert_hist_bear(df, size=1)

def macd_stoch_invert_rsi_up_bull(df):
    if rules.is_rsi_up(df) and rules.macd_invert_hist_bull(df, size=5) and linreg.lin_reg_down_region(df):
        return rules.is_stochasticrsi_down(df,low=80) and rules.stocastic_rsi_invert_up(df, size=5)
    return False

def macd_stoch_invert_rsi_down_bear(df):
    if rules.is_rsi_down(df) and rules.macd_invert_hist_bear(df, size=5) and linreg.lin_reg_up_region(df):
        return rules.is_stochasticrsi_up(df, high=20) and rules.stocastic_rsi_invert_down(df, size=5)
    return False

def macd_stoch_hma_up_bull(df):
    if rules.is_ema_up(df, mavalue=100) and rules.is_rsi_up(df) and rules.macd_invert_hist_bull(df, size=5): #and linreg.lin_reg_down_region(df):
        return rules.is_hma_up(df) and rules.stocastic_rsi_invert_up(df, size=5)
    return False

def macd_stoch_hma_down_bear(df):
    if  rules.is_ema_down(df, mavalue=100) and rules.is_rsi_down(df) and rules.macd_invert_hist_bear(df, size=5): #and linreg.lin_reg_up_region(df):
        return rules.is_hma_down(df) and rules.is_stochasticrsi_up(df, high=20) and rules.stocastic_rsi_invert_down(df, size=5)
    return False

def hma20_55_macd_bull(df):
    if rules.is_ema_up(df, mavalue=100) and rules.is_rsi_up(df) and rules.is_hma_up(df, mavalue=20) and rules.is_hma_up(df, mavalue=55) and rules.macd_invert_hist_bull(df, size=5):
        if supertrend_up(df) > 0:
        #if linreg.lin_reg_down_region(df): #and rules.supertrend(df) == 1: #and rules.stocastic_rsi_invert_up(df, size=10):
            return True
    return False

def hma20_55_macd_bear(df):
    if rules.is_ema_down(df, mavalue=100) and rules.is_rsi_down(df) and rules.is_hma_down(df, mavalue=20) and rules.is_hma_down(df, mavalue=55) and rules.macd_invert_hist_bear(df, size=5):
        if rules.supertrend(df) < 0:#if linreg.lin_reg_up_region(df): #and rules.supertrend(df) == -1: #and rules.stocastic_rsi_invert_down(df, size=10):
            return True
    return False

def supertrend_up(df):
    return rules.supertrend(df, index=-1) > 0

def supertrend_down(df):
    return rules.supertrend(df, index=-1) < 0

def supertrend_rsi_hma_bull(df):
    if rules.green(df, index=-1) and rules.bullish(df, index=-1) and rules.supertrend_bull(df, index=-1):
        if rules.rsi_invert_up(df, index=-1, period=2, value=20, size=2):
            if rules.is_hma_up(df, index=-1, mavalue=10) and rules.is_hma_up(df, index=-1, mavalue=10, attr='low'):
                return True
    return False

def supertrend_rsi_hma_bear(df):
    if rules.red(df, index=-1) and rules.bearish(df, index=-1) and rules.supertrend_bear(df, index=-1):
        if rules.rsi_invert_down(df, index=-1, period=2, value=80, size=2):
            if rules.is_hma_down(df, index=-1, mavalue=10) and rules.is_hma_down(df, index=-1, mavalue=10, attr='high'):
                return True
    return False

def rsi_hma_bull(df):
    if rules.supertrend_bull(df) and rules.green(df, index=-1) and rules.bullish(df, index=-1):
        if rules.green(df, index=-2) and rules.bullish(df, index=-2):
            if rules.rsi_invert_up(df, index=-2, period=2, value=20):
                if rules.is_hma_up(df, index=-1, mavalue=10, attr='open'):
                    return True
    return False

def rsi_hma_bear(df):
    if rules.supertrend_bear(df) and rules.red(df, index=-1) and rules.bearish(df, index=-1):
        if rules.red(df, index=-2) and rules.bearish(df, index=-2):
            if rules.rsi_invert_down(df, index=-2, period=2, value=80):
                if rules.is_hma_down(df, index=-1, mavalue=10, attr='open'):
                    return True
    return False

def rsi2_20_80_hma10_bull(df):
    if rules.green(df, index=-2) and rules.bullish(df, index=-2) and rules.is_hma_up(df, mavalue=10, attr='close_ha', index=-1) and rules.is_hma_up(df, mavalue=10, attr='open_ha', index=-1):
        if rules.is_rsi_down(df, index = -3, period=2, value=20) and rules.is_rsi_down(df, index = -2, period=2, value=20) and rules.is_rsi_up(df, index = -1, period=2, value=20):
            return True
    return False

def rsi2_20_80_hma10_bear(df):
    if rules.green(df, index=-2) and rules.bullish(df, index=-2) and rules.is_hma_down(df, mavalue=10, attr='close_ha', index=-1) and rules.is_hma_down(df, mavalue=10, attr='open_ha', index=-1):
        if rules.is_rsi_up(df, index = -3, period=2, value=80) and rules.is_rsi_up(df, index = -2, period=2, value=80) and rules.is_rsi_down(df, index = -1, period=2, value=80):
            return True
    return False

def supertrend_rsi2_20_80_hma10_regiondown_bull(df):
    if linreg.lin_reg_down_region(df) and rules.rsi_invert_up(df, size=1, period=2, value=20) and rules.supertrend_bull(df):
        if rules.is_hma_up(df, mavalue=10):
            return True
    return False

def supertrend_rsi2_20_80_hma10_regiondown_bear(df):
    if linreg.lin_reg_up_region(df) and rules.rsi_invert_down(df, size=1, period=2, value=80) and rules.supertrend_bear(df):
        if rules.is_hma_down(df, mavalue=10):
            return True
    return False

def linreg_hma_reversion_bull(df, index=-1):
    rev = Reversions()
    return rev.bull(df, index)

def linreg_hma_reversion_bear(df, index=-1):
    rev = Reversions()
    return rev.bear(df, index)

