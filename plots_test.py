import plotly.graph_objs as go
from plotly.offline import plot
from plotly.subplots import make_subplots
import binanceprovider
import matplotlib.pyplot as plt
import rules.rules as rules
import algorithms
import numpy as np
import strategies.strategies as strategies
import rules.linetrend as linetrend
import indicators
import datetime 
from strategies.LinregReversion2 import LinregReversion2

def plot_ah(df):
    fig = go.Figure(data=[go.Candlestick(x=df['date'],
                                     open=df['open'],
                                     close=df['close'])])
    fig.update_layout(xaxis_rangeslider_visible=False)
    plot(fig, filename='go_candle1.html')

def plot_clandlestics_ma_21_100(df):
    fig = go.Figure(data=[go.Candlestick(x=df['date'],
                                     open=df['open'], 
                                     high=df['high'],
                                     low=df['low'],
                                     close=df['close']), 
                      go.Scatter(x=df['date'], y=df['MA_close_21'], line=dict(color='orange', width=2)),
                      go.Scatter(x=df['date'], y=df['MA_close_100'], line=dict(color='green', width=2))])
    fig.update_layout(xaxis_rangeslider_visible=False)
    plot(fig, filename='go_candle1.html')
    
def plot_clandlestics_hma(df):
    fig = go.Figure(data=[go.Candlestick(x=df['date'],
                                     open=df['open'], 
                                     high=df['high'],
                                     low=df['low'],
                                     close=df['close']), 
                      go.Scatter(x=df['date'], y=df['HMA_close_55'], line=dict(color='orange', width=2))])
    fig.update_layout(xaxis_rangeslider_visible=False)
    plot(fig, filename='go_candle1.html')

def plot_clandlestics_bbands_20(df):
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df['id'],
                                     open=df['open'],
                                     high=df['high'],
                                     low=df['low'],
                                     close=df['close']))
    fig.add_trace(go.Scatter(x=df['id'], y=df['UPPER_BAND_close_20'], line=dict(color='green', width=2)))
    fig.add_trace(go.Scatter(x=df['id'], y=df['MA_close_20'], line=dict(color='orange', width=2)))
    fig.add_trace(go.Scatter(x=df['id'], y=df['LOWER_BAND_close_20'], line=dict(color='red', width=2)))
    fig.update_layout(xaxis_rangeslider_visible=False)
    plot(fig, filename='go_candle1.html')

def plot_clandlestics_trend(df):
    #x = strategies.cross_ema_lin_reg_reversion_stocastic_rsi_invert_bear(df)
    #print(x)
    fig = go.Figure(data=[go.Candlestick(x=df['id'],
                                     open=df['open'],
                                     high=df['high'],
                                     low=df['low'],
                                     close=df['close']),
                    go.Scatter(x=df['id'], y=df['UPTREND'], line=dict(color='green', width=2)),
                    go.Scatter(x=df['id'], y=df['DOWNTREND'], line=dict(color='red', width=2))])
    fig.update_layout(xaxis_rangeslider_visible=False)
    plot(fig, filename='go_candle1.html')

def plot_clandlestics_linear_reg(df):
    fig = go.Figure(data=[go.Candlestick(x=df['id'],
                                     open=df['open'],
                                     high=df['high'],
                                     low=df['low'],
                                     close=df['close']),
                    go.Scatter(x=df['id'], y=df['LNC_ABOVE_100_close_2'], line=dict(color='green', width=2)),
                    go.Scatter(x=df['id'], y=df['LNC_MIDDLE_100_close_2'], line=dict(color='orange', width=2)),
                    go.Scatter(x=df['id'], y=df['LNC_BELLOW_100_close_2'], line=dict(color='red', width=2))])
    fig.update_layout(xaxis_rangeslider_visible=False)
    plot(fig, filename='go_candle1.html')

def plot_clandlestics_hma(df):
    fig = go.Figure(data=[go.Candlestick(x=df['id'],
                                     open=df['open'],
                                     high=df['high'],
                                     low=df['low'],
                                     close=df['close']),
                    go.Scatter(x=df['id'], y=df['HMA_close_55'], line=dict(color='green', width=2))])
    fig.update_layout(xaxis_rangeslider_visible=False)
    plot(fig, filename='go_candle1.html')

def plot_clandlestics_supertrend(df):
    strategies.rsi2_20_80_hma10_bull(df)
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df['id'],
                                     open=df['open'],
                                     high=df['high'],
                                     low=df['low'],
                                     close=df['close']))

    fig.add_trace(go.Scatter(x=df['id'], y=df['Supertrend_FinalUpperband'], line=dict(color='green', width=2)))
    fig.add_trace(go.Scatter(x=df['id'], y=df['Supertrend_FinalLowerband'], line=dict(color='red', width=2)))

    fig.update_layout(xaxis_rangeslider_visible=False)
    plot(fig, filename='go_candle1.html')
    
    
def plot_pvp(df):
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df['id'],
                                     open=df['open'],
                                     high=df['high'],
                                     low=df['low'],
                                     close=df['close'], markevery=df['S3']))

    #fig.add_scatter(go.Scatter(x=df['id'], y=df['S3']), cliponaxis=False)
    fig.update_layout(xaxis_rangeslider_visible=False)
    plot(fig, filename='go_candle1.html')


df = binanceprovider.get_candles_15min('C98USDT')
lng = LinregReversion2()
lng.bear(df)
plot_clandlestics_linear_reg(df)
