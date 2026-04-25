
import json
import os

# load json files

base = os.path.dirname(__file__)

with open(os.path.join(base, "price_ticker.json")) as f:
    price_ticker = json.load(f)   # price_ticker["AAPL"]["20250103"] -> price

with open(os.path.join(base, "price_date.json")) as f:
    price_date = json.load(f)     # price_date["20250103"]["AAPL"]   -> price

transactions = []   # list of transaction dicts; append only, never delete

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

