"""
  微信：bitquant51
  火币交易所推荐码：asd43
  币安推荐码: 22795115
  币安推荐链接：https://www.binance.co/?ref=22795115
  Gateio交易所荐码：1100714
  Bitmex交易所推荐码：SzZBil 或者 https://www.bitmex.com/register/SzZBil

  代码地址： https://github.com/ramoslin02/51bitqunt
  视频更新：首先在Youtube上更新，搜索51bitquant 关注我
  B站视频更新：https://space.bilibili.com/401686908

"""

__author__ = "51bitquant"  # 作者.
__weixin__ = "bitquant51"  # 微信.


from backtest.backtester import Broker, BaseStrategy, BarData, ArrayManager
import pandas as pd


class DemoStrategy(BaseStrategy):

    params = {'long_period': 110, 'short_period': 70}  #

    def __init__(self, data):
        super(DemoStrategy, self).__init__(data)
        self.am = ArrayManager(size=1000)   # 计算产生的信号..

    def on_start(self):
        print("策略开始运行..")

    def on_stop(self):
        print("策略停止运行..")

    def next_bar(self, bar: BarData):
        """
        这里是核心，整个策略都在这里实现..
        :param bar:
        :return:
        """
        print(bar)
        self.am.update_bar(bar)
        if not self.am.inited:
            return

        # 计算技术指标.. 产生交易新号..
        # 或者合成不同周期的K线数据等.
        # 第一个数[-1] ---> [-2]

        if True:
            self.buy(bar.close_price, 1)
        else:
            self.sell(bar.close_price, 1)


if __name__ == '__main__':


    df = pd.read_csv('bitmex_btc_usd_1min_data.csv')
    df = df[df['open_time'] >= '2019-01-01']
    df = df[df['open_time'] <= '2019-02-01']

    df.reset_index(inplace=True, drop=True)
    # print(df)

    broker = Broker()
    broker.set_strategy(DemoStrategy)
    broker.set_leverage(1.0)
    broker.set_cash(1_000_000)  # 100万初始资金.
    broker.set_backtest_data(df)  # 数据.
    broker.run()

    # 参数优化， 穷举法， 遗传算法。
    # broker.optimize_strategy(long_period=[i for i in range(100, 300, 10)], short_period=[i for i in range(50, 100, 5)])






