import ccxt
import datetime
import os
from dotenv import load_dotenv
import pandas as pd
import ast
from collections import defaultdict

TOP_CRYPTO = [
    ("Bitcoin", "btc"),
    ("Ethereum", "eth"),
    ("Tether", "usdt"),
    ("BNB", "bnb"),
    ("Solana", "sol"),
    ("XRP", "xrp"),
    # ("USDC", "usdc"),
    ("Lido Staked Ether", "steth"),
    ("Cardano", "ada"),
    ("Avalanche", "avax"),
    ("Dogecoin", "doge"),
    ("TRON", "trx"),
    ("Polkadot", "dot"),
    ("Chainlink", "link"),
    # ("Toncoin", "ton"),
    ("Polygon", "matic"),
    ("Wrapped Bitcoin", "wbtc"),
    ("Internet Computer", "icp"),
    ("Shiba Inu", "shib"),
    ("Dai", "dai"),
    ("Litecoin", "ltc"),
    ("Bitcoin Cash", "bch"),
    ("Uniswap", "uni"),
    ("LEO Token", "leo"),
    ("Cosmos Hub", "atom"),
    ("Ethereum Classic", "etc"),
    ("Stellar", "xlm"),
    ("OKB", "okb"),
    ("NEAR Protocol", "near"),
    ("Injective", "inj"),
    ("Optimism", "op"),
    ("Aptos", "apt"),
    # ("Monero", "xmr"),
    ("Lido DAO", "ldo"),
    ("Celestia", "tia"),
    ("First Digital USD", "fdusd"),
    ("Filecoin", "fil"),
    ("Immutable", "imx"),
    ("Hedera", "hbar"),
    ("Kaspa", "kas"),
    ("Arbitrum", "arb"),
    ("Stacks", "stx"),
    ("Cronos", "cro"),
    ("Bittensor", "tao"),
    ("Mantle", "mnt"),
    ("VeChain", "vet"),
    ("Maker", "mkr"),
    # ("TrueUSD", "tusd"),
    ("Quant", "qnt"),
    ("Sei", "sei"),
    ("Render", "rndr"),
    ("The Graph", "grt"),
    ("Sui", "sui"),
    ("Rocket Pool ETH", "reth"),
    ("Bitcoin SV", "bsv"),
    ("MultiversX", "egld"),
    ("Algorand", "algo"),
    ("Aave", "aave"),
    ("THORChain", "rune"),
    ("ORDI", "ordi"),
    ("Flow", "flow"),
    ("Mina Protocol", "mina"),
    ("Synthetix Network", "snx"),
    ("Helium", "hnt"),
    ("The Sandbox", "sand"),
    ("Chiliz", "chz"),
    ("dYdX", "dydx"),
    ("Tokenize Xchange", "tkx"),
    ("Fantom", "ftm"),
    ("Axie Infinity", "axs"),
    ("Theta Network", "theta"),
    # ("KuCoin", "kcs"),
    ("Osmosis", "osmo"),
    # ("SATS (Ordinals)", "sats"),
    ("Astar", "astr"),
    ("WhiteBIT Coin", "wbt"),
    ("Beam", "beam"),
    ("Tezos", "xtz"),
    ("WEMIX", "wemix"),
    ("Cheelee", "cheel"),
    ("dYdX", "ethdydx"),
    ("ApeCoin", "ape"),
    ("Decentraland", "mana"),
    ("BitTorrent", "btt"),
    ("Bitget Token", "bgb"),
    ("EOS", "eos"),
    ("Blur", "blur"),
    ("Frax Share", "fxs"),
    # ("Manta Network", "manta"),
    ("Conflux", "cfx"),
    ("NEO", "neo"),
    ("IOTA", "iota"),
    ("Kava", "kava"),
    ("GALA", "gala"),
    ("USDD", "usdd"),
    ("Bonk", "bonk"),
    ("Klaytn", "klay"),
    ("Oasis Network", "rose"),
    ("Frax Ether", "frxeth"),
    ("Flare", "flr"),
]

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# loop through the finalized csv file
# df = pd.read_csv("./vader.csv")
recommened_coins = {}
df = pd.read_csv("./vader.csv")
df_list = df.apply(lambda row: row.to_dict(), axis=1).tolist()


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


def convert_to_ticker_format(name):
    for full_name, ticker in TOP_CRYPTO:
        if name.lower() == full_name.lower() or name.lower() == ticker.lower():
            return f"{ticker.upper()}/USD"


accumulated_scores = defaultdict(lambda: {"sum": 0, "count": 0})


def analyze_posts():
    print(len(df))
    for i in range(len(df)):
        cur = df.iloc[i]
        compound_score = cur["compound"]
        if cur["coins"] == "[]":
            continue

        # coin list
        coin_list_str = cur["coins"]
        coin_list = ast.literal_eval(coin_list_str)

        for coin_name in coin_list:
            coin_name = convert_to_ticker_format(coin_name)

            symbol = coin_name
            start_date = cur["created_time"]
            percent_change = get_percent_change(symbol, start_date)
            print(
                f"Percent Change for {symbol} since {start_date}: {percent_change:.2f}%"
            )

            accumulated_scores[coin_name]["sum"] += compound_score
            accumulated_scores[coin_name]["count"] += 1
    average_scores = {
        coin_name: data["sum"] / data["count"]
        for coin_name, data in accumulated_scores.items()
    }
    print(average_scores)


analyze_posts()


def generate_recommendation(average_scores):
    # TODO: generate recommendation
    return


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
