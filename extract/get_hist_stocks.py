import pandas as pd

from polygon import RESTClient

# Setup API
client = RESTClient("yDF8gsrzRB8zJzzAcpBxW1mEcuivfy48")

# Setup date points
limit = 10000
start_date = "2015-01-01"
end_date = "2023-06-01"

# Set training cutoff
train_start = "2023-02-01"


# Stocks of interest
stocks = [
    "AAPL",
    "TSLA"
]

# Client arguments
client_dict = {
    'multiplier': 1,
    'timespan': 'day',
    'from_': start_date,
    'to': end_date,
    'limit': limit
}

# Extract stock data
ext_data = [
    pd.DataFrame(client.list_aggs(stock, **client_dict)).assign(stock_name=stock)
    for stock in stocks
]

# Concatenate dataframes
comb_data = pd.concat(ext_data)

# Convert timestamp to readable format
comb_data['timestamp'] = pd.to_datetime(comb_data['timestamp'], unit='ms')

# Sort by time and stock
comb_data = comb_data.sort_values(['timestamp', 'stock_name']).reset_index()

# Identify training rows
comb_data['set'] = 'train'
comb_data.loc[comb_data.timestamp > train_start, 'set'] = 'test'

# Write output data to csv
comb_data.to_csv('data/historical_stocks.csv', index=False)