
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

