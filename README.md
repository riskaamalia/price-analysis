Input :
Given price of stock everyday (in this case, I used data from yahoo finance). Hers's the example :

             Open       High        Low      Close      Adj Close     Volume
Date
2016-01-04  54.320000  54.799999  53.389999  54.799999  52.433533   53778000
2016-01-05  54.930000  55.389999  54.540001  55.049999  52.672737   34079700
2016-01-06  54.320000  54.400002  53.639999  54.049999  51.715916   39518900
2016-01-07  52.700001  53.490002  52.070000  52.169998  49.917099   56564900


Purpose :
Predict stock price trends, is it bullish or bearish.

Sollution :
- For managing data and predicting stock price trends, I use 4 algorithms then compare the results. The algorithms are :
  Simple Moving Average, Exponential Moving Average, Moving Average Convergent Divergent, and RSI.

  Simple Moving Average
  The important value of this algorithm is the current price of stock. Based on example above , I just can get close price in a day as 'current price'.
  Range for current price (I set range 20 means 20 days in price sample above) and get mean of those data, so I can get prediction by number of the 21 data,
  I can know that the 21 data will higher or not than the 20 data.

  Exponential Moving Average
  Similar with SMA , but it needs a formula exponential , it uses exponential formula to get the biggest affect of prediction in the last price.
  So, the important aspect of this algorithm is not just the current price, moreover the current price that nearest to last price.
  For example if we uses 20 range, so the affect of prediction from the biggest to smallest are price number 20,19 .... until 1.

  MACD
  MACD needs EMA to execute. it contains both convergence and divergence, from literature I read, the most famous formula of this is :
  macd = emasfast - emaslow
  emasfast means EMA algorithm with 12 days period
  emaslow means EMA algorithm with 26 days period
  So the important indicator is the value of EMASLOW and EMAFAST

  RSI
  RSI needs EMA algotihm too. the other indicator is the price of comparation loses (down) or gain(up) at that day(from example price I set to 14 period/day).

- Technology stack :
  - Programming language : python 3.6
  - Libraries : pandas, matplotlib, numpy

- To visualize the result of 4 algorithms, I used matpotlib which display graph axis X: date, axis Y: price.

- How to run program :
  run main.py , it will print out sample of json output and print prediction bullish/bearish from previous price.
  Here's the output (I just print out 20 sample in this project) :
  {
      "MSFT": {
        "DATE": "2016-03-07",
        "HIGH": 54.886362270706556,
        "LOW": 34.47284950213938,
        "PREVIOUS": 50.27636838351264,
        "LAST": 45.576447329703704,
        "OPEN": 37.256571571984416,
        "CLOSE": 0
      }
  }

  If you want to see more you can set range in variable start_date and end_date, you can set in json_output(rsi.head(30),'MSFT').Also it will show graph,
  I just show 2 graph for real price and rsi, to compare result of rsi prediction, just uncomment if you want to see all of result in module
  generate_matplotlib.

  If output of program like this :
  Unable to read URL: https://query1.finance.yahoo.com/v7/finance/download/MSFT?period1=1451754000&period2=1464454799&interval=1d&events=history&crumb=I%5Cu002F6kVP0PE0Z
  Just re run again.

- In conclusion, some indicator to predict bullish or bearish are :
  - average of current price in some period
  - average of current price in some period especially the latest index price
  - The comparation of go down or go up price in that day
  Which one is the best ?
  According to graph result for some days in matplotlib, prediction graph that is close to price graph (up and down graph, not exactly pice itself)is RSI.
