import matplotlib.pyplot as plt
import plotly.graph_objs as go
from plotly.offline import plot
from plotly.subplots import make_subplots

def plot_clandlestics(df):

    fig = go.Figure(data=[go.Candlestick(x=df['date'],
                                     open=df['open'], 
                                     high=df['high'],
                                     low=df['low'],
                                     close=df['close']), 
                      go.Scatter(x=df['date'], y=df['MA_close_21'], line=dict(color='orange', width=2)),
                      go.Scatter(x=df['date'], y=df['MA_close_100'], line=dict(color='green', width=2))])

    fig.update_layout(xaxis_rangeslider_visible=False)

    plot(fig, filename='go_candle1.html')

def plot_cross_ma(df):
    plt.figure(figsize=(15,5))
    plt.plot(df['close'], label='Close')
    plt.plot(df['MA9'], label='MA9')
    plt.plot(df['MA21'], label='MA21')
    
    plt.plot(df[df['PositionCrossMA'] == 1].index, 
            df['MA20'][df['PositionCrossMA'] == 1], 
            '^', markersize = 15, color = 'g', label = 'buy')
    
    plt.plot(df[df['PositionCrossMA'] == -1].index, 
            df['MA20'][df['PositionCrossMA'] == -1], 
            'v', markersize = 15, color = 'r', label = 'sell')
    plt.title('Price chart ')
    plt.show()
    return None

def plot_price(df, attr):
    # plot price
    plt.figure(figsize=(15,5))
    plt.plot(df[attr])
    plt.title('Price chart ' + attr)
    plt.show()
    return None

def plot_RSI(df, upper=80, down=20):
    # plot correspondingRSI values and significant levels
    plt.figure(figsize=(15,5))
    plt.title('RSI chart')
    plt.plot(df['RSI'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(down, linestyle='--', alpha=0.5)
    plt.axhline(30, linestyle='--')

    plt.axhline(70, linestyle='--')
    plt.axhline(upper, linestyle='--', alpha=0.5)
    plt.axhline(100, linestyle='--', alpha=0.1)
    plt.show()
    return None

def plot_stoch_RSI(df, upper=80, down=20):
    # plot corresponding Stoch RSI values and significant levels
    plt.figure(figsize=(15,5))
    plt.title('stochRSI chart')
    plt.plot(df['K'])
    plt.plot(df['D'])

    plt.axhline(0, linestyle='--', alpha=0.1)
    plt.axhline(down, linestyle='--', alpha=0.5)
    #plt.axhline(30, linestyle='--')

    #plt.axhline(70, linestyle='--')
    plt.axhline(80, linestyle='--', alpha=0.5)
    plt.axhline(upper, linestyle='--', alpha=0.1)
    plt.show()
    return None

