import requests
from datetime import datetime
import pandas as pd

import requests
import pandas as pd

# CoinGecko API endpoint for getting market data for multiple cryptocurrencies
url = "https://api.coingecko.com/api/v3/coins/markets"

# Define parameters for the request
params = {
    "vs_currency": "usd",  # Specify the currency (in this case, USD)
    "order": "market_cap_desc",  # Order the results by market cap in descending order
    "per_page": 10,  # Specify the number of cryptocurrencies to retrieve
    "page": 1,  # Specify the page number
    "sparkline": False,  # Disable sparkline data for simplicity
}

# Make the API request
response = requests.get(url, params=params)
data = response.json()

# Check if the response contains data
if data:
    crypto_info = [
        {
            "id": entry["id"],
            "symbol": entry["symbol"],
            "name": entry["name"],
            "price": entry["current_price"],
            "date_updated": entry["last_updated"],
        }
        for entry in data
    ]

    # Create a DataFrame from the extracted information
    df = pd.DataFrame(crypto_info)

    # Print the DataFrame
    print(df)
else:
    print("No data received from the API.")


# # CoinGecko API endpoint for historical market chart
# url = "https://api.coingecko.com/api/v3/coins/{symbol}/market_chart"

# # Define the list of cryptocurrency symbols
# cryptos = ["bitcoin", "ethereum", "ripple"]

# # Define common parameters
# params = {
#     "vs_currency": "usd",
#     "days": "1",  # Adjust the number of days as needed
#     "interval": "daily",
# }

# # Fetch data for each cryptocurrency
# dfs = []
# for crypto in cryptos:
#     # Make the API request
#     response = requests.get(url.format(symbol=crypto), params=params)
#     data = response.json()

#     # Check if the 'prices' key is present in the response
#     if "prices" in data:
#         # Extract relevant data (timestamps and prices)
#         timestamps = [
#             datetime.utcfromtimestamp(entry[0] / 1000) for entry in data["prices"]
#         ]
#         prices = [entry[1] for entry in data["prices"]]

#         # Create a DataFrame for the current cryptocurrency
#         df = pd.DataFrame({"Timestamp": timestamps, f"Price_{crypto.upper()}": prices})
#         dfs.append(df)
#     else:
#         print(f"Invalid or unexpected API response structure for {crypto}.")

# # Merge DataFrames on the 'Timestamp' column
# merged_df = pd.concat(dfs, axis=1, join="outer", sort=True)

# # Print the first few rows of the merged DataFrame
# print(merged_df.head())
