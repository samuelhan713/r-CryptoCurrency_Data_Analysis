import ccxt
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# Replace 'YOUR_EXCHANGE_API_KEY' and 'YOUR_EXCHANGE_SECRET' with your actual API key and secret
exchange = ccxt.coinbasepro(
    {
        "apiKey": API_KEY,
        "secret": API_SECRET,
        # 'password': 'YOUR_API_PASSPHRASE',  # Passphrase used during API key creation
    }
)


def get_percent_change(symbol, start_date):
    # Get current ticker price
    ticker = exchange.fetch_ticker(symbol)
    current_price = ticker["last"]
    print("current price: ", current_price)

    # Get historical trades data
    since_timestamp = exchange.parse8601(start_date)
    trades = exchange.fetch_trades(symbol, since=since_timestamp)

    # Extract the trade price from the historical data for the start date
    start_price = float(trades[0]["price"])
    print("start price: ", start_price)

    # Calculate percent change
    percent_change = ((start_price - current_price) / start_price) * 100

    return percent_change


# Example usage
symbol = "BTC/USD"  # Note the different symbol format for Coinbase Pro
start_date = "2024-01-25T00:00:00"  # Replace with your desired start date
percent_change = get_percent_change(symbol, start_date)

print(f"Percent Change for {symbol} since {start_date}: {percent_change:.2f}%")

# historical_prices = get_historical_prices(symbol, start_date)

# for candle in historical_prices:
#     timestamp = exchange.iso8601(candle['timestamp'])
#     close_price = candle['close']
#     print(f"At {timestamp}, BTC/USD closing price was: {close_price}")
