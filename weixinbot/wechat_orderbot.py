"""
  微信：bitquant51
  火币交易所推荐码：asd43
  币安推荐码: 22795115
  币安推荐链接：https://www.binance.co/?ref=22795115
  Gateio交易所荐码：1100714
  Bitmex交易所推荐码：SzZBil 或者 https://www.bitmex.com/register/SzZBil

  代码地址： https://github.com/ramoslin02/51bitqunt
  视频更新：首先在Youtube上更新，搜索51bitquant 关注我

  1. B站 51bitquant
  2. 优酷: 51bitquant
  3. 百家号: 51bitquant

"""

__author__ = '51bitquant'

# 微信交易所机器人, 实现下单， 插叙账户功能.
from wxpy import *
import ccxt

binance = ccxt.binance({'apiKey':'jXD7h5RoGa7VjZP5mWhsNAO4Fg7J6mkveG4a8MP8QsuzMg8JqIwksB6066RJcRYm',
                        'secret': 'kwg6EjlbtBzlKdZ97byEA4sc8EMsssxtLD7luibl5BbEZtfSXR2YNbCG7Pxd0v4G'
                        })

bot = Bot(cache_path=True, console_qr=-2)  # Bot() #

# # 查找好友.
bitquant = bot.friends().search('51bitquant')[0]  # 搜索昵称为bitquant51的朋友, 微信为:bitquant51
print(bitquant)


@bot.register([bitquant], msg_types=TEXT)
def receive_message(msg: Message):
    txt = msg.text
    # txt的格式 #ex=binance, price=300.8, 'amount'=1, symbol=BTC/USDT, type=limit#
    # #symbol, price, amount, type, side# 看你对对订单的数据定义.
    print(txt)

    try:
        txt = txt.strip(' ')

        if txt.find("下单") >= 0:
            bitquant.send("#交易所名称如binance/huobipro/okex等,交易对如BTC/USDT,下单价格,下单数量,订单类型如limit/market,买或卖如buy/sell#"
                          )

        if txt.startswith('#') and txt.endswith("#"):
            txt = txt.strip('#')  # 去掉头尾的两个#字符.
            order_fields = txt.split(',')  # 分割键值对.  #binance, BTC/USDT, 10000, 0.01, limit, buy#
            order_datas = []

            for item in order_fields:
                order_datas.append(item.strip(" "))
                # 把空白字符给处理掉， 如下面的输入.
                #binance,  BTC/USDT, 9000, 0.01, limit, buy#

            print(order_datas)
            if len(order_datas) >= 6:
                create_order(order_datas[0], order_datas[1], order_datas[2], order_datas[3], order_datas[4], order_datas[5])
    except Exception as error:
        bitquant.send(error)


    # 还可处理撤单、以及各种逻辑.
    #binance, cancel_id#    #binance,xxxxxxx#

    #binance, 查询账户#

def create_order(exchange, symbol, price, amount, order_type, side):

    try:
        if exchange == 'binance':  # 币安的

            price = float(price)
            amount = float(amount)
            print(f"symbol={symbol}, type={order_type}, price={price} amount={amount}, side={side}")

            order = binance.create_order(symbol=symbol, type=order_type, price=price, amount=amount, side=side)
            # ccxt.huobipro().create_order()
            print(order)
            bitquant.send(order)

        elif exchange == 'huobi':  # 火币的.
            pass  # 自己去实现下.

        else:
            pass

    except Exception as error:
        print(error)
        bitquant.send(error)

embed()  # 进入 Python 命令行、让程序保持运行

# 解答一些问题

# 交易所订单的问题 type,
# 解答一些疑问, 微信登录问题
# 火币的接口
