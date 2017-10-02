import pandas as pd
import pandas_datareader.data as web
import datetime as dt
import matplotlib.pyplot as plt
from matplotlib import gridspec
import matplotlib.dates as mdates


def getEma(ticker,n,start,end):
#    creates, initializes multiplier which will be used to weight more recent values heavily
    multiplier = 2/(n + 1)

#   creates dataframe w/ all of ticker's info from yahoo in range
#   deletes all columns except 'Adj Close'
    data = web.DataReader(ticker,'yahoo',start,end)

#    creates new dataframe to store info, creates columns
    results = pd.DataFrame()
    results['Adj Close']=0
    results['SMA']=0
    results['EMA']=0

#    fills columns, calculates SMA and sets first value of EMA to match 1st value of SMA
    results['Adj Close']=data['Adj Close']
    results['SMA']=results['Adj Close'].rolling(window=n).mean()
    results['EMA'][n-1]=results['SMA'][n-1]

#    EMA: {Close - EMA(previous day)} x multiplier + EMA(previous day)
#    loops through calculating EMA for remaining dates using formula above
    for i in range(n,results.shape[0]):
        results['EMA'][i] = ((results['Adj Close'][i]- results['EMA'][i-1])*multiplier) + results['EMA'][i-1]

    return results

def compileFrames(df1,df2):
#    takes in df1,df2
#    df1: dataframe w/ larger n
#    df2: dataframe w/ smaller n

#    creates dataframe where everything will be compiled finally
    result = pd.DataFrame()
    result['Slow EMA'] = 0
    result['Fast EMA'] =0

    result['Slow EMA']= df1['EMA']
    result['Fast EMA'] = df2['EMA']

    return result

def calcMACD(result):
#    takes in combined matrix
#    computes and adds column w/ MACD values

    result['MACD'] = result['Fast EMA']-result['Slow EMA']
    return result

def plot(result,ticker):
    fig = plt.figure()
#    height ratio for subplots is 2:1
    gs = gridspec.GridSpec(2, 1, height_ratios=[2, 1])

    fig.suptitle(ticker)
    fig.set_figheight(6)
    fig.set_figwidth(8)

    ax1 = plt.subplot(gs[0])
    line0, = ax1.plot(result.index,result['Fast EMA'],"r",label='Fast')
    line1, = ax1.plot(result.index,result['Slow EMA'],"g",label='Slow')
    plt.ylabel('$',fontsize=10)
    plt.grid()

    ax2 = plt.subplot(gs[1],sharex=ax1)
    line2, = ax2.plot(result.index,result['MACD'],"m",label='MACD')
    line3, = ax2.plot(result.index,result['Signal'],"k--",label='Signal')

    plt.setp(ax1.get_xticklabels(),visible=False)
    yticks = ax2.yaxis.get_major_ticks()
    yticks[-1].label1.set_visible(False)
    plt.xlabel('Date',fontsize=10)
    plt.ylabel('$',fontsize=10)
    plt.grid()

    myFmt = mdates.DateFormatter('%Y-%m')
    ax2.xaxis.set_major_formatter(myFmt)
    plt.tick_params(axis='x',labelsize=7)

    ax1.legend((line0, line1,line2,line3), ('Fast', 'Slow','MACD','Signal'), loc='upper left')

    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=None, hspace=0)
    plt.show()

def reduceFrame(df,name):
#    takes in dataframe, modifies to start from where no values are NaN
    df = df[df[name].notnull()]
    return df

def calcSignal(df,n):
#    calculates values for signal line

    multiplier = 2/(n + 1)
    signal = pd.DataFrame()
    signal['Signal']=0
    signal['MACD'] = df['MACD']


    signal['Signal'][n-1] = signal['MACD'][n-1]

    for i in range(n,signal.shape[0]):
        signal['Signal'][i] = (signal['MACD'][i]- signal['Signal'][i-1])*multiplier + signal['Signal'][i-1]

    df['Signal']=0
    df['Signal']=signal['Signal']

    return df

def main():
#    sets start, end dates
#    declares ticker for which we will be doing analysis
#    sets two time periods
    start = dt.datetime(2015,1,1)
    end = dt.datetime(2017,1,1)
    ticker = 'GOOG'
    n_1 = 26
    n_2 = 12
    n_3 = 9

    slow = getEma(ticker,n_1,start,end)
    fast = getEma(ticker,n_2,start,end)

    total = compileFrames(slow,fast)
    total = calcMACD(total)
    total = reduceFrame(total,'Slow EMA')
    total = calcSignal(total,n_3)
    total=reduceFrame(total, 'Signal')

    plot(total,ticker)

#    print(total)

if  __name__ =='__main__':main()

