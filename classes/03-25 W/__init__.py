cash = 10000
positions = {"AAPL": 10, "MSFT": 5}
prices = {"AAPL": 190, "MSFT": 420}

port = {'cash': 10000.00, 
        'positions' : [{'ticker':'AAPL', 'shares':10, 'price':190.00}, 
                       {'ticker':'MSFT', 'shares':5, 'price':420.00}]}

def buy_stock(port): 
    ticker = input('enter stock symbol you want to buy: ')

    txt = 'enter shares you want to buy: '
    while True: 
        try: 
            shares = int(input(txt))
            break
        except ValueError: 
            txt = 'you must enter an integer: '

    txt = f'enter price of {ticker}: '
    while True: 
        try: 
            price = float(input(txt))
            break 
        except ValueError: 
            txt = 'you must enter a float: '

    if shares * price > port ['cash']: 
        print('insufficent cash. transaction denied')
        return None 
    else: 
        new_position = {'ticker': ticker, 'shares': shares, 'price': price}

        port['positions'].append(new_position)
        return None