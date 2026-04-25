
import json
import os

# load json files

base = os.path.dirname(__file__)

with open(os.path.join(base, "price_ticker.json")) as f:
    price_ticker = json.load(f)   # price_ticker["AAPL"]["20250103"] -> price

with open(os.path.join(base, "price_date.json")) as f:
    price_date = json.load(f)     # price_date["20250103"]["AAPL"]   -> price

transactions = []   # list of transaction dicts; append only, never delete


def list_transactions_for_ticker(ticker):
   
    ticker = ticker.upper()
    result = [trn for trn in transactions if trn['ticker'] == ticker]
    result.sort(key=lambda t: t['date'])
    return result