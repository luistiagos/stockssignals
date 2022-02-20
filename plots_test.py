import plotly.graph_objs as go
from plotly.offline import plot
from plotly.subplots import make_subplots
import binanceprovider

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

def plot_clandlestics_bbands_20(df):
    fig = go.Figure(data=[go.Candlestick(x=df['date'],
                                     open=df['open'], 
                                     high=df['high'],
                                     low=df['low'],
                                     close=df['close']), 
                      go.Scatter(x=df['date'], y=df['UPPER_BAND_close_20'], line=dict(color='green', width=2)),
                      go.Scatter(x=df['date'], y=df['MA_close_20'], line=dict(color='orange', width=2)),
                      go.Scatter(x=df['date'], y=df['LOWER_BAND_close_20'], line=dict(color='red', width=2))])
    fig.update_layout(xaxis_rangeslider_visible=False)
    plot(fig, filename='go_candle1.html')

def plot_clandlestics_linear_reg(df):
    fig = go.Figure(data=[go.Candlestick(x=df['id'],
                                     open=df['open'],
                                     high=df['high'],
                                     low=df['low'],
                                     close=df['close']),

                      go.Scatter(x=df['id'], y=df['UPTREND'], line=dict(color='orange', width=2)),
                      go.Scatter(x=df['id'], y=df['DOWNTREND'], line=dict(color='orange', width=2))])
    fig.update_layout(xaxis_rangeslider_visible=False)
    plot(fig, filename='go_candle1.html')


df = binanceprovider.get_candles_hour('BTCUSDT')
plot_clandlestics_linear_reg(df)