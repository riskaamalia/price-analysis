import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

my_year_month_fmt = mdates.DateFormatter('%m/%y')

data = pd.read_pickle('./data.pkl')
data.head(20)

# Calculating the short-window simple moving average
short_rolling = data.rolling(window=20).mean()
short_rolling.head(20)

# Calculating the long-window simple moving average
long_rolling = data.rolling(window=100).mean()
long_rolling.tail()

start_date = '2015-01-01'
end_date = '2016-12-31'

plt.interactive(False)
fig = plt.figure(figsize=(15,9))
ax = fig.add_subplot(1,1,1)

ax.plot(data.ix[start_date:end_date, :].index, data.ix[start_date:end_date, 'MSFT'], label='Price')
ax.plot(long_rolling.ix[start_date:end_date, :].index, long_rolling.ix[start_date:end_date, 'MSFT'], label = '100-days SMA')
ax.plot(short_rolling.ix[start_date:end_date, :].index, short_rolling.ix[start_date:end_date, 'MSFT'], label = '20-days SMA')

ax.legend(loc='best')
ax.set_ylabel('Price in $')
ax.xaxis.set_major_formatter(my_year_month_fmt)
plt.show()
