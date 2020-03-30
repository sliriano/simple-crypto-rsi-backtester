import requests, json
from collections import OrderedDict
from datetime import datetime
from data import get_rsi_and_price
from dbhelper import DBHelper

# function that backtests the simple rsi strategy of opening positions when the RSI
# is breaking above 30 and closing positions when the RSI falls back below 70
def rsi_reentry_test(symbol, timeframe, length, start_balance=0.0):
    # setup database to store results
    db = DBHelper()
    db.setup()

    test_data = get_rsi_and_price(symbol, timeframe,length)

    initial_rsi_value = test_data[next(iter(test_data))][0]
    
    if initial_rsi_value < 30:
        under30 = True
        over70 = False
    elif initial_rsi_value > 70:
        under30 = False
        over70 = True
    else:
        under30 = False
        over70 = False
    
    in_trade = False

    usd_balance = float(start_balance)
    crypto_balance = 0.0

    for date in test_data:
        rsi_value = test_data[date][0]
        price = test_data[date][1]

        if rsi_value < 30 and under30 == False:
            under30 = True

        if rsi_value > 30 and under30 == True:
            under30 = False
            if in_trade == False:
            # BUY ORDER CODE HERE
                in_trade = True
                crypto_balance = usd_balance / price
                usd_balance = 0
                db.add_trade((date, "buy", price, crypto_balance, usd_balance))

        if rsi_value > 70 and over70 == False: 
            over70 = True

        if rsi_value < 70 and over70 == True:
            over70 = False
            if in_trade == True:
            # SELL ORDER CODE HERE
                in_trade = False
                usd_balance = price * crypto_balance
                crypto_balance = 0
                db.add_trade((date, "sell", price, crypto_balance, usd_balance))
#                 symbol   timeframe  length  balance 
#rsi_reentry_test("btcusd", "hour", 1300, 100.0)

# function that backtests trades that are opened when the rsi reaches
# a certain value and sells when it reaches another. 
def rsi_test(symbol, timeframe, length, buy_value, sell_value, start_balance=0.0):
    # setup database to store results
    db = DBHelper()
    db.setup()

    test_data = get_rsi_and_price(symbol, timeframe, length)

    usd_balance = float(start_balance)
    crypto_balance = 0.0

    in_trade = False

    for date in test_data:
        rsi_value = test_data[date][0]
        price = test_data[date][1]

        if rsi_value >= sell_value and in_trade:
            in_trade = False
            usd_balance = price * crypto_balance
            crypto_balance = 0
            db.add_trade((date, "sell", price, crypto_balance, usd_balance))
        
        if rsi_value <= buy_value and not in_trade:
            in_trade = True
            crypto_balance = usd_balance / price
            usd_balance = 0
            db.add_trade((date, "buy", price, crypto_balance, usd_balance))
    
    if crypto_balance > 0.00:
        return crypto_balance * 9750.50
    return usd_balance
            
# rsi_test("ETHUSD", "hour", 1300, 25, 60, 100.0)

