import requests, json
from collections import OrderedDict
from datetime import datetime

# time frame options: day, hour, minute
# length paramter represents how far back you would like the data to go
# Ex) if you want data going back to 100 hours ago:
#     get_price_data("BTCUSD","hour",100)
def get_price_data(symbol, timeframe, length):
    timeframe = timeframe.lower()
    symbol = symbol.upper()
    length= str(length)
    url = "https://min-api.cryptocompare.com/data/histo"+timeframe+"?fsym="+symbol[0:3]+"&tsym="+symbol[3::]+"&limit="+length+"&api_key=INSERT CRYPTOCOMPARE API KEY HERE"
    data = requests.get(url)
    return data.json()['Data']

def rsi(symbol, timeframe):
    url = "https://www.alphavantage.co/query?function=RSI&symbol="+symbol+"&interval="+ timeframe +"&time_period=14&series_type=open&apikey=INSERT ALPHAVANTAGE API KEY HERE"
    data = requests.get(url)
    return data.json()['Technical Analysis: RSI']

# combines rsi data and avg entry price data into dictionary up to and not including the date specified
def get_rsi_and_price(symbol, timeframe, length):
    rsi_timeframes = ['1min', "60min", "daily"]
    price_timeframes = ['minute', 'hour', 'day']

    price_data = get_price_data(symbol, timeframe, length)

    # creates list of key values for new dictionary
    times = []
    for values in price_data:
        times.append(str(datetime.fromtimestamp(values['time']))[:-3])

    # parses the rsi_data to only include what matches the price data
    rsi_data = rsi(symbol.upper(), rsi_timeframes[price_timeframes.index(timeframe.lower())])
    rsi_keys = [*rsi_data]
    rsi_keys.pop(0)
    rsi_keys.reverse()
    index = rsi_keys.index(rsi_keys[-len(times)])
    rsi_keys = rsi_keys[index::]

    rsi_values = []
    for keys in rsi_keys:
        rsi_values.append(float(rsi_data[keys]['RSI']))

    parsed_data = {}
    counter = 0
    for i in times:
        # average between the hourly open and close
        avg_entry = float(price_data[counter]['open'] + price_data[counter]['close'])/2
        parsed_data[i] = [rsi_values[counter], avg_entry]
        counter+=1
    return parsed_data
