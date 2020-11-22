#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 17:20:38 2020

@author: akimlavrinenko
"""
from binance.client import Client
import numpy as np
from keys import *  
import statistics as st
import matplotlib.pyplot as plt
import itertools
from binance.enums import *

client = Client(api_key, api_secret)
# client = Client("", "")
acc_info = client.get_account()

balance = acc_info['balances']

for i in balance:
    if float(i['free']) > 0:
        x = 'starting_balance_' + str(i['asset'])
        p = i['free']
        b = {x: p}
        print (x , p)
        starting_balance = b['starting_balance_' + str(i['asset'])]



        # 1499040000000,      0 # Open time
        # "0.01634790",       1 # Open
        # "0.80000000",       2 # High
        # "0.01575800",       3 # Low
        # "0.01577100",       4 # Close
        # "148976.11427815",  5 # Volume
        # 1499644799999,      6 # Close time
        # "2434.19055334",    7 # Quote asset volume
        # 308,                8 # Number of trades
        # "1756.87402397",    9 # Taker buy base asset volume
        # "28.46694368",      10 # Taker buy quote asset volume
        # "17928899.62484339" 11 # Can be ignored

klines_month = client.get_historical_klines("BNBUSDT", Client.KLINE_INTERVAL_1DAY, "24 day ago UTC")   
klines_week = client.get_historical_klines("BNBUSDT", Client.KLINE_INTERVAL_6HOUR, "6 day ago UTC")           
klines_day = client.get_historical_klines("BNBUSDT", Client.KLINE_INTERVAL_1HOUR, "1 day ago UTC")
klines_hour = client.get_historical_klines("BNBUSDT", Client.KLINE_INTERVAL_5MINUTE, "2 hour ago UTC")        
avg_price = client.get_avg_price(symbol='BNBUSDT')
        
# info = client.get_symbol_info('BNBUSDT')
# candles = client.get_klines(symbol='BNBUSDT', interval=Client.KLINE_INTERVAL_1HOUR)

acc_info = client.get_account()
# open_price = []
close_price_month = []
close_price_week = []
close_price_day = []
close_price_hour = []
# high_price = []
# low_price = []
n = sum(1 for line in klines_month)
for i in range(0, n):
    a = klines_month[i]
    b = klines_week[i]
    c = klines_day[i]
    d = klines_hour[i]
    close_p_m = float(a[4])
    close_p_w = float(b[4])
    close_p_d = float(c[4])
    close_p_h = float(d[4])
    close_price_month.append(close_p_m)
    close_price_week.append(close_p_w)
    close_price_day.append(close_p_d)
    close_price_hour.append(close_p_h)

mean_month = st.mean(close_price_month)
mean_week = st.mean(close_price_week)
mean_day = st.mean(close_price_day)
mean_hour = st.mean(close_price_hour)

if float(avg_price['price']) > mean_month and mean_week and mean_day and mean_hour :
    print('Good price to sell')
else:
    print('Good price to buy')
info = client.get_symbol_info('BNBUSDT')
# print(info)
ppp = str(round((float(avg_price['price']) * 0.97), 8))
print('{:0.8f}'.format((float(avg_price['price']) * 0.97)))

# amount = 0.000614250470875
# precision = 8
# amount_str = "{:0.0{}f}".format(amount, precision)
# print(amount_str)
order = client.create_order(
    symbol='BNBUSDT',
    side=SIDE_SELL,
    type=ORDER_TYPE_LIMIT,
    timeInForce=TIME_IN_FORCE_GTC,
    quantity=1,
    price='{:0.8f}'.format((float(avg_price['price']) * 1.01)))

# order_result = client.create_margin_order(symbol="BTCUSDT", side=SIDE_BUY, type=ORDER_TYPE_LIMIT, timeInForce=TIME_IN_FORCE_GTC, sideEffectType="MARGIN_BUY", quantity=0.5, price=3000)

# med_price_hist = st.median((open_price + close_price)/2)
# print('last 2 hour average open price: ', st.mean(open_price))
# print('last 2 hour average close price: ', st.mean(close_price))
# print('average price for last 7 days: ', avg_price_hist)
# print('current price:',float(avg_price['price']))

# t = np.linspace(1,n,n)

#plot
# fig, ax = plt.subplots()
# ax.grid(True)
# plt.figure(1)
# plt.plot(t, open_price)
# plt.plot(t, close_price)
#plt.legend()
# plt.xlabel('Time, sec')
# plt.ylabel('Vx')
# plt.show()

