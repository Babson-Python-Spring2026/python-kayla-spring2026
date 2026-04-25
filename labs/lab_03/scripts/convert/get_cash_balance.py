
import json
import os

# load json files

base = os.path.dirname(__file__)

with open(os.path.join(base, "price_ticker.json")) as f:
    price_ticker = json.load(f)   # price_ticker["AAPL"]["20250103"] -> price

with open(os.path.join(base, "price_date.json")) as f:
    price_date = json.load(f)     # price_date["20250103"]["AAPL"]   -> price

transactions = []   # list of transaction dicts; append only, never delete

def get_cash_balance(as_of_date):

    balance = 0.0
    for trn in transactions:
        if trn['ticker'] == '$$$$' and trn['date'] <= as_of_date:
            balance += trn['shares']   # shares of $$$$ == cash units

    return round(balance, 2)