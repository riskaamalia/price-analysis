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
import logging
from vipbtc import trade
from logging.handlers import TimedRotatingFileHandler

class Trading :

    def __init__(self):
        self.setup_logging('history.log')
        self.order_price = 0
        self.order_status = True
        self.akun = None

    def setup_logging(self,log_filename):

        fmt = '%(asctime)s : %(lineno)d - %(levelname)s - %(message)s'

        # create console log stream and and to root
        logging.basicConfig(level=logging.INFO, format=fmt)

        # create custom log handler and add to root
        file_handler = TimedRotatingFileHandler(filename=log_filename, when='H', interval=12, backupCount=40)
        file_handler.setFormatter(logging.Formatter(fmt))
        logging.getLogger('').addHandler(file_handler)

    # get price from vip.bitoin.co.id every 10 sec
    def get_10seconds_price(self,total_loop):
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
                total_price = total_price + float(last_price)
                logging.info('Time : ' + last_time + ' Last Price : ' + prices_dict[loop])
                loop = loop + 1
                # for pending order
                if self.order_price != 0 :
                    if float(last_price) >= self.order_price :
                        order_status = True
                    else:
                        order_status = False

            sleep(5)

            previous_price = last_price

        # get average price
        prices_dict['average'] = total_price / total_loop
        prices_dict['high'] = full_result['high']
        prices_dict['low'] = full_result['low']
        return prices_dict

    def execute (self,my_asset, akun) :
        self.akun = akun
        if my_asset['idr'] < 1 :
            order_buy = True
        else:
            order_buy = False
        buy_price = 1

        while True :
            try :
                logging.info('get 5 last price')
                get_prices = self.get_10seconds_price(5)
                average_price = get_prices['average']
                first_price = float(get_prices[0])
                logging.info('average price : '+str(average_price)+" | first price : "+str(first_price))

                if average_price < first_price:
                    logging.info("price is DOWN")
                    is_up = False
                else:
                    logging.info ("price is UP")
                    is_up = True

                # get ready to buy or sell in different module
                # check open order from api
                orders = akun.openOrders()['return']['orders']
                if self.order_status == True and len(orders) == 0 :
                    if order_buy == False and is_up == True :
                        if average_price > float(get_prices[4]) :
                            buy_price = int(average_price) + 200000
                        else:
                            buy_price = int(get_prices[4]) + 200000


                        akun.trade('buy',my_asset['idr'],str(buy_price))
                        logging.info("#buy in price : "+str(buy_price))
                        self.order_price = buy_price
                        order_buy = True
                    elif is_up == False and order_buy == True:
                        if average_price > float(get_prices[4]) :
                            average_price = average_price + 200000
                        else:
                            average_price = float(get_prices[4]) + 200000

                        if average_price > buy_price :
                            if buy_price < 100 :
                                buy_price = average_price
                            aset_sold = float(average_price/buy_price) * float(my_asset['btc'])

                            akun.trade('sell',my_asset['btc'],str(float(average_price) * float(aset_sold)))
                            logging.info("#sell in price : "+str(average_price))
                            buy_price = 0
                            order_buy = False

                    assets = akun.getInfo()
                    my_asset['idr'] = assets['return']['balance']['idr']
                    my_asset['btc'] = assets['return']['balance']['btc']
                else :
                    logging.info('waiting for pending order execute')

                if order_buy == False :
                    logging.info("waiting for BUYING , MY ASET : "+str(my_asset))
                else:
                    logging.info("waiting for SELLING , MY ASET : "+str(my_asset))
            except Exception as e :
                logging.error(str(e))


# test API
akun = trade.TradeAPI(key, secret)

assets = akun.getInfo()
idr = assets['return']['balance']['idr']
btc = assets['return']['balance']['btc']

trading = Trading()
my_asset = {'idr':float(idr),'btc':float(btc)}
trading.execute(my_asset, akun)
