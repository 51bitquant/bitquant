"""
    Base Strategy for CTA.

    微信：bitquant51
    火币交易所推荐码：asd43
    币安推荐码: 22795115
    币安推荐链接：https://www.binance.co/?ref=22795115
    Gateio交易所荐码：1100714
    Bitmex交易所推荐码：SzZBil 或者 https://www.bitmex.com/register/SzZBil

    代码地址： https://github.com/ramoslin02/51bitqunt
    视频更新：首先在Youtube上更新，搜索51bitquant 关注我
    B站视频：https://space.bilibili.com/401686908
"""
import numpy as np
import pandas as pd
from .data import BarData

__author__ = '51bitquant'  # 作者.
__wxchat__ = 'bitquant51'   # 微信.



class BaseStrategy(object):

    broker = None  # 经纪人..
    data = None

    def __init__(self, data: pd.DataFrame):
        super(BaseStrategy, self).__init__()
        self.data = data

    def on_start(self):
        """
        策略开始运行.
        :return:
        """

    def on_stop(self):
        """
        策略运行结束.
        :return:
        """

    def next_bar(self, bar: BarData):
        raise NotImplementedError("请在子类中实现该方法..")


    def buy(self, price, volume):
        """
        期货中做多，或者现货买
        :param price: 价格
        :param volume: 数量
        :return:
        """
        self.broker.buy(price, volume)


    def sell(self, price, volume):
        """
        期货合约平多，现货中的卖
        :param price: 价格
        :param volume: 数量
        :return:
        """
        self.broker.sell(price, volume)


    def short(self, price, volume):
        """
        期货做空，
        :param price: 价格
        :param volume: 数量
        :return:
        """

        self.broker.short(price, volume)


    def cover(self, price, volume):
        """
        做空平仓,
        :param price: 价格
        :param volume: 数量
        :return:
        """

        self.cover(price, volume)

