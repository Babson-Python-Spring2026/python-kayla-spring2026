
import json
import os

# load json files

base = os.path.dirname(__file__)

with open(os.path.join(base, "price_ticker.json")) as f:
    price_ticker = json.load(f)   # price_ticker["AAPL"]["20250103"] -> price

with open(os.path.join(base, "price_date.json")) as f:
    price_date = json.load(f)     # price_date["20250103"]["AAPL"]   -> price

transactions = []   # list of transaction dicts; append only, never delete

# create transactions

def create_transaction(trn_type, date, ticker=None, shares=None,
                       price=None, cash_amount=None):

    trn_type = trn_type.upper()

    if trn_type == 'deposit':

        if cash_amount is None or cash_amount <= 0:
            raise ValueError("deposit requires a positive cash amount")

        transactions.append({
            'date':       date,
            'trnType':    'deposit',
            'ticker':     '$$$$',
            'shares':     cash_amount, # treat cash units as "shares"
            'price':      1.00,
            'cashAmount': +cash_amount,
        })

    elif trn_type == 'withdraw':
  
        if cash_amount is None or cash_amount <= 0:
            raise ValueError("withdraw requires a positive cash amount "
                             "(the sign is handled internally)")

        transactions.append({
            'date':       date,
            'trnType':    'withdraw',
            'ticker':     '$$$$',
            'shares':     -cash_amount,    # negative = cash leaving
            'price':      1.00,
            'cashAmount': -cash_amount,
        })

    elif trn_type == 'buy':

        if ticker is None or shares is None or price is None:
            raise ValueError("buy requires ticker, shares, and price")
        if shares <= 0 or price <= 0:
            raise ValueError("shares and price must be positive")

        trade_value = round(shares * price, 2)

        transactions.append({
            'date':       date,
            'trnType':    'buy',
            'ticker':     ticker.upper(),
            'shares':     +shares,
            'price':      price,
            'cashAmount': None,
        })

        transactions.append({
            'date':       date,
            'trnType':    'buy',
            'ticker':     '$$$$',
            'shares':     -trade_value,
            'price':      1.00,
            'cashAmount': -trade_value,
        })

    elif trn_type == 'sell':

        if ticker is None or shares is None or price is None:
            raise ValueError("sell requires ticker, shares, and price")
        if shares <= 0 or price <= 0:
            raise ValueError("shares and price must be positive")

        trade_value = round(shares * price, 2)

        transactions.append({
            'date':       date,
            'trnType':    'sell',
            'ticker':     ticker.upper(),
            'shares':     -shares,
            'price':      price,
            'cashAmount': None,
        })

        transactions.append({
            'date':       date,
            'trnType':    'sell',
            'ticker':     '$$$$',
            'shares':     +trade_value,
            'price':      1.00,
            'cashAmount': +trade_value,
        })

    else:
        raise ValueError(f"Unknown transaction type: '{trn_type}'. "
                         "Use deposit, withdraw, buy, or sell.")


# get_cash_balance

def get_cash_balance(as_of_date):

    balance = 0.0
    for trn in transactions:
        if trn['ticker'] == '$$$$' and trn['date'] <= as_of_date:
            balance += trn['shares']   # shares of $$$$ == cash units

    return round(balance, 2)

# build_portfolio

def build_portfolio(as_of_date):

    holdings = {}   

    for trn in transactions:
        if trn['date'] > as_of_date:
            continue                    

        ticker = trn['ticker']
        delta_shares = trn['shares']

        if ticker not in holdings:
            holdings[ticker] = {'shares': 0.0, 'cost_basis': 0.0}

        holdings[ticker]['shares'] = round(
            holdings[ticker]['shares'] + delta_shares, 6)

        # Cost basis: only count buys 
        if trn['trnType'] == 'BUY' and ticker != '$$$$':
            holdings[ticker]['cost_basis'] = round(
                holdings[ticker]['cost_basis'] + abs(delta_shares) * trn['price'], 2)

    date_key = str(as_of_date)
    portfolio = {}

    for ticker, pos in holdings.items():
        if ticker == '$$$$':
            mkt_price = 1.00
        else:
            try:
                mkt_price = price_date[date_key][ticker]
            except KeyError:
                ticker_prices = price_ticker.get(ticker, {})
                past_dates = sorted(
                    [d for d in ticker_prices if d <= date_key], reverse=True)
                mkt_price = ticker_prices[past_dates[0]] if past_dates else None

        portfolio[ticker] = {
            'shares':     round(pos['shares'], 6),
            'price':      mkt_price,
            'value':      round(pos['shares'] * mkt_price, 2) if mkt_price else None,
            'cost_basis': pos['cost_basis'],
        }

    return portfolio


# list_transactions_for_ticker

def list_transactions_for_ticker(ticker):
   
    ticker = ticker.upper()
    result = [trn for trn in transactions if trn['ticker'] == ticker]
    result.sort(key=lambda t: t['date'])
    return result