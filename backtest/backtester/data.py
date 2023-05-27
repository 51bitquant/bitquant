"""
    测试用的 barData,

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


class BarData(object):
    """
    K 线数据模型.
    """
    def __init__(self, datetime, open_price, high_price, low_price, close_price, volume):
        self.datetime = datetime
        self.open_price = open_price
        self.high_price = high_price
        self.low_price = low_price
        self.close_price = close_price
        self.volume = volume

    def __str__(self):
        return f"{self.datetime} {self.open_price} {self.high_price} {self.low_price} {self.close_price}"


class TradeData(object):
    pass