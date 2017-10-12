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
    while loop < total_loop :
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

        if previous_price != last_price :
            prices_dict[last_time] = last_price
            print('Time : '+last_time+' Last Price : '+prices_dict[last_time])
            loop = loop + 1

        sleep(5)

        previous_price = last_price

    prices_dict['high'] = full_result['high']
    prices_dict['low'] = full_result['low']
    return prices_dict

def order_buy (profit, total_loop) :
    is_buy = {}
    last_price = 0
    first_price = 0
    prices_dict = get_10seconds_price(total_loop)
    mean_price = count_mean(prices_dict, total_loop)
    print("mean price : "+str(mean_price))

    loop = 0
    for value in prices_dict.values() :
        if loop == 0 :
            first_price = int(value)
        if loop == total_loop - 1 :
            last_price = int(value)
        loop = loop + 1

    high_price = int(prices_dict['high'])
    lowest_price = int(prices_dict['low'])
    # prepare to buy
    if first_price < mean_price :
        print('bullish detected.. price is up wuhuuuu')
        is_up = True
    else :
        print('bearish detected.. price is down :(')
        is_up = False

    # prepare to initialize buy
    if high_price - last_price >= profit:
        # go buy in this price
        previous = last_price
        update_price = last_price
        while is_up == False :
            # stop looping until get to lowest price
            update_price = count_mean(get_10seconds_price(5),5)
            print('GET ready to buy ....')
            if previous > update_price :
                print('still bearish ...... :(')
                is_up = False
            else :
                print("Yepeee bullish, ready to buy ...")
                is_up = True
            previous = update_price

        print('FINALLY buy in price : '+str(update_price))
        is_buy[1] = 'True'
        is_buy[2] = update_price
        return is_buy

    is_buy[1] = 'False'
    is_buy[2] = last_price
    return is_buy

def order_sell (profit, total_loop, buy_price) :
    is_buy = {}
    last_price = 0
    first_price = 0
    prices_dict = get_10seconds_price(total_loop)
    mean_price = count_mean(prices_dict, total_loop)
    print("mean price : "+str(mean_price))

    loop = 0
    for value in prices_dict.values() :
        if loop == 0 :
            first_price = int(value)
        if loop == total_loop - 1 :
            last_price = int(value)
        loop = loop + 1

    # prepare to sell or buy
    if first_price < mean_price :
        print('bullish detected.. price is up wuhuuuu')
        is_up = True
    else :
        print('bearish detected.. price is down :(')
        is_up = False

    # prepare to initialize sell
    if last_price - buy_price >= profit:
        # go sell in this price
        previous = last_price
        update_price = last_price
        while is_up == True :
            # stop looping until get to highest price
            update_price = count_mean(get_10seconds_price(5),5)
            print('GET ready to sell ....')
            if previous > update_price :
                print('still bearish, prepare to sell')
                is_up = False
            else :
                print("Yepeee bullish, waiting to get more profit ...")
                is_up = True
            previous = update_price

        print('FINALLY sell in price : '+str(update_price))
        is_buy[1] = 'False'
        is_buy[2] = update_price
        return is_buy

    is_buy[1] = 'True'
    is_buy[2] = last_price
    return is_buy

def count_mean (price_dict, loop) :
    total = 0
    l = 0
    values = price_dict.values()
    for value in values :
        if l < loop :
            total = total + int(value)
            l = l + 1

    return total / loop

# for first time, I set order buy
is_buy = order_buy(100000,5)
while True :
    print('is buy : .... '+str(is_buy))
    if 'True' in is_buy[1] :
        print('waiting for selling signal ..............................')
        print('is sell : .... '+str(is_buy))
        is_buy = order_sell(100000,5, is_buy[2])
    else :
        print('waiting for buying signal ..............................')
        is_buy = order_buy(100000,5)

# low di update jam 6 sore
