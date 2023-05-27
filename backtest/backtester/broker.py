"""
    Broker 经济人，负责处理处理撮合交易订单等功能.

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
import os
import itertools
import numpy as np
import pandas as pd
import collections

from .strategy import BaseStrategy, BarData


class Broker(object):
    def __init__(self):
        super(Broker, self).__init__()

        # 策略实例.
        self.strategy_instance = None

        # 手续费
        self.commission = 2/1000

        # 杠杆的比例, 默认使用杠杆.
        self.leverage = 1.0

        # 滑点率，设置为万5
        self.slipper_rate = 5/10000

        # 购买的资产的估值，作为计算爆仓的时候使用.
        self.asset_value = 0

        # 最低保证金比例, 使用bitfinex 的为例子.
        self.min_margin_rate = 0.15

        # 初始本金.
        self.cash = 1_000_000

        self.strategy_class = None

        # 交易的数据.
        self.trades = []

        # 当前提交的订单.
        self.active_orders = []

        # 回测的数据 dataframe数据
        self.backtest_data = None

        self.pos = 0  # 当前的持仓量..

        # 是否是运行策略优化的方法。
        self.is_optimizing_strategy = False


    def set_strategy(self, strategy_class:BaseStrategy):
        """
        设置要跑的策略类.
        :param strategy_class:
        :return:
        """
        self.strategy_class = strategy_class

    def set_leverage(self, leverage: float):
        """
        设置杠杆率.
        :param leverage:
        :return:
        """
        self.leverage = leverage

    def set_commission(self, commission: float):
        """
        设置手续费.
        :param commission:
        :return:
        """
        self.commission = commission

    def set_backtest_data(self, data: pd.DataFrame):
        self.backtest_data = data

    def set_cash(self, cash):
        self.cash = cash

    def buy(self, price, volume):
        """
        这里生成订单.
        order需要包含的信息， order_id, order_price, volume, order_time.
        :param price:
        :param volume:
        :return:
        """
        print(f"做多下单: {volume}@{price}")

        """
        在这里生成订单， 等待价格到达后成交.
        """

    def sell(self, price, volume):
        print(f"做多平仓下单: {volume}@{price}")  #
        """
        在这里生成订单， 等待价格到达后成交.
        """

    def short(self, price, volume):
        print(f"做空下单: {volume}@{price}")
        """
        在这里生成订单， 等待价格到达后成交.
        """

    def cover(self, price, volume):
        print(f"做空平仓下单: {volume}@{price}")
        """
        在这里生成订单， 等待价格到达后成交.
        """

    def run(self):

        self.trades = []  # 开始策略前，把trades设置为空列表，表示没有任何交易记录.
        self.active_orders = []  #
        self.strategy_instance = self.strategy_class(self.backtest_data)
        self.strategy_instance.broker = self
        self.strategy_instance.on_start()


        for index, candle in self.backtest_data.iterrows():
            bar = BarData(candle['open_time'], candle['open'],
                          candle['high'], candle['low'], candle['close'], candle['volume'])

            self.check_order(bar)  # 检查订单是否成交..
            self.strategy_instance.next_bar(bar)  # 处理数据..

        self.strategy_instance.on_stop()


        # 统计成交的信息.. 夏普率、 盈亏比、胜率、 最大回撤 年化率/最大回撤
        self.calculate()  # usdt.

    def calculate(self):

        # 拿到成交的信息，把成交的记录统计出来.

        for trade in self.trades:
            """
             order_id 
             trade_id
             price,
             volume 
             
             10000 --> 1BTC
             12000 --> 1BTC  -- >  2000
            """
            pass

    def check_order(self, bar):
        """
        根据订单信息， 检查是否满足成交的价格， 然后生成交易的记录.
        :param bar:
        :return:
        """
        """
        在这里比较比较订单的价格与当前价格是否满足成交，如果满足，在这里撮合订单。
        """


    def optimize_strategy(self, **kwargs):
        """
        优化策略， 参数遍历进行..
        :param kwargs:
        :return:
        """
        self.is_optimizing_strategy = True

        optkeys = list(kwargs)
        vals = iterize(kwargs.values())
        optvals = itertools.product(*vals)  #
        optkwargs = map(zip, itertools.repeat(optkeys), optvals)
        optkwargs = map(dict, optkwargs)  # dict value...

        for params in optkwargs:
            print(params)

        # 参数列表, 要优化的参数, 放在这里.

        cash = self.cash
        leverage = self.leverage
        commission = self.commission
        for params in optkwargs:

            self.strategy_class.params = params
            self.set_cash(cash)
            self.set_leverage(leverage)
            self.set_commission(commission)
            self.run()

def iterize(iterable):
    '''Handy function which turns things into things that can be iterated upon
    including iterables
    '''
    niterable = list()
    for elem in iterable:
        if isinstance(elem, str):
            elem = (elem,)
        elif not isinstance(elem, collections.Iterable):
            elem = (elem,)

        niterable.append(elem)

    return niterable