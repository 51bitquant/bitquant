"""
    1. 技术指标讲解.

    微信：bitquant51
    火币交易所推荐码：asd43
    币安推荐码: 22795115
    币安推荐链接：https://www.binance.co/?ref=22795115
    Gateio交易所荐码：1100714
    Bitmex交易所推荐码：SzZBil 或者 https://www.bitmex.com/register/SzZBil
    代码地址： https://github.com/ramoslin02/51bitqunt
    视频更新：首先在Youtube上更新，搜索51bitquant 关注我

"""

import ccxt
import numpy as np
import pandas as pd
import talib as ta
import time

pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 1000)

binance = ccxt.binance()
bitmex = ccxt.bitmex()


# limit = 500
# since = time.time() * 1000 - limit * 60 * 5 * 1000
# data = bitmex.fetch_ohlcv('BTC/USD', timeframe='5m', since=since, limit=limit)
# df = pd.DataFrame(data, columns={'close_time': 0, 'open': 1, 'high': 2, 'low':3 , 'close':4, 'volume': 5})
# df['close_time'] = pd.to_datetime(df['close_time'], unit='ms') + pd.Timedelta(hours=8)
# print(df)

data = binance.fetch_ohlcv('BTC/USDT', timeframe='15m')
df = pd.DataFrame(data, columns={'open_time': 0, 'open': 1, 'high': 2, 'low':3 , 'close':4, 'volume': 5})
df['open_time'] = pd.to_datetime(df['open_time'], unit='ms') + pd.Timedelta(hours=8)

# df['sma'] = ta.SMA(df['close'], timeperiod=20)
# df['ma'] = ta.MA(df['clsoe'], timeperiod=20, matype=1)
# df['ema'] = ta.EMA(df['clsoe'], timeperiod=20)
#
# # 如何学习Ta-Lib  文档：http://mrjbq7.github.io/ta-lib/
# print(help(ta.SMA))
# print(help(ta.MA))
# print(help(ta.MA_Type))
# ndarray, numpy array， pd.Series
# print(help(ta.BBANDS))
#
# df['upperband'],df['middleband'], df['lowerband'] = ta.BBANDS(df['close'], timeperiod=20, nbdevup=3.0, nbdevdn=3.0, matype=0)
# print(df)
# exit()

# df['sma'] = talib.SMA(df['close'], timeperiod=20)
# df['ma'] = talib.MA(df['close'], timeperiod=20, matype=1)
# df['NATR'] = talib.NATR(df['high'], df['low'],df['clsoe'],timeperiod=14)
# talib.BBANDS()



# 自己计算技术指标
"""
1. 30期CMI = 100*absvalue(close - 30期前close)/(30期最高价-30期最低价）
    AvgCMI = CMI的30期移动平均值
    AVGCMI如果小于20， 我们认为市场处于盘整状态。
    如果大于等于20，我们认为市场处于趋势状态。

"""


print(help(ta.STOCH))  #


def calculate_cmi_indicator(df):  # RSI

    cmi_period = 30
    cmi_ma_period = 10
    roc = df['close'].diff(cmi_period)
    h1 = ta.MAX(df['high'], cmi_period) - ta.MIN(df['low'], cmi_period)
    cmi = abs(roc / h1) * 100
    cmi_ma = ta.MA(cmi, cmi_ma_period)  # rolling.
    return cmi_ma


def rsi(close_prices, length):
    """
    :param df:  计算rsi相对强弱指标.
    :param rsi_length: rsi的长度.
    :return:
    """
    deltas = np.diff(close_prices)
    seed = deltas[:length + 1]
    up = seed[seed >= 0].sum() / length
    down = -seed[seed < 0].sum() / length
    rs = up / down
    rsi = np.zeros_like(close_prices)
    rsi[:length] = 100. - 100. / (1. + rs)

    for i in range(length, len(close_prices)):
        delta = deltas[i - 1]  # cause the diff is 1 shorter
        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up * (length - 1) + upval) / length
        down = (down * (length - 1) + downval) / length

        rs = up / down
        rsi[i] = 100. - 100. / (1. + rs)

    return rsi




def stoch_rsi(df, length, k_smooth, d_smooth):

    """

    STOCHRSI(...)
    STOCHRSI(real[, timeperiod=?, fastk_period=?, fastd_period=?, fastd_matype=?])

    Stochastic Relative Strength Index (Momentum Indicators)

    Inputs:
        real: (any ndarray)
    Parameters:
        timeperiod: 14
        fastk_period: 5
        fastd_period: 3
        fastd_matype: 0
    Outputs:
        fastk
        fastd

None

    :param df:
    :param length:
    :param k_smooth:
    :param d_smooth:
    :return:
    """

    """

    study(title="StochRSI", shorttitle="StochRSI")
    source = close
    lengthRSI = input(14, minval=8), 
    lengthStoch = input(14, minval=5)
    smoothK = input(3,minval=3), 
    smoothD = input(3,minval=3)
    OverSold = input(25), OverBought = input(75)
    rsi1 = rsi(source, lengthRSI)
    k = sma(stoch(rsi1, rsi1, rsi1, lengthStoch), smoothK)
    d = sma(k, smoothD)
    hline(OverSold,color=blue)
    hline(OverBought,color=blue)
    plot(k, color=black,title="k-line")
    plot(d, color=fuchsia,title="d-line",linewidth=1)

    stoch 计算公式. 100 * (close - lowest(low, length)) / (highest(high, length) - lowest(low, length))

    :param df: dataFrame
    :param rsi_length:  计算相对相若指标
    :param stoch_length: 计算stoch长度
    :param k_smooth: 计算k的平滑值
    :param d_smooth: 计算d的平滑值.
    :return:

    """
    df['rsi'] = ta.RSI(df['close'], timeperiod=length)
    df['rsi_H'] = df['rsi_'].rolling(window=length).max()
    df['rsi_L'] = df['rsi_'].rolling(window=length).min()
    # df.apply(lambda x: print(x), axis=1)
    df['k_series'] = df.apply(lambda x: 100 * (x['rsi'] - x['rsi_L']) / (x['rsi_H'] - x['rsi_L']),
                              axis=1)
    # 100 * (df['close'] - df['rsi_L'])/(df['rsi_H'] - df['rsi_L'])

    fastK = ta.SMA(df['k_series'], timeperiod=k_smooth)
    faskd = ta.SMA(fastK, timeperiod=d_smooth)

    del df['k_series']
    del df['rsi_H']
    del df['rsi_L']
    del df['rsi_']

    return (fastK, faskd)






