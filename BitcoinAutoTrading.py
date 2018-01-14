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
import sys
import logging

# set up logging
import logging
from logging.handlers import TimedRotatingFileHandler

def setup_logging(log_filename):

    fmt = '%(asctime)s : %(lineno)d - %(levelname)s - %(message)s'

    # create console log stream and and to root
    logging.basicConfig(level=logging.INFO, format=fmt)

    # create custom log handler and add to root
    file_handler = TimedRotatingFileHandler(filename=log_filename, when='H', interval=12, backupCount=40)
    file_handler.setFormatter(logging.Formatter(fmt))
    logging.getLogger('').addHandler(file_handler)

setup_logging('history.log')

# get price from vip.bitoin.co.id every 10 sec
def get_10seconds_price(total_loop):
    loop = 0
    prices_dict = {}
    previous_price = 0
    full_result = None
    total_price = 0
    while loop < total_loop:
        url_ticker = 'https://vip.bitcoin.co.id/api/btc_idr/ticker'
        success = False
        response = None
        while success is False:
            try:
                response = urlopen(url_ticker)
                if response.getcode() == 200:
                    success = True
            except Exception as e:
                success = True

        get_response = response.read().decode('utf-8')
        full_result = json.loads(get_response)['ticker']
        # logging.info(full_result)

        last_price = full_result['last']
        last_time = datetime.datetime.fromtimestamp(int(full_result['server_time'])).strftime('%Y-%m-%d %H:%M:%S')

        if previous_price != last_price:
            prices_dict[loop] = last_price
            total_price = total_price + int(last_price)
            logging.info('Time : ' + last_time + ' Last Price : ' + prices_dict[loop])
            loop = loop + 1

        sleep(5)

        previous_price = last_price

    # get average price
    prices_dict['average'] = total_price / total_loop
    prices_dict['high'] = full_result['high']
    prices_dict['low'] = full_result['low']
    return prices_dict

# start from rupiah
my_asset = {'idr':10000000,'btc':0}
is_up = False
count = 0
order_buy = False
buy_price = 0

# just for order buy
while True :
    logging.info('get 10 last price')
    get_prices = get_10seconds_price(10)
    average_price = get_prices['average']
    first_price = int(get_prices[0])
    logging.info('average price : '+str(average_price)+" | first price : "+str(first_price))

    if average_price < first_price and count != 2:
        logging.info("price is DOWN")
        is_up = False
        count = count + 1
    else:
        if count == 2 :
            logging.info("#two times, just buy it")
        else:
            logging.info ("price is UP")
            is_up = True

        # get ready to buy or sell in different module
        if order_buy == False :
            buy_price = average_price
            my_asset['btc'] = float(my_asset['idr']/buy_price)
            my_asset['idr'] = 0
            logging.info("#buy in price : "+str(buy_price))
            count = 0
            order_buy = True
        else:
            if average_price < buy_price :
                aset_sold = float((average_price/buy_price) * my_asset['btc'])
            else:
                aset_sold = my_asset['btc']

            my_asset['btc'] = my_asset['btc'] - aset_sold
            my_asset['idr'] = average_price
            logging.info("#sell in price : "+str(average_price))
            count = 0
            buy_price = 0
            order_buy = False
    logging.info("MY ASET : "+str(my_asset))
