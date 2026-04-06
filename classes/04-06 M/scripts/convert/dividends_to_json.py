import json
divs_by_date = {}
divs_by_ticker = {}

with open('classes/04-06 M/data/source/portfolio_dividends_20260331b.csv', 'r') as f:
    next(f)
    for line in f: 
        date, ticker, dividend = line.strip().split(',')

        divs_by_date.setdefault(date, []).append({
            'ticker': ticker,
            'dividend': dividend
        })

        divs_by_ticker.setdefault(ticker, []).append({
            'date': date,
            'dividend': dividend
        })

with open('classes/04-06 M/data/system/dividends_by_date.json', 'w') as f:
    json.dump(divs_by_date, f, indent=2)

with open('classes/04-06 M/data/system/dividends_by_ticker.json', 'w') as f:
    json.dump(divs_by_ticker, f, indent=2)