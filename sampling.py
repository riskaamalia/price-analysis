import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

def RSI(series, period=14):
    delta = series.diff().dropna()
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


my_year_month_fmt = mdates.DateFormatter('%m/%y')

data = pd.read_pickle('./data.pkl')
data.head(20)

# Calculating the short-window simple moving average
short_rolling = data.rolling(window=20).mean()
short_rolling.head(20)

# Using Pandas to calculate a 20-days span EMA. adjust=False specifies that we are interested in the recursive calculation mode.
ema_short = data.ewm(span=20, adjust=False).mean()

# macd
macd = data.ewm(span=12, adjust=False).mean() - data.ewm(span=26, adjust=False).mean()

#RSI
rsi_data = RSI(data)

start_date = '2015-01-01'
end_date = '2016-12-31'

fig = plt.figure(figsize=(15,9))
ax = fig.add_subplot(1,1,1)

ax.plot(data.ix[start_date:end_date, :].index, data.ix[start_date:end_date, 'MSFT'], label='Price')
ax.plot(short_rolling.ix[start_date:end_date, :].index, short_rolling.ix[start_date:end_date, 'MSFT'], label = '20-days SMA')
ax.plot(ema_short.ix[start_date:end_date, :].index, ema_short.ix[start_date:end_date, 'MSFT'], label = 'Span 20-days EMA')
ax.plot(macd.ix[start_date:end_date, :].index, macd.ix[start_date:end_date, 'MSFT'], label = 'MACD 12 EMA - 26 EMA')
ax.plot(rsi_data.ix[start_date:end_date, :].index, rsi_data.ix[start_date:end_date, 'MSFT'], label = 'RSI')

ax.legend(loc='best')
ax.set_ylabel('Price in $')
ax.xaxis.set_major_formatter(my_year_month_fmt)
plt.show()
