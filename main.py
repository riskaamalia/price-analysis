import json
# simple moving average predict
def sma_predict (json_price) :
    return None

# moving average convergence divergence predict
def macd_predict (json_price) :
    return None

# stochastic RSI algorithm
def rsi_predict (json_price) :
    return None

def get_realtime_price () :
    location = "input_price.json"
    with open(location) as data_file:
        price = json.load(data_file)['AAPL']
    return price[0]

print (get_realtime_price())
# input price every 10 second
# OUTPUT FORMAT
# {
#       "DATE": "2017-07-01 12:00:00",
#       "HIGH": 3400,
#       "LOW": 3200,
#       "LAST": 3421,
#       "OPEN": 3300,
#       "CLOSE": 3250
# }
