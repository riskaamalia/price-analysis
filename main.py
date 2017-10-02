import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

# simple moving average predict
def sma_predict (data) :
    sma_result = data.rolling(window=20).mean()
    return sma_result


# Using Pandas to calculate a 20-days span EMA. adjust=False is for recursive
def ema_predict (data) :
    ema_short = data.ewm(span=20, adjust=False).mean()
    return ema_short

# moving average convergence divergence predict
def macd_predict (data) :
    macd = data.ewm(span=12, adjust=False).mean() - data.ewm(span=26, adjust=False).mean()
    return macd

# stochastic RSI algorithm
def rsi_predict (data):
    period = 14
    delta = data.diff().dropna()
    u = delta * 0
    d = u.copy()
    u[delta > 0] = delta[delta > 0]
    d[delta < 0] = -delta[delta < 0]
    u[u.index[period-1]] = np.mean( u[:period] ) #first value is sum of avg gains
    u = u.drop(u.index[:(period-1)])
    d[d.index[period-1]] = np.mean( d[:period] ) #first value is sum of avg losses
    d = d.drop(d.index[:(period-1)])
    rs = pd.stats.moments.ewma(u, com=period-1, adjust=False) / \
    pd.stats.moments.ewma(d, com=period-1, adjust=False)
    return 100 - 100 / (1 + rs)

def get_realtime_price () :
    # This is sample json format I want to create in future
    # location = "input_price.json"
    # with open(location) as data_file:
    #     price = json.load(data_file)['MSFT']
    # print(price[0])
    # set to dataframe to make easy using numpy and pandas library
    # data = pd.DataFrame.insert(0,'MSFT',price[0])
    # I use this to get sample data, there are many sample stock price here,
    # but I just can get sample price stock daily , not every 10 seconds
    data = pd.read_pickle('./data.pkl')
    data.head(20)

    return data

def generate_matplotlib (real_price, sma, ema, macd, rsi) :
    my_year_month_fmt = mdates.DateFormatter('%y-%m-%d')
    start_date = '2016-01-03'
    end_date = '2016-02-28'

    fig = plt.figure(figsize=(15, 9))
    ax = fig.add_subplot(1, 1, 1)

    ax.plot(real_price.ix[start_date:end_date, :].index, real_price.ix[start_date:end_date, 'MSFT'], label='PRICE')
    ax.plot(sma.ix[start_date:end_date, :].index, sma.ix[start_date:end_date, 'MSFT'],
            label='20-days SMA')
    ax.plot(ema.ix[start_date:end_date, :].index, ema.ix[start_date:end_date, 'MSFT'],
            label='20-days EMA')
    ax.plot(macd.ix[start_date:end_date, :].index, macd.ix[start_date:end_date, 'MSFT'], label='MACD 12 EMA - 26 EMA')
    ax.plot(rsi.ix[start_date:end_date, :].index, rsi.ix[start_date:end_date, 'MSFT'], label='RSI')

    ax.legend(loc='best')
    ax.set_ylabel('Price in $')
    ax.xaxis.set_major_formatter(my_year_month_fmt)
    plt.show()

# this is output of json format
def json_output (data, stock_price) :
    # format
    '''
    {
      "MSFT" :
        {
          "DATE": "2017-07-01 08:50:50",
          "HIGH": 0,
          "LOW": 0,
          "LAST": 0,
          "OPEN": 0,
          "CLOSE": 1000
        }
    }
    '''

    prediction_data = data.get('MSFT')[15]
    data_value = {"MSFT":{"DATE":"2017-07-01","HIGH":0,"LOW":0,"LAST":data,"OPEN":0,"CLOSE":1000}}
    # because in RSI prediction result can be seen after 15 days, I set period into 14 days
    print(json.dumps(data_value))


    # json_output = None
    # for d in data :
    #     print (d)
    # return None

# get realtime data first
preprocessing_data = get_realtime_price()
# get sma prediction
sma = sma_predict(preprocessing_data)
# get ema prediction
ema = ema_predict(preprocessing_data)
# get macd prediction
macd = macd_predict(preprocessing_data)
# get rsi prediction
rsi = rsi_predict(preprocessing_data)
#
# # create chart to see result of prediction
# # this is real price chart from sample data, I got real sample data of real stock price
# # we can easily see price prediction bullish or bealish by see the graph up or down day by day (graph update every day)
# generate_matplotlib(preprocessing_data, sma, ema, macd, rsi)

# this is sample for json output format
json_output(preprocessing_data,'MSFT')
json_output(rsi,'MSFT')
