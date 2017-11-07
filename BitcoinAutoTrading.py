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

# get price from vip.bitoin.co.id every 10 sec
def get_10seconds_price (total_loop) :

    loop = 0
    prices_dict = {}
    previous_price = 0
    full_result = None
    while loop < total_loop :
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
        # print(full_result)

        last_price = full_result['last']
        last_time = datetime.datetime.fromtimestamp(int(full_result['server_time'])).strftime('%Y-%m-%d %H:%M:%S')

        if previous_price != last_price :
            prices_dict[loop] = last_price
            print('Time : '+last_time+' Last Price : '+prices_dict[loop])
            loop = loop + 1

        sleep(5)

        previous_price = last_price

    prices_dict['high'] = full_result['high']
    prices_dict['low'] = full_result['low']
    return prices_dict

def order_buy (profit, total_loop) :
    is_buy = {}
    status_price = 0
    prices_dict = get_10seconds_price(total_loop)
    last_price = int(prices_dict[total_loop - 1])
    high_price = int(prices_dict['high'])
    is_up = False

    # prepare to initialize buy
    if high_price - last_price >= profit:
        # go buy in this price
        previous = last_price
        while is_up == False :
            # stop looping until get to lowest price
            print('GET ready to buy ...., last price average : '+str(previous))
            update_price = count_mean(get_10seconds_price(5),5)
            if previous > update_price :
                print('still bearish ...... :(')
                previous = update_price
                is_up = False
            else :
                print("Yepeee bullish, ready to buy ...")
                is_up = True
                status_price = previous - 180000
                order_api(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),'buy',status_price)
                print('FINALLY buy in price : ' + str(status_price))

        is_buy[1] = 'True'
        is_buy[2] = status_price
        return is_buy

    is_buy[1] = 'False'
    is_buy[2] = status_price
    return is_buy

def order_sell (profit, total_loop, buy_price) :
    is_buy = {}
    status_price = buy_price
    prices_dict = get_10seconds_price(total_loop)
    last_price = int(prices_dict[total_loop - 1])
    is_up = False

    # prepare to initialize sell
    if last_price - buy_price >= profit:
        # go sell in this price
        previous = last_price
        while is_up == True :
            # stop looping until get to highest price
            print('GET ready to sell ...., last price average : '+str(previous))
            update_price = count_mean(get_10seconds_price(5),5)
            if previous > update_price :
                print('still bearish, prepare to sell')
                is_up = False
                status_price = previous + 180000
                print('FINALLY sell in price : ' + str(status_price))
                order_api(str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')), 'sell', status_price)
            else :
                print("Yepeee bullish, waiting to get more profit ...")
                is_up = True
                previous = update_price

        is_buy[1] = 'False'
        is_buy[2] = status_price
        return is_buy

    is_buy[1] = 'True'
    is_buy[2] = status_price
    return is_buy

def count_mean (price_dict, loop) :
    total = 0
    values = price_dict.keys()
    for key in values :
        if key is not 'high' and key is not 'low' :
            total = total + int(price_dict[key])

    return int(total / loop)

def order_api(date,order_status,price) :
    print('go to '+order_status+' , connect to API with price : ' + str(price))

    location = 'status_order.txt'
    data_file = open(location,'r')
    if order_status == 'sell' :
        status = str(data_file.read().split(' = ')[1])
        if status == 'buy' :
            # check status buy first in real API


            # sell in this price
            data_file.close()
            write_file = open(location,'w')
            write_file.write(date + ' = ' + order_status + ' = ' + str(price))
            print('SUCCESS place SELL in price : '+str(price))
            write_file.close()
    else :
        data_file.close()
        write_file = open(location, 'w')
        write_file.write(date+' = '+order_status+' = '+str(price))
        print('SUCCESS place BUY in price : ' + str(price))
        write_file.close()

# for first time, I set order buy
is_buy = [0,'False']
while True :
    if 'True' in is_buy[1] :
        print('waiting for selling signal ..............................')
        is_buy = order_sell(500000,5, is_buy[2])
    else :
        print('waiting for buying signal ..............................')
        is_buy = order_buy(500000,5)

    print('is buy : .... ' + str(is_buy))

# order_api('2017-08-01 12:45:34','sell',100000000)
