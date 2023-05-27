
#-*-coding:gb2312
#coding=utf-8

import ccxt
import time

def readInstrument(csv_name='account.txt'):
    Instrument=[]
    myfile = open(csv_name, 'r')
    line = myfile.readline()
    while line:
        list = line.split(';')
        if len(list)>1:
            Instrument.append(list[0])
        line = myfile.readline()
    myfile.close()
    return Instrument

if __name__ == '__main__':
    KeyList= readInstrument('account.txt')

    print(KeyList)


    # huobipro = ccxt.huobipro({
    #             'urls': {
    #             'logo': 'https://user-images.githubusercontent.com/1294454/27766569-15aa7b9a-5edd-11e7-9e7f-44791f4ee49c.jpg',
    #             'api': {
    #                 'market': 'https://api.huobi.br.com',
    #                 'public': 'https://api.huobi.br.com',
    #                 'private': 'https://api.huobi.br.com',
    #                 'zendesk': 'https://huobiglobal.zendesk.com/hc/en-us/articles',
    #             },
    #             'www': 'https://www.huobi.pro',
    #             'referral': 'https://www.huobi.br.com/en-us/topic/invited/?invite_code=rwrd3',
    #             'doc': 'https://github.com/huobiapi/API_Docs/wiki/REST_api_reference',
    #             'fees': 'https://www.huobi.pro/about/fee/',
    #             }
    #         })

    huobipro = ccxt.huobipro({
        'hostname': 'api.huobi.br.com',
        'urls': {
            'logo': 'https://user-images.githubusercontent.com/1294454/27766569-15aa7b9a-5edd-11e7-9e7f-44791f4ee49c.jpg',
            'api': {
                'market': 'https://api.huobi.br.com',
                'public': 'https://api.huobi.br.com',
                'private': 'https://api.huobi.br.com',
                'zendesk': 'https://huobiglobal.zendesk.com/hc/en-us/articles',
            },
            'www': 'https://www.huobi.br.com',
            'referral': 'https://www.huobi.br.com/en-us/topic/invited/?invite_code=rwrd3',
            'doc': 'https://github.com/huobiapi/API_Docs/wiki/REST_api_reference',
            'fees': 'https://www.huobi.pro/about/fee/',
        }
    })

    huobipro.apiKey= 'c3fc24cbc2905f8-671763e8-ht4tgq1e4t'
    huobipro.secret= 'ccc774b1-aa791-ef28f9e5-56661'

    huobipro.load_markets()

    #print(huobipro.calculate_fee('HT/USDT'))
    #下单进行交易
    # ordersend= huobipro.create_order(symbol='HT/USDT',type= 'limit', side='buy', amount= 1, price= 1)
    # #print(ordersend)
    # if 'id' in ordersend:
    #     print(ordersend['id'], ordersend['status'])

    time.sleep(10)
    #cancelorder= huobipro.cancel_order(ordersend['id'])
    #读取所有order相关信息
    fetchorder= huobipro.fetch_orders()

    print(fetchorder)

    # signature invalid

    # for order in fetchorder:
    #     #print(order)
    #     #print(order['id'],order['status'])
    #     if order['status']=='open':
    #        print(huobipro.cancel_order(order['id']))
