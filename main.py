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
    return price

print (get_realtime_price())
