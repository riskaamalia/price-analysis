import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas_datareader.data as web

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
    rs = pd.stats.moments.ewma(u, com=period-1, adjust=False) / pd.stats.moments.ewma(d, com=period-1, adjust=False)
    return 100 - 100 / (1 + rs)

def get_realtime_price (stock_name,start, end) :
    # get sample data from yahoo price
    get_price = web.DataReader(stock_name,'yahoo',start,end)
    print(get_price)
    data = get_price['Adj Close']

    return data

def generate_matplotlib (real_price, sma, ema, macd, rsi, start_date, end_date) :
    my_year_month_fmt = mdates.DateFormatter('%y-%m-%d')

    fig = plt.figure(figsize=(10, 4))
    ax = fig.add_subplot(1, 1, 1)

    # if you want to see all of result, just uncomment them
    ax.plot(real_price.ix[start_date:end_date].index, real_price.ix[start_date:end_date], label='PRICE')
    ax.plot(sma.ix[start_date:end_date].index, sma.ix[start_date:end_date],label='20-days SMA')
    ax.plot(ema.ix[start_date:end_date].index, ema.ix[start_date:end_date],label='20-days EMA')
    ax.plot(macd.ix[start_date:end_date].index, macd.ix[start_date:end_date],label='MACD')
    ax.plot(rsi.ix[start_date:end_date].index, rsi.ix[start_date:end_date],label='RSI')

    ax.legend(loc='best')
    ax.set_ylabel('Price in $')
    ax.xaxis.set_major_formatter(my_year_month_fmt)
    plt.show()

# this is output of json format
def json_output (data, stock_name) :
    # format
    '''
    {
      "MSFT" :
        {
          "DATE": "2017-07-01 08:50:50",
          "HIGH": 0,
          "LOW": 0,
          "PREVIOUS": 0,
          "LAST": 0,
          "OPEN": 0,
          "CLOSE": 1000
        }
    }
    '''
    index_loop = 0
    high = 0
    low = 0
    previous = 0
    open = 0
    close = 0
    for index in data.index :
        if data[index_loop] >= 0 :
            date = str(index).split(' ')[0]
            price = data[index_loop]
            # print(str(price)+' date : '+date)
            if open == 0 :
                open = data[index_loop]
            if price > high :
                high = price
            if price < low or low == 0 :
                low = price
            # create json here
            data_value = {stock_name:{"DATE":date,"HIGH":high,"LOW":low,"PREVIOUS":previous,"LAST":price,"OPEN":open,"CLOSE":close}}
            print(json.dumps(data_value))

            # print out status bearish or bullish
            if price > previous and previous != 0 :
                print("BULLISH detected....")
            else :
                print("BEARISH detected....")
            previous = price


        index_loop = index_loop + 1
    close = data[index_loop - 1]
    data_value = {stock_name:{"DATE":date,"HIGH":high,"LOW":low,"PREVIOUS":0,"LAST":price,"OPEN":open,"CLOSE":close}}
    print("close price : "+json.dumps(data_value))

start_date = '2016-01-03'
end_date = '2016-05-28'
# get realtime data first
preprocessing_data = get_realtime_price('MSFT', start_date, end_date)
# get sma prediction
sma = sma_predict(preprocessing_data)
# get ema prediction
ema = ema_predict(preprocessing_data)
# get macd prediction
macd = macd_predict(preprocessing_data)
# get rsi prediction
rsi = rsi_predict(preprocessing_data)

# sample of json output format , I just print out 30 data for sample , use one algorithm for sample output
json_output(rsi.head(30),'MSFT')

# create chart to see result of prediction
# this is real price chart from sample data, I got real sample data of real stock price
# we can easily see price prediction bullish or bealish by see the graph up or down day by day (graph update every day)
generate_matplotlib(preprocessing_data, sma, ema, macd, rsi, start_date, end_date)
