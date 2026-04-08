import json
price_by_date = {}
price_by_ticker = {}

with open('classes/04-06 M/data/source/portfolio_prices_raw_and_split_adjusted_20260331b.csv', 'r') as f:
    next(f)
    for line in f: 
        date,ticker,raw_close,adjusted_close = line.strip().split(',')

        price_by_date.setdefault(date, []).append({
            'ticker': ticker,
            'raw_close': raw_close
        })

        price_by_ticker.setdefault(ticker, []).append({
            'date': date,
            'raw_close': raw_close
        })

with open('classes/04-06 M/data/system/price_by_date.json', 'w') as f:
    json.dump(price_by_date, f, indent=2)

with open('classes/04-06 M/data/system/price_by_ticker.json', 'w') as f:
    json.dump(price_by_ticker, f, indent=2)