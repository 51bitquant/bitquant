"""
1. 注册链接: https://www.bybit.com/app/register?ref=yXjOz
推荐码:yXjOz, 目前官方有推荐返佣和奖励，以及各种活动奖励.

2. 官方网址:www.bybit.com, 注册需要科学上网，以后访问不需要.
api文档: https://bybit-exchange.github.io/docs/zh-cn/inverse/#rest-api

3. 微信: 51bitquant, 网易云课程链接: https://study.163.com/course/introduction/1209509824.htm
或者网易云课堂(https://study.163.com)搜索: 51bitquant
4. 代码链接：https://github.com/ramoslin02/51bitqunt

5. 目标: 爬取Bybit交易所的行情数据， 对数据进行处理.


"""

import pandas as pd
import time
import os
import datetime
import ccxt

pd.set_option('expand_frame_repr', False)


def crawl_bybit_datas(symbol, start_time, end_time):
    """
    爬取交易所数据的方法.
    :param symbol: 请求的symbol: like BTC/USDT, ETH/USD等。
    :param start_time: like 2018-1-1
    :param end_time: like 2019-1-1
    :return:
    """
    print(ccxt.__version__)  # 1.18.1213  1.26.50
    # pip install ccxt==1.26.50 通过这个命令来安装最新的版本.
    # exchange_class = getattr(ccxt, 'bybit')  # 获取交易所的名称 ccxt.binance
    # exchange = exchange_class()  # 交易所的类. 类似 ccxt.bitfinex()
    exchange = ccxt.bybit()

    print(exchange)
    # exit()

    current_path = os.getcwd()
    file_dir = os.path.join(current_path, symbol.replace('/', ''))
    print(file_dir)
    if not os.path.exists(file_dir):
        # 如果这个文件路径不存在,则创建这个文件夹，来存放数据.
        os.makedirs(file_dir)

    start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d')
    end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d')

    start_time_stamp = int(time.mktime(start_time.timetuple())) * 1000
    end_time_stamp = int(time.mktime(end_time.timetuple())) * 1000

    limit_count = 200  # bybit 请求的数据有限制，每次只能请求200个.

    while True:
        try:
            print(start_time_stamp)
            data = exchange.fetch_ohlcv(symbol, timeframe='1m', since=start_time_stamp, limit=limit_count)
            df = pd.DataFrame(data)
            df.rename(columns={0: 'open_time', 1: 'open', 2: 'high', 3: 'low', 4: 'close', 5: 'volume'}, inplace=True)

            start_time_stamp = int(df.iloc[-1]['open_time'])  # 获取下一个次请求的时间.
            filename = str(start_time_stamp) + '.csv'
            save_file_path = os.path.join(file_dir, filename)
            print("文件保存路径为：%s" % save_file_path)
            df.set_index('open_time', drop=True, inplace=True)
            df.to_csv(save_file_path)

            if start_time_stamp > end_time_stamp:
                print("完成数据的请求.")
                break

            time.sleep(0.2)  # 1/25

        except Exception as error:
            print(error)
            time.sleep(10)


def sample_datas(symbol):
    """
    :param exchange_name:
    :param symbol:
    :return:
    """
    path = os.path.join(os.getcwd(), symbol.replace('/', ''))
    print(path)
    file_paths = []
    for root, dirs, files in os.walk(path):
        if files:
            for file in files:
                if file.endswith('.csv'):
                    file_paths.append(os.path.join(path, file))

    file_paths = sorted(file_paths)
    all_df = pd.DataFrame()

    for file in file_paths:
        df = pd.read_csv(file)
        all_df = all_df.append(df, ignore_index=True)

    all_df = all_df.sort_values(by='open_time', ascending=True)

    print(all_df)

    return all_df

    # for index, item in all_df.iterrows():
    #     try:
    #         dt = (pd.to_datetime(item['open_time'], unit='ms'))
    #         print(dt)
    #         dt = datetime.datetime.strptime(str(dt), '%Y-%m-%d %H:%M:%S')  # 2018-01-01 17:36:00:42
    #         print(dt)
    #     except:
    #         dt = (pd.to_datetime(item['open_time'], unit='ms'))
    #         print(dt)


def clear_datas(symbol):
    df = sample_datas(symbol)
    # print(df)
    # exit()
    # df['open_time'] = df['open_time'].apply(lambda x: time.mktime(x.timetuple()))
    # # 日期.timetuple() 这个用法 通过它将日期转换成时间元组
    # # print(df)
    # df['open_time'] = df['open_time'].apply(lambda x: (x // 60) * 60 * 1000)
    df['open_time'] = df['open_time'].apply(lambda x: (x // 60) * 60)  # 获取整分的数据.
    print(df)
    df['Datetime'] = pd.to_datetime(df['open_time'], unit='ms') + pd.Timedelta(hours=8)  # 把UTC时间转成北京时间.
    df['Datetime'] = df['Datetime'].apply(lambda x: str(x)[0:19])  # 2018-11-15 00:47:0034, 通过截取字符串长度.
    df.drop_duplicates(subset=['open_time'], inplace=True)
    df.set_index('Datetime', inplace=True)
    print("*" * 20)
    print(df)
    symbol_path = symbol.replace('/', '')
    df.to_csv(f'{symbol_path}_1min_data.csv')


if __name__ == '__main__':
    # crawl_bybit_datas('BTC/USD', '2018-11-15', '2020-4-18')  # ccxt symbol BTC/USDT
    clear_datas('BTC/USD')
