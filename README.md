Business Process :
- This project predicts stock price trends, is price bullish or bearish in a day.
- Input format is a price of a stock in every 10 seconds
Format (I change format from exercise example in order to make it easier if I want to create example of more than one price as an array):
{
  "AAPL" :
    [{
      "DATE": "2017-07-01 12:00:00",
      "HIGH": 3400,
      "LOW": 3200,
      "LAST": 3421,
      "OPEN": 3300,
      "CLOSE": 3250
    },
    {
      "DATE": "2017-07-01 12:10:00",
      "HIGH": 3400,
      "LOW": 3200,
      "LAST": 3421,
      "OPEN": 3300,
      "CLOSE": 3250
    }]
}
- Output result is a prediction of trend (bullish or bealish)

Watch stocks :
- In order to make it easily to see, I created a graph for watching stocks, so it could be easily watched.

Manage Data :

Some algorithm that is used for predicting trends:
- Simple Moving Average
- Exponential Moving Average
- MACD
- RSI

Simple Moving Average
The important value of this algorithm is the current price of stock. in JSON format above , the current price is in "LAST" . you just need to get some range for current price (I set range 20) and get mean of those data, so I can get prediction by number of the 21 data, I can know that the 21 data will higher or not than the 20 data.

Exponential Moving Average
Similar with SMA , but it needs a formula exponential , it uses exponential formula to get the biggest affect of prediction in the last price. So, the important aspect of this algorithm is not just the current price, moreover the current price that nearest to last price. For example if we uses 20 range, so the affect of prediction from the biggest to smallest are price number 20,19 .... until 1.

MACD
MACD needs EMA to execute. it contains both convergence and divergence, from literature I read, the most famous formula of this is :
macd = emasfast - emaslow
emasfast means EMA algorithm with 12 days period
emaslow means EMA algorithm with 26 days period
So the important indicator is the value of EMASLOW and EMAFAST

RSI
RSI needs EMA algotihm too. the other indicator is the price of comparation loses (down) or gain(up) at that day.

Dependencies :
Lucikly, python has some library that maintains SMA and EMA. I uses pandas in python.

I use matplotlib to visualize the graph.

So in conclusion, some indicator to predict bullish or bearish are :
- average of current price in some period
- average of current price in some period especially the latest index price
- The comparation of go down or go up price in that day.