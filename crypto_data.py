# This file fetches real-time data from the crypto market and determines the percent change of the price of a coin from the date a reddit post was made to the current date.
import ccxt
import datetime
import os
from dotenv import load_dotenv
import pandas as pd
import ast
from collections import defaultdict
import time
from TOP_CRYPTO import TOP_CRYPTO_TUPLES

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

recommened_coins = {}
df = pd.read_csv("./vader.csv")
df_list = df.apply(lambda row: row.to_dict(), axis=1).tolist()
average_scores = {}

exchange = ccxt.coinbasepro(
    {
        "apiKey": API_KEY,
        "secret": API_SECRET,
        # 'password': 'YOUR_API_PASSPHRASE',  # Passphrase used during API key creation
    }
)


def get_percent_change(symbol, start_date):
    ticker = exchange.fetch_ticker(symbol)

    current_price = ticker["last"]
    print("current price: ", current_price)

    # Get historical trades data
    since_timestamp = exchange.parse8601(start_date)
    trades = exchange.fetch_trades(symbol, since=since_timestamp)

    start_price = float(trades[0]["price"])
    print("start price: ", start_price)

    percent_change = ((start_price - current_price) / start_price) * 100

    return percent_change


def convert_to_ticker_format(name):
    for full_name, ticker in TOP_CRYPTO_TUPLES:
        if name.lower() == full_name.lower() or name.lower() == ticker.lower():
            return f"{ticker.upper()}/USD"


accumulated_scores = defaultdict(lambda: {"sum": 0, "count": 0})


def analyze_posts():
    empty = 0
    df_copy_index = 0
    df_copy = pd.DataFrame(columns=df.columns)

    print(len(df))
    for i in range(len(df)):
        # if i >= len(df):
        #     break
        cur = df.iloc[i]
        compound_score = cur["compound"]
        if cur["coins"] == "[]":
            print("empty!")
            empty += 1
            # df.drop(i, inplace=True)
            continue
        df_copy.loc[len(df_copy)] = cur

        # coin list
        coin_list_str = cur["coins"]
        coin_list = ast.literal_eval(coin_list_str)

        for coin_name in coin_list:
            coin_name = convert_to_ticker_format(coin_name)

            symbol = coin_name
            start_date = cur["created_time"]
            percent_change = get_percent_change(symbol, start_date)

            # print(
            #     f"Percent Change for {symbol} since {start_date}: {percent_change:.2f}%"
            # )

            df_copy.at[df_copy_index, "percent_change"] = percent_change
            accumulated_scores[coin_name]["sum"] += compound_score
            accumulated_scores[coin_name]["count"] += 1
            time.sleep(1)
        df_copy_index += 1

    average_scores = {
        coin_name: data["sum"] / data["count"]
        for coin_name, data in accumulated_scores.items()
    }
    # print(average_scores)
    print(df_copy)
    print("there should be ", (len(df) - empty), "rows")
    file_path = "final.csv"
    df_copy.to_csv(file_path, index=False)


if __name__ == "__main__":
    analyze_posts()


# -------------For testing--------------
# Example usage
# symbol = "XMR/USD"  # Note the different symbol format for Coinbase Pro
# start_date = "2024-01-25T00:00:00"  # Replace with your desired start date
# percent_change = get_percent_change(symbol, start_date)

# print(f"Percent Change for {symbol} since {start_date}: {percent_change:.2f}%")

# historical_prices = get_historical_prices(symbol, start_date)

# for candle in historical_prices:
#     timestamp = exchange.iso8601(candle['timestamp'])
#     close_price = candle['close']
#     print(f"At {timestamp}, BTC/USD closing price was: {close_price}")
