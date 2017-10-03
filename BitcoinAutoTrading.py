'''
Automatic trading bitcoin to rupiah from vip.bitcoin.co.id
Bot Trading bitcoin Indonesia dengan bahasa pemrograman python
python 3.6
This project runs automatic trading bitcoin. Bitcoin price got from vip.bitcoin.co.id
Program ini menjalakankan bot trading bitcoin secara otomatis. Sumber pantauan harga dari vip.bitcoin.co.id


If you want to get full code, you can contact me.
email : riskaamalia.mail@gmail.com
linkedin : linkedin.com/in/riskaamalia
'''
import json
from urllib.request import urlopen
from time import sleep
import datetime
import pandas as pd
import numpy as np

# get price from vip.bitoin.co.id every 10 sec
def get_10seconds_price () :

    loop = 0
    prices_dict = {}
    while loop < 20 :
        url_ticker = 'https://vip.bitcoin.co.id/api/btc_idr/ticker'
        success = False
        while success is False:
            try:
                response = urlopen(url_ticker)
                if response.getcode() == 200:
                    success = True
            except Exception as e:
                success = True

        full_result = json.loads(response.read())['ticker']
        # print(full_result)

        last_price = full_result['last']
        last_time = datetime.datetime.fromtimestamp(int(full_result['server_time'])).strftime('%Y-%m-%d %H:%M:%S')

        prices_dict[last_time] = last_price
        print('Time : '+last_time+' Last Price : '+prices_dict[last_time])

        sleep(10)
        loop = loop + 1
    prices_series_20 = pd.Series(prices_dict)
    prices_dataframe = pd.DataFrame({'price':prices_series_20})
    print(prices_dataframe)


# analyze bearish or bullish
def price_analysis () :
    return None

def place_order () :
    return None


get_10seconds_price()
