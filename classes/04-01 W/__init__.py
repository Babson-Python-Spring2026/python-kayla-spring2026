#prompt 1 
import pandas as pd
import json

# Input/output paths
csv_file = "pricing.csv"
json_file = "market_dates.json"

# Read only the Date column
df = pd.read_csv(csv_file, usecols=["Date"])

# Convert to datetime, drop missing/invalid dates, keep unique, sort
dates = (
    pd.to_datetime(df["Date"], errors="coerce")
    .dropna()
    .dt.strftime("%Y-%m-%d")
    .unique()
)

sorted_dates = sorted(dates)

# Write to JSON
with open(json_file, "w") as f:
    json.dump(sorted_dates, f, indent=2)

print(f"Wrote {len(sorted_dates)} unique dates to {json_file}")

#prompt 2 
import pandas as pd
import json

# Input/output files
pricing_file = "pricing.csv"
market_dates_file = "market_dates.json"
ticker_universe_file = "ticker_universe.json"

# Load pricing data
df = pd.read_csv(pricing_file, usecols=["Date", "Ticker"])

# Normalize dates to YYYYMMDD strings
df["Date"] = pd.to_datetime(df["Date"], errors="coerce").dt.strftime("%Y%m%d")
df = df.dropna(subset=["Date", "Ticker"])

# Load the complete ordered market-date calendar
with open(market_dates_file, "r") as f:
    market_dates = json.load(f)

# Normalize market dates to YYYYMMDD strings
market_dates = [
    pd.to_datetime(d).strftime("%Y%m%d")
    for d in market_dates
]

# Map each market date to its position in the calendar
date_index = {d: i for i, d in enumerate(market_dates)}
last_market_date = market_dates[-1]

ticker_universe = {}

# Process each ticker independently
for ticker, group in df.groupby("Ticker"):
    # Unique sorted valid dates for this ticker that exist in the market calendar
    ticker_dates = sorted(
        d for d in group["Date"].unique()
        if d in date_index
    )

    if not ticker_dates:
        continue

    ranges = []
    start_date = ticker_dates[0]
    prev_date = ticker_dates[0]

    for current_date in ticker_dates[1:]:
        # If current date is not the next market date, close the previous range
        if date_index[current_date] != date_index[prev_date] + 1:
            end_date = (
                "99999999"
                if prev_date == last_market_date
                else prev_date
            )
            ranges.append({
                "start_date": start_date,
                "end_date": end_date
            })
            start_date = current_date

        prev_date = current_date

    # Close final range
    end_date = (
        "99999999"
        if prev_date == last_market_date
        else prev_date
    )
    ranges.append({
        "start_date": start_date,
        "end_date": end_date
    })

    ticker_universe[ticker] = ranges

# Write sorted output
ticker_universe = dict(sorted(ticker_universe.items()))

with open(ticker_universe_file, "w") as f:
    json.dump(ticker_universe, f, indent=2)

print(f"Wrote ticker universe for {len(ticker_universe)} tickers to {ticker_universe_file}")
