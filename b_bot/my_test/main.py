#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 19:28:03 2020

@author: akimlavrinenko
"""

from binance.client import Client
from pandas import DataFrame as df
from datetime import datetime
from binance.enums import *

import keys

def binance_price(coin):
    client = Client(keys.api_key, keys.api_secret)
    
    candels = client.get_klines(symbol = coin , interval = Client.KLINE_INTERVAL_1HOUR)
    
    candels_dataframe = df(candels)
    
    candels_dataframe_time = candels_dataframe[0]
    
    final_time = []
    
    for time in candels_dataframe_time.unique():
        readable = datetime.fromtimestamp(int(time/1000))
        final_time.append(readable)
        
    candels_dataframe.pop(0)
    candels_dataframe.pop(11)
    
    dataframe_time_final = df(final_time)
    dataframe_time_final.columns = ['date']
    
    dataframe_final = candels_dataframe.join(dataframe_time_final)
    
    dataframe_final.set_index('date', inplace = True)
    
    dataframe_final.columns = ['open', 'high', 'low', 'close', 'volume', 'close_time', 'asset_volume', 'trade_number', 'taker_buy_base', 'taker_buy_quote']
    
    return(dataframe_final)


class F():
    order = Client.create_order(
    symbol='BNBBTC',
    side=SIDE_BUY,
    type=ORDER_TYPE_LIMIT,
    timeInForce=TIME_IN_FORCE_GTC,
    quantity=0.01,
    price='0.00000000001')






