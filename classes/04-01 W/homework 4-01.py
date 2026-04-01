import pandas as pd
import json

# Input files
pricing_csv = r"C:/PythonClass/student_repo/classes/04-01 W/data/source/portfolio_prices_raw_and_split_adjusted_20260331b.csv"
market_dates_json = r"C:/PythonClass/student_repo/classes/04-01 W/data/system/mkt_dates.json"

# Output file
output_json = "ticker_universe.json"

# Load data
df = pd.read_csv(pricing_csv)
with open(market_dates_json, "r") as f:
    market_dates = json.load(f)

# Normalize dates
df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")
market_dates = sorted(market_dates)

# Map date -> index for fast gap detection
date_to_idx = {d: i for i, d in enumerate(market_dates)}
last_market_date = market_dates[-1]

# Group by ticker
ticker_ranges = {}

for ticker, group in df.groupby("Ticker"):
    ticker_dates = sorted(set(group["Date"]))

    ranges = []
    start = ticker_dates[0]
    prev_idx = date_to_idx[start]

    for d in ticker_dates[1:]:
        curr_idx = date_to_idx[d]

        # Gap detected (non-consecutive market date)
        if curr_idx != prev_idx + 1:
            end = market_dates[prev_idx]
            ranges.append({
                "start_date": start,
                "end_date": end
            })
            start = d

        prev_idx = curr_idx

    # Final range
    if ticker_dates[-1] == last_market_date:
        end = "99999999"
    else:
        end = ticker_dates[-1]

    ranges.append({
        "start_date": start,
        "end_date": end
    })

    ticker_ranges[ticker] = ranges

# Write output
with open(output_json, "w") as f:
    json.dump(ticker_ranges, f, indent=2)

print(f"Saved ticker universe to {output_json}")